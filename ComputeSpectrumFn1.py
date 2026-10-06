def compute_spectrum(x, fs,
                     use_window=False,
                     use_mean=False,
                     use_detrend=False,
                     zero_padding_factor=1):

    x_proc = np.array(x, dtype=float)

    if use_mean:
        x_proc -= np.mean(x_proc)

    if use_detrend:
        x_proc = detrend(x_proc)

    N_orig = len(x_proc)
    N = N_orig * zero_padding_factor

    if zero_padding_factor > 1:
        x_proc = np.pad(x_proc, (0, N - N_orig), 'constant')

    if use_window:
        window = np.hanning(len(x_proc))
        x_proc *= window

    X = np.fft.fft(x_proc)

    amps = 2 * np.abs(X[:N//2]) / N
    freqs = np.fft.fftfreq(N, d=1/fs)[:N//2]

    return freqs, amps

def refine_peak_parabolic(freqs, amps, k):
    """
    Уточнение частоты пика параболической интерполяцией.
    
    freqs — массив частот
    amps  — массив амплитуд
    k     — индекс пика
    """

    if k <= 0 or k >= len(amps) - 1:
        return freqs[k], amps[k]

    y1 = amps[k - 1]
    y2 = amps[k]
    y3 = amps[k + 1]

    denom = (y1 - 2*y2 + y3)
    if denom == 0:
        return freqs[k], amps[k]

    delta = 0.5 * (y1 - y3) / denom

    df = freqs[1] - freqs[0]
    f_refined = freqs[k] + delta * df
    A_refined = y2 - 0.25 * (y1 - y3) * delta

    return f_refined, A_refined
