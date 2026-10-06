import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, hilbert, find_peaks, savgol_filter

# === Авто-генерация параметров для каждой моды ===
def make_params(freq, fs):
    bw = max(1.0, freq/50.0)  # полоса по умолчанию
    return dict(
        freq=freq,
        bandwidth=bw,
        filter_type="butter",
        filter_order=4,
        transient_cut=max(3.0/freq, 0.01),
        peak_distance=0.8/freq,
        envelope_smooth=dict(method="savgol", window=max(5, int(fs/(10*freq))//2*2+1), poly=2),
        fit_method="peaks",
        min_peaks=5,
        output_mode="params",
        notes=""
    )

# === Оценка затухания для одной моды ===
def process_mode(x, t, fs, params):
    f0 = params["freq"]
    bw = params["bandwidth"]
    nyq = fs/2
    
    # Фильтрация
    low = max(0.1, (f0 - bw/2)/nyq)
    high = min(0.999, (f0 + bw/2)/nyq)
    b, a = butter(params["filter_order"], [low, high], btype="band")
    x_filt = filtfilt(b, a, x)

    # Огибающая через Гильберта
    analytic = hilbert(x_filt)
    A = np.abs(analytic)

    # Отсечь начальный переходный процесс
    cut_samples = int(params["transient_cut"]*fs)
    if cut_samples < len(A):
        A = A[cut_samples:]
        t_seg = t[cut_samples:]
    else:
        return None

    # Сглаживание огибающей
    if params["envelope_smooth"]:
        w = params["envelope_smooth"]["window"]
        p = params["envelope_smooth"]["poly"]
        if len(A) > w:
            A = savgol_filter(A, w, p)

    # Поиск пиков
    dist = int(params["peak_distance"]*fs)
    peaks, _ = find_peaks(A, distance=dist)
    if len(peaks) < params["min_peaks"]:
        return None

    t_peaks = t_seg[peaks]
    A_peaks = A[peaks]

    # Логарифмическая регрессия
    y = np.log(A_peaks)
    C = np.mean(t_peaks)
    D = np.mean(y)
    num = np.sum((t_peaks - C)*(y - D))
    den = np.sum((t_peaks - C)**2)
    beta = num/den
    alpha = D - beta*C

    # Метрики
    y_pred = alpha + beta*t_peaks
    SSR = np.sum((y - y_pred)**2)
    SST = np.sum((y - np.mean(y))**2)
    R2 = 1 - SSR/SST
    E = SSR/(len(t_peaks)-2)

    delta = -beta
    tau = 1.0/delta if delta>0 else np.inf
    Q = np.pi*f0/delta if delta>0 else np.inf

    return dict(
        freq=f0,
        bandwidth=bw,
        n_peaks=len(peaks),
        alpha=alpha,
        beta=beta,
        delta=delta,
        tau=tau,
        Q=Q,
        R2=R2,
        E=E,
        notes=params["notes"]
    )

# === Основной анализ для списка частот ===
def process_modes(x, t, fs, freq_list):
    results = []
    for f in freq_list:
        params = make_params(f, fs)
        res = process_mode(x, t, fs, params)
        if res is not None:
            results.append(res)
    return pd.DataFrame(results)
