# based on 2_2, 2_2 in 2_2 s'diqal'd
# ak 2_2, S lir l'file et keeps main data in class obj
# amda es signal_sensor1 et signal_sensor2 vars/ Normalization arb't
# ei errs s'corr'd
# also corrected system of calculating bounds and writing em.
# S'lif'd ac cond do_WriteImpactsBounds, and work't
# n'utf'd et n'arb't sys of calc l'ends (2nd ends) o'bounds, nu whole signal s'div'd by maxs
# added fun, uniting l'2 sets of bounds ad 1 common, ic lif'tc ad file: FindCommonSegnmentLists
# n'arb brunch for single csv-file for both sensors
# vrn arb'bl
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

def FindCommonSegnmentLists(segs1, segs2, dt_s=1.0, vsh=0):
    NewSegs=[]
    NewSeg=[]
    tss11=[]
    tss12=[]
    tss21=[]
    tss22=[]
    tss1=[]
    tss2=[]
    Ns2=[]
    if vsh==1:
        print("FindCommonSegnmentLists starts working. Elements: "+str(len(segs1))+"="+str(len(segs2)))
    #
    if isinstance(segs1, list) and len(segs1)>0 and (segs2==[] or not isinstance(segs2, list)):
        NewSegs=copy.deepcopy(segs1)
        if vsh==1:
            print("FindCommonSegnmentLists starts working. Segments - only set 1")
        #
    elif isinstance(segs2, list) and len(segs2)>0 and (segs1==[] or not isinstance(segs1, list)):
        NewSegs=copy.deepcopy(segs2)
        if vsh==1:
            print("FindCommonSegnmentLists starts working. Segments - only set 2")
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
            t22=segs1[N2-1][2-1]
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
            t11=tss11[N1-1]
            NewSeg.append(t11)
            t12=tss12[N1-1]
            NewSeg.append(t12)
            NewSegs.append(NewSeg)
        #
    if vsh==1:
        for segment in NewSegs:
            print(str(segment[1-1])+"..."+str(segment[2-1]))
        print("FindCommonSegnmentLists finishes working. Elements: "+str(len(NewSegs)))
    #
    return NewSegs
#

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

    unitedSegments=FindCommonSegnmentLists(allSegments[1-1], allSegments[2-1], dt_s=1.0, vsh=0)
    print("United segments")
    print(unitedSegments)

    csv_filenam=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+dataRead.File[0]+dataRead.fileNameEnding_ImpactBounds
    print("writing file of impacts bounds: "+csv_filenam)
    rowHdr=["N","tStart", "tFin"]
    with open(csv_filenam, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(rowHdr)
        j=0
        for segment in unitedSegments:
            j+=1
            writer.writerow([str(j), str(segment[1-1]),str(segment[2-1])])
            
print("Step1 finishes working")

