import numpy as np


def decompose_into_modes(t, x, frequencies, alpha, use_mean=True):
    """
    Разложение затухающего сигнала на моды методом МНК.

    Модель:
        x(t) = C + sum_k exp(-alpha*t) *
                    [A_k*cos(2*pi*f_k*t) +
                     B_k*sin(2*pi*f_k*t)]

    Parameters
    ----------
    t : array-like
        Время сигнала.
    x : array-like
        Сигнал одного удара.
    frequencies : array-like
        Частоты мод, найденные на предыдущем шаге, Гц.
    alpha : float
        Общий коэффициент затухания, 1/с.
    use_mean : bool
        Добавлять ли постоянную составляющую C.

    Returns
    -------
    result : dict
        coefficients
        amplitudes
        phases
        reconstructed
        residual
        rms_signal
        rms_residual
        relative_residual
    """

    t = np.asarray(t, dtype=float)
    x = np.asarray(x, dtype=float)
    frequencies = np.asarray(frequencies, dtype=float)

    if len(t) != len(x):
        raise ValueError("t и x должны иметь одинаковую длину")

    if len(frequencies) == 0:
        raise ValueError("Список frequencies пуст")

    # Время относительно начала удара.
    # Это важно для exp(-alpha*t).
    tau = t - t[0]

    # Экспоненциальное затухание
    decay = np.exp(-alpha * tau)

    columns = []

    if use_mean:
        # Постоянная составляющая
        columns.append(np.ones(len(t)))

    # Запоминаем, какие столбцы относятся к каким модам
    mode_columns = []

    for f in frequencies:

        omega = 2.0 * np.pi * f

        cos_column = decay * np.cos(omega * tau)
        sin_column = decay * np.sin(omega * tau)

        mode_columns.append((len(columns), len(columns) + 1))

        columns.append(cos_column)
        columns.append(sin_column)

    # Матрица признаков
    X = np.column_stack(columns)

    # Линейный МНК:
    # X @ coefficients ~= x
    coefficients, residuals, rank, singular_values = np.linalg.lstsq(
        X, x, rcond=None
    )

    # Восстановленный сигнал
    x_reconstructed = X @ coefficients

    # Остаток
    x_residual = x - x_reconstructed

    # Извлекаем параметры мод
    amplitudes = []
    phases = []

    for k, (iA, iB) in enumerate(mode_columns):

        A = coefficients[iA]
        B = coefficients[iB]

        amplitude = np.sqrt(A**2 + B**2)

        # A*cos(wt) + B*sin(wt)
        # = R*cos(wt - phi)
        phase = np.arctan2(-B, A)

        amplitudes.append(amplitude)
        phases.append(phase)

    rms_signal = np.sqrt(np.mean(x**2))
    rms_residual = np.sqrt(np.mean(x_residual**2))

    if rms_signal > 0:
        relative_residual = rms_residual / rms_signal
    else:
        relative_residual = np.nan

    return {
        "coefficients": coefficients,
        "amplitudes": np.asarray(amplitudes),
        "phases": np.asarray(phases),
        "reconstructed": x_reconstructed,
        "residual": x_residual,
        "rms_signal": rms_signal,
        "rms_residual": rms_residual,
        "relative_residual": relative_residual,
        "rank": rank,
        "s
