import numpy as np
from scipy.io import wavfile
import wave

def read_wav_safe(filename, max_seconds=None, channel=None):
    """
    Безопасное чтение WAV-файла (с поддержкой многоканальных).
    
    filename : str — путь к файлу
    max_seconds : float | None — ограничить длительность (сек)
    channel : int | None — номер канала (0..n-1) или None для всех
    
    return fs, data
    """
    try:
        fs, data = wavfile.read(filename)
        
        # Преобразуем в float
        if np.issubdtype(data.dtype, np.integer):
            data = data.astype(np.float32) / np.iinfo(data.dtype).max
        
        # Обрезаем по времени, если указано
        if max_seconds is not None:
            n_samples = int(fs * max_seconds)
            data = data[:n_samples]
        
        # Если задан канал
        if data.ndim > 1:
            n_channels = data.shape[1]
            if channel is not None:
                if 0 <= channel < n_channels:
                    data = data[:, channel]
                else:
                    raise ValueError(f"Недопустимый номер канала: {channel}, всего каналов: {n_channels}")
        return fs, data
    
    except Exception as e:
        print(f"[!] Ошибка чтения через scipy.io.wavfile: {e}")
        print("    Попробуем стандартный модуль wave...")

        with wave.open(filename, "rb") as wf:
            fs = wf.getframerate()
            n_channels = wf.getnchannels()
            n_frames = wf.getnframes()

            if max_seconds is not None:
                n_frames = min(n_frames, int(fs * max_seconds))

            raw = wf.readframes(n_frames)
            wf.close()

            data = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
            data = data.reshape(-1, n_channels)
            data /= np.iinfo(np.int16).max

            if channel is not None:
                if 0 <= channel < n_channels:
                    data = data[:, channel]
                else:
                    raise ValueError(f"Недопустимый номер канала: {channel}, всего каналов: {n_channels}")

            return fs, data

# to use so
#ONE CHANNEL
fs, ch0 = read_wav_safe("vibration.wav", channel=0)

