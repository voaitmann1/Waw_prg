import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft
import pywt   # для wavelet

#spectrum

# --- 1. Чтение WAV ---
def read_wav(filename):
    fs, data = wavfile.read(filename)
    if data.ndim > 1:  # если стерео, берём только 1 канал
        data = data[:, 0]
    if np.issubdtype(data.dtype, np.integer):
        data = data.astype(np.float32) / np.iinfo(data.dtype).max
    return fs, data

# --- 2. FFT ---
def plot_fft(data, fs):
    N = len(data)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    spectrum = np.abs(np.fft.rfft(data))**2 / N  # спектральная энергия
    
    plt.figure(figsize=(10,4))
    plt.plot(freqs, spectrum)
    plt.xlabel("Частота, Гц")
    plt.ylabel("Энергия")
    plt.title("FFT спектр")
    plt.grid(True)
    plt.show()

# --- 3. STFT ---
def plot_stft(data, fs, nperseg=1024):
    f, t, Zxx = stft(data, fs=fs, nperseg=nperseg)
    plt.figure(figsize=(10,4))
    plt.pcolormesh(t, f, np.abs(Zxx), shading='gouraud')
    plt.ylabel("Частота, Гц")
    plt.xlabel("Время, с")
    plt.title("STFT спектрограмма")
    plt.colorbar(label="Амплитуда")
    plt.show()

# --- 4. Wavelet ---
def plot_wavelet(data, fs, wavelet="cmor1.5-1.0"):
    scales = np.arange(1, 200)
    coefficients, freqs = pywt.cwt(data, scales, wavelet, 1/fs)
    
    plt.figure(figsize=(10,6))
    plt.imshow(np.abs(coefficients), extent=[0, len(data)/fs, freqs[-1], freqs[0]],
               aspect='auto', cmap='jet')
    plt.ylabel("Частота, Гц")
    plt.xlabel("Время, с")
    plt.title("Wavelet спектрограмма (CWT)")
    plt.colorbar(label="Амплитуда")
    plt.show()

# --- пример использования ---
fileName = "test.wav"   # замените на свой путь
fs, data = read_wav(fileName)

plot_fft(data, fs)
plot_stft(data, fs)
plot_wavelet(data, fs)
