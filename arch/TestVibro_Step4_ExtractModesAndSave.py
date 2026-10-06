from MyPyVibroLib import *

if __name__ == "__main__":







    # Примерные данные
    #fs = 1000  # Гц
    #t = np.linspace(0, 5, fs*5, endpoint=False)
    #signal = (np.sin(2*np.pi*3*t) + 0.5*np.sin(2*np.pi*7*t))*np.exp(-t/2) + 0.05*np.random.randn(len(t))

    # Извлекаем моды
    peaks, modes = extract_modes_and_save(t, signal, fs,
                                          save_dir="modes_results",
                                          bandwidth=2.0,
                                          peak_thresh=0.1)

    # Визуализация
    plt.figure(figsize=(10,6))
    for f, sig_f in modes.items():
        plt.plot(t, sig_f, label=f"{f:.1f} Hz")
    plt.plot(t, signal, "k--", alpha=0.4, label="Исходный")
    plt.legend()
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.title("Выделенные моды колебаний")
    plt.grid(True)
    plt.show()
