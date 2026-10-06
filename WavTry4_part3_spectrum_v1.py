import math
import numpy as np
import matplotlib.pyplot as plt

import math
import numpy as np
import matplotlib.pyplot as plt

def spectrum_dft(x, fs=1000, use_window=False):#direct, no libs
    N = len(x)
    x_proc = np.array(x, dtype=float)

    # Применяем окно Hann
    if use_window:
        window = np.hanning(N)
        x_proc *= window

    X_real = [0.0] * N
    X_imag = [0.0] * N

    for k in range(N):
        for n in range(N):
            angle = 2 * math.pi * k * n / N
            X_real[k] += x_proc[n] * math.cos(angle)
            X_imag[k] -= x_proc[n] * math.sin(angle)

    amps = [2 * math.sqrt(X_real[k]**2 + X_imag[k]**2) / N for k in range(N//2)]
    freqs = [k * fs / N for k in range(N//2)]
    return freqs, amps


def spectrum_fft(x, fs=1000, use_window=False):#quick with libs
    x_proc = np.array(x, dtype=float)
    N = len(x_proc)

    # window Hann, if cond
    if use_window:
        window = np.hanning(N)
        x_proc *= window

    X = np.fft.fft(x_proc)
    amps = 2 * np.abs(X[:N//2]) / N
    freqs = np.fft.fftfreq(N, d=1/fs)[:N//2]
    return freqs, amps

def compute_spectrum(x, fs=1000, method='fft', use_window=False, plot=True):
    """
    x - сигнал (список или numpy array)
    fs - частота дискретизации
    method - 'fft' или 'dft'
    use_window - применять окно Hann
    plot - строить график
    """
    if method == 'fft':
        freqs, amps = spectrum_fft(x, fs, use_window)
    elif method == 'dft':
        freqs, amps = spectrum_dft(x, fs, use_window)
    else:
        raise ValueError("method must be 'fft' or 'dft'")

    if plot:
        plt.figure(figsize=(8,4))
        plt.plot(freqs, amps)
        plt.xlabel("Частота, Гц")
        plt.ylabel("Амплитуда")
        plt.title(f"Спектр сигнала ({method}, window={use_window})")
        plt.grid(True)
        plt.show()

    return freqs, amps

if __name__ == "__main__":
    # Сигнал: синусоида 50 Гц + 120 Гц
    fs = 1000
    t = np.arange(0, 1, 1/fs)
    x = 1.0 * np.sin(2*np.pi*50*t) + 0.5 * np.sin(2*np.pi*120*t)

    # FFT с окном
    compute_spectrum(x, fs, method='fft', use_window=True)

    # DFT без окна (медленно!)
    # compute_spectrum(x, fs, method='dft', use_window=False)
