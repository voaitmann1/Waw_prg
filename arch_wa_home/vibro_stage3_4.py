import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch, find_peaks, butter, filtfilt, hilbert
from scipy.signal import detrend

# -----------------------
# Утилиты чтения/записи
# -----------------------
def read_signal_csv(filename):
    """
    Пытаемся считать CSV с заголовком. Ожидаемые колонки: Time_s, Signal [, ...]
    Возвращает t (numpy), x (numpy)
    """
    # Попробуем numpy.genfromtxt (robust)
    try:
        data = np.genfromtxt(filename, delimiter=',', names=True)
        # имена колонок
        cols = data.dtype.names
        if 'Time_s' in cols:
            t = data['Time_s']
            # взять первую колонку после Time_s как сигнал
            sig_col = [c for c in cols if c != 'Time_s'][0]
            x = data[sig_col]
            return np.asarray(t), np.asarray(x)
    except Exception:
        pass

    # fallback: простая загрузка без заголовка
    raw = np.loadtxt(filename, delimiter=',')
    if raw.ndim == 1:
        t = np.arange(raw.size)
        x = raw
    else:
        t = raw[:,0]
        x = raw[:,1]
    return t, x

def save_spectrum_csv(filename, freqs, amps):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Frequency_Hz','Amplitude'])
        for ff, aa in zip(freqs, amps):
            writer.writerow([ff, aa])

def save_mode_csv(filename, t, sig):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time_s','Signal'])
        for ti, si in zip(t, sig):
            writer.writerow([ti, si])

def save_decay_table(filename, decay_rows):
    # decay_rows: list of dicts with keys f0, alpha, A0, Q, n_peaks, r2
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['f0_Hz','alpha_1s','A0','Q','n_peaks','r2'])
        for r in decay_rows:
            writer.writerow([r.get('f0'), r.get('alpha'), r.get('A0'), r.get('Q'), r.get('n_peaks'), r.get('r2')])

# -----------------------
# Параболическая интерполяция (для уточнения пика)
# -----------------------
def parabolic_interpolation(A, k):
    # A: амплитудный массив (1D), k: индекс локального пика (1..len-2)
    alpha = A[k-1]
    beta  = A[k]
    gamma = A[k+1]
    denom = (alpha - 2*beta + gamma)
    if denom == 0:
        p = 0.0
    else:
        p = 0.5 * (alpha - gamma) / denom
    k_true = k + p
    amp_true = beta - 0.25 * (alpha - gamma) * p
    return k_true, amp_true

# -----------------------
# Полосовой фильтр (zero-phase)
# -----------------------
def bandpass_filtfilt(x, fs, f0, bw, order=4):
    nyq = 0.5 * fs
    low = max((f0 - bw/2.0) / nyq, 1e-6)
    high = min((f0 + bw/2.0) / nyq, 0.999999)
    if low >= high:
        raise ValueError(f"Bad band: f0={f0}, bw={bw}, nyq={nyq}")
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, x)

# -----------------------
# Адаптивный детектор пиков в спектре
# -----------------------
def detect_spectral_peaks(freqs, amps, noise_factor=4.0, use_savgol=False,
                          sg_window=11, sg_poly=3, min_distance_hz=0.5, min_prominence=None):
    """
    Возвращает список пиков: (freq, amp, idx)
    """
    f = np.array(freqs)
    A = np.array(amps)

    # простой сглаживающий запас (опционально)
    if use_savgol:
        from scipy.signal import savgol_filter
        w = min(sg_window, len(A) // 2 * 2 + 1)
        if w % 2 == 0: w += 1
        if w >= 5:
            A_proc = savgol_filter(A, w, sg_poly)
        else:
            A_proc = A.copy()
    else:
        A_proc = A.copy()

    # адаптивный порог по медиане/MAD
    med = np.median(A_proc)
    mad = np.median(np.abs(A_proc - med))
    thr = med + noise_factor * (mad if mad>0 else (np.std(A_proc)+1e-12))

    # distance в точках
    df = f[1] - f[0] if len(f)>1 else 1.0
    distance_samples = max(1, int(round(min_distance_hz / df)))
    kwargs = {'distance': distance_samples}
    if min_prominence is not None:
        kwargs['prominence'] = min_prominence
    kwargs['height'] = thr

    peaks_idx, props = find_peaks(A_proc, **kwargs)
    peaks = []
    for i, k in enumerate(peaks_idx):
        # уточним параболой (если возможно)
        if 1 <= k < len(A)-1:
            k_true, a_true = parabolic_interpolation(A_proc, k)
            f_true = f[0] + k_true*(df)
        else:
            f_true = f[k]
            a_true = A_proc[k]
        prom = props['prominences'][i] if 'prominences' in props else None
        peaks.append({'idx': int(k), 'freq': float(f_true), 'amp': float(a_true), 'prominence': prom})
    return peaks, thr

# -----------------------
# STAGE 3: вычисление спектра и сохранение
# -----------------------
def stage3_compute_and_save_spectrum(signal_csv_files, params_list, out_dir='stage3_results'):
    """
    signal_csv_files: list of CSV filenames (по одному на датчик)
    params_list: список словарей параметров длиной = len(signal_csv_files)
       Каждый dict может содержать:
         - fs (обязательно) : частота дискретизации
         - method: 'fft' или 'welch'
         - use_window: True/False (hann)
         - pad_factor: int (например 4 или 8)
         - welch_nperseg, welch_noverlap (если method=='welch')
         - peak_detection params: noise_factor, use_savgol, sg_window, sg_poly, min_distance_hz, min_prominence
    """
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for i, fname in enumerate(signal_csv_files):
        print(f"[stage3] File {i+1}/{len(signal_csv_files)}: {fname}")
        t, x = read_signal_csv(fname)
        p = params_list[i]
        fs = p['fs']
        x_proc = np.array(x, dtype=float)
        x_proc = x_proc - np.mean(x_proc)  # убрать DC
        x_proc = detrend(x_proc)

        method = p.get('method','fft')
        use_window = p.get('use_window', True)

        if method == 'welch':
            nperseg = p.get('welch_nperseg', 2048)
            noverlap = p.get('welch_noverlap', nperseg//2)
            f, Pxx = welch(x_proc, fs=fs, window='hann' if use_window else 'boxcar',
                           nperseg=nperseg, noverlap=noverlap)
            # приближённо переведём PSD в амплитуду (односторонняя)
            amps = np.sqrt(Pxx*2)
            freqs = f
        else:
            N = len(x_proc)
            pad = p.get('pad_factor', 4)
            Nfft = int(2**np.ceil(np.log2(N*pad)))
            if use_window:
                w = np.hanning(N)
                xw = x_proc * w
            else:
                xw = x_proc
            X = np.fft.fft(xw, n=Nfft)
            freqs = np.fft.fftfreq(Nfft, d=1.0/fs)[:Nfft//2]
            amps = 2.0 * np.abs(X[:Nfft//2]) / N

        # Сохранить spectrum CSV
        base = os.path.splitext(os.path.basename(fname))[0]
        out_csv = os.path.join(out_dir, f"{base}_spectrum.csv")
        save_spectrum_csv(out_csv, freqs, amps)
        print("  → Saved spectrum:", out_csv)

        # Поиск пиков (адаптивно)
        pd_params = {
            'noise_factor': p.get('noise_factor', 4.0),
            'use_savgol': p.get('use_savgol', False),
            'sg_window': p.get('sg_window', 11),
            'sg_poly': p.get('sg_poly', 3),
            'min_distance_hz': p.get('min_distance_hz', 0.5),
            'min_prominence': p.get('min_prominence', None)
        }
        peaks, thr = detect_spectral_peaks(freqs, amps, **pd_params)

        # Plot
        plt.figure(figsize=(9,4))
        plt.plot(freqs, amps, label='Amplitude')
        if len(peaks)>0:
            pf = [p['freq'] for p in peaks]
            pa = [p['amp'] for p in peaks]
            plt.plot(pf, pa, 'ro', label='Peaks')
        plt.xlabel('Frequency, Hz')
        plt.ylabel('Amplitude')
        plt.title(f"Spectrum: {base}  (method={method})")
        plt.xlim(0, min(freqs.max(), p.get('plot_max_freq', fs/2)))
        plt.grid(True)
        plt.legend()
        plt.show()

        results.append({'file': fname, 'spectrum_csv': out_csv, 'peaks': peaks, 'thr': thr, 'freqs': freqs, 'amps': amps})
    return results

# -----------------------
# STAGE 4: выделение мод и оценка затухания на фрагменте
# -----------------------
def stage4_extract_modes_and_estimate_decay(signal_csv, start_t, end_t, params, out_dir='stage4_results'):
    """
    signal_csv: CSV с полным сигналом (Time_s, Signal)
    start_t, end_t: границы фрагмента (сек)
    params: dict с параметрами
        - fs
        - search_peak_params: params for detect_spectral_peaks (noise_factor, ...)
        - bw_default: ширина полосы (Гц) для выделения моды (или функция)
        - filter_order
        - envelope_peak_thresh (fraction of max envelope)
        - min_peak_distance_peaks (сек) for envelope peaks detection
    Возвращает dict с modes и decay estimates.
    """
    os.makedirs(out_dir, exist_ok=True)
    t, x = read_signal_csv(signal_csv)
    fs = params['fs']

    # выделяем фрагмент по времени
    idx0 = int(round(start_t * fs))
    idx1 = int(round(end_t * fs))
    idx0 = max(0, idx0)
    idx1 = min(len(x), idx1)
    t_seg = t[idx0:idx1]
    x_seg = x[idx0:idx1].astype(float)
    x_seg = x_seg - np.mean(x_seg)
    x_seg = detrend(x_seg)

    # 1) spectrum of fragment (use FFT padded)
    N = len(x_seg)
    pad = params.get('pad_factor', 4)
    Nfft = int(2**np.ceil(np.log2(max(1,N*pad))))
    window = np.hanning(N)
    X = np.fft.fft(x_seg * window, n=Nfft)
    freqs = np.fft.fftfreq(Nfft, d=1.0/fs)[:Nfft//2]
    amps = 2.0 * np.abs(X[:Nfft//2]) / N

    # detect peaks in fragment spectrum
    sp_params = params.get('search_peak_params', {})
    peaks, thr = detect_spectral_peaks(freqs, amps, **sp_params)
    peak_freqs = [p['freq'] for p in peaks]

    modes = {}
    decay_rows = []
    for j, f0 in enumerate(peak_freqs):
        bw = params.get('bw_default', 1.0)
        try:
            sig_mode = bandpass_filtfilt(x_seg, fs, f0, bw, order=params.get('filter_order',4))
        except Exception as e:
            print(f"  [warn] filter failed for f0={f0:.3f} Hz: {e}")
            continue

        # огибающая
        env = np.abs(hilbert(sig_mode))

        # Найти пики огибающей (для регрессии)
        # порог относительно max env
        env_thr_frac = params.get('envelope_peak_thresh', 0.05)
        env_thr = np.max(env) * env_thr_frac
        # минимальное расстояние между пиками: convert seconds to samples
        min_dist_s = params.get('min_peak_distance_peaks', 1.0 / max(f0, 1.0))
        min_dist_samp = max(1, int(round(min_dist_s * fs)))
        peaks_env_idx, props = find_peaks(env, height=env_thr, distance=min_dist_samp)
        t_peaks = t_seg[peaks_env_idx]
        A_peaks = env[peaks_env_idx]

        # Регрессия ln(A) = ln(A0) - alpha * t
        decay_info = {'f0': f0, 'alpha': None, 'A0': None, 'Q': None, 'n_peaks': len(A_peaks), 'r2': None}
        if len(A_peaks) >= 3:
            # чтобы реже учитывать , возьмём первые K пиков вплоть до тех пор, пока A не станет очень малой
            # используем все найденные пики
            logA = np.log(A_peaks + 1e-15)
            # регрессия (временная шкала: от 0 относительно начала фрагмента)
            xreg = t_peaks - t_seg[0]
            coeffs = np.polyfit(xreg, logA, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            alpha = -slope
            A0 = np.exp(intercept)
            # оценка R^2:
            pred = coeffs[0]*xreg + coeffs[1]
            ss_res = np.sum((logA - pred)**2)
            ss_tot = np.sum((logA - np.mean(logA))**2)
            r2 = 1 - ss_res/ss_tot if ss_tot>0 else None

            Q = None
            if alpha > 0:
                # приблизительная связь Q = pi * f / alpha
                Q = np.pi * f0 / alpha

            decay_info.update({'alpha': float(alpha), 'A0': float(A0), 'Q': float(Q) if Q is not None else None, 'r2': float(r2)})
        else:
            # не хватило пиков для регрессии
            decay_info.update({'alpha': None, 'A0': None, 'Q': None, 'r2': None})

        modes[f0] = {'t': t_seg, 'mode_signal': sig_mode, 'envelope': env, 'env_peaks_t': t_peaks, 'env_peaks_A': A_peaks}
        decay_rows.append(decay_info)

        # сохранить режим и огибающую
        base = os.path.splitext(os.path.basename(signal_csv))[0]
        fname_mode = os.path.join(out_dir, f"{base}_f{f0:.3f}Hz_mode.csv")
        save_mode_csv(fname_mode, t_seg, sig_mode)
        fname_env = os.path.join(out_dir, f"{base}_f{f0:.3f}Hz_env.csv")
        save_mode_csv(fname_env, t_seg, env)
        print(f"  Saved mode {f0:.3f} Hz → {fname_mode}, envelope → {fname_env}")

    # сохранить таблицу с декрементами
    decay_csv = os.path.join(out_dir, os.path.splitext(os.path.basename(signal_csv))[0] + "_decay_table.csv")
    save_decay_table(decay_csv, decay_rows)
    print("  Decay table saved ->", decay_csv)

    # вернуть данные
    return {'freqs': freqs, 'amps': amps, 'peaks': peaks, 'modes': modes, 'decay_rows': decay_rows}

# -----------------------
# Пример использования
# -----------------------
if __name__ == "__main__":
    # Пример: 2 файла (замените на ваши)
    files = ["D:/.../sensor1_signal.csv", "D:/.../sensor2_signal.csv"]
    params_list = [
        {'fs': 5000, 'method': 'fft', 'use_window': True, 'pad_factor': 4,
         'noise_factor': 4.0, 'use_savgol': True, 'sg_window': 21, 'sg_poly': 3, 'min_distance_hz': 0.5},
        {'fs': 5000, 'method': 'fft', 'use_window': True, 'pad_factor': 4,
         'noise_factor': 4.0, 'use_savgol': True, 'sg_window': 21, 'sg_poly': 3, 'min_distance_hz': 0.5},
    ]
    # Stage 3: compute and save spectrum (visual inspection -> tune params)
    res_stage3 = stage3_compute_and_save_spectrum(files, params_list, out_dir='stage3_results')

    # Stage 4: pick one fragment (for example from the first file)
    frag_params = {'fs': 5000, 'pad_factor': 4, 'search_peak_params': {'noise_factor':3.0,'use_savgol':True,'sg_window':21,'sg_poly':3,'min_distance_hz':0.5},
                   'bw_default': 1.0, 'filter_order':4, 'envelope_peak_thresh':0.05, 'min_peak_distance_peaks':0.01}
    # pick start/end in seconds for some selected hit:
    # e.g. start=0.200, end=0.500
    # res4 = stage4_extract_modes_and_estimate_decay(files[0], 0.20, 0.70, frag_params, out_dir='stage4_results')
