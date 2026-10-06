def compute_spectrum(x, fs, use_window=True, remove_mean=True, zero_padding_factor=1):

    x = np.asarray(x, dtype=float)

    if remove_mean:
        x = x - np.mean(x)

    N0 = len(x)
    N = N0 * zero_padding_factor

    if zero_padding_factor > 1:
        x = np.pad(x, (0, N - N0))

    if use_window:
        w = np.hanning(len(x))
        x = x * w
        w_norm = np.sum(w) / len(w)
    else:
        w_norm = 1.0

    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(N, d=1/fs)

    amps = np.abs(X) / (N * w_norm)
    amps[1:] *= 2

    return freqs, amps
	
def compute_spectrum(x, fs,
                     use_window=False,
                     use_mean=False,
                     use_detrend=False,
                     zero_padding_factor=1):

    x_proc = np.array(x, dtype=float)

    if use_mean:
        x_proc -= np.mean(x_proc)

    if use_detrend:
        x_proc = detrend(x_proc)

    N_orig = len(x_proc)
    N = N_orig * zero_padding_factor

    if zero_padding_factor > 1:
        x_proc = np.pad(x_proc, (0, N - N_orig), 'constant')

    if use_window:
        window = np.hanning(len(x_proc))
        x_proc *= window

    X = np.fft.fft(x_proc)

    amps = 2 * np.abs(X[:N//2]) / N
    freqs = np.fft.fftfreq(N, d=1/fs)[:N//2]

    return freqs, amps
	
	
from scipy.signal import detrend

def compute_spectrum(
    x,
    fs,
    window_type=None,      # None, 'hann', 'decay'
    alpha=None,            # только для decay
    use_mean=False,
    use_detrend=False,
    zero_padding_factor=1
):
    """
    Вычисление амплитудного спектра.
    """

    x_proc = np.array(x, dtype=float)

    # --- подготовка сигнала ---
    if use_mean:
        x_proc -= np.mean(x_proc)

    if use_detrend:
        x_proc = detrend(x_proc)

    N_orig = len(x_proc)

    # --- zero padding ---
    if zero_padding_factor > 1:
        N = N_orig * zero_padding_factor
        x_proc = np.pad(x_proc, (0, N - N_orig), 'constant')
    else:
        N = N_orig

    # --- окна ---
    if window_type == 'hann':
        window = np.hanning(len(x_proc))
        x_proc *= window

    elif window_type == 'decay':
        if alpha is None:
            raise ValueError("Для decay окна необходимо задать alpha")
        window = decay_window(len(x_proc), fs, alpha)
        x_proc *= window

    # --- FFT ---
    X = np.fft.fft(x_proc)
    amps = 2 * np.abs(X[:N // 2]) / N
    freqs = np.fft.fftfreq(N, d=1/fs)[:N // 2]

    return freqs, amps
	
#

def extract_modes(
    t,
    x,
    fs,
    frequencies,
    bandwidths,
    decay_windows=None
):
    """
    frequencies — список частот мод
    bandwidths — список полос
    decay_windows — [(t1, t2), ...] или None
    """

    modes = []

    for i, f0 in enumerate(frequencies):
        bw = bandwidths[i]

        win = None
        if decay_windows:
            win = decay_windows[i]

        mode = extract_mode(
            t,
            x,
            fs,
            f0,
            bw,
            decay_fit_window=win
        )

        modes.append(mode)

    return modes
	
def extract_mode(
    t,
    x,
    fs,
    f0,
    bandwidth,
    filter_order=4,
    decay_fit_window=None
):
    """
    Полный цикл выделения моды.
    """

    # 1. Фильтр
    x_mode = bandpass_filter(
        x, fs, f0, bandwidth, filter_order
    )

    # 2. Огибающая
    env = envelope_hilbert(x_mode)

    # 3. Затухание
    if decay_fit_window:
        decay, coef = estimate_decay(
            t,
            env,
            decay_fit_window[0],
            decay_fit_window[1]
        )
    else:
        decay, coef = estimate_decay(t, env)

    return {
        "frequency": f0,
        "signal": x_mode,
        "envelope": env,
        "decay_rate": decay,
        "fit_coef": coef
    }
	
#decay rate ut'modes	
def estimate_decay(
    t,
    envelope,
    t_start=None,
    t_end=None
):
    """
    Оценка коэффициента затухания по огибающей.
    """

    mask = np.ones_like(t, dtype=bool)

    if t_start is not None:
        mask &= t >= t_start
    if t_end is not None:
        mask &= t <= t_end

    t_fit = t[mask]
    env_fit = envelope[mask]

    # защита от лог(0)
    env_fit = np.maximum(env_fit, np.max(env_fit) * 1e-6)

    ln_env = np.log(env_fit)

    # линейная аппроксимация
    coef = np.polyfit(t_fit, ln_env, 1)

    decay_rate = -coef[0]  # 1/с
    return decay_rate, coef
	
from scipy.signal import butter, filtfilt

def bandpass_filter(
    x,
    fs,
    f0,
    bandwidth,
    order=4
):
    """
    Узкополосный фильтр вокруг моды f0.
    bandwidth — полная ширина полосы (Гц)
    """

    f1 = max(f0 - bandwidth / 2, 0.1)
    f2 = f0 + bandwidth / 2

    nyq = fs / 2
    b, a = butter(
        order,
        [f1 / nyq, f2 / nyq],
        btype='band'
    )

    return filtfilt(b, a, x)
	
#Как выбрать bandwidth
#Ситуация	bandwidth
#чистая мода	2–5% от f₀
#близкие пики	1–2%
#сильный шум	5–10%
#
#👉 Слишком широко → биения
#👉 Слишком узко → «размазанная» фаза

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window

def spectrum(x, fs):
    N = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(N, d=1/fs)
    A = np.abs(X) / N
    return f, A

# === входные данные ===
# t, x, fs должны быть уже определены

# --- окно ---
window_type = 'hann'   # 'hann', 'hamming', 'blackman'
w = get_window(window_type, len(x))

x_windowed = x * w

# --- спектры ---
f, A = spectrum(x, fs)
fw, Aw = spectrum(x_windowed, fs)

# --- графики во времени ---
plt.figure(figsize=(10,4))
plt.plot(t, x, label='Исходный сигнал', alpha=0.7)
plt.plot(t, x_windowed, label='С окном', alpha=0.7)
plt.legend()
plt.xlabel('t, s')
plt.ylabel('x')
plt.title('Сигнал во времени')
plt.grid()
plt.show()

# --- графики спектров ---
plt.figure(figsize=(10,4))
plt.semilogy(f, A, label='Без окна')
plt.semilogy(fw, Aw, label='С окном')
plt.legend()
plt.xlabel('f, Hz')
plt.ylabel('|X(f)|')
plt.title('Амплитудный спектр')
plt.grid()
plt.show()

#📌 semilogy обязателен, иначе хвосты ты просто не увидишь.
