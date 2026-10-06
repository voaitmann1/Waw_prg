import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

fs=1000
t=np.linspace(0, 2, 2*fs, endpoint=False)

f0=40
x=np.exp(-2*t)*np.sin(2*np.pi*f0*t)
X=np.fft.rfft(x)
freqs=np.fft.rfftfreq(len(x), 1/fs)
amps=np.abs(X)

peaks, _ = find_peaks(amps, height=10)

plt.plot(freqs, amps)
plt.plot(freqs[peaks], amps[peaks], "ro")
plt.xlabel("Частота, Гц")
plt.ylabel("Амплитуда")
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Пример сигнала
fs = 1000  # частота дискретизации
t = np.linspace(0, 1, fs)
x = np.sin(2*np.pi*5*t) * np.exp(-3*t) + 0.05*np.random.randn(fs)

# Пример найденных сегментов (start, end)
segments = [(0.1, 0.2), (0.2, 0.35), (0.35, 0.55), (0.55, 0.8)]

# Найдём диапазон по y (от минимального до максимального пика)
ymin, ymax = np.min(x), np.max(x)

# График
plt.figure(figsize=(10, 4))
plt.plot(t, x, label="сигнал")

# Добавляем вертикальные линии по границам сегментов
for seg in segments:
    start, end = seg
    plt.vlines([start, end], ymin, ymax, colors="r", linestyles="--")

plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.title("Сигнал с разделительными линиями сегментов")
plt.legend()
plt.grid(True)
plt.show()
