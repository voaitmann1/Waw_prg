mean_spec = np.sqrt(np.mean(all_spectra**2, axis=0))
find_peaks(mean_spec)

from scipy.signal import find_peaks
import numpy as np

def find_spectrum_peaks(freqs, amps,
                        prominence_ratio=0.05,
                        min_distance_hz=1.0,
                        max_freq=None):

    amps = np.array(amps)
    freqs = np.array(freqs)

    # шаг частоты
    df = freqs[1] - freqs[0]

    # минимальная дистанция в точках FFT
    distance_pts = int(min_distance_hz / df)

    # prominence
    prom = prominence_ratio * np.max(amps)

    peaks, props = find_peaks(
        amps,
        prominence=prom,
        distance=distance_pts
    )

    peak_freqs = freqs[peaks]
    peak_amps = amps[peaks]

    # ограничение по частоте
    if max_freq is not None:
        mask = peak_freqs <= max_freq
        peak_freqs = peak_freqs[mask]
        peak_amps = peak_amps[mask]
        peaks = peaks[mask]

    return peaks, peak_freqs, peak_amps

def refine_all_peaks(freqs, amps, peak_indices):

    refined_freqs = []
    refined_amps = []

    for p in peak_indices:
        f,a = refine_peak_frequency(freqs, amps, p)
        refined_freqs.append(f)
        refined_amps.append(a)

    return np.array(refined_freqs), np.array(refined_amps)

#geq pipeline
#step 1 - reading impacts
all_amps = []

for impact in impacts:

    freqs, amps = compute_spectrum(
        impact,
        fs,
        use_window=True,
        use_mean=True,
        use_detrend=True,
        zero_padding_factor=4
    )

    all_amps.append(amps)

#STEP 2 — averaging
all_amps = np.array(all_amps)
avg_amps = np.sqrt(np.mean(all_amps**2, axis=0))
#STEP 3 — поиск пиков
from scipy.signal import find_peaks

peaks, props = find_peaks(
    avg_amps,
    prominence=0.05*np.max(avg_amps),
    distance=5
)
#
#STEP 4 — refine peaks
refined_freqs, refined_amps = refine_all_peaks(freqs, avg_amps, peaks)

#Что ты получаешь
#Очень чистый список: modal_frequencies

#Теперь твой любимый момент: Сравнение со статьёй.

for f_article in FreqsSample:
    найти ближайшую refined_freq

#
#claster'g
for f_article in FreqsSample:
    найти ближайшую refined_freq

#FFT шаг
df = fs / N
#Без интерполяции:
#tol ≈ df/2
#С параболической интерполяцией: точность лучше. Реально используют:
#tol ≈ df/3  или  df/5
#tol НЕ должен быть:
#❌ слишком маленьким → одна мода распадётся на несколько.
#❌ слишком большим → разные моды сольются.tol НЕ должен быть:
tol = 2 * std(freq_estimates) #qo sdi?

#Если две реальные моды ближе чем df:
#👉 FFT плохо их разделяет.
#Тогда кластеризация особенно нужна.

#Общая идея

#Для каждой найденной модальной частоты 
#fh
#f
#h
#	​
#
#:
#
#👉 фильтруем исходный временной сигнал узкой полосой вокруг неё.
#
#Результат:
# xh(t) — вклад одной моды
#
#sha
#
#signal      # временной сигнал одного удара
#fs          # частота дискретизации
#f_modal     # список модальных частот (после find_peaks)
#
#zB f_modal = [1.538, 5.897, 10.768, 31.024]
#df = 1–3 FFT bins
df_fft = freqs[1] - freqs[0]
df = 2 * df_fft
#STEP 3 — функция bandpass
#Используем zero-phase фильтр:
from scipy.signal import butter, filtfilt

def bandpass_filter(x, fs, f0, df, order=4):
    nyq = fs / 2
    low = (f0 - df) / nyq
    high = (f0 + df) / nyq
    if low <= 0:
        low = 1e-6
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, x)

#STEP 4 — получение всех гармоник
xh_list = []
for fh in f_modal:
    xh = bandpass_filter(signal, fs, fh, df)
    xh_list.append(xh)
#nu:
xh_list[h] = xh(t)
#STEP 5 — проверка (обязательно!)
plt.plot(signal)
plt.plot(xh)
#Очень важный момент (частая ошибка)
#НЕ фильтруйте FFT.
#Фильтровать надо:
#временной сигнал!
#
#сумма всех мод примерно восстанавливает сигнал:
#
#reconstructed = sum(xh_list)
