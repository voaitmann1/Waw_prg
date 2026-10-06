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

def FindCommonSegnments(segs1, segs2, dt_s=1.0):#meaning same impact
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

if __name__ == "__main__":#qo sdi?

    PathToNamesFile="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"
    fileOwnNames=[]
    #with open(PathToNamesFile+"\\FolderAndFiles.csv", newline='') as f:
    #    reader = csv.DictReader(f)
    #    LineN=0
    #    for row in reader:
    #        LineN+=1
    #        if LineN==1:
    #            #filePath=row[2-1]
    #            filePath=row["Value"]
    #        elif LineN==2:
    #            #QFiles=int(row[2-1])
    #            QFiles=int(row["Value"])
    #        elif LineN>2:
    #            #fileOwnNames.append(row[2-1]+".csv")
    #            fileOwnNames.append(row["Value"]+".wav")
    #        else:
    #            QBefore=2#filePath and QFiles
    #            QForSnglFile=2#File name and Q channels
    #            SubN=LineN-QBefore)%QForSnglFile
    #            if SubN==0:
    #                SubN=QForSnglFile
    #            FileN=(LineN-QBefore+SubN)/QForSnglFile
    #            if SubN==1:#filename
    #                fname=row["Value"]
    #                fileOwnNames.append(fname+".wav")
    #                print("LineN "+str(LineN)+" File N "+str(FileN)+" file name: "+fname)
    #            elif SubN==QForSnglFile:#factic 2 - QChannels
    #                n_channel=int(row["Value"])
    #                print("LineN "+str(LineN)+" File N "+str(FileN)+" channels: "+str(n_channel))
    #            #
    #        #
    #    #
    ##
    filePath, QFiles, fileOwnNames, channels =  read_csv_of_files_and_channels(PathToNamesFile+"\\"+"FolderAndFiles.csv")              
    
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
        fname=filePathIniData+"\\"+fileOwnName # os fname - fullname =path + own name ab FolderAndFiles.csv
        filenames.append(fname)
    
    # Времена ударов задаются вручную
    # ImpactID, StartTime_s, EndTime_s
    impacts = [
        (1, 0.12, 0.45),
        (2, 1.23, 5.67)
    ]
    #
    #ifMultiChannel_AllChannelsIn1File_not_1File1Channel=True
    #
    allSegments=[]
    #
    #filechars=[]filechars_allRecs
    #
    # Сохраняем ImpactBounds в CSV
    with open(filePathResults+"\\"+"ImpactBounds.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ImpactID", "StartTime_s", "EndTime_s"])
        for impact in impacts:
            writer.writerow(impact)

    print("ImpactBounds.csv создан")
    
    do_DefImpactBoundsAuto=True
    # Обработка каждого файла
    energySums_allRecs=[]
    filechars_allRecs=[]
    fileN=0
    for fname in filenames:
        fname+=".wav"#new
        fileN+=1
        #reading wav
        #t, signal, fs = read_wav_and_calc_t(fname)# here !
        #fs, n_channels, data = read_wav_safe_2(fname, max_seconds=None, channel=None)
        t, n_channels, signal, fs = read_wav_and_calc_t_1(fname, max_seconds=None)
        #writing to csv
        if n_channels==1:
            #fileN+=1
            print("Single-channel")       
            csv_filename = os.path.splitext(fname)[0] + "_signal_whole.csv"
            with open(csv_filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                #writer.writerow(["Time_s", "Signal"])
                writer.writerow(["Time_s", "Signal", "Energy"])
                for i in range(len(t)):
                    #writer.writerow([t[i], data[i]])
                    writer.writerow([t[i], signal[i], signal[i]*signal[i]])
        elif n_channels>1:
            print("Multy-channel")
            #if ifMultiChannel_AllChannelsIn1File_not_1File1Channel==False:
            csv_filenames_cnns=[]
            for chN in range(n_channels):
                #csv_filenameударов = os.path.splitext(fname)[0] +"_channelN"+str(chN)+"_signal_whole.csv"#wa so!
                #csv_filename = os.path.splitext(fname)[0] +"_channelN"+str(chN)+"_signal_whole.csv"
                csv_filename = os.path.splitext(fname)[0] +"_chN"+str(chN)+"_signal_whole.csv"
                csv_filenames_cnns.append(csv_filename)
                with open(csv_filename, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    #print("csv_filename="+csv_filename+" hope is open")
                    signal_chn=signal[:,chN]#qo sdi? Os: interleaved: ch1val1, ch2val1, ch3val1, ch1val2, ch2val2, ch3val2
                    writer.writerow(["Time_s", "Signal", "Energy"])
                    for i in range(len(t)):
                        writer.writerow([t[i], signal_chn[i], signal_chn[i]*signal_chn[i]])
                print(f"Сигнал сохранён в {csv_filename}")
            print("Channels divided to:")
            for fnm in csv_filenames_cnns:
                print(fnm)
            print("Single csv-file for all channels:")#ms'n'b do'd
            #for chN in range(n_channels):
            #elif ifMultiChannel_AllChannelsIn1File_not_1File1Channel==True:
            csv_filename = os.path.splitext(fname)[0] +"_signal_whole.csv"
            rowHdr=[]
            rowHdr.append("Time_s")
            for chN in range(n_channels):
                rowHdr.append("Signal_chN"+str(chN))
                rowHdr.append("Energy_chN"+str(chN))
            with open(csv_filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(rowHdr)
                for i in range(len(t)):
                    rowContent=[]
                    rowContent.append(t[i])
                    for chN in range(n_channels):
                        signal_chn=signal[:,chN]
                        signal_sngl=signal_chn[i]
                        rowContent.append(signal_sngl)
                        rowContent.append(signal_sngl*signal_sngl)
                    writer.writerow(rowContent)
                
        print(f"Сигнал сохранён в (общий) {csv_filename}")
        #
        fname=fname[:-4]#new#ASs V see tic nam n'vikt ob n'utf'd, filename utf'tc further, ma atal var.
        #
        print(fname+" read, now plotting")
        #
        # cycle of filenames continues
        #
        fileEnding_toWrite="_signal_ImpactRange_AutoDef.csv"#"_signal_ImpactRange.csv"
        do_WriteImpactBounds_AutoDef=False
        #
        tmax=t[-1]
        #fs 1 uz all channels
        if n_channels==1:
            energySum=np.sum(signal**2)
            #filechar=(fileN, fname, fs, tmax)
            signal_chn=copy.deepcopy(signal)
            filechar = (fileN, fname, fs, tmax, energySum)
            #filechars.append(filechar)
            energySums_allRecs.append(energySum)
            filechars_allRecs.append(filechar)
        elif n_channels>1:
            #energySums_allRecs=[]
            #filechars_allRecs=[]
            for chN in range(n_channels):#admem: os in cycle for fname!
                signal_chn=signal_chn=signal[:,chN]
                energySum=np.sum(signal_chn**2)
                filechar = (fileN, fname, fs, tmax, energySum)
                energySums_allRecs.append(energySum)
                filechars_allRecs.append(filechar)
        else:
            print("error, so can't be: 0 channels")
            
        # График всего сигнала
        if n_channels==1:
            plot_signal(t, signal, title=f"{fname} - весь сигнал")
        elif n_channels>1:
            for chN in range(n_channels):
                signal_chn=signal_chn=signal[:,chN]
                plot_signal(t, signal_chn, title=f"{fname} channel {chN} - весь сигнал")
        # Графики отдельных ударов по заранее заданным временам
        Nimp=0
        for impact in impacts:
            Nimp+=1
            if ((fileN==1 or fileN==3) and Nimp==1) or ((fileN==2 or fileN==4) and Nimp==2):
                _, t_start, t_end = impact
                if n_channels==1:
                    plot_signal(t, signal, title=f"{fname} - удар {impact[0]}", t_start=t_start, t_end=t_end)
                elif n_channels>1:
                    for chN in range(n_channels):
                        signal_chn=signal_chn=signal[:,chN]
                        plot_signal(t, signal_chn, title=f"{fname} channel {chN} - удар {impact[0]}", t_start=t_start, t_end=t_end)
                    
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
            if n_channels==1:
                peaks_time, segments = detect_impacts_segments(signal, fs=fs, min_distance=7, threshold_ratio=0.66)
            elif n_channels>1:
                for chN in range(n_channels):
                    signal_chn=signal_chn=signal[:,chN]
                    peaks_time, segments = detect_impacts_segments(signal_chn, fs=fs, min_distance=7, threshold_ratio=0.66)
            #
            allSegments.append(segments)
            #
            print("Bounds")
            for seg in segments:
                print(str(seg[1-1])+"..."+str(seg[2-1]))
            #
            #writing impact bounds to csv
            csv_filename = os.path.splitext(fname)[0] + "_segments_bounds.csv" #fname = 
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
            plt.title(f"Сигнал с разделительными линиями сегментов {fileOwnNames[fileN-1]}")
            plt.plot(t, signal)#signal ablb maq-dim arr. If so, plt.plot int ce et plot in idy CS l'curves ot dims! Et uz tic utas -show impact bnds - os norm
            plt.legend()
            plt.grid(True)
            plt.show()
            #        
        #if do_DefImpactBoundsAuto
    #for fname in filenames
    
    #-------------------------------------------------------------------------------
    with open(filePathData+"\\"+"FileChar.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(["DataID", "FileName", "tmax", "freq.discr"])
        writer.writerow(fileCharsHeadersRow)#see in MyPyVibroLib
        #for filechar in filechars:
        for filechar in filechars_allRecs:
            # musb QChannels in filechar et rec musb uz je channel
            writer.writerow(filechar)
            fileN, fname, fs, tmax, energySum=filechar
            print(str(fileN)+" "+OwnNameOfFullName(fname)+" : tmax ="+str(tmax))
    print("FileChar.csv создан")
    #--------------------------------------------------------------------------------
    #print("fileOwnNames: ", fileOwnNames)
    #print("energySum: ", energySums_allRecs)
    #with open(filePathData+"\\"+"FileChar.csv", mode='w', newline='') as f:
    #    writer = csv.writer(f)
    #    writer.writerow(fileCharsHeadersRow)#see in MyPyVibroLib#writer.writerow(["DataID", "FileName", "tmax", "freq.discr"])
    #    recN=0
    #    #sha data: filePath, QFiles, fileOwnNames, channels
    #    for fileN in range(1, QFiles+1):
    #        if channels[fileN-1]==1:
    #            recN+=1
    #            fileOwnName=fileOwnNames[fileN-1]
    #            #fname=filePath+"\\"+fileOwnName
    #            fname=fileOwnName
    #            energySum=energySums_allRecs[recN-1]
    #            filechar=filechars_allRecs[recN-1]
    #            fileN, fname, fs, tmax, energySum=filechar#os exta data ab filechar ut lif, ma n'calc l'filechar!
    #            fname=OwnNameOfFullName(fname)#ob fname was ab Fuilechar, qam S'fullName
    #            filechar=(recN, fname, fs, tmax, energySum)
    #            writer.writerow(filechar)
    #            #print(str(recN)+" "+OwnNameOfFullName(fname)+" : tmax ="+str(tmax))
    #            #print("recN "+str(recN)+" fileN "+str(fileN)+" "+OwnNameOfFullName(fname)+" : tmax ="+str(tmax))
    #            print("recN "+str(recN)+" fileN "+str(fileN)+" "+OwnNameOfFullName(fname)+" : tmax ="+str(tmax))
    #        elif channels[fileN-1]>1:
    #            for chN in range(1, n_channels+1):
    #                recN+=1
    #                fileOwnName=fileOwnNames[fileN-1]
    #                #fname=filePath+"\\"+fileOwnName+"channelN"+str(chN-1)
    #                #fname=fileOwnName+"channelN"+str(chN-1)
    #                energySum=energySums_allRecs[recN-1]
    #                filechar=filechars_allRecs[recN-1]
    #                fileN, fname, fs, tmax, energySum=filechar#os exta data ut lif, ma n'calc l'filechar!
    #                #fname=filePath+"\\"+fname+"_chN"+str(chN-1)
    #                #fname=fname+"_chN"+str(chN-1)
    #                fname=OwnNameOfFullName(fname)+"_chN"+str(chN-1)#ob fname was ab Fuilechar, qam S'fullName
    #                filechar=(recN, fname, fs, tmax, energySum)
    #                writer.writerow(filechar)
    #                #print("recN "+str(recN)+" fileN "+str(fileN)+" "+OwnNameOfFullName(fname)+" : tmax ="+str(tmax))
    #                print("recN "+str(recN)+" fileN "+str(fileN)+" "+OwnNameOfFullName(fname)+" : tmax ="+str(tmax))
    #              
    #print("FileChar.csv создан")
    #--------------------------------------------------------------------------------
                
            
        #with open(filePathData+"\\"+"FileChar.csv", mode='w', newline='') as f:
        #    writer = csv.writer(f)
        #    #writer.writerow(["DataID", "FileName", "tmax", "freq.discr"])
        #    writer.writerow(fileCharsHeadersRow)#see in MyPyVibroLib
        #    for filechar in filechars:
        #        # musb QChannels in filechar et rec musb uz je channel
        #        writer.writerow(filechar)
        #        fileN, fname, fs, tmax, energySum=filechar
        #        print(str(fileN)+" "+OwnNameOfFullName(fname)+" : tmax ="+str(tmax))
        #print("FileChar.csv создан")
        #print("FileChar.csv is NOT создан yet, ob filechar in filechars must be formed considering channels, zb add QChannels or form spec files uz je channel")

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
