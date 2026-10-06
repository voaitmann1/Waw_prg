#part 1

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import csv
import os

#---

def read_wav(fullFileName):
    fs, data = wavfile.read(fullFileName)
    if np.issubdtype(data.dtype, np.integer):
        max_val=np.info(data.dtype).max
        data=data.astype(np.float32)/max_val
    return(fs, data)

def read_wav_safe(fullFileName, max_seconds=None):
    try:
        fs, data=wavfile.read(fullFileName)
        #norm'g if data s'numoz
        if np.issubdtype(data.dtype, np.integer):
            max_val= np.iinfo(data.dtype).max
            data=data.astype(np.float32)
        return fs, data
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
        return fs, data

#---

def read_wav_and_calc_t(filename):
    #fs, data = wavfile.read(filename)
    fs, data = read_wav_safe(filename, max_seconds=None)
    if data.ndim > 1:
        data = data[:,0]  # первый канал, если стерео

    t = np.arange(len(data)) / fs
    return t, data, fs
    

def read_wav_and_save_csv(filename):
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
if __name__ == "__main__":
    fileOwnNames=["051_1_M.wav", "051-2.wav", "052-1.wav", "052-2.wav"]# добавьте свои файлы
    filePath="D:\\MyFilesCur\\MyPrgs\\Python\\Wav"
    filePathIniData=filePath+"\\"+"assets"#+"\\"+"IniData"
    filePathResults=filePath+"\\"+"assets"#+"\\"+"Results"
    filenames =[]
    for fileOwnName in fileOwnNames:
        fname=filePathIniData+"\\"+fileOwnName
        filenames.append(fname)
    
    # Времена ударов задаются вручную
    # ImpactID, StartTime_s, EndTime_s
    impacts = [
        (1, 0.12, 0.45),
        (2, 1.23, 5.67)
    ]
    #
    filechars=[]
    # Сохраняем ImpactBounds в CSV
    with open(filePathResults+"\\"+"ImpactBounds.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ImpactID", "StartTime_s", "EndTime_s"])
        for impact in impacts:
            writer.writerow(impact)

    print("ImpactBounds.csv создан")

    # Обработка каждого файла
    Nrec=0
    for fname in filenames:
        Nrec+=1
        #reading wav
        #t, signal, fs = read_wav_and_save_csv(fname)
        t, signal, fs = read_wav_and_calc_t(fname)
        #writing to csv
        csv_filename = os.path.splitext(fname)[0] + "_signal_whole.csv"
        with open(csv_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(["Time_s", "Signal"])
            writer.writerow(["Time_s", "Signal", "Energy"])
            for i in range(len(t)):
                #writer.writerow([t[i], data[i]])
                writer.writerow([t[i], signal[i], signal[i]*signal[i]])
            #
        print(f"Сигнал сохранён в {csv_filename}")
        #
        tmax=t[-1]
        energySum=np.sum(signal**2)
        filechar=(Nrec, fname, fs, tmax)
        filechar = (Nrec, fname, fs, tmax, energySum)
        filechars.append(filechar)
        # График всего сигнала
        plot_signal(t, signal, title=f"{fname} - весь сигнал")
        # Графики отдельных ударов по заранее заданным временам
        Nimp=0
        for impact in impacts:
            Nimp+=1
            if ((Nrec==1 or Nrec==3) and Nimp==1) or ((Nrec==2 or Nrec==4) and Nimp==2):
                _, t_start, t_end = impact
                plot_signal(t, signal, title=f"{fname} - удар {impact[0]}", t_start=t_start, t_end=t_end)
                #
                csv_filename = os.path.splitext(fname)[0] + "_signal_ImpactRange.csv"
                with open(csv_filename, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    #writer.writerow(["Time_s", "Signal"])
                    writer.writerow(["Time_s", "Signal", "Energy"])
                    for i in range(len(t)):
                        #writer.writerow([t[i], data[i]])
                        if t[i]>=t_start and t[i]<=t_end:
                            writer.writerow([t[i], signal[i], signal[i]*signal[i]])
                #
                print(f"Сигнал сохранён в {csv_filename}")

    with open(filePathResults+"\\"+"FileChar.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["DataID", "FileName", "tmax", "freq.discr"])
        for filechar in filechars:
            writer.writerow(filechar)
    print("FileChar.csv создан")
