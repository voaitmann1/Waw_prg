import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

#realtime harmonics separate



def extract_harmonic(data, fs, f0, bandwidth=5.0):
    """
    Выделяет одну гармонику методом фильтрации в спектре.
    f0        - центральная частота гармоники (Гц)
    bandwidth - ширина полосы (Гц)
    """
    N = len(data)
    # FFT
    spectrum = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(N, d=1/fs)

    # Фильтр: обнуляем всё, кроме нужной полосы
    mask = (freqs > f0 - bandwidth/2) & (freqs < f0 + bandwidth/2)
    filtered_spectrum = np.zeros_like(spectrum)
    filtered_spectrum[mask] = spectrum[mask]

    # Обратное FFT -> временной сигнал гармоники
    harmonic = np.fft.irfft(filtered_spectrum, n=N)
    return harmonic

# --- Пример использования ---
fs, data = wavfile.read("test.wav")
if data.ndim > 1:
    data = data[:, 0]  # первый канал, если стерео
if np.issubdtype(data.dtype, np.integer):
    data = data.astype(np.float32) / np.iinfo(data.dtype).max

# Выделяем гармоники 50 Гц, 150 Гц и 300 Гц
harm1 = extract_harmonic(data, fs, f0=50, bandwidth=5)
harm2 = extract_harmonic(data, fs, f0=150, bandwidth=5)
harm3 = extract_harmonic(data, fs, f0=300, bandwidth=5)

# Рисуем
t = np.arange(len(data)) / fs
plt.figure(figsize=(12,6))
plt.plot(t, data, label="Исходный сигнал", alpha=0.5)
plt.plot(t, harm1, label="50 Гц")
plt.plot(t, harm2, label="150 Гц")
plt.plot(t, harm3, label="300 Гц")
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid(True)
plt.show()
