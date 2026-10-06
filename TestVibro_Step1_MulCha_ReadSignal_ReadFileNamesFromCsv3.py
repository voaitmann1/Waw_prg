# based on 2_3, 2_3 in 2_3 s'diqal'd
# atal str, ic mus uz 1 et 2 files et sensors arb, utce same str tbi uz channels et files
# FindCommonSegmentLists Tam wa sflu/exnot li 'n' in to name, amda S'corr'd, ver 
#

from MyPyVibroLib import *
from MyLib1 import *

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
#

def FindCommonSegmentLists(segs1, segs2, dataRead, dt_s=1.0, vsh=0):
    NewSegs=[]
    NewSeg=[]
    tss11=[]
    tss12=[]
    tss21=[]
    tss22=[]
    tss1=[]
    tss2=[]
    Ns2=[]
    fs=dataRead.fs[0]
    dt=1/fs
    if vsh==1:
        print("FindCommonSegmentLists starts working. Elements: "+str(len(segs1))+"="+str(len(segs2)))
    #
    if isinstance(segs1, list) and len(segs1)>0 and (segs2==[] or not isinstance(segs2, list)):
        NewSegs=copy.deepcopy(segs1)
        if vsh==1:
            print("FindCommonSegmentLists starts working. Segments - only set 1")
        #
    elif isinstance(segs2, list) and len(segs2)>0 and (segs1==[] or not isinstance(segs1, list)):
        NewSegs=copy.deepcopy(segs2)
        if vsh==1:
            print("FindCommonSegmentLists starts working. Segments - only set 2")
        #
    elif isinstance(segs1, list) and len(segs1)>0 and isinstance(segs2, list) and len(segs2)>0:
        L1=len(segs1)
        L2=len(segs2)
        if vsh==1:
            print("choosing from sets of "+str(L1)+" and "+str(L2)+" elements")
            print("segs1:")
            print(segs1)
            print("segs2:")
            print(segs2)
        #
        for N1 in range(1, L1+1):
            t11=segs1[N1-1][1-1]
            tss11.append(t11)
            t12=segs1[N1-1][2-1]
            tss12.append(t12)
        #
        if vsh==1:
            print("tss11")
            print(tss11)
            print("tss12")
            print(tss12)
        #
        for N2 in range(1, L2+1):
            t21=segs2[N2-1][1-1]
            tss21.append(t21)
            t22=segs2[N2-1][2-1]#t22=segs1[N2-1][2-1]
            tss22.append(t22)
        #
        if vsh==1:
            print("tss21")
            print(tss21)
            print("tss22")
            print(tss22)
        #
        tss1=copy.deepcopy(tss11)
        tss2=copy.deepcopy(tss12)
        if vsh==1:
            print("At first - set 1:")
            for N1 in range(1, L1+1):
                t1=tss11[N1-1]
                t2=tss12[N1-1]
                print(str(t1)+"..."+str(t2))
            #
            print("Analyzing set 2 step by step:")
        #
        for N2 in range(1, L2+1):
            if isInArray(Ns2, N2)==False:
                t21=tss21[N2-1]
                t22=tss22[N2-1]
                Poss1=valIsAtPos(tss1, t21, vsh=0)
                Poss2=valIsAtPos(tss1, t22, vsh=0)
                if vsh==1:
                    print("At first - set 1:")
                    print("t21="+str(t21)+"... t22="+str(t22))
                    if(Poss1.isLess):
                        print("t21 is before first: t21="+str(t21)+" t11="+str(tss1[1-1]))
                    elif (Poss1.equalNN>0):
                        print("t21 already present ")
                    elif  (Poss1.lessNN>0):
                        print("t21="+str(t21)+" is between "+str(tss1[Poss1.lessNN-1])+" and "+str(tss1[Poss1.lessNN+1-1]))
                    elif Poss1.isGreater:
                        print("t21="+str(t21)+" is greater than last t11="+str(tss1[L1-1]))
                    #
                    if(Poss2.isLess):
                        print("t21 is before first: t22="+str(t22)+" t11="+str(tss1[1-1]))
                    elif Poss2.equalNN>0:
                        print("t22 is equal to one of t1: t22="+str(t22)+" t1E="+str(tss1[Poss2.equalNN-1]))
                    elif Poss2.lessNN>0:
                        print("t22 is less than one off t1: t22="+str(t22)+" t1E="+str(tss1[Poss2.lessNN-1]))
                    elif Poss2.isGreater:
                        print("t21="+str(t21)+" is greater than last t11="+str(tss1[L1-1]))
                    #
                #
                if vsh==1:
                    print("Analyzing set 2 step by step:")
                #
                if Poss2.equalNN>0:#t11==t21
                    if(Poss2.lessNN==Poss1.lessNN):#norm case: t11<t22<(t11 next)
                        t12=tss2[Poss1.lessNN-1]
                        if vsh==1:
                            print("t21="+str(t21)+"  and t22="+str(t22)+" are both less than same t1="+str(tss1[Poss1.lessNN-1]))
                        #
                        if t22<t12:
                            tss2[Poss1.lessNN-1]=t22
                            if vsh==1:
                                print("t22="+str(t22)+"<t12="+str(t12)+" - so now t1="+str(tss1[Poss1.lessNN-1])+" t2="+str(tss2[Poss1.lessNN-1]))
                        #else remain val
                        elif Poss2.lessNN>Poss1.lessNN:#t22>=(t11 next)
                            if vsh==1:
                                print("Poss2.lessNN="+str(Poss2.lessNN)+" = "+" Poss1.lessNN="+str(Poss1.lessNN)+" - doing nothing")
                            #
                            #pass#vals remain: t12<t22
                        #
                    #
                    Ns2.append(N2)
                elif(Poss1.lessNN>0):
                    t11=tss1[Poss1.lessNN-1]
                    if vsh==1:
                        print("t21="+str(t21)+" ios greater than nearest less t11="+str(t11))
                    #if t21<=t11:
                    if abs(t21-t11)<dt_s:#same
                        tss1[Poss1.lessNN-1]=t21
                        if vsh==1:
                            print("t21 ="+str(t21)+" is somewhat less, but approximately equal to existing: t11="+str(t11))
                        #
                        Poss2=valIsAtPos(tss1, t22, vsh=0)#if it is motre
                        if(Poss2.lessNN==Poss1.lessNN):#norm case: t11<t22<(t11 next)
                            if vsh==1:
                                print("t22 ="+str(t22)+" is also less than t11="+str(t11)+" as t21="+str(t21))
                            #
                            t12=tss12[Poss1.lessNN-1]
                            if t22<t12:
                                tss2[Poss1.lessNN-1]=t22
                                if vsh==1:
                                    print("t22 ="+str(t22)+" <t12="+str(t12)+" -correcting existing t2="+str(tss2[Poss1.lessNN-1]))
                                #
                            #
                            #else remain val
                        elif Poss2.lessNN>Poss1.lessNN:#t22>=(t11 next)
                            if vsh==1:
                                print("t21 is greater than t1 N"+str(Poss1.lessNN)+" which is "+str(tss1[Poss1.lessNN])+" and t22 is greatrer than greaterr than t11 byt N"+str(Poss2.lessNN)+" which is "+str(tss1[Poss2.lessNN-1])+" - remaining old")
                            #
                            #pass#vals remain: t12<t22
                        #
                    else:# t11 and t21 are diffterent, no tss1 vals equal to t21
                        if vsh==1:
                            print("t21="+str(t21)+" is between t11="+str(tss1[Poss1.lessNN-1])+" and t11="+str(Poss1.lessNN+1-1)+" - adding to list")
                        #
                        arr1DComparableInsByOrder(tss1, t21)#inserted t21 at NN Poss1.lessNN+1-1
                        if t22>tss1[Poss1.lessNN+1-1]: #tss1[Poss1.lessNN-1] is nearest less than t21, t21 and t22 must be less than tss1[Poss1.lessNN+1-1]
                            arr1DComparableInsByOrder(tss2, (tss11[Poss1.lessNN-1]-dt))# using t12 ob t22 is incorrect
                            if vsh==1:
                                print("second bound is NOT adequatre - adding stasrt of next boundx="+str(tss11[Poss1.lessNN-1]-dt))
                            #
                        else:
                            arr1DComparableInsByOrder(tss2, t22)
                            if vsh==1:
                                print("second bound is adequatre - adding t22="+str(t22))
                            #
                        #
                    #
                    Ns2.append(N2)
                #
            #if N2 ns'in Ns2                
        #for N2
        L1new=len(tss1)
        for N1 in range(1, L1new+1):
            NewSeg=[]
            t11=tss1[N1-1]#t11=tss11[N1-1]
            NewSeg.append(t11)
            t12=tss2[N1-1]#t12=tss12[N1-1]
            NewSeg.append(t12)
            NewSegs.append(NewSeg)
        #
    if vsh==1:
        for segment in NewSegs:
            print(str(segment[1-1])+"..."+str(segment[2-1]))
        print("FindCommonSegmentLists finishes working. Elements: "+str(len(NewSegs)))
    #
    return NewSegs
#FindCommonSegmentLists

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
                #if t11>=t21:
                if t11<=t21:
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
#



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
    #new:
    n_channels=dataRead.Channels[0]
    QFiles=len(dataRead.File)
    SensorsQuantity=0
    for i in range (QFiles):
        CurChannelsQ=dataRead.Channels[i]
        SensorsQuantity+=CurChannelsQ
    #
    #CaseN_1sensor1_2files1chn2_1file2chns3_another4
    if(SensorsQuantity==1):
        CaseN_1sensor1_2files1chn2_1file2chns3_other4=1
        CaseN_1sensor1_2files1chn2_1file2chns3_another4("non-standard primitive case: 1 sensor")
    elif SensorsQuantity==2 and QFiles==2 and n_channels==1:
        CaseN_1sensor1_2files1chn2_1file2chns3_another4=2
        print("standard case: 2 sensors, 2 1-channel files")
    elif SensorsQuantity==2 and QFiles==1 and n_channels==2:
        CaseN_1sensor1_2files1chn2_1file2chns3_another4=3
        print("standard case: 2 sensors, 1 2-channels file")
    else:
        CaseN_1sensor1_2files1chn2_1file2chns3_another4=4
        print("non standard case or error!")
    #
    signals=[]
    #
    ImpactsBoundDefMode=2 # 1 - fun ic es, 2 - new fun, am ZB dat > gut gefa r' fun 1
    #
    allSegments=[]
    #print("ImpactBounds.csv создан")
    #
    do_CheckReadingSignal=True#False#True
    #
    #do_ConvertToNpArray=True
    do_Normalize=True
    #do_CreateSingleSignalFileForBothSensors=True# ! for each sensors separately both files wi abfa independently
    #
    do_ShowSeparateImpacts=True# am graph
    #
    #do_DefImpactBoundsAuto=True
    #do_WriteBounds=True
    #do_WriteImpactBounds=True#False
    do_WriteAllImpactsNotSingle=True # switch: 1 impact or eiq
    #do_WriteImpactBounds_AutoDef=False # noam utf'd
    #
    # Обработка каждого файла: lir .wav, lif .csv.
    energySums_allRecs=[]
    filechars_allRecs=[]
    #
    #fileOwnNames=[]
    #
    #if do_CreateSingleSignalFileForBothSensors:
    #    pass
    #    #creater,  
    #fileN=0
    #for fname in filenames:
    print("QFiles="+str(dataRead.QFiles))
    #for sensorN in range(1, SensorsQuantity+1):
    for fileN in range(1, dataRead.QFiles+1):
        #if CaseN_1sensor1_2files1chn2_1file2chns3_another4==2
        print("fileN="+str(fileN))
        fileOwnName=dataRead.File[fileN-1]
        #fileOwnNames.append(fileOwnName)
        #
        fname=dataRead.Folder+"\\"+dataRead.SubFolder_IniData+"\\"+dataRead.File[fileN-1]+".wav"
        #fileN+=1
        #
        ts, n_channels, signal, fs = read_wav_and_calc_t_1(fname, max_seconds=None)
        print("Read successfully. Values: "+str(len(signal)))
        #
        tmax=ts[-1]
        print("checking: fs="+str(fs)+" tmax="+str(tmax))
        #
        if CaseN_1sensor1_2files1chn2_1file2chns3_another4==1 or CaseN_1sensor1_2files1chn2_1file2chns3_another4==2:
            fileN=sensorN
            if fileN==1:
                signal_sensor1=copy.deepcopy(signal)
            elif fileN==2:
                signal_sensor2=copy.deepcopy(signal)
            #
        elif CaseN_1sensor1_2files1chn2_1file2chns3_another4==3:
            for chN in range(n_channels):
                signal_chn=signal[:,chN]#qo sdi? Os: interleaved: ch1val1, ch2val1, ch3val1, ch1val2, ch2val2, ch3val2
                if chN==0:
                    signal_sensor1=copy.deepcopy(signal_chn)
                else:
                    signal_sensor2=copy.deepcopy(signal_chn)
                #
                signals.append(signal_chn)
            #
        #
        #fs, tmax s'last, if 2 channels, D s'idy uz tbi, so remain af last arbf'd
    #for
    #------------------------------------------------------------------------------------------------
    for sensorN in range(1, SensorsQuantity+1):
        signal_chn=signals[sensorN-1]
        plot_signal(ts, signal_chn, title=f"{fname} - весь сигнал (исходный (from .wav)), датчик N"+str(sensorN))
    #------------------------------------------------------------------------------------------------
    signals_normd=[]
    if do_Normalize:
        for sensorN in range(1, SensorsQuantity+1):
            #
            signal_chn=copy.deepcopy(signals[sensorN-1])
            #signal_chn=np.array(signal_chn)
            #signal_chn-=np.median(signal_chn)
            #signal_chn=signal_chn.tolist()
            signal_chn=NormalizeSignal(signal_chn, by_Mean1Median2=2)
            signals_normd.append(signal_chn)
        #
        signals=[]
        signals=copy.deepcopy(signals_normd)
        print("normalized")
    #-------------------------------------------------------------------------------------------------
    for sensorN in range(1, SensorsQuantity+1):
        signal_chn=copy.deepcopy(signals[sensorN-1])
        plot_signal(ts, signal_chn, title=f"{fname} - весь сигнал (нормализация), датчик N"+str(sensorN))
    #-------------------------------------------------------------------------------------------------
    for sensorN in range(1, SensorsQuantity+1):
        if CaseN_1sensor1_2files1chn2_1file2chns3_another4==1 or CaseN_1sensor1_2files1chn2_1file2chns3_another4==2:
            fileOwnName=dataRead.File[sensorN-1]+dataRead.fileNameEnding_Signal
        elif CaseN_1sensor1_2files1chn2_1file2chns3_another4==3:
            #fileOwnName=dataRead.File[0]+"_chN"+str(sensorN-1)+"_"+dataRead.fileNameEnding_Signal
            fileOwnName=dataRead.File[0]+"_chN"+str(sensorN-1)+dataRead.fileNameEnding_Signal
        #
        signal_chn=copy.deepcopy(signals[sensorN-1])
        fileName=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+fileOwnName
        csv_filename=fileName
        print("writing signal to "+csv_filename)
        with open(csv_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Time_s", "Signal", "Energy"])
            for i in range(len(ts)):
                writer.writerow([ts[i], signal_chn[i], signal_chn[i]*signal_chn[i]])
            #
        #
        print("written")
    #--------------------------------------------------------------------------------------------------
    if do_CheckReadingSignal:
        print("Reading signal(s) from .csv")
        signals=[]
        for sensorN in range(1, SensorsQuantity+1):
            if CaseN_1sensor1_2files1chn2_1file2chns3_another4==1 or CaseN_1sensor1_2files1chn2_1file2chns3_another4==2:
                fileOwnName=dataRead.File[sensorN-1]+dataRead.fileNameEnding_Signal
            elif CaseN_1sensor1_2files1chn2_1file2chns3_another4==3:
                fileOwnName=dataRead.File[0]+"_chN"+str(sensorN-1)+dataRead.fileNameEnding_Signal
            #
            fileName=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+fileOwnName
            csv_filename=fileName
            print("Reading from: "+fileName)
            #
            ts, signal_chn, es_chn = ReadSensorSignalFromCsv(fileName)
            #
            signals.append(signal_chn)
            #
            print("Read successfully. Values: "+str(len(signal_chn)))
        #----------------------------------------------------------------------------------------------
        for sensorN in range(1, SensorsQuantity+1):
            signal_chn=copy.deepcopy(signals[sensorN-1])
            print("Sensor N "+str(sensorN)+" Signal Values: "+str(len(signal_chn)))
            plot_signal(ts, signal_chn, title=f"{fname} - весь сигнал (прочитанный из .csv), датчик N"+str(sensorN))
        #
    # ----- Impacts Bounds ----------------------------------------------------------------------------
    #if do_DefImpactBoundsAuto: # amda def impacts auto 88888888888888888888888888888888888888888888888
    TrashBeforeT=1
    TrashAfterT=1
    vsh=0
    N0=0
    #print("do_DefImpactBoundsAuto = true => finding impacts bounds")
    print("Finding impacts bounds")
    fss=fs#I n'ved nu, qut s'fss
    for sensorN in range(1, SensorsQuantity+1):
        signal_chn=copy.deepcopy(signals[sensorN-1])
        sig_for_bnds=copy.deepcopy(signal_chn)
        #
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
                    trashT1=sig_for_bnds[trashN1-1]
                    trashT2=sig_for_bnds[trashN2-1]
                    print("Between impact ts = ["+str(impT1)+"..."+str(impT2)+"] there exists trash range [t1="+str(trashT1)+"... t2="+str(trashT2)+"]")
                #
            #
        elif ImpactsBoundDefMode==2:
            #print("n_channels=1, ImpactsBoundDefMode=2")
            peaks_time, segments = FindTImpactStart(sig_for_bnds, fs=fs, SectT=6, TrashBeforeT=1, TrashAfterT=1, MoreThanTrashCoef=3, vsh=0)
            #was: ne sig_for_bnds, ma signal
            #
            #for impN in range(1, len(peaks_time)+1):
            #    if impN==2:
            #        impT1=peaks_time[impN-1]
            #        impT2=peaks_time[impN+1-1]
            #        trashN1, trashN2 = findTrashNsAfterVibr(sig_for_bnds, fss, impT1, impT2, FindTrashMax(sig_for_bnds, fs, TrashBeforeT, TrashAfterT, vsh), N0, vsh)
            #        trashT1=sig_for_bnds[trashN1-1]
            #        trashT2=sig_for_bnds[trashN2-1]
            #        print("Between impact ts = ["+str(impT1)+"..."+str(impT2)+"] there exists trash range [t1="+str(trashT1)+"... t2="+str(trashT2)+"]")
            #    #
            ##
        #
        allSegments.append(segments) #ce redo 2 tids ob 2 files
        print("Bounds (sensorN"+str(sensorN)+"): "+str(len(segments)))
        print(segments)
    #---------------------------------------------------------------------------------------------------
    print("Displaying segments:")
    print("SensorsQuantity="+str(SensorsQuantity))
    #print(" len(ts)="+str(len(ts))+" len(signal_chn)="+str(len(signal_chn)))
    for sensorN in range(1, SensorsQuantity+1):
        signal_chn=copy.deepcopy(signals[sensorN-1])
        #print(" len(ts)="+str(len(ts))+" len(signal_chn)="+str(len(signal_chn)))
        sig_for_bnds=copy.deepcopy(signal_chn)
        segments=copy.deepcopy(allSegments[sensorN-1])
        #
        #PlotSignalWithImpactsBounds(sig_for_bnds, segments, sensorN)
        #
        ymin, ymax = np.min(signal_chn), np.max(signal_chn) # plot impact bounds # 8888888888888888888888888888888888888888888888888888888888
        for seg in segments:
            start, end = seg
            plt.vlines([start, end], ymin, ymax, colors="r", linestyles="--")
        #
        plt.xlabel("Время t, с")
        plt.ylabel("Амплитуда ")
        #plt.title(f"Сигнал с разделительными линиями сегментов File: {fileOwnNames[chnN-1]}")
        plt.title(f"Сигнал с разделительными линиями сегментов Датчик: {sensorN}")
        plt.plot(ts, signal_chn)#signal ablb maq-dim arr. If so, plt.plot int ce et plot in idy CS l'curves ot dims! Et uz tic utas -show impact bnds - os norm
        plt.legend()
        plt.grid(True)
        plt.show()
    #---------------------------------------------------------------------------------------------------
    print("Finding United segments")
    print(" len(segs1)="+str(len(allSegments[1-1]))+" len(segs2)="+str(len(allSegments[2-1])))
    unitedSegments=FindCommonSegmentLists(allSegments[1-1], allSegments[2-1], dataRead, dt_s=1.0, vsh=0)
    print("United segments")
    print(unitedSegments)
    print("Displaying united segments:")
    for sensorN in range(1, SensorsQuantity+1):
        signal_chn=copy.deepcopy(signals[sensorN-1])
        #print(" len(ts)="+str(len(ts))+" len(signal_chn)="+str(len(signal_chn)))
        sig_for_bnds=copy.deepcopy(signal_chn)
        #def PlotSignalWithImpactsBounds(ts, signal, segments, sensorN)
        PlotSignalWithImpactsBounds(ts, sig_for_bnds, unitedSegments, sensorN)
    #
    for sensorN in range(1, SensorsQuantity+1):
        #signal_chn=signals[sensorN-1]
        segments=copy.deepcopy(unitedSegments)
        ymin, ymax = np.min(signal), np.max(signal) # plot impact bounds # 8888888888888888888888888888888888888888888888888888888888
        for seg in segments:
            start, end = seg
            plt.vlines([start, end], ymin, ymax, colors="r", linestyles="--")
        #
        plt.xlabel("Время t, с")
        plt.ylabel("Амплитуда ")
        #plt.title(f"Сигнал с разделительными линиями сегментов File: {fileOwnNames[chnN-1]}")
        plt.title(f"Сигнал с разделительными линиями сегментов Датчик: {sensorN}")
        plt.plot(ts, signal)#signal ablb maq-dim arr. If so, plt.plot int ce et plot in idy CS l'curves ot dims! Et uz tic utas -show impact bnds - os norm
        plt.legend()
        plt.grid(True)
        plt.show()
    #----------------------------------------------------------------------------------------------------
    csv_filename=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+dataRead.File[0]+dataRead.fileNameEnding_ImpactBounds
    print("writing file of impacts bounds: "+csv_filename)
    #rowHdr=["N", "tStart", "tFin"]
    rowHdr=["N", "tStart", "tFin", "tFin2"]
    with open(csv_filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(rowHdr)
        j=0
        for segment in unitedSegments:
            j+=1
            #writer.writerow([str(j), str(segment[1-1]),str(segment[2-1])])
            writer.writerow( [ str(j), str(segment[1-1]), str(segment[2-1]), str(segment[2-1]) ] )
        #
    #
       
print("Step1 finishes working")

