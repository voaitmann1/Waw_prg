from MyPyVibroLib import *

if __name__ == "__main__":
    fileOwnNames=["051_1_M.wav", "051-2.wav", "052-1.wav", "052-2.wav"]
    filePath="D:\\MyFilesCur\\MyPrgs\\Python\\Wav"
    filePathIniData=filePath+"\\"+"assets"#+"\\"+"IniData"
    filePathResults=filePath+"\\"+"assets"#+"\\"+"Results"
    filenames =[]
    for fileOwnName in fileOwnNames:
        fname=filePathIniData+"\\"+fileOwnName
        filenames.append(fname)
    
    filechars=[]
    #segments
    
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
            writer.writerow(signalFileHeader)
            for i in range(len(t)):
                #writer.writerow([t[i], data[i]])
                writer.writerow([t[i], signal[i], signal[i]*signal[i]])
            #
        #
        print(f"Сигнал сохранён в {csv_filename}")
        #
        tmax=t[-1]
        #print("dt="+"=t1-t0="+str(t[1]-t[plot_signal(t, signal, title="Сигнал", t_start=None, t_end=None)0])+"=tLast-tPreLast="+str(t[-1]-t[-2])+"=1/n="+str(1/fs))#ja,idq vals, ce arb
        energySum=np.sum(signal**2)
        filechar=(Nrec, fname, fs, tmax)
        filechar = (Nrec, fname, fs, tmax, energySum)
        filechars.append(filechar)
        #
        peaks_time, segments = detect_impacts_segments(signal, fs=fs, min_distance=7, threshold_ratio=0.66)
        #
        print("Bounds")
        for seg in segments:
            print(str(seg[1-1])+"..."+str(seg[2-1]))
        #
        #writing impact bounds to csv
        csv_filename = os.path.splitext(fname)[0] + "_segments_bounds.csv"
        with open(csv_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(impactRangesHeadersRow)
            writer.writerows(segments)
        #
        print(f"Переменные границы сохранёны в {csv_filename}")

        
        ymin, ymax = np.min(signal), np.max(signal)
        for seg in segments:
            start, end = seg
            plt.vlines([start, end], ymin, ymax, colors="r", linestyles="--")

        plt.xlabel("Время, с")
        plt.ylabel("Амплитуда")
        plt.title(f"Сигнал с разделительными линиями сегментов {fileOwnNames[Nrec-1]}")
        plt.plot(t, signal)
        plt.legend()
        plt.grid(True)
        plt.show()

        #if Nrec==1:
        #freqs, amps= spectrum_dft(signal, fs, use_window=False)
        freqs, amps= spectrum_fft(signal, fs, use_window=True)
        
        plt.xlabel("Частота, Гц")
        plt.ylabel("Амплитуда")
        plt.title(f"Спектр сигнала {fileOwnNames[Nrec-1]}")
        plt.plot(freqs, amps)
        plt.legend()
        plt.grid(True)
        plt.show()

        #def spectrum_fft(x, fs=1000, use_window=False, use_mean=False, use_detrend=False)
        freqs, amps= spectrum_fft(signal, fs, use_window=True, use_mean=True, use_detrend=True)

        plt.xlabel("Частота, Гц")
        plt.ylabel("Амплитуда")
        plt.title(f"Спектр сигнала (corrected) {fileOwnNames[Nrec-1]}")
        plt.plot(freqs, amps)
        plt.legend()
        plt.grid(True)
        plt.show()
    #    
    
    with open(filePathResults+"\\"+"FileChar.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fileCharsHeadersRow)
        for filechar in filechars:
            writer.writerow(filechar)
    print("FileChar.csv создан")

#--------------------------------------------------------------------------------


    
