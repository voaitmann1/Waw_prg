import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.optimize import curve_fit
import glob
import os


# === 1. Функции ===


def load_signal_csv(filename):
    """Загрузка CSV с одним столбцом сигналов"""
    data = pd.read_csv(filename, header=None)
    return data.values.flatten()

def envelope_hilbert(signal):
    analytic = hilbert(signal)
    return np.abs(analytic)


def envelope_lsq(signal):
    """Аппроксимация огибающей методом наименьших квадратов (экспонента)"""
    x = np.arange(len(signal))
    y = np.abs(signal)

    def model(x, a, b):
        return a * np.exp(b * x)

    # берём только положительные значения
    y_pos = y[y > 0]
    x_pos = x[:len(y_pos)]
    if len(y_pos) < 5:
        return y
    try:
        popt, _ = curve_fit(model, x_pos, y_pos, p0=(np.max(y_pos), -0.001))
        return model(x, *popt)
    except:
        return y


def energy(signal):
    return np.sum(signal**2)


def log_decrement(envelope):
    """Вычисление декремента затухания по пикам огибающей"""
    peaks = envelope[::len(envelope)//10] # берём 10 характерных точек
    peaks = peaks[peaks > 0]
    if len(peaks) < 2:
        return None
    deltas = []
    for i in range(len(peaks)-1):
        d = np.log(peaks[i] / peaks[i+1])
        deltas.append(d)
    return np.mean(deltas)


# === 2. Основная логика ===

data_dir = "." # рабочая папка
impact_files = sorted(glob.glob(os.path.join(data_dir, "*_signal_ImpactRange.csv")))
whole_files = sorted(glob.glob(os.path.join(data_dir, "*_signal_whole.csv")))


results = []


for impact_file, whole_file in zip(impact_files, whole_files):
    signal_impact = load_signal_csv(impact_file)
    signal_whole = load_signal_csv(whole_file)


    # Огибающие
    env_hilbert = envelope_hilbert(signal_impact)
    env_lsq = envelope_lsq(signal_impact)


    # Энергии
    energy_impact = energy(signal_impact)
    energy_whole = energy(signal_whole)


    # Декременты
    dec_hilbert = log_decrement(env_hilbert)
    dec_lsq = log_decrement(env_lsq)


    results.append({
        "file": os.path.basename(impact_file),
        "energy_impact": energy_impact,
        "energy_whole": energy_whole,
        "dec_hilbert": dec_hilbert,
        "dec_lsq": dec_lsq
    })


    # Графики огибающих
    plt.figure(figsize=(10,5))
    plt.plot(signal_impact, label="сигнал удара")
    plt.plot(env_hilbert, 'r--', label="огибающая Гильберт")
    plt.plot(env_lsq, 'g--', label="огибающая МНК")
    plt.title(f"Огибающие: {os.path.basename(impact_file)}")
    plt.legend()
    plt.show()


# === 3. Суммарные энергии ===
energy_sum_13 = results[0]["energy_whole"] + results[2]["energy_whole"]
energy_sum_24 = results[1]["energy_whole"] + results[3]["energy_whole"]


# === 4. Вывод результатов ===
print("Результаты по каждому файлу:")
for r in results:
    print(r)


print("\nСуммарная энергия (1+3):", energy_sum_13)
print("Суммарная энергия (2+4):", energy_sum_24)
