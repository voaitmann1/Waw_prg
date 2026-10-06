# based on 2_2, 2_2 in 2_2 s'diqal'd
# amda es signal_sensor1 et signal_sensor2 vars - nu ne es, ma msb, nu nur try
#

from MyPyVibroLib import *

print("Step1 starts working")
print("\nThink about what impact to choose for elaboration an find its bounds\n")

def OwnNameOfFullName(fname):
    n=0
    L=len(fname)
    for i in range(L):
        li=fname[i:i+1]
        if li=="\\":
            n=i
    ownName=fname[n+1:L+1]
    return ownName

def FindCommonSegnments(segs1, segs2, dt_s=1.0, vsh=0):#meaning same impact
    NewSegs=[]
    if vsh==1:
        print("FindCommonSegnments starts working. Elements: "+str(len(segs1))+"="+str(len(segs2)))
    for i in range(1, len(segs1)+1):
        for j in range(1, len(segs2)+1):
            seg1=segs1[i-1]
            seg2=segs2[j-1]
            t11=seg1[1-1]
            t12=seg1[2-1]
            t21=seg2[1-1]
            t22=seg2[2-1]
            if vsh==1:
                print("Comparing: ["+str(t11)+","+str(t12)+"] with ["+str(t21)+","+str(t22)+"]")
            NewSeg=[]
            if np.abs(t11-t21)<dt_s and np.abs(t12-t22)<dt_s:
                #t1= t11>=t12 ? t11 : t12
                #t2= t21<=t22 ? t21 : t22
                if t11>=t21:
                    t1=t11
                else:
                    t1=t21              # sdi exta max, ors 
                if t12<=t22:
                    t2=t12
                else:
                    t2=t22
                # et hin exta min. So s'exta'd 
                #print("this: ["+str(t1)+","+str(t2)+"]")
                NewSeg.append(t1)
                NewSeg.append(t2)
                NewSegs.append(NewSeg)# Was: segs1[], segs2[]. WillBe: NewSeg[i]=[segs1[i], segs2[i]]
            else:
                #print("no")
                pass
            #
        #
    #
    if vsh==1:
        print("FindCommonSegnments finishes working")
    #
    return NewSegs

if __name__ == "__main__":# S'asal, ma qo sdi?

    dataRead=FilesData()
    #                                                                                   FolderAndFiles_1_Full.csv
    dataRead.DataOfFiles(dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+"FolderAndFiles_1_Full.csv", 1)
    #dataRead.DataOfFiles()
    print("reading file: "+dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+"FolderAndFiles_1_Full.csv")
    print(dataRead)
    #
    signal_sensor1=[]
    signal_sensor2=[]
    #
    filenames=dataRead.File
    print(filenames)
    impacts = [
        (1, 0.12, 0.45),
        (2, 1.23, 5.67)
    ]
    #
    ImpactsBoundDefMode=2 # 1 - fun ic es, 2 - new fun, am ZB dat > gut gefa r' fun 1
    #
    allSegments=[]

    print("ImpactBounds.csv создан")
    #
    do_ConvertToNpArray=True
    do_Normalize=True
    do_CreateSingleSignalFileForBothSensors=True# ! for each sensors separately both files wi abfa independently
    #
    do_ShowSeparateImpacts=True# am graph
    #
    do_DefImpactBoundsAuto=True
    #do_WriteBounds=True
    do_WriteImpactBounds=True#False
    do_WriteAllImpactsNotSingle=True # switch: 1 impact or eiq
    #do_WriteImpactBounds_AutoDef=False # noam utf'd
    #
    # Обработка каждого файла: lir .wav, lif .csv.
    energySums_allRecs=[]
    filechars_allRecs=[]
    #
    fileOwnNames=[]
    #
    if do_CreateSingleSignalFileForBothSensors:
        pass
        #creater,  
    #fileN=0
    #for fname in filenames:
    print("QFiles="+str(dataRead.QFiles))
    for fileN in range(1, dataRead.QFiles+1):
        print("fileN="+str(fileN))
        fileOwnName=dataRead.File[fileN-1]
        fileOwnNames.append(fileOwnName)
        #
        fname=dataRead.Folder+"\\"+dataRead.SubFolder_IniData+"\\"+fileOwnName+".wav"
        #fileN+=1
        #
        t, n_channels, signal, fs = read_wav_and_calc_t_1(fname, max_seconds=None)
        #
        tmax=t[-1]
        #
        signalL=len(signal)
        #for i in range(signalL):
        #    signal_nrm[i]=signal[i]/np.mean(signal)
        #writing to csv
        if n_channels==1:
            print("Single-channel")       
            #csv_filename = os.path.splitext(fname)[0] + dataRead.fileNameEnding_Signal#"_signal_whole.csv"#works well
            csv_filename = dataRead.Folder+"\\"+dataRead.SubFolder_IniData+"\\"+dataRead.File[fileN-1] + dataRead.fileNameEnding_Signal#"_signal_whole.csv"
            print("signal statistics: mean="+str(np.mean(signal))+" median="+str(np.median(signal)))
            if do_Normalize:
                #print("normalizing...")
                #for i in range(signalL):
                #    signal[i]=signal[i]-np.mean(np.array(signal))
                #    print(str(i+1)+"/"+str(signalL))
                #ce arb, ma zu long
                signal=np.array(signal)
                #signal-=np.mean(signal)
                signal-=np.median(signal)
                signal=signal.tolist()
                print("normalized")
                #
            else:
                print("normalizing turned off, initial signal elaborated")
            #
            plot_signal(t, signal, title=f"{fname} - весь сигнал (нормализация)")
            print("writing signal to "+csv_filename)
            with open(csv_filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Time_s", "Signal", "Energy"])
                for i in range(len(t)):
                    writer.writerow([t[i], signal[i], signal[i]*signal[i]])
                #
            #
            if fileN==1:
                signal_sensor1=copy.deepcopy(signal_chn)
            else:
                signal_sensor2=copy.deepcopy(signal_chn)
            #
            if fileN==1:#mab sflu/exnot
                signal_chn=copy.deepcopy(signal_sensor1)#=copy.deepcopy(signal_chn)
            else:
                signal_chn=copy.deepcopy(signal_sensor2)
            #
        elif n_channels>1:
            print("Multy-channel")
            csv_filenames_cnns=[]
            for chN in range(n_channels):
                #csv_filename = os.path.splitext(fname)[0] +"_chN"+str(chN)+dataRead.fileNameEnding_Signal#"_signal_whole.csv"#works well
                csv_filename = dataRead.Folder+"\\"+dataRead.SubFolder_IniData+"\\"+fileOwnName +"_chN"+str(chN)+dataRead.fileNameEnding_Signal#"_signal_whole.csv"
                csv_filenames_cnns.append(csv_filename)
                with open(csv_filename, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    signal_chn=signal[:,chN]#qo sdi? Os: interleaved: ch1val1, ch2val1, ch3val1, ch1val2, ch2val2, ch3val2
                    #if chN==1:
                    if chN==0:
                        signal_sensor1=copy.deepcopy(signal_chn)
                    else:
                        signal_sensor2=copy.deepcopy(signal_chn)
                    #
                    print("signal stztistics: mean="+str(np.mean(signal_chn))+" median="+str(np.median(signal_chn)))   
                    if do_Normalize:
                        print("normalizing...")
                        signal_chn=np.array(signal_chn)
                        #for i in range(signalL):
                        #    #signal_chn[i]=signal_chn[i]-np.mean(np.array(signal_chn))
                        #    signal_chn[i]=signal_chn[i]-np.mean(signal_chn)
                        #    print(str(i+1)+"/"+str(signalL))
                        #
                        #signal_chn-=np.mean(signal_chn)
                        signal_chn-=np.median(signal_chn)
                        signal_chn=signal_chn.tolist()
                        #
                        if chN==0:
                            signal_sensor1=copy.deepcopy(signal_chn)
                        else:
                            signal_sensor2=copy.deepcopy(signal_chn)
                        #
                        print("normalized")
                    else:
                        print("Nornalization is turned off")
                    #
                    if chN==0:
                        signal_chn=copy.deepcopy(signal_sensor1)
                    else:
                        signal_chn=copy.deepcopy(signal_sensor2)
                    #
                    plot_signal(t, signal_chn, title=f"{fname} channel {chN} - весь сигнал (нормализвация)")
                    #
                    writer.writerow(["Time_s", "Signal", "Energy"])
                    for i in range(len(t)):
                        writer.writerow([t[i], signal_chn[i], signal_chn[i]*signal_chn[i]])
                    #
                #
                print(f"Сигнал сохранён в {csv_filename}") # signal s'def'd, 
            #
            print("Channels divided to:")
            for fnm in csv_filenames_cnns:
                print(fnm)
            #
            if do_CreateSingleSignalFileForBothSensors:
                print("Single csv-file for all channels:")#ms'n'b do'd
                #for chN in range(n_channels):
                #elif ifMultiChannel_AllChannelsIn1File_not_1File1Channel==True:
                csv_filename = os.path.splitext(fname)[0] + dataRead.fileNameEnding_Signal#"_signal_whole.csv"
                rowHdr=[]
                rowHdr.append("Time_s")
                for chN in range(n_channels):
                    rowHdr.append("Signal_chN"+str(chN))
                    rowHdr.append("Energy_chN"+str(chN))
                #
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
                        #
                        writer.writerow(rowContent)
                    #
                #
                print(f"Сигнал сохранён в (общий) {csv_filename}")
            #end if
        #nu sha signal (ut'tbi chns, ut je chn signal[:,chN]
        #
        print(fname+" read, now plotting")
        #
        # cycle of filenames continues
        # vvv I men sn'nod vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        #fileEnding_toWrite="_signal_ImpactRange_AutoDef.csv"#"_signal_ImpactRange.csv"
        #tmax=t[-1]
        if n_channels==1:
            #energySum=np.sum(signal**2)
            energySum=np.sum(signal_chn**2)
            #signal_chn=copy.deepcopy(signal) #defined
            filechar = (fileN, fname, fs, tmax, energySum)
            energySums_allRecs.append(energySum)
            filechars_allRecs.append(filechar)
        elif n_channels>1:
            for chN in range(n_channels):#admem: os in cycle for fname!
                #signal_chn=signal_chn=signal[:,chN]
                if chN==0:
                    signal_chn=copy.deepcopy(signal_sensor1)
                else:
                    signal_chn=copy.deepcopy(signal_sensor2)
                #
                #print("bef (len(sig_ch="+str(len(signal_chn))+")")
                ##if isinstance(signal_chn ,list):
                #    print("signal_chn is list")
                #elif isinstance(signal_chn ,np.array):
                #    print("signal_chn is np.array")
                #else:
                    #print("signal_chn is neither list, nor np.array")
                 #   print("signal_chn isn't list")
                #
                signal_chn=np.array(signal_chn)
                #
                energySum=np.sum(signal_chn**2)
                #
                signal_chn=signal_chn.tolist()
                #print("aft")
                filechar = (fileN, fname, fs, tmax, energySum)
                energySums_allRecs.append(energySum)
                filechars_allRecs.append(filechar)
            #
        else:
            print("error, so can't be: 0 channels")
        #
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    
        # График всего сигнала
        if n_channels==1:
            #plot_signal(t, signal, title=f"{fname} - весь сигнал")
            plot_signal(t, signal_chn, title=f"{fname} - весь сигнал")
        elif n_channels>1:
            for chN in range(n_channels):
                #signal_chn=signal_chn=signal[:,chN]
                if chN==0:
                    signal_chn=copy.deepcopy(signal_sensor1)
                else:
                    signal_chn=copy.deepcopy(signal_sensor2)
                #
                plot_signal(t, signal_chn, title=f"{fname} channel {chN} - весь сигнал")
            #
        #
        #Графики отдельных ударов по заранее заданным временам
        if do_ShowSeparateImpacts:
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
                    #
                #
            #
        #
        # ----- Impacts Bounds! --------------------------------------------------------------------------------------------------------
        if do_DefImpactBoundsAuto: # amda def impacts auto 8888888888888888888888888888888888888888888888888888888888888888888888888888888888
            TrashBeforeT=1
            TrashAfterT=1
            vsh=0
            N0=0
            print("do_DefImpactBoundsAuto = true => finding impacts bounds")
            
            if n_channels==1:
                #sig_for_bnds=copy.deepcopy(signal)
                sig_for_bnds=copy.deepcopy(signal_chn)
                if ImpactsBoundDefMode==1:
                    #print("n_channels=1, ImpactsBoundDefMode=1")
                    peaks_time, segments = detect_impacts_segments(sig_for_bnds, fs=fs, min_distance=7, threshold_ratio=0.66)
                    #was: ne sig_for_bnds, ma signal 
                    #
                    for impN in range(1, len(peaks_time)+1):
                        if impN==2:
                            impT1=peaks_time[impN-1]
                            impT2=peaks_time[impN+1-1]
                            trashN1, trashN2 = findTrashNsAfterVibr(sig_for_bnds, fss, impT1, impT2, FindTrashMax(signal, fs, TrashBeforeT, TrashAfterT, vsh), N0, vsh)
                            trashT1=signal[trashN1-1]
                            trashT2=signal[trashN2-1]
                            print("Between impact ts = ["+str(impT1)+"..."+str(impT2)+"] there exists trash range [t1="+str(trashT1)+"... t2="+str(trashT2)+"]")
                        #
                    #
                elif ImpactsBoundDefMode==2:
                    #print("n_channels=1, ImpactsBoundDefMode=2")
                    peaks_time, segments = FindTImpactStart(sig_for_bnds, fs=fs, SectT=6, TrashBeforeT=1, TrashAfterT=1, MoreThanTrashCoef=3, vsh=0)
                    #was: ne sig_for_bnds, ma signal
                    #
                    for impN in range(1, len(peaks_time)+1):
                        if impN==2:
                            impT1=peaks_time[impN-1]
                            impT2=peaks_time[impN+1-1]
                            trashN1, trashN2 = findTrashNsAfterVibr(sig_for_bnds, fss, impT1, impT2, FindTrashMax(signal, fs, TrashBeforeT, TrashAfterT, vsh), N0, vsh)
                            trashT1=signal[trashN1-1]
                            trashT2=signal[trashN2-1]
                            print("Between impact ts = ["+str(impT1)+"..."+str(impT2)+"] there exists trash range [t1="+str(trashT1)+"... t2="+str(trashT2)+"]")
                        #
                    #
                #
                allSegments.append(segments) #ce redo 2 tids ob 2 files
            elif n_channels>1:
                if ImpactsBoundDefMode==1:
                    #print("n_channels="+str(n_channels)+", ImpactsBoundDefMode=1")
                    for chN in range(n_channels):
                        #signal_chn=signal_chn=signal[:,chN]
                        if(chN==1):
                            signal_chn=copy.deepcopy(signal_sensor1)
                        elif (chN==2):
                            signal_chn=copy.deepcopy(signal_sensor2)
                        #    
                        if do_ConvertToNpArray:
                            signal_chn=np.array(signal_chn)
                        peaks_time, segments = detect_impacts_segments(signal_chn, fs=fs, min_distance=7, threshold_ratio=0.66)
                        #
                        print("peaks: channel "+str(chN)+" peaks bounds detected: "+str(len(segments)))
                        #
                        allSegments.append(segments)#new! qvi q'arb if 1 chn
                        #
                        print("chN="+str(chN)+" len(segments)="+str(len(segments))+" len(signal_chn)="+str(len(signal_chn))+" (mode 1)")
                        print("peaks_time", peaks_time)
                    #
                elif ImpactsBoundDefMode==2:
                    #print("n_channels="+str(n_channels)+", ImpactsBoundDefMode=2")
                    for chN in range(n_channels):
                        #signal_chn=signal_chn=signal[:,chN]
                        if(chN==1):
                            signal_chn=copy.deepcopy(signal_sensor1)
                        elif (chN==2):
                            #signal_chn=copy.deepcopy(signal_sensor2)
                            signal_chn=signal_chn=signal[:,chN]
                        # 
                        peaks_time, segments = FindTImpactStart(signal_chn, fs=fs, SectT=6, TrashBeforeT=1, TrashAfterT=1, MoreThanTrashCoef=3, vsh=1)
                        #
                        print("peaks: channel "+str(chN)+" peaks bounds detected: "+str(len(segments)))
                        #
                        allSegments.append(segments)#new! iqv q'arb if 1 chn #ce redo 2 tids ob 1 file, ma 2 chns
                        #
                        print("chN="+str(chN)+" len(segments)="+str(len(segments))+" len(signal_chn)="+str(len(signal_chn))+" (mode 2)")
                        print("peaks_time", peaks_time)
                    #
                else:
                    pass
                
                    #print("another varianrt")
                #
            #-------------------------------------------------------------------------
            print("Bounds")# var segments, list of 2 elts
            for seg in segments:
                print(str(seg[1-1])+"..."+str(seg[2-1]))
            #-------------------------------------------------------------------------
            print("len(allSegments)="+str(len(allSegments)))
            j=0
            for aSeg in allSegments:
                j+=1
                print("len(aSeg)["+str(j)+"]="+str(len(aSeg)))
            #
            
            #
            for chnN in range(n_channels):
                #signal_chn=signal[:,chnN]
                if chN==0:
                    signal_chn=copy.deepcopy(signal_sensor1)
                else:
                    signal_chn=copy.deepcopy(signal_sensor2)
                #
                #
                ymin, ymax = np.min(signal), np.max(signal) # plot impact bounds # 8888888888888888888888888888888888888888888888888888888888
                for seg in segments:
                    start, end = seg
                    plt.vlines([start, end], ymin, ymax, colors="r", linestyles="--")
                #
                plt.xlabel("Время t, с")
                plt.ylabel("Амплитуда ")
                plt.title(f"Сигнал с разделительными линиями сегментов File: {fileOwnNames[chnN-1]}")
                plt.plot(t, signal_chn)#signal ablb maq-dim arr. If so, plt.plot int ce et plot in idy CS l'curves ot dims! Et uz tic utas -show impact bnds - os norm
                plt.legend()
                plt.grid(True)
                plt.show()
                #
            #                    
            ymin, ymax = np.min(signal), np.max(signal) # plot impact bounds # 8888888888888888888888888888888888888888888888888888888888
            for seg in segments:
                start, end = seg
                plt.vlines([start, end], ymin, ymax, colors="r", linestyles="--")
            #
            plt.xlabel("Время, с")
            plt.ylabel("Амплитуда")
            plt.title(f"Сигнал с разделительными линиями сегментов {fileOwnNames[fileN-1]}")
            plt.plot(t, signal)#signal ablb maq-dim arr. If so, plt.plot int ce et plot in idy CS l'curves ot dims! Et uz tic utas -show impact bnds - os norm
            plt.legend()
            plt.grid(True)
            plt.show()
            #        elaboratedImpactN
        else:#if do_DefImpactBoundsAuto
            print("do_DefImpactBoundsAuto = false")
        #
    # for - as for fname in filenames ----------------------------------------------------------------------------------------
    
    print("fileOwnNames: ", fileOwnNames)# nu neved nam o'var!!
    print("energySum: ", energySums_allRecs)
    
    print("files and data rows: "+str(len(allSegments))) #

    if do_DefImpactBoundsAuto and len(allSegments)==2:
        print("cond to elaborate segms")
        #dt_s=1.01
        segs1=allSegments[1-1]
        segs2=allSegments[2-1]
        print("len(allSegments)="+str(len(allSegments))+" len(segs1)="+str(len(segs1))+" len(segs2)="+str(len(segs2)))
        #
        segsNew=FindCommonSegnments(segs1, segs2, dt_s=0.8, vsh=1)
        if len(segsNew)>0:
            print("Рекомендуемые диапазоны:")
            for i in range(len(segsNew)): 
                seg=segsNew[i]
                t1=seg[1-1]
                t2=seg[2-1]
                print(str(t1)+" ... "+str(t2))
            #
        else:
            print("segsNew: не найдены")
        #
    else:
        print("No cond to elaborate segms")
    #
    impacts=[]
    tsOfImpact=[]
    impactsQ=len(segsNew)
    print("len(segsNew)="+str(impactsQ))
    for i in range(impactsQ):
        seg=segsNew[i]
        t1=seg[1-1]
        t2=seg[2-1]
        #tsOfImpact=[]
        #tsFin=[]
        tsFin=[t2, t2]
        tsOfImpact=[t1, tsFin]
        tsOfImpact.append(seg)
        impact=[i, tsOfImpact]
        impacts.append(impact)
    #
    
    if do_WriteImpactBounds:
        pathBounds=dataRead.SubFolder_IntermediateData+"\\"+dataRead.File[0]+dataRead.fileNameEnding_ImpactBounds
        print("writing file of impacts bounds "+pathBounds)#2 names ac exts + _ImpactsRanges"+".csv"
        impactsQ=len(impacts)
        print("impactsQ="+str(impactsQ))
        elaboratedImpactN=0
        #with open(filePathResults+"\\"+fileEnding_toWriteImpactBounds, mode='w', newline='') as f:
        with open(pathBounds, mode='w', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(["impactN", "tStart", "tFin1", "tFin2"])#2026-07-28
            writer.writerow(["impactN", "tStart", "tFin"])
            print("do_WriteAllImpactsNotSingle="+str(do_WriteAllImpactsNotSingle))
            if do_WriteAllImpactsNotSingle:
                #for impact in impacts:
                impactsQ=len(impacts)
                print("__impactsQ="+str(impactsQ)) # S lir 0
                for impact in impacts:
                    print("impact: ", impact)
                    elaboratedImpactN+=1
                    #impactN=impact[1-1] # mut r'ef v
                    impactN=elaboratedImpactN
                    #print("impactN=",impactN)
                    tsOfImpact=impact[2-1] # mut r'ef v
                    tStart, tsFin= tsOfImpact # mut r'ef v
                    if len(tsFin)==2:
                        tFin1=tsFin[1-1]
                        tFin2=tsFin[2-1]
                    elif len(tsFin)==1 or tsFin[2-1]==0:
                        tFin1=tsFin[1-1]
                        tFin2=tFin1
                    elif len(tsFin)==0:
                        if(impactN==impactsQ):
                            tFin1=tmax-2-dt
                            tFin2=tFin1
                        else:
                            tFin1=impacts[elaboratedImpactN+1-1][1-1]-dt#mut r'ef v
                            tFin2=tFin1
                        #
                    #
                    print("impactN="+str(impactN)+" tStart="+str(tStart)+" tFin1="+str(tFin1)+" tFin2="+str(tFin2))
                    writer.writerow([str(impactN), str(tStart), str(tFin1), str(tFin2)])
                #for
            else:
                writer.writerow([str(1), str(ImpLB), str(ImpHB), str(ImpHB)])
                print("1) ImpLB="+str(ImpLB)+" ImpHB="+str(ImpHB)+" ImpHB="+str(ImpHB))
            #
        #
    #
            
print("Step1 finishes working")

