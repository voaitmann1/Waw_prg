import numpy as np
import csv
import os
import matplotlib


# Попытка использовать интерактивный бэкенд, если он доступен. Если нет — переходим в неинтерактивный.
try:
    matplotlib.use('TkAgg')
except Exception:
    try:
        matplotlib.use('Agg')
    except Exception:
        pass


import matplotlib.pyplot as plt
from scipy.signal import hilbert, find_peaks
from scipy.optimize import curve_fit


# -----------------------------
# Надёжное чтение CSV (поддерживает заголовок или без)
# -----------------------------

def read_csv_signal(filename):
    """Читает CSV с колонками Time_s, Signal, Energy или без заголовка.
    Возвращает (t, signal, energy)
    """
    t = []
    s = []
    e = []
    with open(filename, newline='') as f:
        # Попробуем читать как DictReader (с заголовками)
        f.seek(0)
        first = f.readline()
        f.seek(0)
        # Если первая строка содержит нечисловые слова — скорее всего заголовок
        has_header = any(c.isalpha() for c in first)
        f.seek(0)
        if has_header:
            reader = csv.DictReader(f)
            # Поддерживаем разные написания заголовков
            for row in reader:
                # Некоторые CSV могут иметь пустые строки
                if not row:
                    continue
                # Попробуем брать по именам, иначе по порядок
                try:
                    t.append(float(row.get('Time_s') or row.get('time_s') or row.get('Time') or list(row.values())[0]))
                    s.append(float(row.get('Signal') or row.get('signal') or list(row.values())[1]))
                    # энергия может отсутствовать
                    e_val = row.get('Energy') or row.get('energy')
                    if e_val is None or e_val == '':
                        e.append((float(row.get('Signal') or list(row.values())[1]))**2)
                    else:
                        e.append(float(e_val))
                except Exception:
                    # если не получилось читать по именам — попытаемся позиционно
                    vals = list(row.values())
                    if len(vals) >= 3:
                        t.append(float(vals[0])); s.append(float(vals[1])); e.append(float(vals[2]))
                    elif len(vals) >= 2:
                        t.append(float(vals[0])); s.append(float(vals[1])); e.append(float(vals[1])**2)
        else:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                # ожидаем минимум 2 колонки: time, signal
                if len(row) >= 3:
                    t.append(float(row[0])); s.append(float(row[1])); e.append(float(row[2]))
                elif len(row) >= 2:
                    t.append(float(row[0])); s.append(float(row[1])); e.append(float(row[1])**2)
                else:
                    continue
    return np.array(t), np.array(s), np.array(e)


# -----------------------------
# Огибающие и подгонка экспоненты по пикам
# -----------------------------

def compute_envelope_hilbert(signal):
    analytic = hilbert(signal)
    return np.abs(analytic)

def fit_exponential_to_peaks(t_peaks, a_peaks, with_offset=True):
    """Фит функции A*exp(-delta * t) + C к набору пиков.
    Возвращает popt (A, delta, C) или None если не получилось"""
    if len(a_peaks) < 3:
        return None
    # приводим время относительно первой точки
    t_rel = t_peaks - t_peaks[0]

    if with_offset:
        def model(t, A, delta, C):
            return A * np.exp(-delta * t) + C
        p0 = (a_peaks[0], 1.0, 0.0)
        bounds = ([0.0, 0.0, -np.inf], [np.inf, np.inf, np.inf])
    else:
        def model(t, A, delta):
            return A * np.exp(-delta * t)
        p0 = (a_peaks[0], 1.0)
        bounds = ([0.0, 0.0], [np.inf, np.inf])


    try:
        popt, pcov = curve_fit(model, t_rel, a_peaks, p0=p0, bounds=bounds, maxfev=20000)
        return popt
    except Exception as ex:
        # неудачная подгонка
        return None


def compute_peaks_and_fit(t_segment, segment, peak_prominence=0.01, peak_distance_samples=10):
    """Находит пики в сегменте, возвращает времена пиков, амплитуды,
    параметры экспоненциальной аппроксимации и линейной регрессии ln(A)~t"""
    # ищем пики по модулю
    abs_seg = np.abs(segment)
    if len(abs_seg) < 3:
        return np.array([]), np.array([]), None, None
    # find_peaks: высота = порог (примерно 1% от макс) или по prominence
    height = np.max(abs_seg) * peak_prominence
    peaks, props = find_peaks(abs_seg, height=height, distance=peak_distance_samples)
    if len(peaks) == 0:
        return np.array([]), np.array([]), None, None
        peak_times = t_segment[peaks]
        peak_amps = abs_seg[peaks]


    # экспоненциальная аппроксимация по пикам
    popt = fit_exponential_to_peaks(peak_times, peak_amps, with_offset=True)

    # линейная аппроксимация ln(A) = ln(A0) - delta * t
    lin_delta = None
    if len(peak_amps) >= 2 and np.all(peak_amps > 0):
        try:
            coeffs = np.polyfit(peak_times - peak_times[0], np.log(peak_amps), 1)
            slope = coeffs[0]
            lin_delta = -slope
        except Exception:
            lin_delta = None

    return peak_times, peak_amps, popt, lin_delta


# -----------------------------
# Главная обработка — работает с csv-файлами
# -----------------------------

def process_files(fileOwnNames, data_dir):
    results = {}
    # Собираем списки файлов
    for idx, fname in enumerate(fileOwnNames, start=1):
        base = os.path.splitext(fname)[0]
        whole_csv = os.path.join(data_dir, base + "_signal_whole.csv")
        impact_csv = os.path.join(data_dir, base + "_signal_ImpactRange.csv")

    # читаем whole (если есть)
    if os.path.exists(whole_csv):
        t_whole, s_whole, e_whole = read_csv_signal(whole_csv)
    else:
        print(f"⚠ Не найден {whole_csv}")
        t_whole = np.array([]); s_whole = np.array([]); e_whole = np.array([])

    # читаем impact (если есть)
    if os.path.exists(impact_csv):
        t_imp, s_imp, e_imp = read_csv_signal(impact_csv)
    else:
        print(f"⚠ Не найден {impact_csv}")
        t_imp = np.array([]); s_imp = np.array([]); e_imp = np.array([])

    # вычисления
    energy_whole = np.sum(s_whole**2) if s_whole.size else 0.0
    energy_imp = np.sum(s_imp**2) if s_imp.size else 0.0

    # огибающие
    env_hilbert_imp = compute_envelope_hilbert(s_imp) if s_imp.size else np.array([])

    # пики и аппроксимация
    peak_times, peak_amps, popt, lin_delta = compute_peaks_and_fit(t_imp, s_imp)
    fit_delta = None
    fit_A = None
    fit_C = None
    if popt is not None:
        if len(popt) == 3:
            fit_A, fit_delta, fit_C = popt
    elif len(popt) == 2:
        fit_A, fit_delta = popt
        fit_C = 0.0

    results[base] = {
        't_whole': t_whole, 's_whole': s_whole, 'e_whole': e_whole,
        't_imp': t_imp, 's_imp': s_imp, 'e_imp': e_imp,
        'energy_whole': energy_whole, 'energy_imp': energy_imp,
        'env_hilbert_imp': env_hilbert_imp,
        'peak_times': peak_times, 'peak_amps': peak_amps,
        'fit_A': fit_A, 'fit_delta': fit_delta, 'fit_C': fit_C,
        'lin_delta': lin_delta
    }
    
    return results


# -----------------------------
# Визуализация
# -----------------------------

def plot_results(results, fileOwnNames, data_dir):
    for idx, fname in enumerate(fileOwnNames, start=1):
        base = os.path.splitext(fname)[0]
        res = results.get(base)
        if res is None:
            continue

    # 1) график whole (если есть)
    if res['t_whole'].size:
        plt.figure(figsize=(10,4))
        plt.plot(res['t_whole'], res['s_whole'], label='whole signal')
        plt.title(f'{base} - whole')
        plt.xlabel('Time, s')
        plt.grid(); plt.legend(); plt.show()

    # 2) график impact (из whole по ImpactBounds) — у вас уже есть impact csv, строим его
    if res['t_imp'].size:
        plt.figure(figsize=(10,4))
        plt.plot(res['t_imp'], res['s_imp'], label='impact signal')
        if res['env_hilbert_imp'].size:
            plt.plot(res['t_imp'], res['env_hilbert_imp'], 'r--', label='Hilbert envelope')
    # если есть аппроксимация
    if res['fit_delta'] is not None and res['fit_A'] is not None:
        t_rel = res['t_imp'] - res['t_imp'][0]
        fitted = res['fit_A'] * np.exp(-res['fit_delta'] * t_rel) + (res['fit_C'] if res['fit_C'] is not None else 0.0)
        plt.plot(res['t_imp'], fitted, 'g-', label=f'LSQ fit (delta={res["fit_delta"]:.4f})')
    # пики
    if res['peak_times'].size:
        plt.scatter(res['peak_times'], res['peak_amps'], color='k', zorder=5, label='peaks')
    # подпись декрементов
    txt = ''
    if res['lin_delta'] is not None:
        txt += f' lin_delta={res["lin_delta"]:.4f}'
    if res['fit_delta'] is not None:
        txt += f' fit_delta={res["fit_delta"]:.4f}'
    if txt:
        plt.text(0.02, 0.95, txt, transform=plt.gca().transAxes, verticalalignment='top')

    plt.title(f'{base} - impact and envelopes')
    plt.xlabel('Time, s')
    plt.grid(); plt.legend(); plt.show()


# -----------------------------
# Подсчёт сумм энергий по группам и вывод
# -----------------------------

def summarize_and_print(results, fileOwnNames):
    # группы: (1+3) -> indices 0 and 2; (2+4) -> indices 1 and 3
    group1 = 0.0
    group2 = 0.0
    for i, fname in enumerate(fileOwnNames):
        base = os.path.splitext(fname)[0]
        res = results.get(base)
        if res is None:
            continue
        if i in (0,2):
            group1 += res['energy_imp']
        if i in (1,3):
            group2 += res['energy_imp']


    print('Summary:')
    for fname in fileOwnNames:
        base = os.path.splitext(fname)[0]
        r = results.get(base)
        if r is None:
            print(f"{base}: no data")
            continue
        print(f"{base}: energy_whole={r['energy_whole']:.6f}, energy_imp={r['energy_imp']:.6f}, lin_delta={r['lin_delta']}, fit_delta={r['fit_delta']}")


    print(f"Group (1+3) energy_imp = {group1:.6f}")
    print(f"Group (2+4) energy_imp = {group2:.6f}")


# -----------------------------
# Пример использования
# -----------------------------

if __name__ == '__main__':
    fileOwnNames = ["051_1_M.wav", "051-2.wav", "052-1.wav", "052-2.wav"]
    data_dir = 'D:\MyFilesCur\MyPrgs\Python\Wav\assets' # так соединение пути и имени съедает слэш и 1-ю букву имени файла, заменяет их непечатным символом
    data_dir = "D:\\MyFilesCur\\MyPrgs\\Python\\Wav\\assets"

    results = process_files(fileOwnNames, data_dir)
    plot_results(results, fileOwnNames, data_dir)
    summarize_and_print(results, fileOwnNames)
