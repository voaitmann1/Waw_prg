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
