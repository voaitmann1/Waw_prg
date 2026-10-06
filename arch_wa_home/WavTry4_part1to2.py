import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# --- функции ---

def read_csv_signal(filename):
    """Читает CSV с Time_s, Signal, Energy"""
    t, s, e = [], [], []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            t.append(float(row["Time_s"]))
            s.append(float(row["Signal"]))
            e.append(float(row["Energy"]))
    return np.array(t), np.array(s), np.array(e)

def read_impact_bounds(filename):
    """Читает ImpactBounds.csv"""
    bounds = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bounds.append((int(row["ImpactID"]),
                           float(row["StartTime_s"]),
                           float(row["EndTime_s"])))
    return bounds

def plot_signal(t, s, title="Сигнал", t_start=None, t_end=None):
    """Строит график всего или фрагмента"""
    if t_start is None:
        t_start, t_end = t[0], t[-1]
    mask = (t >= t_start) & (t <= t_end)
    plt.figure(figsize=(12,6))
    plt.plot(t[mask], s[mask])
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.title(title)
    plt.grid()
    plt.show()

# --- основная программа ---

if __name__ == "__main__":
    fileOwnNames = ["051_1_M.wav", "051-2.wav", "052-1.wav", "052-2.wav"]
    filePath = "D:\\MyFilesCur\\MyPrgs\\Python\\Wav"
    filePathIniData = filePath + "\\" + "assets"
    filePathResults = filePath + "\\" + "assets"

    # читаем ImpactBounds
    bounds = read_impact_bounds(filePathResults + "\\" + "ImpactBounds.csv")

    Nrec = 0
    for fileOwnName in fileOwnNames:
        Nrec += 1
        base = os.path.splitext(fileOwnName)[0]

        # --- читаем сигнал целиком ---
        whole_csv = filePathIniData + "\\" + base + "_signal_whole.csv"
        t, s, e = read_csv_signal(whole_csv)
        plot_signal(t, s, title=f"{base} - весь сигнал")

        # --- вариант 1: вырезка по ImpactBounds ---
        Nimp = 0
        for impact in bounds:
            Nimp += 1
            # условие: для 1 и 3 файла берем первый удар, для 2 и 4 второй
            if ((Nrec==1 or Nrec==3) and Nimp==1) or ((Nrec==2 or Nrec==4) and Nimp==2):
                imp_id, t_start, t_end = impact
                plot_signal(t, s, title=f"{base} - удар {imp_id} (из whole.csv)", 
                            t_start=t_start, t_end=t_end)

        # --- вариант 2: готовый ImpactRange CSV ---
        impact_csv = filePathIniData + "\\" + base + "_signal_ImpactRange.csv"
        if os.path.exists(impact_csv):
            t_imp, s_imp, e_imp = read_csv_signal(impact_csv)
            plot_signal(t_imp, s_imp, title=f"{base} - удар (из ImpactRange.csv)")
        else:
            print(f"⚠ {impact_csv} не найден")
