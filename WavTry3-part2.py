# part 2 - not needed

import numpy as np
from scipy.signal import find_peaks, hilbert
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
import csv
import os

def read_signal_csv(filename):
    times = []
    values = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row["Time_s"]))
            values.append(float(row["Signal"]))
    return np.array(times), np.array(values)

def read_impact_bounds(filename):
    impacts = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            impacts.append((int(row["ImpactID"]), float(row["StartTime_s"]), float(row["EndTime_s"])))
    return impacts

def analyze_impact(t, signal, t_start, t_end, peak_threshold=0.05, spline_smooth_factor=0.1):
    mask = (t >= t_start) & (t <= t_end)
    segment = signal[mask]
    t_segment = t[mask]

    # --- Пики ---
    peaks, _ = find_peaks(np.abs(segment), height=np.max(np.abs(segment))*peak_threshold)
    peak_times = t_segment[peaks]
    peak_values = np.abs(segment[peaks])

    # --- Огибающая по пикам ---
    spline = UnivariateSpline(peak_times, peak_values, s=spline_smooth_factor*np.sum(peak_values**2))
    envelope_peaks = spline(t_segment)

    # --- Огибающая через Гильберта ---
    analytic_signal = hilbert(segment)
    envelope_hilbert = np.abs(analytic_signal)

    return t_segment, segment, peak_times, peak_values, envelope_peaks, envelope_hilbert

def save_segment_csv(filename, t_segment, segment, peak_times, peak_values, envelope_peaks, envelope_hilbert, impact_id):
    base = os.path.splitext(filename)[0]
    # Сигнал сегмента
    signal_csv = f"{base}_impact{impact_id}_signal.csv"
    with open(signal_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time_s", "Signal"])
        for i in range(len(t_segment)):
            writer.writerow([t_segment[i], segment[i]])
    # Пики
    peaks_csv = f"{base}_impact{impact_id}_peaks.csv"
    with open(peaks_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Peak_Time_s", "Peak_Amplitude"])
        for i in range(len(peak_times)):
            writer.writerow([peak_times[i], peak_values[i]])
    # Огибающие
    env_csv = f"{base}_impact{impact_id}_envelopes.csv"
    with open(env_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time_s", "Envelope_Peaks", "Envelope_Hilbert"])
        for i in range(len(t_segment)):
            writer.writerow([t_segment[i], envelope_peaks[i], envelope_hilbert[i]])

    print(f"Файлы сохранены для удара {impact_id}: {signal_csv}, {peaks_csv}, {env_csv}")

def plot_segment(t_segment, segment, peak_times, peak_values, envelope_peaks, envelope_hilbert, impact_id):
    plt.figure(figsize=(12,6))
    plt.plot(t_segment, segment, label='Сигнал')
    plt.plot(t_segment, envelope_peaks, 'r', label='Огибающая по пикам')
    plt.plot(t_segment, envelope_hilbert, 'g--', label='Огибающая через Гильберта')
    plt.scatter(peak_times, peak_values, color='k', marker='o', label='Пики')
    plt.xlabel('Время, с')
    plt.ylabel('Амплитуда')
    plt.title(f'Удар {impact_id}')
    plt.legend()
    plt.grid()
    plt.show()

# -----------------------------
if __name__ == "__main__":
    signal_csv_file = "file1_signal.csv"  # CSV сигнал из программы 1
    impact_bounds_file = "ImpactBounds.csv"

    t, signal = read_signal_csv(signal_csv_file)
    impacts = read_impact_bounds(impact_bounds_file)

    for impact_id, t_start, t_end in impacts:
        t_seg, seg, peak_times, peak_values, env_peaks, env_hilbert = analyze_impact(t, signal, t_start, t_end)
        save_segment_csv(signal_csv_file, t_seg, seg, peak_times, peak_values, env_peaks, env_hilbert, impact_id)
        plot_segment(t_seg, seg, peak_times, peak_values, env_peaks, env_hilbert, impact_id)
