from MyPyVibroLib import *

print("Step1 starts working")

def OwnNameOfFullName(fname):
    n=0
    L=len(fname)
    for i in range(L):
        li=fname[i:i+1]
        if li=="\\":
            n=i
    ownName=fname[n+1:L+1]
    return ownName

def FindCommonSegnments(segs1, segs2, dt_s=1.0):
    NewSegs=[]
    for i in range(1, len(segs1)+1):
        for j in range(1, len(segs2)+1):
            seg1=segs1[i-1]
            seg2=segs2[j-1]
            t11=seg1[1-1]
            t12=seg1[2-1]
            t21=seg2[1-1]
            t22=seg2[2-1]
            #print("Comparing: ["+str(t11)+","+str(t12)+"] with ["+str(t21)+","+str(t22)+"]")
            NewSeg=[]
            if np.abs(t11-t21)<dt_s and np.abs(t12-t22)<dt_s:
                #t1= t11>=t12 ? t11 : t12
                #t2= t21<=t22 ? t21 : t22
                if t11>=t21:
                    t1=t11
                else:
                    t1=t21
                if t12<=t22:
                    t2=t12
                else:
                    t2=t22
                #print("this: ["+str(t1)+","+str(t2)+"]")
                NewSeg.append(t1)
                NewSeg.append(t2)
                NewSegs.append(NewSeg)
            else:
                #print("no")
                pass
    return NewSegs

if __name__ == "__main__":

    PathToNamesFile="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"
    fileOwnNames=[]
    with open(PathToNamesFile+"\\FolderAndFiles.csv", newline='') as f:
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
            elif LineN>2:
                #fileOwnNames.append(row[2-1]+".csv")
                fileOwnNames.append(row["Value"]+".wav")

    print("Must work with")
    print("path: C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav")
    print("files: 051_1_M.wav, 051-2.wav")
    print("Working with:")
    print("path: "+filePath)
    print("Files: "+str(QFiles))
    for i in range(QFiles):
        print(fileOwnNames[i])
    
    #fileOwnNames=["051_1_M.wav", "051-2.wav", "052-1.wav", "052-2.wav"]
    #filePath="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav"
    filePathIniData=filePath+"\\"+"data"#+"\\"+"IniData"
    filePathResults=filePath+"\\"+"data"#+"\\"+"Results"
    filePathData=filePath+"\\"+"data"
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
    allSegments=[]
    #
    filechars=[]
    # Сохраняем ImpactBounds в CSV
    with open(filePathResults+"\\"+"ImpactBounds.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ImpactID", "StartTime_s", "EndTime_s"])
        for impact in impacts:
            writer.writerow(impact)

    print("ImpactBounds.csv создан")
    do_DefImpactBoundsAuto=True
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
                
        print(f"Сигнал сохранён в {csv_filename}")
        #
        fileEnding_toWrite="_signal_ImpactRange_AutoDef.csv"#"_signal_ImpactRange.csv"
        do_WriteImpactBounds_AutoDef=False
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
                if do_WriteImpactBounds_AutoDef:
                    csv_filename = os.path.splitext(fname)[0] + fileEnding_toWrite
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
                #
            #
        #
        if do_DefImpactBoundsAuto:
            #
            peaks_time, segments = detect_impacts_segments(signal, fs=fs, min_distance=7, threshold_ratio=0.66)
            #
            allSegments.append(segments)
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
            #        
        #if do_DefImpactBoundsAuto
    #

    with open(filePathData+"\\"+"FileChar.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(["DataID", "FileName", "tmax", "freq.discr"])
        writer.writerow(fileCharsHeadersRow)#see in MyPyVibroLib
        for filechar in filechars:
            writer.writerow(filechar)
            Nrec, fname, fs, tmax, energySum=filechar
            print(str(Nrec)+" "+OwnNameOfFullName(fname)+" : tmax ="+str(tmax))
    print("FileChar.csv создан")

    #if do_DefImpactBoundsAuto:
    #    print("do_DefImpactBoundsAuto: ON")
    #else:
    #    print("do_DefImpactBoundsAuto: OFF")

    print("files and data rows: "+str(len(allSegments)))

    if do_DefImpactBoundsAuto and len(allSegments)==2:
        dt_s=1.01
        segs1=allSegments[1-1]
        segs2=allSegments[2-1]
        segsNew=FindCommonSegnments(segs1, segs2, 0.8)
        if len(segsNew)>0:
            print("Рекомендуемые диапазоны:")
            for i in range(len(segsNew)):
                seg=segsNew[i]
                t1=seg[1-1]
                t2=seg[2-1]
                print(str(t1)+" ... "+str(t2))
        else:
            print("не найдены")
            
print("Step1 finishes working")
