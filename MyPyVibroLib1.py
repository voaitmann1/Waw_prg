import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import csv
import os
#
from scipy.signal import find_peaks
from scipy.signal import detrend
from scipy.signal.windows import tukey # scipy version more fresh than 1.7.3 which was for py 3.8
import math
from scipy.optimize import curve_fit
#
from scipy.signal import butter, filtfilt, hilbert
import copy

import wave#
#---

signalFileHeader=["Time_s", "Signal", "Energy"]
fileCharsHeadersRow=["DataID", "FileName", "freq.discr", "tmax", "SumEnergy"]
impactRangesHeadersRow=["tStart", "tFin"]

#

def FindPosInSucc(X, val):
    isLess=0
    isGreater=0
    isWithin=0
    equalN=0
    lessN=0
    if isinstance(X, list):
        Q=len(X)
        if Q>0:
            if val<X[1-1]:
                isLess=1
            elif val>X[Q-1]:
                isGreater=1
            else:
                isWithin=1
                for N in range(1, Q+1):
                    if val==X[N-1]:
                        equalN=N
                if equalN==0:
                    for N in range(1, Q-1+1):
                        if val>X[N-1] and val<X[N+1-1]:
                            lessN=N
    R=[["isLess", isLess],["isGreater", isGreater],["isWithin", isWithin],["equalN", equalN],["lessN", lessN]]
    return R

def LinInterp(X, Y, x):
    y=0
    Q=len(X)
    pos=FindPosInSucc(X, x)
    isLess=pos[1-1][2-1]
    isGreater=pos[2-1][2-1]
    isWithin=pos[3-1][2-1]
    equalN=pos[4-1][2-1]
    lessN=pos[5-1][2-1]
    if equalN>0:
       y=Y[equalN-1]
    else:
        if isLess!=0:
            x1=X[1-1]
            x2=X[2-1]
            y1=Y[1-1]
            y2=Y[2-1]
        elif isGreater!=0:
            x1=X[Q-1-1]
            x2=X[Q-1]
            y1=Y[Q-1-1]
            y2=Y[Q-1]
        else:#lessN!=0
            x1=X[lessN-1]
            x2=X[lessN+1-1]
            y1=Y[lessN-1]
            y2=Y[lessN+1-1]
        k=(y2-y1)/(x2-x1)
        y=k*(x-x1)+y1
    return y
            

def FindExtremsOfArray(arr):
    if isinstance(arr, list) and len(arr)>0:
        mx=arr[1-1]
        mn=arr[1-1]
        mxN=1
        mnN=1
        for N in range(1, len(arr)+1):
            val=arr[N-1]
            if val>mx:
                mx=val
                mxN=N
            if val<mn:
                mn=val
                mnN=N
    return mnN, mn, mxN, mx

def SwapVals(arr, N1, N2):
    if isinstance(arr, list) and len(arr)>0 and N1>=1 and N1<=len(arr) and N2>=1 and N2<=len(arr):
        val1=arr[N1-1]
        val2=arr[N2-1]
        buf=val1
        arr[N1-1]=arr[N2-1]
        arr[N2-1]=buf
    #return arr#
        
def SortArray(arr, AscNotDesc=True):
    if isinstance(arr, list):
        Q=len(arr)
        buf=0
        if AscNotDesc:
            for i in range(1, Q-1+1):
                for j in range(i, Q+1):
                    if(arr[j-1]<arr[i-1]):
                        buf=copy.deepcopy(arr[i-1])
                        arr[i-1]=copy.deepcopy(arr[j-1])
                        arr[j-1]=copy.deepcopy(buf)
                    #
                #
            #
        else:
            for i in range(1, Q-1+1):
                for j in range(i, Q+1):
                    if(arr[j-1]>arr[i-1]):
                        buf=copy.deepcopy(arr[i-1])
                        arr[i-1]=copy.deepcopy(arr[j-1])
                        arr[j-1]=copy.deepcopy(buf)
                    #
                #
            #
        #
    #return arr
#

def read_csv_of_files_and_channels(fullFileName):
    #PathToNamesFile="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"
    #this function is universal uz evot QForSnglFile et QBefore
    fileOwnNames=[]
    fileOwnNames_noExt=[]
    channels=[]
    #with open(PathToNamesFile+"\\FolderAndFiles.csv", newline='') as f:
    with open(fullFileName, newline='') as f:
        reader = csv.DictReader(f)
        LineN=0
        for row in reader:
            LineN+=1
            if LineN==1:
                #filePath=row[2-1]
                filePath=row["Value"]
            elif LineN==2:
                #QFiles=int(row[2-1])
                QFiles=int(row["Value"])
            #elif LineN>2:
            #    #fileOwnNames.append(row[2-1]+".csv")
            #    fileOwnNames.append(row["Value"]+".wav")
            else:
                QBefore=2#filePath and QFiles
                QForSnglFile=2#File name and Q channels
                SubN=(LineN-QBefore)%QForSnglFile
                if SubN==0:
                    SubN=QForSnglFile
                #FileN=(LineN-QBefore+SubN)/QForSnglFile
                FileN=(LineN-QBefore+QForSnglFile-SubN)/QForSnglFile
                FileN=int((LineN-QBefore+QForSnglFile-SubN)/QForSnglFile)
                if SubN==1:#filename
                    fname=row["Value"]
                    fileOwnNames_noExt.append(fname)
                    fileOwnNames.append(fname+".wav")
                    print("LineN "+str(LineN)+" File N "+str(FileN)+" file name: "+fname)
                elif SubN==QForSnglFile:#factic 2 - QChannels
                    n_channel=int(row["Value"])
                    channels.append(n_channel)
                    print("LineN "+str(LineN)+" File N "+str(FileN)+" channels: "+str(n_channel))
    return filePath, QFiles, fileOwnNames_noExt, channels

def read_wav_safe(fullFileName, max_seconds=None):
    print("read_wav_safe starts working")
    print("reading: "+fullFileName)
    try:
        fs, data=wavfile.read(fullFileName)
        #norm'g if data s'numoz
        if np.issubdtype(data.dtype, np.integer):
            max_val= np.iinfo(data.dtype).max
            data=data.astype(np.float32)#div to max?
        return fs, data
    except Exception as e:
        print("Error reading file "+str(e))
        print("trying to read via wave")
        #with wave.open(fileName, "rb") as wf:#os not l'methods __enter__ et __exit__, so n'arb
        print("reading: "+fullFileName)
        wf=wave.open(fullFileName, "rb")
        fs=wf.getframerate()
        n_channels = wf.getnchannels()
        n_frames = wf.getnframes()

        if max_seconds is not None:
            #data = data.reshape(-1, n_channels)
            n_frames = min(n_frames, int(fs * max_seconds))

        raw = wf.readframes(n_frames)

        wf.close()#ute nur uz py 2.7 ob in py 3 to obj ha attr __exit__
          
        data = np.frombuffer(raw,dtype = np.int16)

        if n_channels >1:
            data = data.reshape(-1, n_channels)
            #print(str(n_channels)+" channels")
        else:
            pass
            #print(str(n_channels)+" channels")

        data = data.astype(np.float32)/ np.iinfo(np.int16).max
        return fs, data#wtf?

def read_wav_safe_1(fullFileName, max_seconds=None, channel=None):
    try:
        fs, data=wavfile.read(fullFileName)
        #norm'g if data s'numoz
        if np.issubdtype(data.dtype, np.integer):
            max_val= np.iinfo(data.dtype).max
            data=data.astype(np.float32)#div to max?
        if data.ndim > 1:
            n_channels = data.shape[1]
            if channel is not None:
                if 0 <= channel < n_channels:
                    data = data[:, channel]
                else:
                    raise ValueError(f"Недопустимый номер канала: {channel}, всего каналов: {n_channels}")
        return fs, n_channels, data
    except Exception as e:
        print("Error reading file "+str(e))
        print("trying to read via wave")
        #with wave.open(fileName, "rb") as wf:#os not l'methods __enter__ et __exit__, so n'arb
        wf=wave.open(fullFileName, "rb")
        fs=wf.getframerate()
        n_channels = wf.getnchannels()
        n_frames = wf.getnframes()

        if max_seconds is not None:
            #data = data.reshape(-1, n_channels)
            n_frames = min(n_frames, int(fs * max_seconds))

        raw = wf.readframes(n_frames)

        wf.close()#ute nur uz py 2.7 ob in py 3 to obj ha attr __exit__
          
        data = np.frombuffer(raw,dtype = np.int16)

        if n_channels >1:
            data = data.reshape(-1, n_channels)
            #print(str(n_channels)+" channels")
        else:
            pass
            #print(str(n_channels)+" channels")

        data = data.astype(np.float32)/ np.iinfo(np.int16).max

        if channel is not None:
            if 0 <= channel < n_channels:
                data = data[:, channel]
            else:
                raise ValueError(f"Недопустимый номер канала: {channel}, всего каналов: {n_channels}")
        
        return fs, n_channels, data#wtf?
    #return fs, data#wtf?

def read_wav_safe_2(fullFileName, max_seconds=None, channel=None):
    try:
        fs, data=wavfile.read(fullFileName)
        #norm'g if data s'numoz
        if np.issubdtype(data.dtype, np.integer):
            #max_val= np.iinfo(data.dtype).max
            data=data.astype(np.float32)/np.iinfo(data.dtype).max
        # Если задан канал
        if data.ndim > 1:
            n_channels = data.shape[1]
            if channel is not None:
                if 0 <= channel < n_channels:
                    data = data[:, channel]
                else:
                    raise ValueError(f"Недопустимый номер канала: {channel}, всего каналов: {n_channels}")
        else:
            n_channels = 1#data.shape[1]
        return fs, n_channels, data
    except Exception as e:
        print("Error reading file "+str(e))
        print("trying to read via wave")
        #with wave.open(fileName, "rb") as wf:#os not l'methods __enter__ et __exit__, so n'arb
        wf=wave.open(fullFileName, "rb")
        fs=wf.getframerate()
        n_channels = wf.getnchannels()
        n_frames = wf.getnframes()

        if max_seconds is not None:
            #data = data.reshape(-1, n_channels)
            n_frames = min(n_frames, int(fs * max_seconds))

        raw = wf.readframes(n_frames)

        wf.close()#ute nur uz py 2.7 ob in py 3 to obj ha attr __exit__
          
        data = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
        data = data.reshape(-1, n_channels)
        data /= np.iinfo(np.int16).max

        if channel is not None:
            if 0 <= channel < n_channels:
                data = data[:, channel]
            else:
                raise ValueError(f"Недопустимый номер канала: {channel}, всего каналов: {n_channels}")
        return fs, n_channels, data

#---

def read_wav_and_calc_t(filename):
    #fs, data = wavfile.read(filename)
    fs, data = read_wav_safe(filename, max_seconds=None)
    if data.ndim > 1:
        data = data[:,0]  # первый канал, если стерео

    t = np.arange(len(data)) / fs
    return t, data, fs

def read_wav_and_calc_t_1(filename, max_seconds=None):
    #fs, data = wavfile.read(filename)
    fs, n_channels, data = read_wav_safe_2(filename, max_seconds)
    if data.ndim > 1:
        data1 = data[:,0]  # первый канал, если стерео
    else:
        data1=copy.deepcopy(data)
    t = np.arange(len(data1)) / fs
    return t, n_channels, data, fs
    

def read_wav_and_save_csv(filename):# not used
    #fs, data = wavfile.read(filename)
    fs, data = read_wav_safe(filename, max_seconds=None)
    if data.ndim > 1:
        data = data[:,0]  # первый канал, если стерео

    t = np.arange(len(data)) / fs

    # --- Сохраняем сигнал в CSV ---
    csv_filename = os.path.splitext(filename)[0] + "_signal.csv"
    with open(csv_filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(["Time_s", "Signal"])
        writer.writerow(["Time_s", "Signal", "Energy"])
        for i in range(len(t)):
            #writer.writerow([t[i], data[i]])
            writer.writerow([t[i], data[i], data[i]*data[i]])

    print(f"Сигнал сохранён в {csv_filename}")
    return t, data, fs

def plot_signal(t, signal, title="Сигнал", t_start=None, t_end=None):
    t = np.array(t)
    signal = np.array(signal)
    if t_start is None:
        t_start = t[0]
    if t_end is None:
        t_end = t[-1]

    mask = (t >= t_start) & (t <= t_end)
    plt.figure(figsize=(12,6))
    plt.plot(t[mask], signal[mask])
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.title(title)
    plt.grid()
    plt.show()

# -----------------------------
def SaveToCsv(csv_filename, headerRow, data2D):
    with open(csv_filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(["Time_s", "Signal"])
        writer.writerow(headerRow)
        #for i in range(len(t)):
            #writer.writerow([t[i], data[i]])
        writer.writerows(data2D)
#------------------------------------------------------------
def ReadAndFindQChannels(filename):#ab single csv for all channels
    QChannels=0
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            L=len(row)
            QChannels=(L-1)/2
    return QChannels

def read_signal_csv(filename, channelN=None):
    times = []
    values = []
    if channelN==None:
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                times.append(float(row["Time_s"]))
                values.append(float(row["Signal"]))
            #
        #
    else:
        with open(filename, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                times.append(float(row["Time_s"]))
                signal_header="Signal_chN"+str(channelN)
                values.append(float(row[signal_header]))
            #
        #
    return np.array(times), np.array(values)

#-------------------------------------------------------------
def read_signal_csv(filename):
    times = []
    values = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row["Time_s"]))
            values.append(float(row["Signal"]))
    return np.array(times), np.array(values)

def read_SignalAndEnergy_csv(filename):
    times = []
    signal = []
    energy = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            times.append(float(row["Time_s"]))
            signal.append(float(row["Signal"]))
            energy.append(float(row["Energy"]))
    return np.array(times), np.array(signal), np.array(energy)

def extractRangeFromSignal(times, signal, energy, fs, tLB, tHB):#new, n'test'd
    QPoints=len(times)
    indexLB=0
    indexHB=QPoints-1
    if tLB>=times[0] and tHB<=times[QPoints-1]:
        indexLB=tLB*fs
        indexHB=tHB*fs
    return times[indexLB:indexHB+1], signal[indexLB:indexHB+1], energy[indexLB:indexHB+1]
    

def read_impact_bounds(filename):
    impacts = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)#all rows
        for row in reader:
            impacts.append((int(row["ImpactID"]), float(row["StartTime_s"]), float(row["EndTime_s"])))
    return impacts

def read_FileChars(filename):
    fileChars = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fileChars.append((int(row["ImpactID"]), float(row["StartTime_s"]), float(row["EndTime_s"])))
    return fileChars

#fileCharsHeadersRow
def ReadDiscretFreq(filename):#arb'te co #old fn
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)#all rows
        for row in reader:
            fN=int(row[fileCharsHeadersRow[1-1]])
            fnm=row[fileCharsHeadersRow[2-1]]
            fs=float(row[fileCharsHeadersRow[3-1]])
            tm=float(row[fileCharsHeadersRow[4-1]])
            es=float(row[fileCharsHeadersRow[5-1]])
            break
#    #return fs
    return fN, fnm, fs, tm, es

def ReadIniDataNamesAndFreq(filename):
    fileOwnNames=[]
    tms=[]
    ess=[]
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)#all rows
        for row in reader:
            fN=int(row[fileCharsHeadersRow[1-1]])
            fnm=row[fileCharsHeadersRow[2-1]]
            fs=float(row[fileCharsHeadersRow[3-1]])
            tm=float(row[fileCharsHeadersRow[4-1]])
            es=float(row[fileCharsHeadersRow[5-1]])
            #
            fileOwnNames.append(fnm)
            tms.append(tm)
            ess.append(es)
    #return fs
    #return fN, fnm, fs, tm, es
    return fileOwnNames, fs, tms, ess
#------------------------------------------------------------
def parabolic_interpolation(k, A):
    # k - индекс пика, A - массив амплитуд
    alpha = A[k-1]
    beta  = A[k]
    gamma = A[k+1]
    p = 0.5 * (alpha - gamma) / (alpha - 2*beta + gamma)
    # скорректированная частота:
    k_true = k + p
    amp_true = beta - 0.25*(alpha - gamma)*p
    return k_true, amp_true
#============================================================

#import numpy as np
#from scipy.signal import find_peaks

def detect_impacts_segments(x, fs=1000, min_distance=0.05, threshold_ratio=0.5):
    """
    x - сигнал (список или numpy array)
    fs - частота дискретизации, Гц
    min_distance - минимальное расстояние между ударами, сек
    threshold_ratio - порог амплитуды относительно максимума для пика
    """
    x = np.array(x, dtype=float)
    distance_samples = int(min_distance * fs)
    max_amp = np.max(x)
    threshold = threshold_ratio * max_amp

    # Находим пики ударов
    peaks_idx, _ = find_peaks(x, height=threshold, distance=distance_samples)

    # Переводим в моменты времени
    peaks_time = peaks_idx / fs

    # Формируем сегменты: от одного удара до следующего
    segments = []
    for i in range(len(peaks_time)-1):
        segments.append((peaks_time[i], peaks_time[i+1]))
    # Последний сегмент до конца записи
    segments.append((peaks_time[-1], len(x)/fs))

    return peaks_time, segments

# ----------------------------
# Пример использования
# ----------------------------
if __name__ == "__main__":
    fs = 1000  # Гц
    t = np.arange(0, 1, 1/fs)

    # Пример сигнала: 3 удара (синусоиды с затуханием) + шум
    x = np.zeros_like(t)
    for center in [0.2, 0.5, 0.8]:
        idx_center = int(center*fs)
        N = 50
        decay = np.exp(-np.arange(N)/20)
        x[idx_center:idx_center+N] += 1.0 * decay * np.sin(2*np.pi*50*np.arange(N)/fs)
    x += 0.05 * np.random.randn(len(t))  # шум

    peaks_time, segments = detect_impacts_segments(x, fs, min_distance=0.1, threshold_ratio=0.3)

    print("Моменты ударов (сек):", peaks_time)
    print("Фрагменты между ударами (сек):", segments)

#===============================================================================

#import math
#import numpy as np
#import matplotlib.pyplot as plt

# ----------------------------
# 1. Прямое вычисление ДПФ
# ----------------------------
def spectrum_dft(x, fs=1000, use_window=False, writeProgress=True):

    if writeProgress==True:
        print("spectrum_dft starts working")
    
    N = len(x)
    x_proc = np.array(x, dtype=float)

    # Применяем окно Hann
    if use_window:
        window = np.hanning(N)
        x_proc *= window

    X_real = [0.0] * N
    X_imag = [0.0] * N

    if writeProgress==True:
        print("starting double cycle")

    N1=0
    
    for k in range(N):
        for n in range(N):

            N1+=1
            workPart=N1*100.0/(N*N)
            if writeProgress==True:
                ##if workPart%10==0 or workPart<10 and workPart%2==0 or workPart==0 or workPart==1:
                #if workPart%2==0 or workPart==1:
                #    print(f"Calculating: {workPart}% done")
                print("Calc "+str(workPart)+"% done")
            
            angle = 2 * math.pi * k * n / N
            X_real[k] += x_proc[n] * math.cos(angle)
            X_imag[k] -= x_proc[n] * math.sin(angle)

    amps = [2 * math.sqrt(X_real[k]**2 + X_imag[k]**2) / N for k in range(N//2)]
    freqs = [k * fs / N for k in range(N//2)]

    if writeProgress==True:
        print("spectrum_dft finishes working")
    
    return freqs, amps

# ----------------------------
# 2. Быстрое преобразование FFT
# ----------------------------
def spectrum_fft(x, fs=1000, use_window=False, use_mean=False, use_detrend=False):
    xi=copy.deepcopy(x)

    x_proc = np.array(xi, dtype=float)#or S'n'ute copy, if utf'tc np.array?

    if use_mean:
        x_proc = x_proc - np.mean(x_proc)  # убрать DC

    if use_detrend:    
        x_proc = detrend(x_proc)
    
    N = len(x_proc)

    # Применяем окно Hann
    if use_window:
        window = np.hanning(N)
        x_proc *= window

    X = np.fft.fft(x_proc)
    amps = 2 * np.abs(X[:N//2]) / N
    freqs = np.fft.fftfreq(N, d=1/fs)[:N//2]
    return freqs, amps



# ----------------------------
# 3. Итоговая функция с выбором варианта
# ----------------------------
def compute_spectrum(x, fs=1000, method='fft', use_window=False, plot=True):
    """
    x - сигнал (список или numpy array)
    fs - частота дискретизации
    method - 'fft' или 'dft'
    use_window - применять окно Hann
   plot - строить график
    """

    print("spectrum fun #2")
    
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

#======================================================================

# Spectrum lib

#import numpy as np
#import matplotlib.pyplot as plt
#from scipy.signal import find_peaks
#import csv


# ------------------------------
# 1. Расчёт спектра
# ------------------------------
def compute_spectrum(x, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1):
    """
    Вычисление спектра сигнала.
    """

    print("spectrum fun #2")
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


#
# new 
#



# ------------------------------
# 2. Поиск пиков в спектре
# ------------------------------
def find_spectrum_peaks(freqs, amps, min_height=None, min_prominence=None,
                        min_distance_hz=None, peak_thresh=None,
                        to_console=False, to_csv=None):
    """
    Поиск пиков спектра с возможностью гибкой настройки параметров.
    """
    df = freqs[1] - freqs[0]
    distance_pts = int(np.ceil(min_distance_hz / df)) if min_distance_hz else None

    if peak_thresh is not None:
        min_height = peak_thresh * np.max(amps)

    peaks, props = find_peaks(
        amps,
        height=min_height,
        prominence=min_prominence,
        distance=distance_pts
    )

    peak_freqs = freqs[peaks]
    peak_vals = amps[peaks]

    if to_console:
        print("Найденные пики:")
        for f, v in zip(peak_freqs, peak_vals):
            print(f"  {f:.2f} Гц : {v:.4f}")

    if to_csv:
        with open(to_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Frequency_Hz", "Amplitude"])
            writer.writerows(zip(peak_freqs, peak_vals))

    return peak_freqs, peak_vals, peaks

# ------------------------------
# 3. Вывод спектра
# ------------------------------
def plot_spectrum(freqs, amps, peak_freqs=None, peak_vals=None, title="Spectrum"):
    plt.figure(figsize=(10,5))
    plt.plot(freqs, amps, label='Spectrum')
    if peak_freqs is not None and peak_vals is not None:
        plt.plot(peak_freqs, peak_vals, 'ro', label='Peaks')
    plt.xlabel("Frequency, Hz")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()

# ------------------------------
# 4. Выделение мод
# ------------------------------
def extract_modes_from_spectrum(t, signal, fs, peaks_csv, save_dir="modes", bandwidth=1.0, use_window=False):
    """
    Выделение отдельных мод по спектру, используя CSV с пиками.
    """
    os.makedirs(save_dir, exist_ok=True)

    # Считываем пики
    peak_freqs = []
    with open(peaks_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # заголовок
        for row in reader:
            peak_freqs.append(float(row[0]))

    N = len(signal)
    if use_window:
        signal_proc = signal * np.hanning(N)
    else:
        signal_proc = np.array(signal, dtype=float)

    spectrum = np.fft.fft(signal_proc)
    freqs = np.fft.fftfreq(N, d=1/fs)

    modes = {}
    for f0 in peak_freqs:
        mask = (np.abs(freqs - f0) <= bandwidth/2) | (np.abs(freqs + f0) <= bandwidth/2)
        spectrum_filt = spectrum * mask
        sig_filt = np.fft.ifft(spectrum_filt).real
        modes[f0] = sig_filt

        # Сохраняем в CSV
        csv_file = os.path.join(save_dir, f"mode_{f0:.2f}Hz.csv")
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Time_s", "Signal"])
            writer.writerows(zip(t, sig_filt))
        print(f"[+] Мода {f0:.2f} Гц сохранена → {csv_file}")

    return modes

def extract_realistic_modes(signal, t, fs, peak_freqs, bandwidth=1.0):
    """
    Выделение мод с сохранением реального затухания.
    
    signal     : массив исходного сигнала
    t          : массив времени
    fs         : частота дискретизации
    peak_freqs : массив пиковых частот
    bandwidth  : ширина полосы вокруг каждого пика
    """
    N = len(signal)
    spectrum = np.fft.fft(signal)
    freqs = np.fft.fftfreq(N, d=1/fs)
    
    # Огибающая сигнала
    analytic_signal = hilbert(signal)
    envelope = np.abs(analytic_signal)
    
    # Найдем момент максимума огибающей
    idx_max = np.argmax(envelope)
    
    modes = {}
    
    for f0 in peak_freqs:
        # маска полосы вокруг пика
        mask = (np.abs(freqs - f0) <= bandwidth/2) | (np.abs(freqs + f0) <= bandwidth/2)
        filtered_spec = spectrum * mask
        mode_signal = np.fft.ifft(filtered_spec).real
        
        # масштабирование амплитуды моды
        factor = envelope[idx_max] / (mode_signal[idx_max] + 1e-12)  # чтобы избежать деления на 0
        mode_signal *= factor
        
        modes[f0] = mode_signal
        
    return modes, envelope


# 1. Функция построения огибающей
def compute_envelope(signal):
    """
    Вычисляет огибающую сигнала через Hilbert
    """
    analytic_signal = hilbert(signal)
    envelope = np.abs(analytic_signal)
    return envelope

## 2. Функция спектра
#def compute_spectrum(signal, fs=1000, use_window=False):
#    """
#    Вычисление спектра сигнала
#    """
#
#    print("spectrum fun #3")
#    
#    N = len(signal)
#    x_proc = np.array(signal, dtype=float)
#    
#    if use_window:
#        window = np.hanning(N)
#        x_proc *= window
#
#    X = np.fft.fft(x_proc)
#    freqs = np.fft.fftfreq(N, d=1/fs)[:N//2]
#    amps = 2 * np.abs(X[:N//2]) / N
#    return freqs, amps

# 3. Поиск пиков спектра с параметрами регулировки
def find_spectrum_peaks(freqs, amps,
                        min_height=None,
                        min_prominence=None,
                        min_distance_hz=None):
    """
    Автоматический поиск пиков спектра с порогами и минимальной дистанцией
    """
    df = freqs[1] - freqs[0]  # шаг по частоте
    min_distance_pts = int(np.ceil(min_distance_hz / df)) if min_distance_hz else None

    peaks, props = find_peaks(
        amps,
        height=min_height,
        prominence=min_prominence,
        distance=min_distance_pts
    )

    peak_freqs = freqs[peaks]
    peak_vals = amps[peaks]

    return peak_freqs, peak_vals, peaks

# 4. Выделение реалистичных мод
def extract_realistic_modes(signal, t, fs, peak_freqs, envelope=None, bandwidth=1.0):
    """
    Выделение мод с реалистичным убывающим затуханием
    """
    N = len(signal)
    spectrum = np.fft.fft(signal)
    freqs = np.fft.fftfreq(N, d=1/fs)
    
    if envelope is None:
        envelope = compute_envelope(signal)
    idx_max = np.argmax(envelope)
    
    modes = {}
    for f0 in peak_freqs:
        mask = (np.abs(freqs - f0) <= bandwidth/2) | (np.abs(freqs + f0) <= bandwidth/2)
        filtered_spec = spectrum * mask
        mode_signal = np.fft.ifft(filtered_spec).real
        
        # Масштабирование моды по огибающей
        factor = envelope[idx_max] / (mode_signal[idx_max] + 1e-12)
        mode_signal *= factor
        
        modes[f0] = mode_signal
        
    return modes

# 5. Визуализация спектра с пиками
def plot_spectrum_with_peaks(freqs, amps, peak_freqs=None, peak_vals=None):
    plt.figure(figsize=(10,5))
    plt.plot(freqs, amps, label="Спектр")
    if peak_freqs is not None and peak_vals is not None:
        plt.plot(peak_freqs, peak_vals, 'ro', label="Пики")
    plt.xlabel("Частота, Гц")
    plt.ylabel("Амплитуда")
    plt.title("Спектр с выделенными пиками")
    plt.grid(True)
    plt.legend()
    plt.show()

#======================================================================

#from scipy.signal import hilbert, find_peaks
#from scipy.optimize import curve_fit


def analyze_signal(t, x, method="hilbert"):
    """
    Вычисление огибающей и логарифмического декремента затухания.
    method: 'hilbert', 'mnk_lib', 'mnk_manual'
    """
    t = np.asarray(t)
    x = np.asarray(x)

    # --- метод Гильберта ---
    if method == "hilbert":
        analytic = hilbert(x)
        envelope = np.abs(analytic)

    # --- МНК библиотечный ---
    elif method == "mnk_lib":
        def exp_decay(t, A0, delta):
            return A0 * np.exp(-delta * t)

        peaks, _ = find_peaks(np.abs(x))
        t_peaks = t[peaks]
        x_peaks = np.abs(x[peaks])

        if len(t_peaks) < 2:
            return np.abs(x), None

        params, _ = curve_fit(exp_decay, t_peaks - t_peaks[0], x_peaks, p0=(x_peaks[0], 1.0))
        A0_fit, delta_fit = params
        envelope = exp_decay(t - t_peaks[0], A0_fit, delta_fit)

    # --- МНК ручной ---
    elif method == "mnk_manual":
        peaks, _ = find_peaks(np.abs(x))
        t_peaks = t[peaks]
        x_peaks = np.abs(x[peaks])

        if len(t_peaks) < 2:
            return np.abs(x), None

        # линейная регрессия: ln(A) = ln(A0) - delta * t
        t_rel = t_peaks - t_peaks[0]
        y = np.log(x_peaks + 1e-8)
        coeffs = np.polyfit(t_rel, y, 1)
        slope, intercept = coeffs
        delta_fit = -slope
        envelope = np.exp(intercept) * np.exp(-delta_fit * (t - t_peaks[0]))

    else:
        raise ValueError("method должен быть 'hilbert', 'mnk_lib' или 'mnk_manual'")

    # --- оценка δ через линейную регрессию по ln(огибающей) ---
    log_env = np.log(envelope + 1e-8)
    coeffs = np.polyfit(t - t[0], log_env, 1)
    delta = -coeffs[0]

    return envelope, delta

def plot_several(signals, labels=None, title="Сигналы"):
    #def plot_signals(signals, labels=None, title="Сигналы"):
    """
    signals: список сигналов
      - (t, x) → рисуем в отдельном подграфике
      - ((t1,x1), (t2,x2)) → рисуем вместе с twinx
    labels: список подписей (по желанию)
    """
    if labels is None:
        labels = [f"Signal {i+1}" for i in range(len(signals))]

    n = len(signals)
    fig, axes = plt.subplots(n, 1, figsize=(10, 4*n), squeeze=False)
    axes = axes.ravel()

    for i, sig in enumerate(signals):
        ax = axes[i]

        # один сигнал
        if isinstance(sig[0], (list, np.ndarray)):
            t, x = sig
            ax.plot(t, x, label=labels[i], color="b")
            ax.set_ylabel(labels[i])
            ax.legend(loc="upper right")
            ax.grid(True)

        # пара сигналов (с twinx)
        else:
            (t1, x1), (t2, x2) = sig
            ax.plot(t1, x1, "b", label=labels[i] + " (L)")
            ax.set_ylabel(labels[i] + " (L)")
            ax2 = ax.twinx()
            ax2.plot(t2, x2, "r", label=labels[i] + " (R)")
            ax2.set_ylabel(labels[i] + " (R)")
            ax.grid(True)

        ax.set_xlabel("Time, s")

    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

def plot_several1(data_groups, labels=None, styles=None, title="Signals"):
    """
    Универсальный вывод сигналов.
    
    data_groups: список элементов вида:
        [
            [
                [(x1, t1), (x2, t2), ...],   # сигналы (x,t)
                mode                         # 1 или 2
            ],
            ...
        ]
    
    Если mode == 2 и ровно 2 сигнала → второй рисуется на twinx.
    
    labels: список списков:
        [
            ["xlabel", "ylabel"],                   # для 1-го графика
            ["xlabel", "ylabel", "ylabel_right"],   # если есть twinx
            ...
        ]
    
    styles: список списков стилей:
        [
            [ {"color":"red"}, {"color":"blue"} ],
            ...
        ]
    
    title: общий заголовок окна.
    """

    fig, axes = plt.subplots(len(data_groups), 1, figsize=(10, 4 * len(data_groups)))
    if len(data_groups) == 1:
        axes = [axes]  # для унификации

    for i, (signals, mode) in enumerate(data_groups):
        ax = axes[i]
        lbls = labels[i] if labels and i < len(labels) else []
        stls = styles[i] if styles and i < len(styles) else []

        # подписи осей
        if len(lbls) >= 1: ax.set_xlabel(lbls[0])
        if len(lbls) >= 2: ax.set_ylabel(lbls[1])

        if mode == 2 and len(signals) == 2:
            # первый сигнал - обычный
            #x1, t1 = signals[0]
            t1, x1 = signals[0]
            stl1 = stls[0] if len(stls) >= 1 else {}
            ax.plot(t1, x1, label=lbls[1] if len(lbls) >= 2 else None, **stl1)

            # второй сигнал - twinx
            #x2, t2 = signals[1]
            t2, x2 = signals[1]
            stl2 = stls[1] if len(stls) >= 2 else {}
            ax2 = ax.twinx()
            if len(lbls) >= 3: ax2.set_ylabel(lbls[2])
            ax2.plot(t2, x2, label=lbls[2] if len(lbls) >= 3 else None, **stl2)
        else:
            # несколько сигналов в одной системе координат
            for j, (t, x) in enumerate(signals):
                #for j, (x, t) in enumerate(signals):
                stl = stls[j] if j < len(stls) else {}
                lbl = lbls[j+1] if len(lbls) > j+1 else None
                ax.plot(t, x, label=lbl, **stl)

        if len(lbls) > 1:
            ax.legend()

    fig.suptitle(title)
    plt.tight_layout()
    plt.show()
    print("graph should be shown: "+title)

#from scipy.signal import tukey

def analyze_signal1(t, x, method="hilbert", n_peaks=8, peak_thresh=0.1, window_alpha=0.1):
    """
    Вычисление огибающей и логарифмического декремента затухания.
    
    method: 'hilbert', 'mnk_lib', 'mnk_manual'
    n_peaks: сколько первых пиков брать для МНК
    peak_thresh: относительный порог (доля от max), ниже которого пики игнорируются
    window_alpha: параметр окна Tukey для Гильберта (0 = прямоугольное, 1 = Хэннинга)
    """
    t = np.asarray(t)
    x = np.asarray(x)

    # --- метод Гильберта ---
    if method == "hilbert":
        win = tukey(len(x), alpha=window_alpha) if window_alpha > 0 else np.ones(len(x))
        x_win = x * win
        analytic = hilbert(x_win)
        envelope = np.abs(analytic)

    # --- МНК библиотечный ---
        #x_proc = x_proc - np.mean(x_proc)  # убрать DC
        #x_proc = detrend(x_proc)#local variable 'x_proc' referenced before assignment
        x_proc=copy.deepcopy(x)
        x_proc = x_proc - np.mean(x_proc)  # убрать DC
        x_proc = detrend(x_proc)#
    elif method == "mnk_lib":
        def exp_decay(t_rel, A0, delta):
            return A0 * np.exp(-delta * t_rel)

        peaks, props = find_peaks(np.abs(x), height=peak_thresh * np.max(np.abs(x)))
        t_peaks = t[peaks]
        x_peaks = np.abs(x[peaks])

        if len(t_peaks) < 2:
            return np.abs(x), None

        # ограничиваем числом первых пиков
        t_peaks, x_peaks = t_peaks[:n_peaks], x_peaks[:n_peaks]

        params, _ = curve_fit(exp_decay, t_peaks - t_peaks[0], x_peaks, p0=(x_peaks[0], 1.0))
        A0_fit, delta_fit = params
        envelope = exp_decay(t - t_peaks[0], A0_fit, delta_fit)

    # --- МНК ручной ---
    elif method == "mnk_manual":
        peaks, props = find_peaks(np.abs(x), height=peak_thresh * np.max(np.abs(x)))
        t_peaks = t[peaks]
        x_peaks = np.abs(x[peaks])

        if len(t_peaks) < 2:
            return np.abs(x), None

        # ограничиваем числом первых пиков
        t_peaks, x_peaks = t_peaks[:n_peaks], x_peaks[:n_peaks]

        # линейная регрессия: ln(A) = ln(A0) - delta * t
        t_rel = t_peaks - t_peaks[0]
        y = np.log(x_peaks + 1e-8)
        slope, intercept = np.polyfit(t_rel, y, 1)
        delta_fit = -slope
        envelope = np.exp(intercept) * np.exp(-delta_fit * (t - t_peaks[0]))
    elif method == "mytry":
        pass
    else:
        raise ValueError("method должен быть 'hilbert', 'mnk_lib' или 'mnk_manual'")

    # --- оценка δ через регрессию по огибающей ---
    log_env = np.log(envelope + 1e-8)
    slope, intercept = np.polyfit(t - t[0], log_env, 1)
    delta = -slope

    return envelope, delta

#============================================================================

def extract_modes_and_save(t, signal, fs, save_dir="results",
                           bandwidth=1.0, peak_thresh=0.05):
    """
    Извлекает отдельные моды колебаний из сигнала по спектру и сохраняет в CSV.

    t          – массив времени
    signal     – сигнал
    fs         – частота дискретизации
    save_dir   – папка для сохранения результатов
    bandwidth  – ширина полосы вокруг пика (Гц)
    peak_thresh– относительный порог для поиска пиков в спектре
    """

    # FFT
    N = len(signal)
    freqs = np.fft.fftfreq(N, d=1/fs)
    spectrum = np.fft.fft(signal)
    amps = np.abs(spectrum) / N

    # Только положительные частоты
    mask_pos = freqs > 0
    freqs_pos, amps_pos = freqs[mask_pos], amps[mask_pos]

    # Поиск пиков
    peak_inds, props = find_peaks(amps_pos, height=peak_thresh * np.max(amps_pos))
    peak_freqs = freqs_pos[peak_inds]

    # Создать папку для результатов
    os.makedirs(save_dir, exist_ok=True)

    modes = {}
    for f0 in peak_freqs:
        mask = (np.abs(freqs - f0) <= bandwidth/2) | (np.abs(freqs + f0) <= bandwidth/2)
        spectrum_filt = spectrum * mask
        sig_filt = np.fft.ifft(spectrum_filt).real
        modes[f0] = sig_filt

        # --- сохраняем в CSV ---
        csv_filename = os.path.join(save_dir, f"mode_{f0:.2f}Hz.csv")
        with open(csv_filename, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Time_s", "Signal"])
            for ti, si in zip(t, sig_filt):
                writer.writerow([ti, si])
        print(f"[+] Сохранён отклик {f0:.2f} Гц → {csv_filename}")

    return peak_freqs, modes

## ===== пример использования =====
#if __name__ == "__main__":
#    # Примерные данные
#    fs = 1000  # Гц
#    t = np.linspace(0, 5, fs*5, endpoint=False)
#    signal = (np.sin(2*np.pi*3*t) + 0.5*np.sin(2*np.pi*7*t))*np.exp(-t/2) + 0.05*np.random.randn(len(t))
#
#    # Извлекаем моды
#    peaks, modes = extract_modes_and_save(t, signal, fs,
#                                          save_dir="modes_results",
#                                          bandwidth=2.0,
#                                          peak_thresh=0.1)
#
#    # Визуализация
#    plt.figure(figsize=(10,6))
#    for f, sig_f in modes.items():
#        plt.plot(t, sig_f, label=f"{f:.1f} Hz")
#    plt.plot(t, signal, "k--", alpha=0.4, label="Исходный")
#    plt.legend()
#    plt.xlabel("Время, с")
#    plt.ylabel("Амплитуда")
#    plt.title("Выделенные моды колебаний")
#    plt.grid(True)
#    plt.show()
#

#==============================================================================
    
def MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, vsh=0):
    #QPoints=125#f'tei
    #QSects=10#100#f'tei
    #QPoints=len(signal)
    QPairs=QPoints-1
    #dt=1/fs
    SectLenMed=QPairs/QSects
    SectLenInt=int(QPairs/QSects)
    rest=QPairs%QSects
    if vsh>0:
        print("QPoints="+str(QPoints)+" QSects="+str(QSects)+" QPairs="+str(QPairs)+" SectLenInt="+str(SectLenInt)+" SectLenMed="+str(SectLenMed)+" rest="+str(rest)+" In all: "+str(SectLenInt*QSects+rest))
        print("Forming rows")
    rows=[]
    row=[]
    rowN=0
    for N in range (1, QPoints+1):
        if vsh==1 or vsh==3:
            print("N="+str(N))
        row.append(N)
        #if N%QSects==0 and N<QPoints:
        if N%SectLenInt==0 and N<QPoints:
            if N<SectLenInt*QSects:
                if vsh==1 or vsh==3:
                    print("row bound reached")
                    print("row:")
                    print(row)
                #rowToAdd=copy.deepcopy(row)
                #rows.append(rowToAdd)
                rows.append(row)
                rowN+=1
                if vsh==1 or vsh==3:
                    print("latest subRow")
                    print(rows[rowN-1])
                if rowN>2:
                    if vsh==1 or vsh==3:
                        print("pre-latest subRow")
                        print(rows[rowN-2])
                row=[]
                #rowToAdd=[]
                row.append(N)
                #print("row bound reached")
            else:
                print("N="+str(N)+"=SectLenInt*QSects="+str(SectLenInt)+"*"+str(QSects)+"="+str(SectLenInt*QSects)+" - ignoring this point")
        elif N==QPoints:
            if vsh==1 or vsh==3:
                print("end reached")
                print("row:")
                print(row)
            #rowToAdd=copy.deepcopy(row)
            #rows.append(rowToAdd)
            rows.append(row)
            rowN+=1
            if vsh==1 or vsh==3:
                print("last subRow")
                print(rows[rowN-1])
            if rowN>2:
                if vsh==1 or vsh==3:
                    print("pre-last subRow")
                    print(rows[rowN-2])
            #rowToAdd=[]
            row=[]
            break
        #
    #
    if vsh==2 or vsh==3:
        QRows=len(rows)
        print("Result - "+str(QRows)+" rows:")
        for rowN in range(1, QRows+1):
            rowL=len(rows[rowN-1])
            print("row"+str(rowN)+" L="+str(rowL))
            for cmpnN in range(1, rowL-1+1):
                print(str(rows[rowN-1][cmpnN-1])+" ... "+str(rows[rowN-1][cmpnN-1+1]))
    #
    return rows
#

def MyEnvelopeBuilding_part2of3_IntegrOrMean(signal, QSects, fs=1):
    dt=1/fs
    rowsSs=[]
    rowsHs=[]
    QPoints=len(signal)
    rowsOfNs=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects)
    QRows=len(rowsOfNs)
    if fs==1:
        for rowN in range(1, QRows+1):
            rowL=len(rowsOfNs[rowN-1])
            rowS=0
            for i in range(1, rowL-1+1):
                N1=rowsOfNs[rowN-1][i-1]
                N2=rowsOfNs[rowN-1][i+1-1]
                rowS+=(signal[N1-1]+signal[N2-1])/2
            rowsSs.append(rowS)#je s'mult'd by 1, so S'S. Div S to (Q-1) = S/b=h
            rowsHs.append(rowS/(rowL-1))
    else:
        for rowN in range(1, QRows+1):
            rowL=len(rowsOfNs[rowN-1])
            rowS=0
            for i in range(1, rowL-1+1):
                N1=rowsOfNs[rowN-1][i-1]
                N2=rowsOfNs[rowN-1][i+1-1]
                rowS+=(signal[N1-1]+signal[N2-1])/2
            rowsSs.append(rowS*dt)#je s'mult'd by 1, so S'S. Div S to (Q-1) = S/b=h
            rowsHs.append(rowS/((rowL-1)*dt))
    return rowsHs

def MyEnvelopeBuilding_part2of3_SortMax(signal, QSects, percent=33, vsh=1):
    Maxs=[]
    NLast=0
    QPoints=len(signal)
    if vsh!=0:
        print("MyEnvelopeBuilding_part2of3_SortMax starts working")
    rowsOfNs=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, vsh=0)
    QRows=len(rowsOfNs)
    for i in range(1, QRows+1):
        rowIni=[]
        rowL=len(rowsOfNs[i-1])
        RowFirstN=rowsOfNs[i-1][1-1]
        RowLastN=rowsOfNs[i-1][rowL-1]
        for j in range(RowFirstN, RowLastN+1):
            val=signal[j-1]
            rowIni.append(val)
        if vsh!=0:
            print("rowN"+str(i))
            print("row initial")
            print(rowIni)
        rowSorted=[]
        rowSorted=copy.deepcopy(rowIni)
        SortArray(rowSorted, False)
        if vsh!=0:
            print("row sorted")
            print(rowSorted)
        rowSelected=[]
        for j in range(1, rowL-1+1):
            if j/rowL<=percent/100 and (j+1)/rowL>percent/100:
                NLast=j
                break
        rowSelected=rowSorted[0:NLast+1]
        if vsh!=0:
            print("row selected")
            print(rowSelected)
        s=0
        for  j in range(1, NLast+1):
            s+=rowSelected[j-1]
        Maxs.append(s/NLast)
    if vsh!=0:
        print("Finally:")
        print(Maxs)
        print("MyEnvelopeBuilding_part2of3_SortMax finishes working")
    return Maxs

def MyEnvelopeBuilding_part2of3_FindMax(signal, QSects, percent=33, vsh=0):
    Maxs=[]
    NLast=0
    QPoints=len(signal)
    if vsh!=0:
        print("MyEnvelopeBuilding_part2of3_SortMax starts working")
    rowsOfNs=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, vsh=0)
    QRows=len(rowsOfNs)
    for i in range(1, QRows+1):
        rowIni=[]
        rowL=len(rowsOfNs[i-1])
        RowFirstN=rowsOfNs[i-1][1-1]
        RowLastN=rowsOfNs[i-1][rowL-1]
        for j in range(RowFirstN, RowLastN+1):
            val=signal[j-1]
            rowIni.append(val)
        if vsh!=0:
            print("rowN"+str(i))
            print("row initial")
            print(rowIni)
        #rowSorted=[]
        #rowSorted=copy.deepcopy(rowIni)
        #SortArray(rowSorted, False)
        #if vsh!=0:
        #    print("row sorted")
        #    print(rowSorted)
        #rowSelected=[]
        #for j in range(1, rowL-1+1):
        #    if j/rowL<=percent/100 and (j+1)/rowL>percent/100:
        #        NLast=j
        #        break
        #rowSelected=rowSorted[0:NLast+1]
        #if vsh!=0:
        #    print("row selected")
        #    print(rowSelected)
        #s=0
        #for  j in range(1, NLast+1):
        #    s+=rowSelected[j-1]
        #Maxs.append(s/NLast)
        mnN, mn, mxN, mx = FindExtremsOfArray(rowIni)
        Maxs.append(mx)
    if vsh!=0:
        print("Finally:")
        print(Maxs)
        print("MyEnvelopeBuilding_part2of3_SortMax finishes working")
    return Maxs
        


def MyEnvelopeBuilding_part3of3_BuildingStairs(signal, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=2, percent=33, vsh=0):
    QPoints=len(signal)
    rowsOfNs=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, 0)
    if vrnN_Integr1_SortedMaxs2_Max3==1:
        rowsHs=MyEnvelopeBuilding_part2of3_IntegrOrMean(signal, QSects, fs)
    elif vrnN_Integr1_SortedMaxs2_Max3==2:
        rowsHs=MyEnvelopeBuilding_part2of3_SortMax(signal, QSects, percent=1, vsh=vsh)#33
    elif vrnN_Integr1_SortedMaxs2_Max3==3:
        rowsHs=MyEnvelopeBuilding_part2of3_FindMax(signal, QSects)
    QRows=len(rowsOfNs)
    Hs=[]
    n=0
    for i in range(1, QRows+1):
        rowL=len(rowsOfNs[i-1])
        val=rowsHs[i-1]
        for j in range(1, rowL-1+1):
            n+=1
            Hs.append(val)
            if(vsh==1):
                print("Pt "+str(n)+" rowN="+str(i)+" N in row="+str(j)+" row lims: ("+str(rowsOfNs[i-1][1-1])+"..."+str(rowsOfNs[i-1][rowL-1])+") val="+str(val)+"="+str(Hs[n-1]))
    n+=1
    Hs.append(val)
    if(vsh==1):
        print("Pt "+str(n)+" rowN="+str(i)+" N in row="+str(j)+" row lims: ("+str(rowsOfNs[i-1][1-1])+"..."+str(rowsOfNs[i-1][rowL-1])+") val="+str(val)+"="+str(Hs[n-1]))
    return Hs

def MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(signal, ts, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=2, percent=33, vsh=0):#new fs s'not f'IntegrOrMean
    trs=[]
    dt=ts[3]-ts[2]#1/fs
    t0=ts[0]
    t=t0-dt
    QPoints=len(signal)
    rowsOfNs=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, 0)
    if vrnN_Integr1_SortedMaxs2_Max3==1:
        rowsHs=MyEnvelopeBuilding_part2of3_IntegrOrMean(signal, QSects, fs)
    elif vrnN_Integr1_SortedMaxs2_Max3==2:
        rowsHs=MyEnvelopeBuilding_part2of3_SortMax(signal, QSects, percent=1, vsh=vsh)#33
    elif vrnN_Integr1_SortedMaxs2_Max3==3:
        rowsHs=MyEnvelopeBuilding_part2of3_FindMax(signal, QSects)
    QRows=len(rowsOfNs)
    for row in rowsOfNs:
        N1=row[1-1]
        t=ts[N1-1]
        #t+=dt
        #print("_t="+str(t))
        trs.append(t)
    if vsh!=0:
        print("fun: len(trs)="+str(len(trs))+" len(hs)="+str(len(rowsHs)))
    return trs, rowsHs

def ExcludeLowerPeaks(peaksHs, trs, vsh=1):#new
    QPeaks=len(peaksHs)
    if vsh==1:
        print("ExcludeLowerPeaks starts working. Qpeaks="+str(QPeaks))
    Hs=[]
    t2s=[]
    Nps=[]
    Hs.append(peaksHs[1-1])
    Nps.append(1)
    t2s.append(trs[1-1])
    print("first selected value: N="+str(Nps[1-1])+" t="+str(t2s[1-1])+" h="+str(Hs[1-1]))
    i=0#ob 1th V ecri
    ContinExt=True
    while ContinExt:
        #for i in range(2, QPeaks-1+1):
        i+=1
        contin=True
        if i==QPeaks-1:
            ContinExt=False
            contin=False
        #
        hi=peaksHs[i-1]
        mx=peaksHs[i+1-1]
        mxN=i+1
        #mxN=i#no infinite cycke
        #print("Checking: h[i="+str(i)+"]="+str(hi))
        #j=i+1-1
        j=i+1-1
        MaxIsFirst=True
        print("Let max be "+str(mx)+" (N "+str(mxN)+")")
        while contin:
            j+=1
            if j==QPeaks:
                #if j>=QPeaks:
                contin=False
                
            #
            hj=peaksHs[j-1]
            #mxN=i+1
            #print("compare with h[j="+str(j)+"]="+str(hj))
            print("compare h[i="+str(i)+"]="+str(hi)+" with h[j="+str(j)+"]="+str(hj))
            if hj>mx:
                mx=hj
                mxN=j
                #contin=False
                MaxIsFirst=False
                print(str(hj)+" - it is local max ")
                if mxN==QPeaks:
                    ContinExt=False
                #
            #
        if MaxIsFirst:
            print("max is first: i="+str(i)+" max's N="+str(mxN)+" mx="+str(peaksHs[i+1-1])+"="+str(mx))
        else:
            print("max found at: N="+str(mxN)+" mx="+str(peaksHs[mxN-1])+"="+str(mx)+"- deleting all before")
        #
        Hs.append(peaksHs[mxN-1])
        Nps.append(mxN)
        t2s.append(trs[mxN-1])
        i=mxN-1
        #i=mxN
        if i>=QPeaks-1:
            ContinExt=False
            contin=False
        #
    #
    if vsh==1:
        print("ExcludeLowerPeaks finishes working")
    return Nps, t2s, Hs
        
            

def MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs, trs, ts, type_Stairs0Line1=0, vsh=0):#new
    peakQ=len(trs)
    signalQ=len(ts)
    print("peakQ="+str(peakQ)+" "+"signalQ="+str(signalQ))
    Hs=[]
    j1=1
    N=0
    if type_Stairs0Line1==0:
        #for i in range(1, peakQ-1+1): #ce code sol ety arb, ma I n'arb, et I n'vid l'err 
        #    if i==1:
        #        #print("i="+str(i))
        #        t1=0
        #    else:
        #        t1=trs[i-1]
        #    if i==peakQ:
        #        t2=ts[signalQ-1]+2
        #    else:
        #        t2=trs[i+1-1]
        #    h=peaksHs[i-1]
        #    contin=True
        #    j=j1-1
        #    while contin:
        #        j+=1
        #        N+=1
        #        if j==signalQ:
        #            contin=False
        #        if i>=11 and j>=100588:
        #            print("i="+str(i)+" j="+str(j))
        #        t=ts[j-1]
        #        ss="Np="+str(i)+" "+"t1="+str(t1)+" "+"t2="+str(t2)+" "+"j1="+str(j1)+" "+"j="+str(j)+" "+"N="+str(N)+" "+"t="+str(t)
        #        if t>=t1 and t<t2:
        #            Hs.append(h)
        #            ss+=" t within range, h="+str(h)
        #            j1=j+1
        #        else:
        #            ss+=" t not within range"
        #            #break;#mab tic break dego ne nur ine, ma et ext cycle
        #            contin=False
        #            N-=1
        #        print(ss)
        #    #
        j1=2
        if vsh!=0:
            print("signalQ="+str(signalQ)+" peakQ="+str(peakQ)+" ts1="+str(ts[0])+" tsL="+str(ts[len(ts)-1])+" trs1="+str(trs[0])+" trsL="+str(trs[len(trs)-1]) )
        for i in range(1, signalQ+1):
            t=ts[i-1]
            ss="i="+str(i)+" t="+str(t)+" "
            if t<trs[2-1]:
                h=peaksHs[1-1]
                found=1
                ss+=" t<t2="+str(trs[2-1])+" "
                if t<trs[1-1]:
                    ss+="(t<t1="+str(trs[1-1])+"!)"+" "
            elif t>=trs[peakQ-1]:
                h=peaksHs[peakQ-1]
                found=1
                ss+=" t>=tL="+str(trs[peakQ-1])+" "
            else:
                contin=True
                j=j1-1
                while contin:
                    found=0
                    j+=1
                    if j==peakQ-1:
                        contin=False
                    t1=trs[j-1]
                    t2=trs[j+1-1]
                    if t>=t1 and t<=t2:
                        h=peaksHs[j-1]
                        #j1=j+1
                        j1=j#ja, n'ef, ma qob ne af ce?
                        contin=False
                        found=1
                        ss+=" j="+str(j)+" t["+str(j)+"]="+str(t1)+"<= t= "+str(t)+"<= t["+str(j+1)+"]="+str(t2)+" j1="+str(j1)+" "
                if found==0:
                    ss+="Not found: t="+str(t)+" t2="+str(trs[2-1])+" tL="+str(trs[peakQ-1])+" "
            ss+=" h="+str(h)
            if vsh!=0:
                print(ss)
            Hs.append(h)
        #
    elif type_Stairs0Line1==1:
        for i in range(1, signalQ+1):
            t=ts[i-1]
            h=LinInterp(trs, peaksHs, t)
            Hs.append(h)
        #
    #
    return Hs
        

def MyEnvelopeBuilding_part3of3_BuildingCurveLinApprox(signal, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=2, percent=33, vsh=0):
    print("MyEnvelopeBuilding_part3of3_BuildingCurveLinApprox starts working")
    QPoints=len(signal)
    print("def rowsOfNs")
    rowsOfNs=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, 0)
    print("def rowsHs")
    if vrnN_Integr1_SortedMaxs2_Max3==1:
        rowsHs=MyEnvelopeBuilding_part2of3_IntegrOrMean(signal, QSects, fs)
    elif vrnN_Integr1_SortedMaxs2_Max3==2:
        rowsHs=MyEnvelopeBuilding_part2of3_SortMax(signal, QSects, percent=1, vsh=vsh)#33
    elif vrnN_Integr1_SortedMaxs2_Max3==3:
        rowsHs=MyEnvelopeBuilding_part2of3_FindMax(signal, QSects)
    print("Forming row of ts of rowsHs row")
    QRows=len(rowsOfNs)
    print("signal length="+str(len(signal))+" "+"rowsHs length="+str(len(rowsHs))+" "+"rowsOfNs length="+str(len(rowsOfNs)))
    trs=[]
    for i in range(len(rowsOfNs)):
        t=rowsOfNs[i][0]/fs
        trs.append(t)
        print("trs["+str(i)+"]="+str(trs[i]))
    print("Forming row of ts of signal row")
    dt=1/fs
    ts=[]
    for i in range(len(signal)):
        t=i*dt
        ts.append(t)
        print("ts["+str(i)+"]="+str(ts[i]))
    Hs=[]
    print("Defining all Hs for all ts by interpolating")
    for i in range(len(signal)):
        t=ts[i]
        h=LinInterp(trs, rowsHs, t)
        Hs.append(h)
        print(str(i+1)+") ts="+str(ts[i])+" Hs="+str(Hs[i]))
    print("signal length="+str(len(signal))+" "+"rowsHs length="+str(len(rowsHs))+" "+"rowsOfNs length="+str(len(rowsOfNs)))
    print("trs length="+str(len(trs))+" "+"rowsHs length="+str(len(rowsHs))+" ts length="+str(len(ts))+" "+"Hs length="+str(len(Hs)))
    print("MyEnvelopeBuilding_part3of3_BuildingCurveLinApprox starts working")
    return Hs
        
    
#def MyEnvelopeBuilding_part4of3_BuildingCurve_NurInitialT
def MyEnvelopeBuilding_part4of3_CalcCoefs_v1(Hs, Ts, do_lnT=False, do_lnY=True, vsh=1):
    QPoints=len(Hs)
    if vsh!=0:
        print("MyEnvelopeBuilding_part4of3_CalcCoefs_v1 starts working. Elaborating row of values: "+str(QPoints))
    SumX=0
    SumY=0
    SumXY=0
    SumXp2=0
    for i in range(QPoints):
        val_t=Ts[i]-Ts[0]
        #if do_lnT:
        #    val_t=np.log(val_t)
        val_y=Hs[i]
        if do_lnY:
            val_y=math.log(val_y+1e-8)#val_x=math.log(val_t) - all ce arb id'y
        #trs.append(val_t)
        #    trf.append(rowsOfNs[i][L-1])
        #MeanX+=val_t
        #MeanY+=val_x
        SumX+=val_t
        SumY+=val_y
        SumXY+=val_t*val_y
        SumXp2+=val_t*val_t
    numerator=QPoints*SumXY-SumX*SumY
    denominator=QPoints*SumXp2-SumX*SumX
    beta=numerator/denominator
    alfa = (SumY - beta*SumX)/QPoints
    if vsh!=0:
        print("SumX="+str(SumX)+" "+"SumY="+str(SumY)+" "+"SumXY="+str(SumXY)+" "+"SumXp2="+str(SumXp2))
        print("alfa="+str(alfa)+" "+"beta="+str(beta)+" ")
        print("MyEnvelopeBuilding_part4of3_CalcCoefs_v1 finishes working")
    return alfa, beta

def MyEnvelopeBuilding_part4of3_CalcCoefs(signal, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, do_lnT=False, do_lnX=True, vsh=0):
    #this function is not for use - it has incorrect formulas
    QPoints=len(signal)
    rowsOfNs=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, 0)
    if vrnN_Integr1_SortedMaxs2_Max3==1:
        rowsHs=MyEnvelopeBuilding_part2of3_IntegrOrMean(signal, QSects, fs)
    elif vrnN_Integr1_SortedMaxs2_Max3==2:
        rowsHs=MyEnvelopeBuilding_part2of3_SortMax(signal, QSects, percent=1, vsh=vsh)#33
    elif vrnN_Integr1_SortedMaxs2_Max3==3:
        rowsHs=MyEnvelopeBuilding_part2of3_FindMax(signal, QSects)
    QRows=len(rowsOfNs)
    trs=[]
    #trf=[]
    MeanX=0
    MeanY=0
    for i in range(QRows):
        L=len(rowsOfNs[i])
        val_t=rowsOfNs[i][1-1]
        if do_lnT:
            val_t=np.log(val_t)
        val_x=rowsHs[i]
        if do_lnX:
            val_x=math.log(val_x+1e-8)#val_x=math.log(val_t) - all ce arb id'y
        trs.append(val_t)
        #    trf.append(rowsOfNs[i][L-1])
        MeanX+=val_t
        MeanY+=val_x
    MeanX/=QRows
    MeanY/=QRows
    numerator=0
    m1=0
    m2=0
    denominator=0
    for i in range(QRows):
        val_t=rowsOfNs[i][1-1]
        if do_lnT:
            val_t=np.log(val_t)
        m1= val_t - MeanX
        val_x=rowsHs[i]
        if do_lnX:
            val_x=math.log(val_x)
        m2= rowsHs[i] - MeanY
    numerator+=(m1*m2)
    denominator+=(m1*m1)
    beta=numerator/denominator
    alfa = MeanY - beta*MeanX
    return alfa, beta

#def exponential_func(x, a, b, c):
#    return a*np.exp(b*x)+c
#
#def MyEnvelopeBuilding_part4of3_CalcCoefs_NeLin(T, Y, a, b, c):
#    p0_guess=(a, b, c)
#    T=np.array(T)
#    Y=np.array(Y)
#    popt, pcov=curve_fit(exponential_func, T, X, p0-p0_guess)
#    a_opt, b_opt, c_opt=popt
#    return a_opt, b_opt, c_opt

def exponential_func(x, al, dc, c):
    return al*np.exp(dc*x)+c

def exponential_envel_theor(x, P):
    al=P[1-1]
    dc=P[2-1]
    #c =P[3-1]
    return al*np.exp(-dc*x)

def exp_envel_regr(P0, ts, Xs):
    QVals=len(ts)
    s=0
    for i in len(QVals):
        t=ts[i]
        ye=Xs[i]
        yt=exponential_envel_theor(t, P0)
        c=(yt-ye)*(yt-ye)
        s+=c
    return s

def FuncToApprox(x, func, X):
    return func(x, X)

def MyEnvelopeBuilding_part4of3_CalcCoefs_NeLin_MyByLib(T, X, exp_envel_regr, al, k):
    iniGuess=np.array([al, k])
    params=fmin_powell(regr_fn, IniGuess)

def MyEnvelopeBuilding_part4of3_CalcCoefs_NeLinLib(T, Y, al, dc, c):
    p0_guess=(al, dc, c)
    T=np.array(T)
    Y=np.array(Y)
    popt, pcov = curve_fit(exponential_func, T, X, p0=p0_guess)
    al_opt, dc_opt, c_opt = popt
    return al_opt, dc_opt, c_opt


def MyFindFreqsPeaks(freqs, ampls, QForPeak=50, vsh=1):
    QFreqs=len(ampls)
    QBefore=QForPeak
    QAfter=QForPeak
    if vsh!=0:
        print("MyFindPeaks starts working: QFreqs="+str(QFreqs)+" QForPeak="+str(QForPeak))
    peaks=[]
    peaksNs=[]
    peakFreqs=[]
    for N in range(1, QFreqs-1+1):
        fn=ampls[N-1]
        if vsh!=0:
            print("f[N="+str(N)+"]="+str(fn))
        NL1=N-QForPeak
        NL2=N-1
        NR1=N+1
        NR2=N+QForPeak
        if N<QForPeak:
            QBefore=N
            NL1=1
        if N>QFreqs-QForPeak:
            QAfrer=QFreqs-N
            NR2=QFreqs
        #if N==QFreqs:
        #    NR1
        if vsh!=0:
            print(" NL1="+str(NL1)+" NL2="+str(NL2)+" NR1="+str(NR1)+" NR2="+str(NR2))
        mxL=ampls[NL1-1]
        for j in range(NL1, NL2+1):
            f=ampls[j-1]
            if j==NL1 or (j>NL1 and f>mxL):
                mxL=f
        mxR=ampls[NR1-1]
        for j in range(NR1, NR2+1):
            f=ampls[j-1]
            if j==NR1 or (j>NR1 and f>mxR):
                mxR=f
        if vsh!=0:
            print("maxn ampl of f("+str(NL1)+"..."+str(NL2)+")="+str(mxL)+"; max ampl of f("+str(NR1)+"..."+str(NR2)+")="+str(mxR))
        if fn>=mxL and fn>=mxR:
            peakN=N
            peaks.append(fn)
            peaksNs.append(N)
            peakFreqs.append(freqs[N-1])
        else:
            if vsh!=0:
                print(str(fn)+" is not a peak at "+str(NL1)+" ... "+str(NR2))
            #
        #
    #
    return peaksNs, peakFreqs, peaks
#
def MyFindFreqsPeaks_onlyNs(freqs, ampls, QForPeak=50, vsh=1):
    QFreqs=len(ampls)
    QBefore=QForPeak
    QAfter=QForPeak
    peaks=[]
    peaksNs=[]
    peakFreqs=[]
    for N in range(1, QFreqs-1+1):
        fn=ampls[N-1]
        NL1=N-QForPeak
        NL2=N-1
        NR1=N+1
        NR2=N+QForPeak
        if N<QForPeak:
            QBefore=N
            NL1=1
        #
        if N>QFreqs-QForPeak:
            QAfrer=QFreqs-N
            NR2=QFreqs
        #
        mxL=ampls[NL1-1]
        for j in range(NL1, NL2+1):
            f=ampls[j-1]
            if j==NL1 or (j>NL1 and f>mxL):
                mxL=f
            #
        #
        mxR=ampls[NR1-1]
        for j in range(NR1, NR2+1):
            f=ampls[j-1]
            if j==NR1 or (j>NR1 and f>mxR):
                mxR=f
            #
        #
        if fn>=mxL and fn>=mxR:
            peakN=N
            peaks.append(fn)
            peaksNs.append(N)
            peakFreqs.append(freqs[N-1])
        #
    #
    return peaksNs
#
        
      
def FindImpactBounds(ts, signal, fs, tSectHalf=4, vsh=0):#not tested
    if vsh==1:
        print("FindImpactBounds starts working")
    #
    boundsNs=[]
    boundsXs=[]
    boundsTs=[]
    bounds=[]
    section=[]
    dt=1/fs
    t0=ts[0]
    tMax=ts[-1]
    tLast=tMax-tSectHalf
    NLast=int(tLast/dt)
    tFirst=10*dt+tSectHalf
    QPointsInSectHalf=int(tSectHalf/dt)
    NFirst=10+QPointsInSectHalf
    N1=NFirst-QPointsInSectHalf
    if vsh==1:
        print(" t0="+str(t0)+" tmax="+str(tMax)+" fs="+str(fs)+" dt="+str(dt)+" QPoints="+len(ts))
        print(" tSectHalf="+str(tSectHalf)+" QPointsInSectHalf="+str(QPointsInSectHalf))
        print(" Starting from: N1="+str(NFirst)+" t1="+str(ts[NFirst-1]))
    #
    while N1<NLast:
        #N1+=1
        N2=N1+2*QPointsInSectHalf
        t1=ts[N1-1]
        t2=ts[N2-1]
        for N in range(N1, N2+1):
            t=ts[N-1]
            x=signal[N-1]
            if vsh==1:
                print("N="+str(N)+" t="+str(t)+" x="+str(x))
            #
            if N==N1 or (N>N1 and abs(x)>xmax):
                xmax=x
                Nmax=N
                tmax=t
                if vsh==1:
                    print("max: N(xmax)="+str(Nmax)+" t(xmax)="+str(tmax)+" x="+str(xmax))
                #
            #
        #
        bounds.append(tmax)
        N1=N2#+QPointsInSectHalf
        if vsh==1:
            print("Section - finally: t="+str(t1)+"..."+str(t2)+": "+" xmax="+str(xmax)+" t(xmax)="+str(tmax))
        #
    #
    if vsh==1:
        print("Answer: ",bounds)
        print("FindImpactBounds finishes working")
    #
    return bounds
#

def compute_spectrum_1(
    x,
    fs,
    window_type="hann",
    remove_mean=True,
    use_detrend=False,
    zero_padding_factor=1,
    fmin=None,
    fmax=None
):
    """
    Улучшенный расчёт спектра для модального анализа.
    """

    x = np.asarray(x, dtype=float)

    # --- DC и тренд ---
    if remove_mean:
        x = x - np.mean(x)

    if use_detrend:
        x = detrend(x)

    N_orig = len(x)

    # --- Zero-padding ---
    N = N_orig * zero_padding_factor
    if zero_padding_factor > 1:
        x = np.pad(x, (0, N - N_orig), mode='constant')

    # --- Окно ---
    if window_type is not None:
        if window_type == "hann":
            window = np.hanning(len(x))
        elif window_type == "hamming":
            window = np.hamming(len(x))
        elif window_type == "blackman":
            window = np.blackman(len(x))
        else:
            raise ValueError("Unknown window type")

        # Нормировка окна
        window /= np.mean(window)
        x = x * window

    # --- FFT ---
    X = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(len(x), 1/fs)
    amps = 2 * np.abs(X) / len(x)

    # --- Ограничение диапазона ---
    if fmin is not None or fmax is not None:
        mask = np.ones_like(freqs, dtype=bool)
        if fmin is not None:
            mask &= freqs >= fmin
        if fmax is not None:
            mask &= freqs <= fmax

        freqs = freqs[mask]
        amps = amps[mask]

    return freqs, amps
#
def compute_spectrum_2(
    # abls exta window type et alfa et zgof ce all
    x,
    fs,
    window_type=None,      # None, 'hann', 'decay'
    alpha=None,            # только для decay
    use_mean=False,
    use_detrend=False,
    zero_padding_factor=1
):
    """
    Вычисление амплитудного спектра.
    """

    x_proc = np.array(x, dtype=float)

    # --- подготовка сигнала ---
    if use_mean:
        x_proc -= np.mean(x_proc)

    if use_detrend:
        x_proc = detrend(x_proc)

    N_orig = len(x_proc)

    # --- zero padding ---
    if zero_padding_factor > 1:
        N = N_orig * zero_padding_factor
        x_proc = np.pad(x_proc, (0, N - N_orig), 'constant')
    else:
        N = N_orig

    # --- окна ---
    if window_type == 'hann':
        window = np.hanning(len(x_proc))
        x_proc *= window

    elif window_type == 'decay':
        if alpha is None:
            raise ValueError("Для decay окна необходимо задать alpha")
        window = decay_window(len(x_proc), fs, alpha)
        x_proc *= window

    # --- FFT ---
    X = np.fft.fft(x_proc)
    amps = 2 * np.abs(X[:N // 2]) / N
    freqs = np.fft.fftfreq(N, d=1/fs)[:N // 2]

    return freqs, amps
#

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

    
def bandpass_filter(
    x,
    fs,
    f0,
    bandwidth,
    order=4
):
    """
    Узкополосный фильтр вокруг моды f0.
    bandwidth — полная ширина полосы (Гц)
    """

    f1 = max(f0 - bandwidth / 2, 0.1)
    f2 = f0 + bandwidth / 2

    nyq = fs / 2
    b, a = butter(
        order,
        [f1 / nyq, f2 / nyq],
        btype='band'
    )

    return filtfilt(b, a, x)
#
#Как выбрать bandwidth
#Ситуация	bandwidth
#чистая мода	2–5% от f₀
#близкие пики	1–2%
#сильный шум	5–10%
#
#Слишком широко → биения
#Слишком узко → «размазанная» фаза
#
def envelope_hilbert(x):
    """
    Огибающая сигнала через аналитический сигнал.
    """
    analytic = hilbert(x)
    env = np.abs(analytic)
    return env
#
def estimate_decay(
    t,
    envelope,
    t_start=None,
    t_end=None
):
    """
    Оценка коэффициента затухания по огибающей.
    """

    mask = np.ones_like(t, dtype=bool)

    if t_start is not None:
        mask &= t >= t_start
    if t_end is not None:
        mask &= t <= t_end

    t_fit = t[mask]
    env_fit = envelope[mask]

    # защита от лог(0)
    env_fit = np.maximum(env_fit, np.max(env_fit) * 1e-6)

    ln_env = np.log(env_fit)

    # линейная аппроксимация
    coef = np.polyfit(t_fit, ln_env, 1)

    decay_rate = -coef[0]  # 1/с
    return decay_rate, coef
#
def extract_mode(
    t,
    x,
    fs,
    f0,
    bandwidth,
    filter_order=4,
    decay_fit_window=None
):
    """
    Полный цикл выделения моды.
    """

    # 1. Фильтр
    x_mode = bandpass_filter(
        x, fs, f0, bandwidth, filter_order
    )

    # 2. Огибающая
    env = envelope_hilbert(x_mode)

    # 3. Затухание
    if decay_fit_window:
        decay, coef = estimate_decay(
            t,
            env,
            decay_fit_window[0],
            decay_fit_window[1]
        )
    else:
        decay, coef = estimate_decay(t, env)

    return {
        "frequency": f0,
        "signal": x_mode,
        "envelope": env,
        "decay_rate": decay,
        "fit_coef": coef
    }
#
def extract_modes(
    t,
    x,
    fs,
    frequencies,
    bandwidths,
    decay_windows=None
):
    """
    frequencies — список частот мод
    bandwidths — список полос
    decay_windows — [(t1, t2), ...] или None
    """

    modes = []

    for i, f0 in enumerate(frequencies):
        bw = bandwidths[i]

        win = None
        if decay_windows:
            win = decay_windows[i]

        mode = extract_mode(
            t,
            x,
            fs,
            f0,
            bw,
            decay_fit_window=win
        )

        modes.append(mode)

    return modes
#
        
# --------------------------------------------------------

def Sort3ArraysByOne(Ns, Freqs, Amps, byNs1Freqs2Amps3=3):
    Q=len(Ns)
    for i in range(1, Q-1+1):
        for j in range(i+1, Q+1):
            N_i=Ns[i-1]
            freq_i=Freqs[i-1]
            Amp_i=Amps[i-1]
            N_j=Ns[j-1]
            freq_j=Freqs[j-1]
            Amp_j=Amps[j-1]
            if (byNs1Freqs2Amps3==1 and N_j>N_i)\
                or \
               (byNs1Freqs2Amps3==1 and freq_j>freq_i)\
                or \
               (byNs1Freqs2Amps3==1 and Amp_j>Amp_i):
                Ns[i-1]=N_j
                Amps[i-1]=Amp_j
                Freqs[i-1]=freq_j
                Ns[j-1]=N_i
                Amps[j-1]=Amp_i
                Freqs[j-1]=freq_i
            #
        #
    #
#
def Sort3ArraysByOne_v1(arr1, arr2, arr3, by123=3, DescNotAsc=True):
    Q=len(arr1)
   
    for i in range(1, Q-1+1):
        for j in range(i+1, Q+1):
            arr1_i=arr1[-1]
            arr2_i=arr2[i-1]
            arr3_i=arr3[i-1]
            arr1_j=arr1[j-1]
            arr2_j=arr2[j-1]
            arr3_j=arr3[j-1]
            #
            if (
                  DescNotAsc
                  and
                  (
                   (by123==1 and arr1_j>arr1_i)
                    or
                   (by123==1 and arr2_j>arr2_i)
                    or
                    (by123==1 and arr3_j>arr3_i)
                   )
               ) \
               or \
               (
                  DescNotAsc==False
                  and
                  (
                   (by123==1 and arr1_j<arr1_i)
                    or
                   (by123==1 and arr2_j<arr2_i)
                    or
                    (by123==1 and arr3_j<arr3_i)
                   )
               ):
                arr1[i-1]=arr1_j
                arr2[i-1]=arr2_j
                arr3[i-1]=arr3_j
                arr1[j-1]=arr1_i
                arr2[j-1]=arr2_i
                arr3[j-1]=arr3_i
            #
        #
    #
#
def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
    if vsh==1:
        print("Sort3ArraysByOne_v2 starts working")
        if DescNotAsc:
            print("sort by arr"+str(by123)+" descending")
        else:
            print("sort by arr"+str(by123)+" ascending")
        #
    #
    Q=len(arr1)
    if vsh==1:
        print("given:")
        if Q%2==0:
            print("Q ="+str(Q)+"- is even")
            N=1
            if isinstance(N, int):
                print("N - int")
            else:
                print("N - ne int")
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q/2
            print("N=Q/2="+str(N))
            if isinstance(N, int):
                print("N - int")
            else:
                print("N - ne int")
            N=Q//2
            print("N=Q//2="+str(N))
            if isinstance(N, int):
                print("N - int")
            else:
                print("N - ne int")
            N=(Q+2.2+2.4-1.3-3.1)//2
            print("N=(Q+2.2+2.4-1.3-3.1)//2="+str(N))
            print("N="+str(N))
            if isinstance(Q, int):
                print("Q - int")
            else:
                print("Q - ne int")
            if isinstance(N, int):
                print("N - int")
            else:
                print("N - ne int")
            N=Q//2
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
        else:
            print("Q ="+str(Q)+" - is odd")
            N=1
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=(Q-1)/2+1
            N=(Q-1)//2+1
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
        #
    #
    for i in range(1, Q-1+1):
        for j in range(i+1, Q+1):
            arr1_i=arr1[i-1]
            arr2_i=arr2[i-1]
            arr3_i=arr3[i-1]
            arr1_j=arr1[j-1]
            arr2_j=arr2[j-1]
            arr3_j=arr3[j-1]
            if vsh==1:
                print("i="+str(i)+" j="+str(j)) 
                print("i: x1["+str(i)+"]="+str(arr1_i)+" x2["+str(i)+"]="+str(arr2_i)+" x3["+str(i)+"]="+str(arr3_i))
                print("j: x1["+str(j)+"]="+str(arr1_j)+" x2["+str(j)+"]="+str(arr2_j)+" x3["+str(j)+"]="+str(arr3_j))
            #
            if DescNotAsc:
                if \
                   (by123==1 and arr1_j>arr1_i) \
                    or \
                   (by123==2 and arr2_j>arr2_i) \
                    or \
                   (by123==3 and arr3_j>arr3_i):
                    arr1[i-1]=arr1_j
                    arr2[i-1]=arr2_j
                    arr3[i-1]=arr3_j
                    arr1[j-1]=arr1_i
                    arr2[j-1]=arr2_i
                    arr3[j-1]=arr3_i
                    if vsh==1:
                        print("exchange")
                    #
                else:
                    if vsh==1:
                        print("stay")
                    #
                #
            else:
                if \
                   (by123==1 and arr1_j<arr1_i) \
                    or \
                   (by123==2 and arr2_j<arr2_i) \
                    or \
                   (by123==3 and arr3_j<arr3_i):
                    arr1[i-1]=arr1_j
                    arr2[i-1]=arr2_j
                    arr3[i-1]=arr3_j
                    arr1[j-1]=arr1_i
                    arr2[j-1]=arr2_i
                    arr3[j-1]=arr3_i
                    if vsh==1:
                        print("exchange")
                    #
                else:
                    if vsh==1:
                        print("stay")
                    #
                #
            #
        #
    #
    if vsh==1:
        print("answer:")
        for N in range(Q):
            print("N="+str(N+1)+": x1["+str(N+1)+"]="+str(arr1[N])+" x2["+str(N+1)+"]="+str(arr2[N])+" x3["+str(N+1)+"]="+str(arr3[N]))
        #
        print("Sort3ArraysByOne_v2 finishes working")    
    #
#
def Sort3ArraysByOne_v3(arr1, arr2, arr3, by123=3, AscNotDesc=False, vsh=0):
    if vsh==1:
        print("Sort3ArraysByOne_v3 starts working")
        if AscNotDesc:
            print("sort by arr"+str(by123)+" ascending")
        else:
            print("sort by arr"+str(by123)+" descending")
        #
    #
    Q=len(arr1)
    if vsh==1:
        print("given:")
        if Q%2==0:
            print("Q ="+str(Q)+" - is even")
            N=1
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q/2
            N=Q//2
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
        else:
            print("Q ="+str(Q)+" - is odd")
            N=1
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=(Q-1)/2+1
            N=(Q-1)//2+1
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
        #
    #
    for i in range(1, Q-1+1):
        for j in range(i+1, Q+1):
            arr1_i=arr1[i-1]
            arr2_i=arr2[i-1]
            arr3_i=arr3[i-1]
            arr1_j=arr1[j-1]
            arr2_j=arr2[j-1]
            arr3_j=arr3[j-1]
            if vsh==1:
                print("i="+str(i)+" j="+str(j)) 
                print("i: x1["+str(i)+"]="+str(arr1_i)+" x2["+str(i)+"]="+str(arr2_i)+" x3["+str(i)+"]="+str(arr3_i))
                print("j: x1["+str(j)+"]="+str(arr1_j)+" x2["+str(j)+"]="+str(arr2_j)+" x3["+str(j)+"]="+str(arr3_j))
            #
            if AscNotDesc:
                if \
                   (by123==1 and arr1_j<arr1_i) \
                    or \
                   (by123==2 and arr2_j<arr2_i) \
                    or \
                   (by123==3 and arr3_j<arr3_i):
                    arr1[i-1]=arr1_j
                    arr2[i-1]=arr2_j
                    arr3[i-1]=arr3_j
                    arr1[j-1]=arr1_i
                    arr2[j-1]=arr2_i
                    arr3[j-1]=arr3_i
                    if vsh==1:
                        print("exchange")
                    #
                else:
                    if vsh==1:
                        print("stay")
                    #
                #
            else:
                if \
                   (by123==1 and arr1_j>arr1_i) \
                    or \
                   (by123==2 and arr2_j>arr2_i) \
                    or \
                   (by123==3 and arr3_j>arr3_i):
                    arr1[i-1]=arr1_j
                    arr2[i-1]=arr2_j
                    arr3[i-1]=arr3_j
                    arr1[j-1]=arr1_i
                    arr2[j-1]=arr2_i
                    arr3[j-1]=arr3_i
                    if vsh==1:
                        print("exchange")
                    #
                else:
                    if vsh==1:
                        print("stay")
                    # 
                #
            #
        #
    #
    if vsh==1:
        print("answer:")
        for N in range(Q):
            print("N="+str(N+1)+": x1["+str(N+1)+"]="+str(arr1[N])+" x2["+str(N+1)+"]="+str(arr2[N])+" x3["+str(N+1)+"]="+str(arr3[N]))
        #
        print("Sort3ArraysByOne_v3 finishes working")    
    #
    return arr1, arr2, arr3
#

def ChooseFreqsBySetMemberN(Ns, Freqs, amps, FreqsSample, N, dFPercent=20, dAPercent=80):
    print("\nChooseFreqsBySetMemberN starts working")
    print("Frequencies standard, nearest to which real frequencies are being chosen:")
    print(FreqsSample)
    rslt=[]
    freqSmp=FreqsSample[N-1]
    print("Choosing frequency, nearest to value N "+str(N)+" : "+str(freqSmp))
    dFPerCentLim=50
    Q=len(Ns)
    QS=len(FreqsSample)
    dFrs=[]
    freqs_chsn=[]
    amps_chsn=[]
    Ns_chsn=[]
    if N==1:
        minFr=0
        maxFr=freqSmp+(FreqsSample[N+1-1]-FreqsSample[N-1])/100*dFPercent
    elif N==QS:
        minFr=freqSmp-(FreqsSample[N-1]-FreqsSample[N-1-1])/100*dFPercent
        maxFr=freqSmp+(FreqsSample[N-1]-FreqsSample[N-1-1])/100*dFPercent
    else:
        minFr=freqSmp-(FreqsSample[N-1]-FreqsSample[N-1-1])/100*dFPercent
        maxFr=freqSmp+(FreqsSample[N+1-1]-FreqsSample[N-1])/100*dFPercent
    #
    print("Chosen range: "+str(dFPercent)+"%: "+str(minFr)+"..."+str(maxFr))
    #
    for i in range (Q):
        amp_cur=amps[i]
        if i==0 or (i>0 and amp_cur>amp_max):
            amp_max=amp_cur
        #
    #
    for i in range (Q):
        freq_cur=Freqs[i]
        if freq_cur>=minFr and freq_cur<=maxFr:
            freqs_chsn.append(freq_cur)
            Ns_chsn.append(i+1)
            amps_chsn.append(amps[i])
            dFrs.append(abs(freq_cur-freqSmp))
        #
    #
    Q_chsn=len(freqs_chsn)
    if(Q_chsn==0):
        
        if N==1:
            minFr=0
            maxFr=freqSmp+(FreqsSample[N+1-1]-FreqsSample[N-1])/100*dFPerCentLim
        elif N==QS:
            minFr=freqSmp-(FreqsSample[N-1]-FreqsSample[N-1-1])/100*dFPerCentLim
            maxFr=freqSmp+(FreqsSample[N-1]-FreqsSample[N-1-1])/100*dFPerCentLim
        else:
            minFr=freqSmp-(FreqsSample[N-1]-FreqsSample[N-1-1])/100*dFPerCentLim
            maxFr=freqSmp+(FreqsSample[N+1-1]-FreqsSample[N-1])/100*dFPerCentLim
        #
        print("no frequencies in this range found, making range wider, now it is: "+str(minFr)+"..."+str(maxFr))
        #
        for i in range (Q):
            freq_cur=Freqs[i]
            if freq_cur>=minFr and freq_cur<=maxFr:
                freqs_chsn.append(freq_cur)
                Ns_chsn.append(i+1)
                amps_chsn.append(amps[i])
                dFrs.append(abs(freq_cur-freqSmp))
            #
        #
    #
    Q_chsn=len(freqs_chsn)
    if Q_chsn>0:
        print("Top NEAREST ("+str(Q_chsn)+") frequencies:")
        for i in range (1, Q_chsn-1+1):
            for j in range(i+1, Q_chsn+1):
                freq_i=freqs_chsn[i-1]
                amp_i=amps_chsn[i-1]
                Ns_i=Ns_chsn[i-1]
                dFr_i=dFrs[i-1]
                freq_j=freqs_chsn[j-1]
                amp_j=amps_chsn[j-1]
                Ns_j=Ns_chsn[j-1]
                dFr_j=dFrs[j-1]
                if(dFr_j<dFr_i):
                    freqs_chsn[i-1]=freq_j
                    amps_chsn[i-1]=amp_j
                    Ns_chsn[i-1]=Ns_j
                    dFrs[i-1]=dFr_j
                    freqs_chsn[j-1]=freq_i
                    amps_chsn[j-1]=amp_i
                    Ns_chsn[j-1]=Ns_i
                    dFrs[j-1]=dFr_i
                #
            #
        #   
        print("returning order by frequencies accending")
        for i in range (1, Q_chsn-1+1):
            for j in range(i+1, Q_chsn+1):
            	freq_i=freqs_chsn[i-1]
            	amp_i=amps_chsn[i-1]
            	Ns_i=Ns_chsn[i-1]
            	dFr_i=dFrs[i-1]
            	freq_j=freqs_chsn[j-1]
            	amp_j=amps_chsn[j-1]
            	Ns_j=Ns_chsn[j-1]
            	dFr_j=dFrs[j-1]
            	if(freq_j<freq_i):
                    freqs_chsn[i-1]=freq_j#
                    amps_chsn[i-1]=amp_j
                    Ns_chsn[i-1]=Ns_j
                    dFrs[i-1]=dFr_j
                    freqs_chsn[j-1]=freq_i
                    amps_chsn[j-1]=amp_i
                    Ns_chsn[j-1]=Ns_i
                    dFrs[j-1]=dFr_i
                #
            #
        #   
        for i in range(1, Q_chsn+1):
            print("N="+str(Ns_chsn[i-1])+" freq="+str(freqs_chsn[i-1])+" amp="+str(amps_chsn[i-1])+" dFr="+str(dFrs[i-1]))
        #
        print("Top MAX amplitude frequencies:")
        for i in range (1, Q_chsn-1+1):
            for j in range(i+1, Q_chsn+1):
                freq_i=freqs_chsn[i-1]
                amp_i=amps_chsn[i-1]
                Ns_i=Ns_chsn[i-1]
                dFr_i=dFrs[i-1]
                freq_j=freqs_chsn[j-1]
                amp_j=amps_chsn[j-1]
                Ns_j=Ns_chsn[j-1]
                dFr_j=dFrs[j-1]
                if(freq_j<freq_i):
                    freqs_chsn[i-1]=freq_j
                    amps_chsn[i-1]=amp_j
                    Ns_chsn[i-1]=Ns_j
                    dFrs[i-1]=dFr_j
                    freqs_chsn[j-1]=freq_i
                    amps_chsn[j-1]=amp_i
                    Ns_chsn[j-1]=Ns_i
                    dFrs[j-1]=dFr_i
                #
            #
        #   
        for i in range(1, Q_chsn+1):
            print("N="+str(Ns_chsn[i-1])+" freq="+str(freqs_chsn[i-1])+" amp="+str(amps_chsn[i-1])+" dFr="+str(dFrs[i-1]))
        #
        if amps_chsn[0]>=amp_max/100*dAPercent:
            rslt=[Ns_chsn[0], freqs_chsn[0], amps_chsn[0]]
            print("Finally chosen:")
            print("N="+str(Ns_chsn[1-1])+" freq="+str(freqs_chsn[1-1])+" amp="+str(amps_chsn[1-1])+" dFr="+str(dFrs[1-1]))
        else:
            print("Chosen :nothing, no approximate frequences with big enough value of amplitude")
        #
    else:
        print("Chosen :nothing, no approximate frequences")
    #
    print("ChooseFreqsBySetMemberN finishes working\n")
    return rslt
#
#==================================================================================
# === Авто-генерация параметров для каждой моды ===
def make_params(freq, fs):
    bw = max(1.0, freq/50.0)  # полоса по умолчанию
    return dict(
        freq=freq,
        bandwidth=bw,
        filter_type="butter",
        filter_order=4,
        transient_cut=max(3.0/freq, 0.01),
        peak_distance=0.8/freq,
        envelope_smooth=dict(method="savgol", window=max(5, int(fs/(10*freq))//2*2+1), poly=2),
        fit_method="peaks",
        min_peaks=5,
        output_mode="params",
        notes=""
    )

# === Оценка затухания для одной моды ===
def process_mode(x, t, fs, params):
    f0 = params["freq"]
    bw = params["bandwidth"]
    nyq = fs/2
    
    # Фильтрация
    low = max(0.1, (f0 - bw/2)/nyq)
    high = min(0.999, (f0 + bw/2)/nyq)
    b, a = butter(params["filter_order"], [low, high], btype="band")
    x_filt = filtfilt(b, a, x)

    # Огибающая через Гильберта
    analytic = hilbert(x_filt)
    A = np.abs(analytic)

    # Отсечь начальный переходный процесс
    cut_samples = int(params["transient_cut"]*fs)
    if cut_samples < len(A):
        A = A[cut_samples:]
        t_seg = t[cut_samples:]
    else:
        return None

    # Сглаживание огибающей
    if params["envelope_smooth"]:
        w = params["envelope_smooth"]["window"]
        p = params["envelope_smooth"]["poly"]
        if len(A) > w:
            A = savgol_filter(A, w, p)

    # Поиск пиков
    dist = int(params["peak_distance"]*fs)
    peaks, _ = find_peaks(A, distance=dist)
    if len(peaks) < params["min_peaks"]:
        return None

    t_peaks = t_seg[peaks]
    A_peaks = A[peaks]

    # Логарифмическая регрессия
    y = np.log(A_peaks)
    C = np.mean(t_peaks)
    D = np.mean(y)
    num = np.sum((t_peaks - C)*(y - D))
    den = np.sum((t_peaks - C)**2)
    beta = num/den
    alpha = D - beta*C

    # Метрики
    y_pred = alpha + beta*t_peaks
    SSR = np.sum((y - y_pred)**2)
    SST = np.sum((y - np.mean(y))**2)
    R2 = 1 - SSR/SST
    E = SSR/(len(t_peaks)-2)

    delta = -beta
    tau = 1.0/delta if delta>0 else np.inf
    Q = np.pi*f0/delta if delta>0 else np.inf

    return dict(
        freq=f0,
        bandwidth=bw,
        n_peaks=len(peaks),
        alpha=alpha,
        beta=beta,
        delta=delta,
        tau=tau,
        Q=Q,
        R2=R2,
        E=E,
        notes=params["notes"]
    )

#------------------------------------------------------
#my modif, wu gut if ver

def process_mode_1_ipse(x, t, fs, params):
    f0 = params["freq"]
    bw = params["bandwidth"]
    nyq = fs/2
    
    # Фильтрация
    low = max(0.1, (f0 - bw/2)/nyq)
    high = min(0.999, (f0 + bw/2)/nyq)
    b, a = butter(params["filter_order"], [low, high], btype="band")
    x_filt = filtfilt(b, a, x)
    return x_filt, t
#

# === Основной анализ для списка частот ===
def process_modes(x, t, fs, freq_list):
    results = []
    for f in freq_list:
        params = make_params(f, fs)
        res = process_mode(x, t, fs, params)
        if res is not None:
            results.append(res)
    return pd.DataFrame(results)


def FindTImpactStart(X, fs, SectT=6, TrashBeforeT=1, TrashAfterT=1, MoreThanTrashCoef=3, vsh=0):
    QAll=len(X)
    SectLen=SectT*fs
    dt=1/fs
    tmax=QAll/fs
    if vsh==1:
        print("FindTImpactStart starts working")
        print("fs="+str(fs)+" SectT="+str(SectT)+" TrashBeforeT="+str(TrashBeforeT)+" TrashAfterT="+str(TrashAfterT)+" MoreThanTrashCoef="+str(MoreThanTrashCoef))
        print("QAll="+str(QAll)+" SectLen="+str(SectLen)+" dt="+str(dt)+" tmax="+str(tmax))
    #
    sectMaxs=[]
    sectMaxNs=[]
    #find TrashMax
    trashMax=0
    N1=1
    N2=TrashBeforeT*fs
    for N in range(N1, N2+1):
        x=X[N-1]
        if abs(x)>trashMax:
            trashMax= abs(x)
        #
    #
    N1=(tmax-TrashAfterT)*fs
    N2=QAll
    for N in range(N1, N2+1):
        x=X[N-1]
        if abs(x)>trashMax:
            trashMax= abs(x)
        #
    #
    if vsh==1:
        print("trashMax="+str(trashMax))
    #
    # nu trashMax s'ved, seek sectMax
    N1=TrashBeforeT*fs
    N2=QALL-TrashAfterT*fs-SectLen
    if vsh==1:
        print("Seek impacts starts ipse - whole range is: N1="+str(N1)+" N2="+str(N2))
    #
    i=0
    while i<N2:
        i+=1
        if vsh==1:
            print("Seek impacts start within current range: N1="+str(i)+" N2="+str(i+SectLen-1))
        #
        for j in range(1, SectLen+1):
            N=i+j-1
            x=X[N-1]
            if j==1 or (j>1 and abs(x)>sectMax):
                sectMax=abs(x)
                sectMaxN=N
                if vsh==1:
                    print("now cur max of cur range: N="+str(sectMaxN)+" val="+str(sectMax)+" = "+str(X[sectMaxN-1]))
                #
            #
        #
        if sectMax>MoreThanTrashCoef*trashMax:
            sectMaxs.append(sectMax)
            sectMaxNs.append(sectMaxN)
            if vsh==1:
                print("max of cur range: N="+str(sectMaxN)+" val="+str(sectMax))
            #
            i+=SectLen
        else:
            print("not max, too small")
        #
    #
    if vsh==1:
        print("Answer")
        print(sectMaxs)
        print(sectMaxNs)
        print("FindTImpactStart finishes working")
    #
    return sectMaxNs, sectMaxs
#
