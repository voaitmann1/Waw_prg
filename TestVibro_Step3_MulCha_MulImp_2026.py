# based on vrn 4_4 - arb'n vrn
# 4_4 s'diqal'd in C
# no reg l'impacts bounds
# HaDo:
# - clasterize l'smooth'd freqs
# - reg l'impacts bounds,
# - lir et lif l'spectrum
# - full harm anal
# - Musbe neto method ut calc t signal:
# - ut'(je channel calc 

from MyPyVibroLib import *

if __name__ == "__main__":

    print("Step3 (2026) starts working")

    do_ShowReadSignal=True#False#True
    do_computeSpectrum=False#True
    do_detrend=True
    do_normalizeByMean=True
    do_ShowWholeSignal=True
    do_ShowSingleSignal=True
    do_ShowWholeSignal_AfterNorm=False#True
    do_ShowWholeSignal_AfterDetrend=False#True
    do_ShowSingleSignal_AfterNorm=False
    do_ShowSingleSignal_AfterDetrend=False
    do_CheckAllSingleSignals=True
    do_showSingleSignals_TogetherFromAllSensors=True
    do_showSingleSignals_SeparatelyFromEachSensor=False
    do_checkSingleSigmnalsWithGraphAtOnce=False
    do_ifImpactTimeRangeNotGiven_ReadFileNotStopAndRepoirtyError=False# nrewe, n'arb
    do_ShowLibEnvelope=True#False
    do_clustrerizeSpectrum=True
    showCurFreqCluster_NeededFragmentOnlyNotWhole=False#True
    do_Smoothing_Extremums=True
    do_printApproximatedExponentEnvelope=True
    #
    _chn_N_=2
    _impN_=2#5
    env_QSects=50
    #
    decrs1=[]
    decrs2=[]
    decrsS=[]
    #
    decrs1s=0
    decrs2s=0
    decrsSs=0
    #
    freqHB_Smooth=65
    freqHB_TryClust=4
    #
    #freqHB=30 #4 #19#65
    #
    decr_all_fileOwnName="Results_byEachImpact.csv"
    decr_all_fileName=dataRead.Folder+"\\"+dataRead.SubFolder_Results+"\\"+decr_all_fileOwnName
    decr_all_header=["ImpactN", "chN", "t1", "t2", "dt", "decr_chn[imp]", "decrMedFrom1stTillCur_chn"]
    if os.path.isfile(decr_all_fileName)==False:
        with open(decr_all_fileName, mode='w', newline='') as dst_f_sngl:
            writer_sngl = csv.writer(decr_all_header)
        #
    #
    dataRead=FilesData()
    dataRead.DataOfFiles(dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+"FolderAndFiles_1_Full.csv", 1)
    print("reading file: "+dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+"FolderAndFiles_1_Full.csv")
    print(dataRead)
    #
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
    impactsBounds_fileName=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+dataRead.File[0]+dataRead.fileNameEnding_ImpactBounds
    #
    signals=[]
    allSegments=[]
    impacts=[]
    #
    fileNames =[]
    fileOwnNames=[]
    for sensorN in range(1, SensorsQuantity+1):
        if CaseN_1sensor1_2files1chn2_1file2chns3_another4==1 or CaseN_1sensor1_2files1chn2_1file2chns3_another4==2:
            fileOwnName=dataRead.File[sensorN-1]+dataRead.fileNameEnding_Signal
        elif CaseN_1sensor1_2files1chn2_1file2chns3_another4==3:
            fileOwnName=dataRead.File[0]+"_chN"+str(sensorN-1)+dataRead.fileNameEnding_Signal
        #
        fileName=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+fileOwnName
        print("fileOwnName: "+fileOwnName)
        LToSubtractFromName=len(dataRead.fileNameEnding_Signal)
        fileOwnName=fileOwnName[:-LToSubtractFromName]
        print("fileOwnName: "+fileOwnName)
        print("File: "+fileName)
        #fileNames =[]
        fileOwnNames.append(fileOwnName)
        #
        ts, signal_chn, es_chn = ReadSensorSignalFromCsv(fileName)
        #
        signals.append(signal_chn)
        #
        print("Read successfully. Values: "+str(len(signal_chn)))

        # here was fragment om impact bounds in Step4 v.4.5
    #---------------------------------------------------------------------------------
    impacts=ReadImpactsBounds(impactsBounds_fileName, vsh=1)
    print("File is successfully read. Impacts bounds (assigned by file data):")
    print(impacts)
    #---------------------------------------------------------------------------------
    
    for sensorN in range(1, SensorsQuantity+1):
        if CaseN_1sensor1_2files1chn2_1file2chns3_another4==1 or CaseN_1sensor1_2files1chn2_1file2chns3_another4==2:
            fileOwnName=dataRead.File[sensorN-1]+dataRead.fileNameEnding_Signal
        elif CaseN_1sensor1_2files1chn2_1file2chns3_another4==3:
            fileOwnName=dataRead.File[0]+"_chN"+str(sensorN-1)+dataRead.fileNameEnding_Signal
        #
        fileName=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+fileOwnName
        #
        print("Reading signal from:"+fileName)
        #
        ts, signal_chn = read_signal_csv(fileName)
        #
        signals.append(signal_chn)
    #-----------------------------------------------------------------------------------
    if do_ShowWholeSignal:
        for sensorN in range(1, SensorsQuantity+1):
            fileOwnName=fileOwnNames[sensorN-1]
            signal_chn=copy.deepcopy(signals[sensorN-1])
            #plot_signal(ts, signal_chn, title=f"{fileOwnName} - весь сигнал (исходный)")
            plot_signal(ts, signal_chn, title=f"{fileOwnName} - весь сигнал ")
        #
    #----------------------------------------------------------------------------
    #if do_normalizeByMean:
    #    signals_normd=[]
    #    for sensorN in range(1, SensorsQuantity+1):
    #        signal_chn=copy.deepcopy(signals[sensorN-1])
    #        signal_chn=NormalizeSignal(signal_chn, by_Mean1Median2=1)
    #        signals_normd.append(signal_chn)
    #    #
    #    signals=[]
    #    signals=copy.deepcopy(signals_normd)
    #----------------------------------------------------------------
    #if do_ShowWholeSignal_AfterNorm:
    #    for sensorN in range(1, SensorsQuantity+1):
    #        fileOwnName=fileOwnNames[sensorN-1]
    #        signal_chn=copy.deepcopy(signals[sensorN-1])
    #        plot_signal(ts, signal_chn, title=f"{fileOwnName} - весь сигнал (нормализация)")
    #    #
    #----------------------------------------------------------------------------
    #if do_detrend:
    #    signals_dtrd=[]
    #    for sensorN in range(1, SensorsQuantity+1):
    #        signal_chn=copy.deepcopy(signals[sensorN-1])
    #        detrend(signal_chn)
    #        signals_dtrd.append(signal_chn)
    #    #
    #    signals=[]
    #    signals=copy.deepcopy(signals_dtrd)
    #----------------------------------------------------------------
    #if do_ShowWholeSignal_AfterDetrend:
    #    for sensorN in range(1, SensorsQuantity+1):
    #        fileOwnName=fileOwnNames[sensorN-1]
    #        signal_chn=copy.deepcopy(signals[sensorN-1])
    #        plot_signal(ts, signal_chn, title=f"{fileOwnName} - весь сигнал (детренд)")
    #    #
    #----------------------------------------------------------------------------
    if do_CheckAllSingleSignals:
        ts_sngl=[]
        xs_sngl=[]
        for impN in range(len(impacts)):
            impNf, impLB, impHB = ExtractImpactBounds2(impacts, impN+1)
            print(str(impN+1)+") impact N "+str(impNf)+" impLB="+str(impLB)+" impHB="+str(impHB))
            t_sngl=[]
            x_sngl=[]
            for sensorN in range(1, SensorsQuantity+1):
                signal_chn=copy.deepcopy(signals[sensorN-1])
                #if impN==1:#<=2:
                #t_sngl_chn, x_sngl_chn = GetSingleImpactSignal(ts, signal_chn, impLB, impHB, 1)
                #else:
                t_sngl_chn, x_sngl_chn = GetSingleImpactSignal(ts, signal_chn, impLB, impHB)
                ##
                t_sngl.append(t_sngl_chn)
                x_sngl.append(x_sngl_chn)
                print("Impact duration: "+str(len(t_sngl_chn))+" s")
                print("Impact t="+str(t_sngl_chn[0])+"..."+str(t_sngl_chn[-1]))
                print("General t="+str(ts[0])+"..."+str(ts[-1]))
                #x_sngl.append(copy.deepcopy(x_sngl_chn))
                #
                if do_checkSingleSigmnalsWithGraphAtOnce:
                    fileOwnName=fileOwnNames[sensorN-1]
                    plot_signal(t_sngl_chn, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар t={t_sngl_chn[0]} ... {t_sngl_chn[-1]} (исходный), канал"+str(sensorN-1))
                #
                #x_sngl.append(copy.deepcopy(x_sngl_chn))
                #x_sngl_chn=[]
                #x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                #
                #plot_signal(t_sngl, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар {impLB} ... {impHB} (исходный), канал"+str(sensorN-1))
                #x_sngl.append(x_sngl_chn)
            #for sensorN
            ts_sngl.append(t_sngl)
            xs_sngl.append(x_sngl)
            #
            #impLB=t_sngl[0][0]
            #impHB=t_sngl[0][-1]
            #
            #GraphName=f"сигнал 1 удар t={impLB} ... {impHB}(исходный.)"
            #plot_several1([
            #         
            #            [
            #               [(t_sngl, x_sngl[1-1])], 1
            #            ],
            #            [
            #               [(t_sngl, x_sngl[2-1])], 1
            #            ]
            #            
            #          ],
            #          [
            #            ["t, с", "Сигнал", "Канал 0"],                  
            #            ["t, с", "Сигнал", "Канал 1"]
            #            
            #          ],
            #          [
            #            [ {"color":"blue"}],
            #            [ {"color":"blue"}]
            #          ],
            #          GraphName
            #    ) 
            ##
            #----------------------------------------------------------------
            if do_ShowSingleSignal:
                #for impN in range(len(impacts)):
                #ampl
                #x_sngl=xs_sngl[impN]
                if do_showSingleSignals_SeparatelyFromEachSensor:
                    for sensorN in range(1, SensorsQuantity+1):
                        x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                        fileOwnName=fileOwnNames[sensorN-1]
                        #
                        plot_signal(t_sngl, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар {t_sngl_chn[0]} ... {impHB} (исходный), канал"+str(sensorN-1))
                    #for
                #if
                #print("data include points: t: "+str(len(t_sngl))+" x1: "+str(len(x_sngl[1-1]))+" x2: "+str(len(x_sngl[2-1])))
                
                if do_showSingleSignals_TogetherFromAllSensors:
                    graph_data_array=[]
                    graph_text_array=[]
                    graph_color_array=[]
                    for sensorN in range(1, SensorsQuantity+1):
                        t_sngl_chn=copy.deepcopy(t_sngl[sensorN-1])
                        x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                        #
                        graph_data_array.append([[(t_sngl[sensorN-1], x_sngl[sensorN-1])], 1])
                        #graph_text_array.append(["t, с", "Сигнал", "Канал "+str(sensorN-1)])
                        graph_text_array.append(["t, с", "Сигнал - chN "+str(sensorN-1)])
                        graph_color_array.append([ {"color":"blue"}])
                    #
                    impLB=t_sngl[0]
                    impHB=t_sngl[-1]
                    GraphName=f"сигнал 1 удар N {impNf} t={t_sngl_chn[0]} ... {t_sngl_chn[-1]}(исходный.)"
                    GraphName=f"сигнал 1 удар N {impNf} t="+str(t_sngl_chn[0])+" ... "+str(t_sngl_chn[-1])+" (исходный.)"
                    plot_several1(
                      #[
                      #  [
                      #     [(t_sngl, x_sngl[1-1])], 1
                      #  ],
                      #  [
                      #     [(t_sngl, x_sngl[2-1])], 1
                      #  ]
                      #]
                      graph_data_array,
                      #[
                      #  ["t, с", "Сигнал", "Канал 0"],                  
                      #  ["t, с", "Сигнал", "Канал 1"]
                      #]
                      graph_text_array,
                      #[
                      #  [ {"color":"blue"}],
                      #  [ {"color":"blue"}]
                      #]
                      graph_color_array,
                      GraphName
                    )
                #
            #----------------------------------------------------------------------------
            if do_normalizeByMean:
                x_sngl_normd=[]
                #for impN in range(len(impacts)):
                for sensorN in range(1, SensorsQuantity+1):
                    x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                    x_sngl_chn=NormalizeSignal(x_sngl_chn, by_Mean1Median2=1)
                    x_sngl_normd.append(x_sngl_chn)
                #
                #x_sngl_normd.append(x_sngl)
                ##
                #xs_sngl=[]
                #xs_sngl=copy.deepcopy(xs_sngl_normd)
            #----------------------------------------------------------------------------    
            if do_ShowSingleSignal_AfterNorm:
                if do_showSingleSignals_SeparatelyFromEachSensor:
                    for sensorN in range(1, SensorsQuantity+1):
                        fileOwnName=fileOwnNames[sensorN-1]
                        x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                        plot_signal(t_sngl, x_sngl, title=f"{fileOwnName} - сигнал 1 удар t={t_sngl_chn[0]} ... {t_sngl_chn[-1]}(нормализация.), канал"+str(sensorN-1))
                    #
                #
                if do_showSingleSignals_TogerherForAllSensors:
                    graph_data_array=[]
                    graph_text_array=[]
                    graph_color_array=[]
                    for sensorN in range(1, SensorsQuantity+1):
                        t_sngl_chn=copy.deepcopy(t_sngl[sensorN-1])
                        x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                        #
                        graph_data_array.append([[(t_sngl[sensorN-1], x_sngl[sensorN-1])], 1])
                        #graph_text_array.append(["t, с", "Сигнал", "Канал "+str(sensorN-1)])
                        graph_text_array.append(["t, с", "Сигнал - chN "+str(sensorN-1)])
                        graph_color_array.append([ {"color":"blue"}])
                    #
                    GraphName=f"сигнал 1 удар N {impNf} t={t_sngl_chn[0]} ... {t_sngl_chn[-1]}(нормализация.)"
                    plot_several1(
                      #[
                      #  [
                      #     [(t_sngl, x_sngl[1-1])], 1
                      #  ],
                      #  [
                      #     [(t_sngl, x_sngl[2-1])], 1
                      #  ]
                      #]
                      graph_data_array,
                      #[
                      #  ["t, с", "Сигнал", "Канал 0"],                  
                      #  ["t, с", "Сигнал", "Канал 1"]
                      #]
                      graph_text_array,
                      #[
                      #  [ {"color":"blue"}],
                      #  [ {"color":"blue"}]
                      #]
                      graph_color_array,
                      GraphName
                    ) 
                #
            #----------------------------------------------------------------------------
            if do_detrend:
                xs_sngl_dtrd=[]
                #for impN in range(len(impacts)):
                for sensorN in range(1, SensorsQuantity+1):
                    x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                    detrend(x_sngl_chn)
                    xs_sngl_dtrd.append(x_sngl_chn)
                #
                #xs_sngl_dtrd.append(x_sngl)
                #
                xs_sngl=[]
                xs_sngl=copy.deepcopy(xs_sngl_dtrd)
            #
            #-------------------------------------------------------------------------------
            if do_ShowSingleSignal_AfterDetrend:
                if do_showSingleSignals_SeparatelyFromEachSensor:
                    for sensorN in range(1, SensorsQuantity+1):
                        fileOwnName=fileOwnNames[sensorN-1]
                        x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                        plot_signal(t_sngl, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар t={t_sngl_chn[0]} ... {t_sngl_chn[-1]} (детренд), канал"+str(sensorN-1))
                    #               
                #
                if do_showSingleSignals_TogerherForAllSensors:                
                    graph_data_array=[]
                    graph_text_array=[]
                    graph_color_array=[]
                    for sensorN in range(1, SensorsQuantity+1):
                        t_sngl_chn=copy.deepcopy(t_sngl[sensorN-1])
                        x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                        #
                        graph_data_array.append([[(t_sngl[sensorN-1], x_sngl[sensorN-1])], 1])
                        #graph_text_array.append(["t, с", "Сигнал", "Канал "+str(sensorN-1)])
                        graph_text_array.append(["t, с", "Сигнал - chN "+str(sensorN-1)])
                        graph_color_array.append([ {"color":"blue"}])
                    #for sensor N
                    GraphName=f"сигнал 1 удар N {impNf} t={t_sngl_chn[0]} ... {t_sngl_chn[-1]}(детренд.)"
                    plot_several1(
                      #[
                      #  [
                      #     [(t_sngl, x_sngl[1-1])], 1
                      #  ],
                      #  [
                      #     [(t_sngl, x_sngl[2-1])], 1
                      #  ]
                      #]
                      graph_data_array,
                      #[
                      #  ["t, с", "Сигнал", "Канал 0"],                  
                      #  ["t, с", "Сигнал", "Канал 1"]
                      #]
                      graph_text_array,
                      #[
                      #  [ {"color":"blue"}],
                      #  [ {"color":"blue"}]
                      #]
                      graph_color_array,
                      GraphName
                    ) 
                #if show signals together for all sensors
            #-------------------------------------------------------------------------------
            do_CalcDecrement_ForWholeSignalOfSingleImpact=True
            if do_CalcDecrement_ForWholeSignalOfSingleImpact:
                Lt_allChns=[]
                for sensorN in range(1, SensorsQuantity+1):
                    t_sngl_chn=copy.deepcopy(t_sngl[sensorN-1])
                    Lt_chn=len(t_sngl_chn)
                    Lt_allChns.append(Lt_chn)
                    if sensorN==1 or (sensorN>1 and Lt_chn>maxSensorImpactDuration):
                        maxSensorImpactDuration=Lt_chn
                        maxImpactDurationSensorN=sensorN
                    #
                    if sensorN==1 or (sensorN>1 and Lt_chn<minSensorImpactDuration):
                        minSensorImpactDuration=Lt_chn
                        minImpactDurationSensorN=sensorN
                    #
                    significantImpactDurationSensorN=maxImpactDurationSensorN
                    print("chN  "+str(sensorN)+" maxQ="+str(maxSensorImpactDuration)+" minQ="+str(minSensorImpactDuration)+" maxImpactDurationSensorN="+str(maxImpactDurationSensorN)+" minImpactDurationSensorN="+str(minImpactDurationSensorN))
                #for sensorN
                t_sngl_signif_allChns=copy.deepcopy(t_sngl[significantImpactDurationSensorN-1])
                tmax_allChns=t_sngl_signif_allChns[-1]
                QvalsMaxAllChns=len(tmax_allChns)
                en_sngl_allChns=[]
                for sensorN in range(1, SensorsQuantity+1):
                    t_sngl_chn = copy.deepcopy(t_sngl[sensorN-1])
                    Qvals=len(t_sngl_chn)
                    en_sngl_chn=[]
                    en_sngl_chn_scndPart=[]
                    en_sngl_chn_part2=[]
                    for i in range(Qvals):
                        sig = copy.deepcopy(x_sngl_chn[i])
                        en = sig*sig
                        en_sngl_chn.append(en)
                    #for i
                    en_sngl_allChns.append(en_sngl_chn)
                    print("chN  "+str(sensorN)+" for "+str(len(t_sngl_chn))+" vals of  t "+str(len(en_sngl_chn))+" vals of  energy done ")
                #for sensorN
                ensum=[]
                t_sngl_max=copy.deepcopy(t_sngl[maxImpactDurationSensorN-1])
                QvalsMax=len(t_sngl_max)
                #print("Energy values: channels: "+str(len(en_sngl_allChns))+" erst: "+str(len(en_sngl_allChns[1-1]))+" second: "+str(len(en_sngl_allChns[2-1])))
                print("Energy values: channels: "+str(len(en_sngl_allChns)))
                print(" erst: "+str(len(en_sngl_allChns[1-1])))
                print(" scnd: "+str(len(en_sngl_allChns[2-1])))
                for valN in range(QvalsMax):
                    en_s=0
                    for sensorN in range(1, SensorsQuantity+1):
                        if valN>=Lt_allChns[sensorN-1]:
                            en=0
                        else:
                            en=copy.deepcopy(en_sngl_allChns[sensorN-1][valN])
                        #
                        en_s+=en
                        #if valN%250==0:
                        #    print("val N "+str(valN+1)+" en="+str(en)+" en sum="+str(ens))
                        ##   
                    #for sensorN
                    ensum.append(en_s)
                #for i in range QvalsMax
                print(str(len(ensum))+" energy sum values calculated")
                print("trying to plot")
                if do_showSingleSignals_TogetherFromAllSensors: 
                    graph_data_allChns=[]
                    graph_text_allChns=[]
                    graph_color_allChns=[]
                    graph_data_chn=[]
                    #graph_text_chn=[]
                    #graph_color_chn=[]
                    for sensorN in range(1, SensorsQuantity+1):
                        #dataPairs=[]
                        #dataPair=(t_sngl_chn, x_sngl_chn)
                        #dataPairs.append(dataPair)
                        #dataPairs=(t_sngl_chn, en_sngl_chn)
                        #dataPairs=[(t_sngl_chn, x_sngl_chn),(t_sngl_chn, en_sngl_chn)]
                        #graph_data_chn.append(dataPairs)
                        #graph_data_chn.append(2)# 2 - graphsQ: signal et su energy, n'sensorsQ
                        #graph_data_chn=[(t_sngl_chn, x_sngl_chn),(t_sngl_chn, en_sngl_chn)]
                        ##
                        #graph_data_allChns.append(graph_data_chn)
                        graph_data_allChns.append([[(t_sngl[sensorN-1], x_sngl[sensorN-1]),(t_sngl[sensorN-1], en_sngl_allChns[sensorN-1])], 2])
                        #
                        #
                        graph_text_allChns.append(["t, с", "Сигнал", "Энергия сигнала"])
                        #
                        #
                        graph_color_chn=[]
                        #dataPair={"color":"blue"}
                        #graph_color_chn.append(dataPair)
                        #dataPair={"color":"green"}
                        #graph_color_chn.append(dataPair)
                        #graph_color_chn=[{"color":"blue"}, {"color":"green"}]
                        #
                        #graph_color_allChns.append(graph_color_chn)
                        graph_color_allChns.append([{"color":"blue"}, {"color":"green"}])
                    #for sensorN
                    #dataPairs=[]
                    #dataPair=[(t_sngl_chn, ensum)]
                    #dataPairs.append(dataPair)
                    #dataPairs.appenfor sensorN in range(1, SensorsQuantity+1):d(1) # means singler for all channels - energy sum
                    #graph_data_allChns.append(dataPairs)
                    graph_data_allChns.append([[(t_sngl[significantImpactDurationSensorN-1], ensum)], 1])
                    #
                    #dataPairs=["t, с", "Энергия"]
                    #graph_text_allChns.append(dataPairs)
                    graph_text_allChns.append(["t, с", "Энергия"])
                    #
                    #dataPairs=[]
                    #dataPair={"color":"green"}
                    #dataPairs.append(dataPair)
                    #graph_color_allChns.append(dataPairs)
                    graph_color_allChns.append([{"color":"green"}])
                    
                    GraphName="Сигналы и их энергия обоих датчиков - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
                    GraphName="Сигналы и их энергия обоих датчиков - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
                    
                    plot_several1(
                        #[
                        #    #[
                        #    #   [(ts, si1), (ts, en1)], 2
                        #    #],
                        #    #[
                        #    #   [(ts, si2), (ts, en2)], 2#[(ts, si1), (ts, en1)], 2
                        #    #],
                        #    #[
                        #    #   #[(ts, en1+en2)], 1
                        #    #   [(ts, ensum)], 1
                        #    #]
                        #    [
                        #        [(t_sngl[1-1], x_sngl[1-1]), (t_sngl[1-1], en_sngl_allChns[1-1])], 2
                        #    ],
                        #    [
                        #        [(t_sngl[2-1], x_sngl[2-1]), (t_sngl[2-1], en_sngl_allChns[2-1])], 2
                        #    ],
                        #    [
                        #        #[(ts, en1+en2)], 1
                        #        #[(t_sngl_chn, ensum)], 1
                        #        [(t_sngl[maxImpactDurationSensorN-1], ensum)], 1
                        #    ]
                        #]
                        graph_data_allChns
                        ,
                        #[
                        #  ["t, с", "Сигнал", "Энергия сигнала"],                  
                        #  ["t, с", "Сигнал", "Энергия сигнала"],
                        #  ["t, с", "Энергия"]
                        #]
                        graph_text_allChns
                        ,
                        #[
                        #  [ {"color":"blue"}, {"color":"green"}],
                        #  [ {"color":"blue"}, {"color":"green"}],
                        #  [ {"color":"green"}]
                        #]
                        graph_color_allChns
                        ,
                        GraphName
                    )
                    print("chN "+str(sensorN)+" Signals, their energy and its sum plotted successfully")
                    #
                #if do_showSingleSignals_TogetherFromAllSensors:
                print(" Signals, their energy and its sum plotted successfully")
                #env_QSects=env_QSects
                QPoints=len(ensum)
                #---------------------------------------------------------------------------
                
                #vsh=0#1 this 67000, 67200, 66800
                #ti=copy.deepcopy(t_sngl[significantImpactDurationSensorN-1])
                #en1=copy.deepcopy(en_sngl_allChns[1-1])
                #en2=copy.deepcopy(en_sngl_allChns[2-1])
                #enS=copy.deepcopy(ensum)
                #    
                #trs1, peaksHs1 = MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(en1, ti, env_QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
                #trs2, peaksHs2 = MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(en2, ti, env_QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
                #trsS, peaksHsS = MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(enS, ti, env_QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
                #    
                #envelopes
                #
                #enve1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ti, type_Stairs0Line1=0)                enve2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ti, type_Stairs0Line1=0)
                #enveS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ti, type_Stairs0Line1=0)
                # 
                #enS=copy.deepcopy(ensum)

                # env_QSects s'const, def'd above
                
                trs_allChns=[]
                peaksHs_allChns=[]
                enve_allChns=[]
                for sensorN in range(1, SensorsQuantity+1):
                    ti=copy.deepcopy(t_sngl[sensorN-1])
                    en_chn=copy.deepcopy(en_sngl_allChns[sensorN-1])
                    trs_chn, peaksHs_chn = MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(en_chn, ti, env_QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
                    enve_chn = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs_chn, trs_chn, ti, type_Stairs0Line1=0)
                    #
                    trs_allChns.append(trs_chn)
                    peaksHs_allChns.append(peaksHs_chn)
                    enve_allChns.append(enve_chn)
                #
                ti=copy.deepcopy(t_sngl[significantImpactDurationSensorN-1])
                #
                trsS, peaksHsS = MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(ensum, ti, env_QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
                enveS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ti, type_Stairs0Line1=0)

                print("linear interpolation calc'd successfully")

                if do_ShowLibEnvelope:#2nd case

                    #env1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ti, type_Stairs0Line1=1)
                    #env2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ti, type_Stairs0Line1=1)
                    #envS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ti, type_Stairs0Line1=1)
                    ti=copy.deepcopy(t_sngl[significantImpactDurationSensorN-1])
                    envS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ti, type_Stairs0Line1=1)
                    env_allChns=[]
                    for sensorN in range(1, SensorsQuantity+1):
                        trs_chn=copy.deepcopy(trs_allChns[sensorN-1])
                        peaksHs_chn=copy.deepcopy(peaksHs_allChns[sensorN-1])
                        env_chn = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ti, type_Stairs0Line1=1)
                        env_allChns.append(env_chn)
                    #

                    print("stairs calc'd successfully")

                    #A01=enve1[0]
                    #A02=enve2[0]
                    #A0S=enveS[0]
                    #
                    #plot_several1([
                    #    [
                    #       [(ti, en1), (ti, enve1), (ti, env1)], 1
                    #    ],
                    #    [
                    #       [(ti, en2), (ti, enve2), (ti, env2)], 1
                    #    ],
                    #    [
                    #       [(ti, enS), (ti, enveS), (ti, envS)], 1
                    #    ]
                    #  ],
                    #  [
                    #    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"],                  
                    #    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"],
                    #    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"]
                    #  ],
                    #  [
                    #    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                    #    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                    #    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}]
                    #  ],
                    #  GraphName
                    #)
                    #
                    A0S=enveS[0]
                    graph_data=[]
                    graph_text=[]
                    graph_colors=[]
                    for sensorN in range(1, SensorsQuantity+1):
                        ti=copy.deepcopy(t_sngl[sensorN-1])
                        en_chn=copy.deepcopy(en_sngl_allChns[sensorN-1])
                        enve_chn=copy.deepcopy(enve_allChns[sensorN-1])
                        env_chn=copy.deepcopy(env_allChns[sensorN-1])
                        A0_chn=enve_chn[0]
                        #
                        graph_data.append([[(ti, en_chn), (ti, enve_chn), (ti, env_chn)], 1])
                        graph_text.append(["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"])
                        graph_colors.append([ {"color":"green"}, {"color":"red"}, {"color":"blue"}])
                    #
                    ti=copy.deepcopy(t_sngl[significantImpactDurationSensorN-1])
                    graph_data.append([[(ti, ensum), (ti, enveS), (ti, envS)], 1])
                    graph_text.append(["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"])
                    graph_colors.append([ {"color":"green"}, {"color":"red"}, {"color":"blue"}])

                    plot_several1(
                      graph_data,
                      graph_text,
                      graph_colors,
                      GraphName
                    )
                    
                else:
                    print("Show envelope partially turned off")
                #
                #if do_ShowLibEnvelope, 2.case
                do_ExcludeLowerPeaks=False #---------------------------

                if do_ExcludeLowerPeaks:
                    #Nps1, t2s1, Hs1 = ExcludeLowerPeaks(peaksHs1, trs1)
                    #Nps2, t2s2, Hs2 = ExcludeLowerPeaks(peaksHs2, trs2)
                    #NpsS, t2sS, HsS = ExcludeLowerPeaks(peaksHsS, trsS)
                    ##
                    #trs1=[]
                    #trs1=t2s1
                    #peaksHs1=[]
                    #peaksHs1=Hs1
                    ##
                    #trs2=[]
                    #trs2=t2s2
                    #peaksHs2=[]
                    #peaksHs2=Hs2
                    ##
                    #trsS=[]
                    #trsS=t2sS
                    #peaksHsS=[]
                    #peaksHsS=HsS
                    ##
                    NpsS, t2sS, HsS = ExcludeLowerPeaks(peaksHsS, trsS)
                    trsS=[]
                    trsS=t2sS
                    peaksHsS=[]
                    peaksHsS=HsS
                    Nps_chn_allChns=[]
                    t2s_allChns=[]
                    Hs_allChns=[]
                    for sensorN in range(1, SensorsQuantity+1):
                        trs_chn=copy.deepcopy(trs_allChns[sensorN-1])
                        peaksHs_chn=copy.deepcopy(peaksHs_allChns[sensorN-1])
                        #
                        Nps_chn, t2s_chn, Hs_chn = ExcludeLowerPeaks(peaksHs_chn, trs_chn)
                        #
                        Nps_chn_allChns.append(Nps_chn)
                        t2s_allChns.append(t2s_chn)
                        Hs_allChns.append(Hs_chn)
                    
                    ##
                    #enve1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ti, type_Stairs0Line1=0)
                    #enve2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ti, type_Stairs0Line1=0)
                    #enveS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ti, type_Stairs0Line1=0)
                    ##
                    enve_allChns=[]
                    for sensorN in range(1, SensorsQuantity+1):
                        trs_chn=copy.deepcopy(trs_allChns[sensorN-1])
                        peaksHs_chn=copy.deepcopy(peaksHs_allChns[sensorN-1])
                        #
                        enve_chn = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs_chn, trs_chn, ti, type_Stairs0Line1=0)
                        #
                        enve_allChns.append(enve_chn)
                    #
                    enveS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ti, type_Stairs0Line1=0)
                    do_CalcStairsAndShowEnvelopedSections=False
                    if do_CalcStairsAndShowEnvelopedSections:
                        #
                        print("linear interpolation calc'd successfully")
                        ##
                        #env1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ti, type_Stairs0Line1=1)
                        #env2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ti, type_Stairs0Line1=1)
                        #envS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ti, type_Stairs0Line1=1)
                        ##
                        env_allChns=[]
                        envS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ti, type_Stairs0Line1=0)
                        for sensorN in range(1, SensorsQuantity+1):
                            trs_chn=copy.deepcopy(trs_allChns[sensorN-1])
                            peaksHs_chn=copy.deepcopy(peaksHs_allChns[sensorN-1])
                            #
                            env_chn = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs_chn, trs_chn, ti, type_Stairs0Line1=0)
                            #
                            env_allChns.append(env_chn)
                        #
                        #
                        print("stairs calc'd successfully")
                        #
                        #print("Peaks of envelope:")
                        #print("N, T1, H1")
                        #for i in range(len(Hs1)):
                        #    print(str(i+1)+" "+str(trs1[i])+" "+str(Hs1[i]))
                        #print("N, T2, H2")
                        #for i in range(len(Hs2)):
                        #    print(str(i+1)+" "+str(trs2[i])+" "+str(Hs2[i]))
                        #print("N, TS, HS")
                        #for i in range(len(HsS)):
                        #    print(str(i+1)+" "+str(trsS[i])+" "+str(HsS[i]))     #
                        #GraphName="Энергия сигналов и огибающая (исключены провалы) - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
                        ##
                        #plot_several1(
                        #  [ 
                        #    [
                        #       [(ti, en1), (ti, enve1), (ti, env1)], 1
                        #    ],
                        #    [
                        #       [(ti, en2), (ti, enve2), (ti, env2)], 1
                        #    ],
                        #    [
                        #       [(ti, enS), (ti, enveS), (ti, envS)], 1
                        #    ]
                        #  ],
                        #  [
                        #    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"],                  
                        #    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"],
                        #    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"]
                        #  ],
                        #  [
                        #    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                        #    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                        #    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}]
                        #  ],
                        #  GraphName
                        #)
                        ##
                        print("N, TS, HS")
                        print("Sum":)
                        for i in range(len(HsS)):
                            print(str(i+1)+" "+str(trsS[i])+" "+str(HsS[i]))     #
                        #
                        for sensorN in range(1, SensorsQuantity+1):
                            print("Channel "+str(sensorN))
                            trs_chn=copy.deepcopy(trs_allChns[sensorN-1])
                            Hs_chn=copy.deepcopy(Hs_allChns[sensorN-1])
                            for i in range (len(Hs_chn)):
                                print(str(i+1)+" "+str(trs1[i])+" "+str(Hs_chn[i]))
                            #
                        #
                        GraphName="Энергия сигналов и огибающая (исключены провалы) - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
                        graph_data=[]
                        graph_text=[]
                        graph_colors=[]
                        for sensorN in range(1, SensorsQuantity+1):
                            en_chn=copy.deepcopy(en_sngl_allChns[sensorN-1])
                            enve_chn=copy.deepcopy(enve_allChns[sensorN-1])
                            env_+chn=copy.deepcopy(env_allChns[sensorN-1])
                            #
                            graph_data.append([[(ti, en_chn), (ti, enve_chn), (ti, env_chn)], 1])
                            graph_text.append(["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"])
                            graph_colors.append([ {"color":"green"}, {"color":"red"}, {"color":"blue"}])
                        #
                        graph_data.append([[(ti, ensum), (ti, enveS), (ti, envS)], 1])
                        graph_text.append(["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"])
                        graph_colors.append([ {"color":"green"}, {"color":"red"}, {"color":"blue"}])
                        #GraphName="Энергия сигналов и огибающая (исключены провалы) - файлы "
                        if SensorsQuantity==1:
                            GraphName+=dataRead.File[0]
                        else:
                            for sensorN in range(1, SensorsQuantity+1):
                                GraphName+=dataRead.File[0]+"-chN "+str(sensorN)
                                if sensorN<SensorsQuantity:
                                    GraphName+=", "
                                #
                            #
                        #
                        plot_several1(
                            graph_data,
                            graph_text,
                            graph_colors,
                            GraphName
                        )
                        #
                    #if do_CalcStairsAndShowEnvelopedSections 
                # if do-ExcludePeaks  ------------------------------------------------------------------------
                print("Approximating peaks")
                #
                #print("Signal Energy - Sensor 1")
                ##
                #alfa1, beta1 = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enve1, ts, do_lnT=False, do_lnY=True, vsh=0)
                ##
                #A01=np.exp(alfa1)
                #delta1 = -beta1
                ##
                #print("alfa1="+str(alfa1)+" beta1="+str(beta1)+" A01="+str(A01)+" delta1="+str(delta1))
                ##
                #print("Signal Energy - Sensor 2")
                #
                #alfa2, beta2 = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enve2, ts, do_lnT=False, do_lnY=True, vsh=0)
                #
                #A02=np.exp(alfa2)
                #delta2 = -beta2
                #
                #print("alfa2="+str(alfa2)+" beta2="+str(beta2)+" A02="+str(A02)+" delta2="+str(delta2))            
                #
                #print("Signal Energy - Sum")
                #alfaS, betaS = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enveS, ts, do_lnT=False, do_lnY=True, vsh=0)
                #
                #print("Signal Energy - Sum")
                #alfaS, betaS = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enveS, ti, do_lnT=False, do_lnY=True, vsh=0)
                ##
                A0_allChns=[]
                delta_allChns=[]
                alfa_allChns=[]
                beta_allChns=[]
                #
                for sensorN in range(1, SensorsQuantity+1):
                    #print("Signal Energy - Sensor "+str(sensorN))
                    #
                    ti=copy.deepcopy(t_sngl[sensorN-1])
                    en_chn=copy.deepcopy(en_sngl_allChns[sensorN-1])
                    enve_chn=copy.deepcopy(enve_allChns[sensorN-1])
                    env_chn=copy.deepcopy(env_allChns[sensorN-1])
                    #
                    alfa_chn, beta_chn = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enve_chn, ti, do_lnT=False, do_lnY=True, vsh=0)
                    #
                    A0_chn=np.exp(alfa_chn)
                    delta_chn = -beta_chn
                    #
                    alfa_allChns.append(alfa_chn)
                    beta_allChns.append(beta_chn)
                    A0_allChns.append(A0_chn)
                    delta_allChns.append(delta_chn)
                    #
                    #print("Channrel "alfa"="+str(alfa_chn)+" beta="+str(beta_chn)+" A0="+str(A0_chn)+" delta="+str(delta_chn))
                #
                for sensorN in range(1, SensorsQuantity+1):
                    print("Signal Energy - Sensor "+str(sensorN))
                    alfa_chn=copy.deepcopy(alfa_allChns[sensorN-1])
                    beta_chn=copy.deepcopy(beta_allChns[sensorN-1])
                    A0_chn=copy.deepcopy(A0_allChns[sensorN-1])
                    delta_chn=copy.deepcopy(delta_allChns[sensorN-1])
                    print("Channrel "alfa"="+str(alfa_chn)+" beta="+str(beta_chn)+" A0="+str(A0_chn)+" delta="+str(delta_chn))
                #
                print("Signal Energy - Sum")
                ti=copy.deepcopy(t_sngl[maxImpactDurationSensorN-1])
                #
                alfaS, betaS = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enveS, ti, do_lnT=False, do_lnY=True, vsh=0)
                #
                A0S=np.exp(alfaS)
                deltaS = -betaS
                #
                print("alfaS="+str(alfaS)+" betaS="+str(betaS)+" A0S="+str(A0S)+" deltaS="+str(deltaS))

                #print("alfa1="+str(alfa1)+" beta1="+str(beta1)+" A01="+str(A01)+" delta1="+str(delta1))
                #print("alfa2="+str(alfa2)+" beta2="+str(beta2)+" A02="+str(A02)+" delta2="+str(delta2))
                #print("alfaS="+str(alfaS)+" betaS="+str(betaS)+" A0S="+str(A0S)+" deltaS="+str(deltaS))
                #
                #env1=[]
                #env2=[]
                #envS=[]
                #
                #for i in range(len(ti)):
                #    #for i in range(len(ts)):
                #    #t=ts[i]-ts[0]
                #    t=ti[i]-ti[0]
                #    env1.append(A01*np.exp(-delta1*t))
                #    env2.append(A02*np.exp(-delta2*t))
                #    envS.append(A0S*np.exp(-delta2*t))
                #    #print(str(i)+" "+str(env1[i])+" "+str(env2[i])+" "+str(envS[i]))
                #
                #print("alfa1="+str(alfa1)+" beta1="+str(beta1)+" A01="+str(A01)+" delta1="+str(delta1))
                #print("alfa2="+str(alfa2)+" beta2="+str(beta2)+" A02="+str(A02)+" delta2="+str(delta2))
                #print("alfaS="+str(alfaS)+" betaS="+str(betaS)+" A0S="+str(A0S)+" deltaS="+str(deltaS))
                #
                #GraphName="Энергия сигналов, ступенчатая огибающая и аппроксимация экспонентой с вычислением и отображением декремента затухания - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
                #
                #plot_several1(
                #      [
                #        [
                #           [(ti, en1), (ti, enve1), (ti, env1)], 1
                #        ],
                #        [
                #           [(ti, en2), (ti, enve2), (ti, env2)], 1
                #        ],
                #        [
                #           [(ti, enS), (ti, enveS), (ti, envS)], 1
                #        ]
                #      ],
                #      [
                #        ["t, с", "Энергия сигнала", "Огибающая", "Аппроксимация: decr="+str(-beta1)],                  
                #        ["t, с", "Энергия сигнала", "Огибающая", "Аппроксимация: decr="+str(-beta2)],
                #        ["t, с", "Энергия сигнала", "Огибающая", "Аппроксимация: decr="+str(-betaS)]
                #      ],
                #      [
                #        [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                #        [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                #        [ {"color":"green"}, {"color":"red"}, {"color":"blue"}]
                #      ],
                #      GraphName
                #)
                #    
                ###

                env_allChns=[]
                envS=[]

                print("Calculating approximated exponent:")
                
                for sensorN in range(1, SensorsQuantity+1):
                    if do_printApproximatedExponentEnvelope:
                        print("Channel "+str(sensorN))
                    #
                    ti=copy.deepcopy(t_sngl[sensorN-1])
                    en_chn=copy.deepcopy(en_sngl_allChns[sensorN-1])
                    enve_chn=copy.deepcopy(enve_allChns[sensorN-1])
                    env_chn=copy.deepcopy(env_allChns[sensorN-1])
                    A0_chn=copy.deepcopy(A0_allChns[sensorN-1])
                    delta_chn=copy.deepcopy(delta_allChns[sensorN-1])
                    env_chn=[]
                    for i in range(len(ti)):
                        t=ti[i]-ti[0]
                        env_chn.append(A0_chn*np.exp(-delta_chn*t))
                        if do_printApproximatedExponentEnvelope:
                            print(str(i)+" "+str(env_chn[i]))
                        #
                    #
                    env_allChns.append(env_chn)
                #
                if do_printApproximatedExponentEnvelope:
                    print("Average by all channels for impact:")
                #
                ti=copy.deepcopy(t_sngl[maxImpactDurationSensorN-1])
                for i in range(len(ti)):
                    t=ti[i]-ti[0]
                    envS.append(A0S*np.exp(-deltaS*t))
                    if do_printApproximatedExponentEnvelope:
                        print(str(i)+" "+str(envS[i]))
                    #
                #

                #GraphName="Энергия сигналов, ступенчатая огибающая и аппроксимация экспонентой с вычислением и отображением декремента затухания - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
                GraphName="Энергия сигналов, ступенчатая огибающая и аппроксимация экспонентой с вычислением и отображением декремента затухания - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
                graph_data=[]
                graph_text=[]
                graph_colors=[]
                for sensorN in range(1, SensorsQuantity+1):
                    ti=copy.deepcopy(t_sngl[sensorN-1])
                    en_chn=copy.deepcopy(en_sngl_allChns[sensorN-1])
                    enve_chn=copy.deepcopy(enve_allChns[sensorN-1])
                    env_chn=copy.deepcopy(env_allChns[sensorN-1])
                    #
                    graph_data.append([[(ti, en_chn), (ti, enve_chn), (ti, env_chn)], 1])
                    graph_text.append(["t, с", "Энергия сигнала", "Огибающая", "Аппроксимация: decr="+str(-beta_allChns[sensorN-1])])
                    graph_colors.append([ {"color":"green"}, {"color":"red"}, {"color":"blue"}])
                #
                graph_data.append([[(ti, ensum), (ti, enveS), (ti, envS)], 1])
                graph_text.append(["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"])
                graph_colors.append([ {"color":"green"}, {"color":"red"}, {"color":"blue"}])
                GraphName="Энергия сигналов и огибающая (исключены провалы) - файлы "
                
        
                decr1=-beta1
                decr2=-beta2
                decrS=-betaS

                decrs1.append(decr1)
                decrs2.append(decr2)
                decrsS.append(decrS)

                decrs1s+=decr1
                decrs2s+=decr2
                decrsSs+=decrS

                countImpactsElaborated=impN+1

                decR1=decrs1s/countImpactsElaborated
                decR2=decrs2s/countImpactsElaborated
                decRS=decrsSs/countImpactsElaborated

                if countImpactsElaborated==1 or (countImpactsElaborated>1 and decr1>decr1Max):
                    decr1Max=decr1
                if countImpactsElaborated==1 or (countImpactsElaborated>1 and decr1<decr1Min):
                    decr1Min=decr1
                if countImpactsElaborated==1 or (countImpactsElaborated>1 and decr2>decr2Max):
                    decr2Max=decr2
                if countImpactsElaborated==1 or (countImpactsElaborated>1 and decr2<decr2Min):
                    decr2Min=decr2
                if countImpactsElaborated==1 or (countImpactsElaborated>1 and decrS>decrSMax):
                    decrSMax=decrS
                if countImpactsElaborated==1 or (countImpactsElaborated>1 and decrS<decrSMin):
                    decrSMin=decrS
                #

                #print("results of impact"+str(impactN)+"("+str(countImpactsElaborated)+")"+": decr1="+str(decr1)+" decr2="+str(decr2)+" decrS="
                #      +str(decrS)+". Medium vals: decr1="+str(decR1)+" decr2="+str(decR2)+" decrS="+str(decRS)+" decrSs="+str(decrsSs))
                print("results of impact"+str(impN)+": decr1="+str(decr1)+" decr2="+str(decr2)+" decrS="
                      +str(decrS)+". Medium vals: decr1="+str(decR1)+" decr2="+str(decR2)+" decrS="+str(decRS)+" decrSs="+str(decrsSs))
                #
                #---------------------------------------------------------------------------
                decr_all_fileOwnName_ending="_Decrement_AllImpacts.csv"
                if CaseN_1sensor1_2files1chn2_1file2chns3_another4==1 or CaseN_1sensor1_2files1chn2_1file2chns3_another4==2:
                    decr_all_fileOwnName_toWrite=dataRead.File[sensorN-1]
                elif CaseN_1sensor1_2files1chn2_1file2chns3_another4==3:
                    decr_all_fileOwnName_toWrite=dataRead.File[0]toWrite+"_chN"+str(sensorN-1)
                #
                
                #decr_all_header=["ImpactN", "chN", "t1", "t2", "dt", "decr_chn[imp]", "decrMedFrom1stTillCur_chn", "chN", "t1", "t2", "dt", "decr_chn[imp]", "decrMedFrom1stTillCur_chn", "decr_sumByChns[imp]", "decrMedFrom1stTillCur_sumByChns"]
                #if os.path.isfile(decr_all_fileName)==False:
                #    with open(decr_all_fileName, mode='w', newline='') as dst_f_sngl:
                #        writer_sngl = csv.writer(decr_all_header)
                ##
                #decr_all_header=[ ("chn", "t1", "t2", "dt", "decr_chn[imp]"), "ImpN", "decrAveBothChnCurImp", "decrAveBothChnImpsUptoCur"]
                #    
                with open(decr_all_fileName, mode='a', newline='') as dst_f_sngl:
                    writer_alllImps=csv.writer(decr_all_fileName)
                    if sensorN==1:
                        decrCur=decr1
                        decrCur=decr1
                    elif sensorN==2:

                    else:

                    #
                    writer_sngl.writerow(str(impN+1),str(sensorN), str(ti[0]), str(ti[-1]), )
                #
                # write! with impacts bounds and impacts length!
            #if do_Calc decrement        
        #for impN
    #if do_CheckAllSingleSignals:
    
    #---------------------------------------------------------------------------------------
    if do_computeSpectrum:
        #
        freqHB=freqHB_Smooth=65
        #
        fs=dataRead.fs[0]
        #
        spectrumWhole=[]
        spectrumWholeLimited=[]
        dfreqmin=100
        impactsSpectrumLengthes=[]
        #
        spectrumElaborated=[]
        spectrumElaboratedByLibFns=[]
        #
        print("for whole spectrum")
        for sensorN in range(1, SensorsQuantity+1):
            fileOwnName=fileOwnNames[sensorN-1]
            signal_chn=copy.deepcopy(signals[sensorN-1])
            print("spectrum (for each impasct)")
            freqs, amps = compute_spectrum(signal_chn, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)
            print(" spectrum: fs="+str(fs)+"; values of frequencies: "+str(len(freqs))+", values of amplitude: "+str(len(amps)))
            GraphName="Спектр колебаний (whole signal chN "+str(sensorN)+") - файл "+fileOwnName
            #GraphName=f"Спектр колебаний (single impact N "+str(impN+1)+" (t={impLB}...{impHB}) signal chN "+str(sensorN)+") - файл "+fileOwnName
            plot_signal(freqs, amps, title="Спектр . "+fileOwnName)
            print("Displaying graph of spectrum (whole signal chN "+str(sensorN)+")")
            plot_several1
            (
                [
                    [
                        [(freqs, amps)], 1
                    ]
                ],
                [
                    ["Частота, Гц", "Амплитуда"]
                    ],
                [
                
                ],
                GraphName
            )
            print("graph of spectrum  (whole signal chN "+str(sensorN)+") was displayed")
                #
                #writer.writerow([str(), "impactN", "tStart", "tFin", "freq", "Ampl"])
            #
            #spectrumQ=len(freqs)
            #for i in range(spectrumQ):
            #    spectrumPair=[]
            #    spectrumPair.append(sensorN)#0
            #    spectrumPair.append(impN)#spectrumPair.append(impNf)#1
            #    spectrumPair.append(t_sngl_chn[0])#2
            #    spectrumPair.append(t_sngl_chn[-1])#3
            #    spectrumQ=len(freqs)
            #    #
            #    freq=copy.deepcopy(freqs[i])
            #    if i>0:
            #        freqprev=freqs[i-1]
            #        if abs(freq-freqprev)<dfreqmin:
            #            dfreqmin=abs(freq-freqprev)
            #        #
            #    #
            #    amp=copy.deepcopy(amps[i])
            #    spectrumPair.append(freq)#freqs[i])#4
            #    spectrumPair.append(amp)#amps[i])#5
            #    #
            #    spectrumWhole.append(spectrumPair)
            #    if freq<=freqHB:
            #        spectrumWholeLimited.append(spectrumPair)
            #        print("writing ((erst)N"+str(len(spectrumWholeLimited))+"): "+"Channel "+str(spectrumPair[0])+" Impact "+str(spectrumPair[1])+" f="+str(spectrumPair[4])+" A="+str(spectrumPair[5]))
            #    #
            ##           
        # for sensorN spectrum - for whole signal
        if do_CheckAllSingleSignals:
            for impN in range(len(impacts)):
                impNf, impLB, impHB = ExtractImpactBounds2(impacts, impN+1)
                print(str(impN+1)+") impact N "+str(impNf)+" impLB="+str(impLB)+" impHB="+str(impHB))
                t_sngl=[]
                x_sngl=[]
                for sensorN in range(1, SensorsQuantity+1):
                    signal_chn=copy.deepcopy(signals[sensorN-1])
                    t_sngl_chn, x_sngl_chn = GetSingleImpactSignal(ts, signal_chn, impLB, impHB)
                    t_sngl.append(t_sngl_chn)
                    x_sngl.append(x_sngl_chn)
                #
                for sensorN in range(1, SensorsQuantity+1):
                    fileOwnName=fileOwnNames[sensorN-1]
                    t_sngl_chn=copy.deepcopy(t_sngl[sensorN-1])
                    x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                    #
                    if do_showSingleSignals_SeparatelyFromEachSensor:
                        plot_signal(t_sngl_chn, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар t={t_sngl_chn[0]} ... {t_sngl_chn[-1]} (исходный), канал"+str(sensorN-1))
                    #
                    print("spectrum (for each impasct)")
                    freqs, amps = compute_spectrum(x_sngl_chn, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)
                    print(" spectrum: fs="+str(fs)+"; values of frequencies: "+str(len(freqs))+", values of amplitude: "+str(len(amps))+"; values of time: "+str(len(t_sngl_chn))+", values of signal: "+str(len(x_sngl_chn)))
                    GraphName=f" G0 Спектр колебаний (single impact N "+str(impN+1)+" (t={impLB}...{impHB}) signal chN "+str(sensorN)+") - файл "+fileOwnName
                    plot_signal(freqs, amps, title=f"Спектр-удар {impN} N {impNf} t={t_sngl_chn[0]} ... {t_sngl_chn[-1]} ). "+fileOwnName)
                    print("Dysplaying graph of spectrum was displayed whole(single impact N "+str(impN+1)+" signal chN "+str(sensorN)+")")
                    plot_several1
                    (
                        [   
                            [
                                [(freqs, amps)], 1
                            ]
                        ],
                        [
                            ["Частота, Гц", "Амплитуда"]
                        ],
                        [
                
                        ],
                        GraphName
                    )
                    print("graph of spectrum was displayed whole(single impact N "+str(impN+1)+" signal chN "+str(sensorN)+" was displayed")
                    #
                    print("Writing spectrum")
                    #spectrumPair=[]
                    #spectrumPair.append(sensorN)#0
                    #spectrumPair.append(impN)#spectrumPair.append(impNf)#1
                    #spectrumPair.append(t_sngl_chn[0])#2
                    #spectrumPair.append(t_sngl_chn[-1])#3
                    spectrumQ=len(freqs)
                    impactsSpectrumLengthes.append(spectrumQ)
                    for i in range(spectrumQ):
                        spectrumPair=[]
                        spectrumPair.append(sensorN)#0
                        spectrumPair.append(impN)#spectrumPair.append(impNf)#1
                        spectrumPair.append(t_sngl_chn[0])#2
                        spectrumPair.append(t_sngl_chn[-1])#3
                        #
                        freq=copy.deepcopy(freqs[i])
                        if i>0:
                            freqprev=freqs[i-1]
                            if abs(freq-freqprev)<dfreqmin:
                                dfreqmin=abs(freq-freqprev)
                            #
                        #
                        amp=copy.deepcopy(amps[i])
                        spectrumPair.append(freq)#freqs[i])#4
                        spectrumPair.append(amp)#amps[i])#5
                        spectrumWhole.append(spectrumPair)
                        if freq<=freqHB:
                            spectrumWholeLimited.append(spectrumPair)
                            print("writing (N"+str(len(spectrumWholeLimited))+"): "+"Channel "+str(spectrumPair[0])+" Impact "+str(spectrumPair[1])+" f="+str(spectrumPair[4])+" A="+str(spectrumPair[5]))
                        #
                        if i<=3 or i>=spectrumQ-3:
                            print("Channel "+str(spectrumPair[0])+" Impact "+str(spectrumPair[1])+" t=("+str(spectrumPair[2])+".."+str(spectrumPair[3])+" spectrum Pair N "+str(i+1)+" of "+str(spectrumQ)+": f= "+str(spectrumPair[4])+" A = "+str(spectrumPair[5]))
                        #
                        
                    #for i in range(spectrumQ):
                    if do_Smoothing_Extremums: #  and impN==_impN_: # and sensorN==_chn_N_
                        #for sensorN in range (1, SensorsQuantity+1):
                        print("\nSpectrum for SMOOTHING peaks ")
                        print("\nInitial spectrum for smoothing")
                        GraphName=f" G2 Спектр колебаний FOR SMOOTHING INITIAL(single impact N "+str(impN+1)+" (t= {t_sngl_chn[0]} ... {t_sngl_chn[-1]} ) signal chN "+str(sensorN)+") - файл "+fileOwnName
                        GraphName=f" G2 Спектр колебаний FOR SMOOTHING INITIAL(single impact N "+str(impN+1)+" (t= "+str(t_sngl_chn[0])+" ... "+str(t_sngl_chn[-1])+" ) signal chN "+str(sensorN)+") - файл "+fileOwnName
                        #plot_signal(freqs, amps, title=f" G1 Спектр-удар {impN} N {impNf} t= {t_sngl_chn[0]} ... {t_sngl_chn[-1]} ). "+fileOwnName)
                        print("Dysplaying graph of spectrum FOR SMOOTHING was displayed whole(single impact N "+str(impN+1)+" signal chN "+str(sensorN)+")")
                        plot_several1(
                                [   
                                    [
                                        [(freqs, amps)], 1
                                    ]
                                ],
                                [
                                    ["Частота, Гц", "Амплитуда"]
                                ],
                                [
                         
                                ],
                                GraphName
                            )
                        freqsMA=copy.deepcopy(freqs)
                        amplsMA=copy.deepcopy(amps)
                        freqsML=copy.deepcopy(freqs)
                        amplsML=copy.deepcopy(amps)
                        freqsMI=copy.deepcopy(freqs)
                        amplsMI=copy.deepcopy(amps)
                        freqsHBNN=0
                        if freqHB>0:
                            for i in range(len(freqsMA)):
                                if freqsMA[i]==freqHB or(freqsMA[i-1]<freqHB and freqsMA[i]>freqHB):
                                    break
                                freqsHBNN=i+1
                                #
                            #
                            print("freqHB="+str(freqHB)+" last shortened f["+str(freqsHBNN)+"]="+str(freqsMA[freqsHBNN-1]))
                            if freqsHBNN>0:
                                freqsMA=freqsMA[:freqsHBNN-1]
                                amplsMA=amplsMA[:freqsHBNN-1]
                                freqsML=freqsML[:freqsHBNN-1]
                                amplsML=amplsML[:freqsHBNN-1]
                                freqsMI=freqsMI[:freqsHBNN-1]
                                amplsMI=amplsMI[:freqsHBNN-1]
                            #
                        #
                        print("\nSMOOTHED spectrum")
                        print(" spectrum: fs="+str(fs)+"; values of frequencies: "+str(len(freqsMA))+", values of amplitude: "+str(len(amplsMA))+"; values of time: "+str(len(t_sngl_chn))+", values of signal: "+str(len(x_sngl_chn)))
                        #GraphName=f"G4 Спектр колебаний FOR SMOOTHING SHORTENED ONLY (single impact N "+str(impN+1)+" (t={t_sngl_chn[0]} ... {t_sngl_chn[-1]}) signal chN "+str(sensorN)+") - файл "+fileOwnName
                        #GraphName=f"G4 Спектр колебаний FOR SMOOTHING SHORTENED ONLY (single impact N "+str(impN+1)+" (t="+str(t_sngl_chn[0])+" ... "+str(t_sngl_chn[-1])+" signal chN "+str(sensorN)+") - файл "+fileOwnName
                        #plot_signal(freqsMA, amplsMA, title=f"G3 Спектр  FOR SMOOTHING SHORTENED ONLY-удар {impN} N {impNf} t={t_sngl_chn[0]} ... {t_sngl_chn[-1]} ). "+fileOwnName)
                        #print("Dysplaying graph of spectrum FOR SMOOTHING SHORTENED ONLY was displayed whole(single impact N "+str(impN+1)+" signal chN "+str(sensorN)+")")
                        #plot_several1(
                        #        [   
                        #            [
                        #                [(freqsMA, amplsMA)], 1
                        #            ]
                        #        ],
                        #        [
                        #            ["Частота, Гц", "Амплитуда"]
                        #        ],
                        #        [
                        # 
                        #        ],
                        #        GraphName
                        #    )
                        #print("\n")
                        #
                        print("SMOOTHING peaks of spectrum")
                        data, ContinSmoothPeaks, CallN2 = MyFindPeaksAndSmoothRestXY1(amplsMA, freqsMA, AllExtrs0NurMaxs1NurMins2=1, MinValsToIgnore=10, prominence=1.5, CallN1=1, CallN=1, vsh=1)
                        print(" spectrum: fs="+str(fs)+"; values of frequencies: "+str(len(freqsMA))+", values of amplitude: "+str(len(amplsMA))+"; values of time: "+str(len(t_sngl_chn))+", values of signal: "+str(len(x_sngl_chn)))
                        GraphName=f"G6 Спектр колебаний SMOOTHED (single impact N "+str(impN+1)+" (t={t_sngl_chn[0]} ... {t_sngl_chn[-1]}) signal chN "+str(sensorN)+") - файл "+fileOwnName
                        #plot_signal(freqsMA, amplsMA, title=f"G5 Спектр-удар {impN} N {impNf} t={t_sngl_chn[0]} ... {t_sngl_chn[-1]} ). "+fileOwnName)
                        print("Dysplaying graph of spectrum SMOOTHED was displayed whole(single impact N "+str(impN+1)+" signal chN "+str(sensorN)+")")
                        #plot_several1(
                        #        [   
                        #            [
                        #                [(freqsMA, amplsMA)], 1
                        #            ]
                        #        ],
                        #        [
                        #            ["Частота, Гц", "Амплитуда"]
                        #        ],
                        #        [
                        # 
                        #        ],
                        #        GraphName
                        #    )
                        print("\n")
                        print("Answer - List of extremums in smoothed spectrum:")
                        for i in range(len(data)):
                            print("Peak "+str(i+1)+" f= "+str(data[i][2])+" A= "+str(data[i][3])+" peak_width: left= "+str(data[i][4])+" right: "+str(data[i][5])+" is higher than values around: left: "+str(data[i][9])+" rigtht: "+str(data[i][10]))
                        #
                        print("\n")
                        dataL=len(data)
                        for i in range(len(data)):
                            #spectrumElement=data[i]
                            spectrumPair=[]
                            spectrumPair.append(sensorN)#0
                            spectrumPair.append(impN)#spectrumPair.append(impNf)#1
                            spectrumPair.append(t_sngl_chn[0])#2
                            spectrumPair.append(t_sngl_chn[-1])#3
                            if i>0:
                                freqprev=freq
                            #
                            freq=copy.deepcopy(data[i][2])# freqs[i]) #4 # element.append(X[i])#2
                            amp=copy.deepcopy(data[i][3])# amps[i]) #5 # element.append(Y[i])#3
                            if i>0:
                                if abs(freq-freqprev)<dfreqmin:
                                    dfreqmin=abs(freq-freqprev)
                                #
                            #
                            spectrumPair.append(freq)#4
                            spectrumPair.append(amp)#5
                            spectrumElaborated.append(spectrumPair)
                        #----------------
                        GraphName=f"G10 Спектр колебаний SMOOTHED (single impact N "+str(impN+1)+" (t={t_sngl_chn[0]} ... {t_sngl_chn[-1]}) signal chN "+str(sensorN)+") - файл "+fileOwnName
                        GraphName=f" Спектр колебаний SMOOTHED (single impact N "+str(impN+1)+" (t="+str(t_sngl_chn[0])+" ... "+str(t_sngl_chn[-1])+") signal chN "+str(sensorN)+") - файл "+fileOwnName
                        freqsML, amplsML, thePeaks=  find_spectrum_peaks(freqsML, amplsML)
                        plot_several1([
                            [
                               [(freqsMI, amplsMI)], 1, 
                            ],
                            [
                               [(freqsMA, amplsMA)], 1,
                            ],
                            [
                               [(freqsML, amplsML)], 1
                            ]
                          ],
                          [
                            ["Частота (исх сокр), Гц", "Амплитуда (исх сокр)"],                  
                            ["Частота, Гц (авт алг)", "Амплитуда (авт алг)"],
                            ["Частота, Гц (биб алг)", "Амплитуда (биб алг)"]
                          ],
                          [
                            [ {"color":"blue"}],
                            [ {"color":"green"}],
                            [ {"color":"red"}]
                          ],
                          GraphName
                        )
                    # if  do_Smoothing_Extremums  and impN==_impN_: # and sensorN==_chn_N_
                #for sensor N
                #spectrumWhole.append(spectrumPair)
            #for impact N
            print("spectrumWhole: "+str(len(spectrumWhole))+" values")
            print("spectrumWhole(limited): "+str(len(spectrumWholeLimited))+" values")
            for i in range(len(impactsSpectrumLengthes)):
                print("impactN"+str(i+1)+" freqs: "+str(impactsSpectrumLengthes[i]))
            #
            print("spectrumElaborated: "+str(len(spectrumElaborated))+" values")
            for i in range(len(spectrumElaborated)):
                print("impactN"+str(i+1)+" freqs: "+str(spectrumElaborated[i]))
            #
            #------------------------------------------------------------------------------------------
            fileNameEnding_SpectrumIni="_spectrumIni.csv"
            spectrumIni_fileOwnName=dataRead.File[0]+fileNameEnding_SpectrumIni
            spectrumIni_fileFullName=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+spectrumIni_fileOwnName
            with open(spectrumIni_fileFullName, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["N", "ImpactN", "SensorN", "tStart", "tFin", "Freq", "Ampl"])
                for sensorN in range(1, SensorsQuantity+1):
                    spPN=0
                    for spectrumPair in spectrumWhole:
                        spPN+=1
                        chN=spectrumPair[0]
                        if chN==sensorN:
                            row=[]
                            row.append(str(spPN))
                            for i in range(5+1):
                                row.append(str(spectrumPair[i]))
                            #
                            writer.writerow(row)
                        #
                    #
                #
            #
            print("file of spectrum (initial) "+spectrumIni_fileFullName+" written successfully")
            #
            fileNameEnding_SpectrumChosen="_spectrumChosen.csv"
            spectrumChosen_fileOwnName=dataRead.File[0]+fileNameEnding_SpectrumChosen
            spectrumChosen_fileFullName=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+spectrumChosen_fileOwnName
            with open(spectrumChosen_fileFullName, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["N", "ImpactN", "SensorN", "tStart", "tFin", "Freq", "Ampl"])
                for sensorN in range(1, SensorsQuantity+1):
                    spPN=0
                    for spectrumPair in spectrumElaborated:
                        spPN+=1
                        chN=spectrumPair[0]
                        if chN==sensorN:
                            row=[]
                            row.append(str(spPN))
                            for i in range(5+1):
                                row.append(str(spectrumPair[i]))
                            #
                            writer.writerow(row)
                        #
                    #
                #
            #
            print("file of spectrum (chosen, elaborated) "+spectrumChosen_fileFullName+" written successfully")
        # if do_CheckAllSingleSignals ----------------------------------------------------------------------
        #if do_Smoothing_Extremums:
        #    print("Spectrum for tryinng: ChnN "+str(_chN_)+" Impsact N "+str(_impN_))
        #    fileOwnName=fileOwnNames[_chN_-1]
        #    t_sngl_chn=copy.deepcopy(t_sngl[_chN_-1])
        #    x_sngl_chn=copy.deepcopy(x_sngl[_chN_-1])
        #    #
        #    freqs, amps = compute_spectrum(x_sngl_chn, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)
        #    if freqHB>0:
        #        print("len(freqs)="+str(len(freqs))+" freq[0]="+str(freqs[0])+" freqs["+str(len(freqs))+"]="+str(freqs[len(freqs)-1]))
        #        for i in range(len(amps)):
        #            if i>1 and amps[i]==freqHB or (amps[i-1]<freqHB and amps[i]>freqHB):
        #                freqHBN=i+1
        #                break
        #            #
        #        #
        #        freqs=freqs[:freqHBN-1]
        #        amps=amps[:freqHBN-1]
        #        print("now len(freqs)="+str(len(freqs))+" freq[0]="+str(freqs[0])+" freqs["+str(freqHBN)+"]="+str(freqs[freqHBN-1]))
        #    #
        #   
        #    print(" spectrum: fs="+str(fs)+"; values of frequencies: "+str(len(freqs))+", values of amplitude: "+str(len(amps))+"; values of time: "+str(len(t_sngl_chn))+", values of signal: "+str(len(x_sngl_chn)))
        #    GraphName=f"Спектр колебаний (single impact N "+str(impN+1)+" (t={impLB}...{impHB}) signal chN "+str(sensorN)+") - файл "+fileOwnName
        #    plot_signal(freqs, amps, title=f"Спектр-удар {impN} N {impNf} t={t_sngl_chn[0]} ... {t_sngl_chn[-1]} ). "+fileOwnName)
        #    print("Dysplaying graph of spectrum was displayed whole(single impact N "+str(impN+1)+" signal chN "+str(sensorN)+")")
        #    plot_several1
        #    (
        #        [   
        #            [
        #                [(freqs, amps)], 1
        #            ]
        #        ],
        #        [
        #            ["Частота, Гц", "Амплитуда"]
        #        ],
        #        [
        #        
        #        ],
        #        GraphName
        #    )
        #    print("graph of spectrum was displayed whole(single impact N "+str(impN+1)+" signal chN "+str(sensorN)+" was displayed")
        #    #
        ##-----------------------
        # freqHB=freqHB_TryClust # no need, fprmed before
        #spectrumToClust=copy.deepcopy(spectrumWholeLimited)
        spectrumToClust=copy.deepcopy(spectrumElaborated)
        #------------------------
        if do_clustrerizeSpectrum:
            ##_chn_N_=1
            #_impN_=5
            #
            dfCluster=[]
            for sensorN in range(1, SensorsQuantity+1):
                dfCluster.append(dfreqmin)
                print("channnel "+str(sensorN)+": dfCluster="+str(dfCluster[sensorN-1]))
            #
            print("For channel(?): "+str(len(spectrumToClust))+" values. d freq min = "+str(dfreqmin))
            #print(spectrumWhole)
            for spectrumPair in spectrumToClust:
                if spectrumPair[0]==_chn_N_ and spectrumPair[1]==_impN_:
                    print("Channel "+str(spectrumPair[0])+" Impact "+str(spectrumPair[1])+" t = ("+str(spectrumPair[2])+".."+str(spectrumPair[3])+"): f= "+str(spectrumPair[4])+" A = "+str(spectrumPair[5]))            
                #
            #
            freqs_Clusters=[]
            ampls_Clusters=[]
            for sensorN in range(1, SensorsQuantity+1):
                freqs_Clusters_chn=[]
                ampls_Clusters_chn=[]
                for spectrumPair in spectrumToClust:
                    if spectrumPair[1]==_impN_ and spectrumPair[0]==sensorN:
                        freq=spectrumPair[4]
                        ampl=spectrumPair[5]
                        freqs_cluster=[]
                        freqs_cluster.append(freq)
                        freqs_Clusters_chn.append(freqs_cluster)
                        #
                        ampls_cluster=[]
                        ampls_cluster.append(ampl)
                        ampls_Clusters_chn.append(ampls_cluster)
                        print("(step1) - Pair ChN"+str(spectrumPair[0])+" Impact "+str(spectrumPair[1])+" f="+str(spectrumPair[4])+" A="+str(spectrumPair[5])+"_impN_="+str(_impN_)+"-fits at 1st step")
                    else:
                        print("(step1) - Pair ChN"+str(spectrumPair[0])+" Impact "+str(spectrumPair[1])+" f="+str(spectrumPair[4])+" A="+str(spectrumPair[5])+"_impN_="+str(_impN_)+"- not fit at 1st step")
                    #
                #for spectrumPair
                freqs_Clusters.append(freqs_Clusters_chn)
                ampls_Clusters.append(ampls_Clusters_chn)
            # for sensorN 
            freqs_repres_allChns=[] # array of representative (mean) values of each cluster of freqs in clusters array
            ampls_repres_allChns=[] # array of representative (mean) values of each cluster of ampls in clusters array
            for sensorN in range(1, SensorsQuantity+1):
                freqs_repres_chn=[]
                ampls_repres_chn=[]
                freqs_Clusters_chn=freqs_Clusters[sensorN-1]
                ampls_Clusters_chn=ampls_Clusters[sensorN-1]
                for clusterN in range(1, len(freqs_Clusters_chn)+1):
                    #for freqs_cluster in freqs_Clusters_chn:
                    freqs_cluster=freqs_Clusters_chn[clusterN-1]
                    ampls_cluster=ampls_Clusters_chn[clusterN-1]
                    #
                    freqs_cluster=np.array(freqs_cluster)
                    freq_repres=np.mean(freqs_cluster)
                    freqs_cluster=freqs_cluster.tolist()
                    freqs_repres_chn.append(freq_repres)
                    #
                    ampls_cluster=np.array(ampls_cluster)
                    ampl_repres=np.mean(ampls_cluster)
                    ampls_cluster=ampls_cluster.tolist()
                    ampls_repres_chn.append(ampl_repres)
                #
                freqs_repres_allChns.append(freqs_repres_chn)
                ampls_repres_allChns.append(ampls_repres_chn)
            #
            print("forming freqs clusters (by one impact, for each channel)")
            for sensorN in range(1, SensorsQuantity+1):
                print("initial clusters of channel "+str(sensorN)+": ")
                freqs_repres_chn=copy.deepcopy(freqs_repres_allChns[sensorN-1])
                freqs_Clusters_chn=copy.deepcopy(freqs_Clusters[sensorN-1])
                for i in range(len(freqs_Clusters_chn)):
                    print("clusterN "+str(i+1)+" med val="+str(freqs_repres_chn[i])+" all vals:")
                    print(freqs_Clusters_chn[i])
                #
            #--------------------------------------------------------------------------------------------
            print("\nAppending freqs cluster by other vals")
            for sensorN in range(1, SensorsQuantity+1):
                print("\nSensor (channel) N "+str(sensorN))
                freqs_Clusters_chn=copy.deepcopy(freqs_Clusters[sensorN-1])
                ampls_Clusters_chn=copy.deepcopy(ampls_Clusters[sensorN-1])
                freqs_repres_chn=copy.deepcopy(freqs_repres_allChns[sensorN-1])
                print("freqs_repres_chn ("+str(sensorN)+"): ",freqs_repres_chn)
                ampls_repres_chn=copy.deepcopy(ampls_repres_allChns[sensorN-1])
                for spectrumPairN in range(1, len(spectrumToClust)):
                    spectrumPair=spectrumToClust[spectrumPairN-1]
                    print("(step 2) Pair: ChN "+str(spectrumPair[0])+" Impact "+str(spectrumPair[1])+" t="+str(spectrumPair[2])+".."+str(spectrumPair[3])+" f= "+str(spectrumPair[4])+" A="+str(spectrumPair[5]))
                    if spectrumPair[0]==sensorN and not (spectrumPair[1]==_impN_):
                        print("ChN "+str(spectrumPair[0]) +" = "+str(sensorN)+" Impact "+str(spectrumPair[1])+" != _impN_="+str(_impN_)+" - elaborating")
                        #spectrumPair=spectrumToClust[spectrumPairN-1]
                        freq=spectrumPair[4]
                        ampl=spectrumPair[5]
                        #
                        #defining position in list of repres vals 
                        #
                        poss=valIsAtPos(freqs_repres_chn, freq, eps=dfCluster[sensorN-1], vsh=0)
                        clustersL=len(freqs_repres_chn)
                        #
                        #print("clusterL= freqs_repres_chn: "+str(len(freqs_repres_chn))+" = (): ")
                        #
                        if poss.equalNN>0:
                            significantNN=poss.equalNN
                        elif poss.lessNN>0:
                            significantNN=poss.lessNN
                        elif poss.isLess:
                            significantNN=1
                        elif poss.isGreater:
                            significantNN=clustersL
                        else:
                            print("Error defining position!")
                            print("freq, whose pos to def: "+str(freq)+"; dFreqMin(chN)="+str(dfCluster[sensorN-1])+"; Need to define ins position among: ")
                            print(freqs_repres_chn)
                        #
                        if showCurFreqCluster_NeededFragmentOnlyNotWhole==False:
                            print("Current frequences cluster (whole, all "+str(clustersL)+" values) before elaboration this value:")
                            print(freqs_repres_chn)
                        else:
                            print("Current frequences cluster (fragment; whole  includes "+str(clustersL)+" values) before elaboration this value:")
                            s=ReturnSomeArrayValsFirstLastAndNearestToNN_asStr(freqs_repres_chn, significantNN)
                            print(s)
                            s=""
                        #if show fragm
                        #print("elaborating")
                        if poss.equalNN>0:
                            #freqs_Clusters[sensorN-1]=freqs_Clusters_chn
                            #freqs_Clusters_chn[poss.equalNN-1]=freqs_cluster
                            #freqs_cluster=freqs_Clusters[sensorN-1][poss.equalNN-1]
                            freqs_Clusters[sensorN-1][poss.equalNN-1].append(freq)
                            ampls_Clusters[sensorN-1][poss.equalNN-1].append(ampl)
                            significantNN=poss.equalNN
                            #clustersL=len(freqs_repres_chn)
                            #freqs_repres_allChns[sensorN-1][poss.equalNN-1]
                            #freqs_repres_chn=freqs_repres_allChns[sensorN-1]
                            #freq_repres=freqs_repres_chn[poss.equalNN-1] - single freq, repres (mean) val
                            print("analyzed freq "+str(freq)+" is equal to f["+str(poss.equalNN)+"]="+str(freqs_repres_chn[poss.equalNN-1])+"- adding to existing cluster")
                        else:#analyzed freq is not equal to existing
                            print("new value - forming new cluster")
                            freqs_cluster=[]
                            ampls_cluster=[]
                            freqs_cluster.append(freq)
                            ampls_cluster.append(ampl)
                            if poss.lessNN>0:
                                arr1DIns(freqs_Clusters[sensorN-1], freqs_cluster, poss.lessNN+1, vsh=0)
                                arr1DIns(ampls_Clusters[sensorN-1], ampls_cluster, poss.lessNN+1, vsh=0)
                                print("f["+str(poss.lessNN)+"]="+str(freqs_repres_chn[poss.lessNN-1])+" < f="+str(freq)+"< f["+str(poss.lessNN+1)+"]="+str(freqs_repres_chn[poss.lessNN+1-1])+" => inserting to pos N "+str(poss.lessNN+1))
                                arr1DIns(freqs_repres_chn, freq, poss.lessNN+1, vsh=0)
                            elif poss.isLess:
                                arr1DIns(freqs_Clusters[sensorN-1], freqs_cluster, 1, vsh=0)
                                arr1DIns(ampls_Clusters[sensorN-1], ampls_cluster, 1, vsh=0)
                                print("f[1]="+str(freqs_repres_chn[1-1])+" < f="+str(freq)+" => inserting to 1st position")
                                arr1DIns(freqs_repres_chn, freq, 1, vsh=0)
                            elif poss.isGreater:
                                freqs_Clusters[sensorN-1].append(freqs_cluster)
                                ampls_Clusters[sensorN-1].append(ampls_cluster)
                                print("f["+str(len(freqs_repres_chn))+"]="+str(freqs_repres_chn[len(freqs_repres_chn)-1])+" < f="+str(freq)+" => adding")
                            else:
                                print("incorrect position definition: neither equal, nor not less or greater")
                            #
                        #
                        clustersL=len(freqs_repres_chn)
                        #
                        freqs_repres_chn=[]
                        ampls_repres_chn=[]
                        freqs_Clusters_chn=copy.deepcopy(freqs_Clusters[sensorN-1])
                        ampls_Clusters_chn=copy.deepcopy(ampls_Clusters[sensorN-1])
                        for clusterN in range(1, len(freqs_Clusters_chn)+1):
                            #for freqs_cluster in freqs_Clusters_chn:
                            freqs_cluster=freqs_Clusters_chn[clusterN-1]
                            ampls_cluster=ampls_Clusters_chn[clusterN-1]
                            #
                            freqs_cluster=np.array(freqs_cluster)
                            freq_repres=np.mean(freqs_cluster)
                            freqs_cluster=freqs_cluster.tolist()
                            freqs_repres_chn.append(freq_repres)
                            #
                            ampls_cluster=np.array(ampls_cluster)
                            ampl_repres=np.mean(ampls_cluster)
                            ampls_cluster=ampls_cluster.tolist()
                            ampls_repres_chn.append(ampl_repres)
                            #
                        #for all clusters in channel
                        #
                        if showCurFreqCluster_NeededFragmentOnlyNotWhole==False:
                            print("Current frequences cluster (whole, all "+str(clustersL)+" values) after elaboration this value:")
                            print(freqs_repres_chn)
                        else:
                            print("cluster (fragment, whole includes "+str(clustersL)+" values) after elaboration this value:")
                            s=ReturnSomeArrayValsFirstLastAndNearestToNN_asStr(freqs_repres_chn, significantNN)
                            print(s)
                            s=""
                        #
                        freqs_repres_allChns[sensorN-1]=copy.deepcopy(freqs_repres_chn)
                        ampls_repres_allChns[sensorN-1]=copy.deepcopy(ampls_repres_chn)
                    else:# spectrumPair[1]==_impN_ or not (spectrumPair[0]==sensorN): # S'nod pair: exy _impN_ et nur nod'd sensorN
                        print("pair chN "+str(sensorN)+" impN "+str(spectrumPair[1])+" - not needed (sensorN="+str(sensorN)+" _impN_="+str(_impN_)+")")
                        #print("this comb of impact is already elaborated")
                    #if show
                    #freqs_repres_allChns[sensorN-1]=copy.deepcopy(freqs_repres_chn)
                    #ampls_repres_allChns[sensorN-1]=copy.deepcopy(ampls_repres_chn)
                    # not all conds ma nur if needed Ns
                #for spectrumPairN in range(1, len(spectrumToClust
            #for sensorN        
            #
            print("\nUnited spectrum ("+str()+" values):") # shows wrong ampls
            minL=[]
            maxL=[]
            minA=[]
            maxA=[]
            #
            minLN1=[]
            maxLN1=[]
            minAN1=[]
            maxAN1=[]
            for sensorN in range(1, SensorsQuantity+1):
                minL.append(100)
                maxL.append(0)
                minA.append(100)
                maxA.append(0)
                #
                minLN1.append(0)
                maxLN1.append(0)
                minAN1.append(0)
                maxAN1.append(0)
            #
            for sensorN in range(1, SensorsQuantity+1):
                clustersQ=len(freqs_Clusters[sensorN-1])
                freqs_Clusters_chn=copy.deepcopy(freqs_Clusters[sensorN-1])
                ampls_Clusters_chn=copy.deepcopy(ampls_Clusters[sensorN-1])
                freqs_repres_chn=copy.deepcopy(freqs_repres_allChns[sensorN-1])
                ampls_repres_chn=copy.deepcopy(ampls_repres_allChns[sensorN-1])
                print("\nSensor (channel) N "+str(sensorN)+" - "+str(clustersQ)+" clustars of freqs")
                for clusterN in range(1, clustersQ+1):
                    freqs_cluster=copy.deepcopy(freqs_Clusters_chn[clusterN-1])
                    ampls_cluster=copy.deepcopy(ampls_Clusters_chn[clusterN-1])
                    freq_repr=freqs_repres_chn[clusterN-1]
                    ampl_repr=ampls_repres_chn[clusterN-1]
                    clusterL=len(freqs_cluster)
                    print("cluster N "+str(clusterN)+" has values: "+str(clusterL)+" mean freq val: "+str(freq_repr)+" repr val of Ampl: "+str(ampl_repr)+" (of cource vals of ampls: "+str(len(ampls_cluster))+")")
                    #if compute spectrum
                    #print("freqs_cluster: ", freqs_cluster)
                    print("freqs_cluster: ")
                    print(freqs_cluster)
                    #print("ampls_cluster: ", ampls_cluster)
                    print("ampls_cluster: ")
                    print(ampls_cluster)
                    if clusterN==1:
                        minL[sensorN-1]=clusterL
                        maxL[sensorN-1]=clusterL
                        minA[sensorN-1]=ampl_repr
                        maxA[sensorN-1]=ampl_repr
                    else:
                        if clusterL<minL[sensorN-1]:
                            minL[sensorN-1]=clusterL
                            minLN1[sensorN-1]=clusterN
                        #
                        if clusterL>maxL[sensorN-1]:
                            maxL[sensorN-1]=clusterL
                            maxLN1[sensorN-1]=clusterN
                            print("current greatest cluster L (N "+str(clusterN)+")")
                        #
                        if ampl_repr<minA[sensorN-1]:
                            minA[sensorN-1]=ampl_repr
                            minAN1[sensorN-1]=clusterN
                        #
                        if ampl_repr>maxA[sensorN-1]:
                            maxA[sensorN-1]=ampl_repr
                            maxAN1[sensorN-1]=clusterN
                            print("current greatest cluster A (N "+str(clusterN)+")")
                        #
                    #
                #for clusterN
            #for sensorN
            maxANs_allChns=[]
            maxLNs_allChns=[]
            for sensorN in range(1, SensorsQuantity+1):
                maxANs_chn=[]
                maxLNs_chn=[]
                for clusterN in range(1, clustersQ+1):
                    L=len(freqs_Clusters[sensorN-1][clusterN-1])
                    A=ampls_repres_allChns[sensorN-1][clusterN-1]
                    if L==maxL[sensorN-1]:
                        maxLNs_chn.append(clusterN)
                    #
                    if abs(A-maxA[sensorN-1])<minA[sensorN-1]/10:
                        maxANs_chn.append(clusterN)
                    #
                #
                maxLNs_allChns.append(maxLNs_chn)
                maxANs_allChns.append(maxANs_chn)
            #
            print("\n")
            for sensorN in range(1, SensorsQuantity+1):
                print("ChN"+str(sensorN)+"- maxLNs: "+str(maxLNs_allChns[sensorN-1]))
                print("ChN"+str(sensorN)+"- maxANs: "+str(maxANs_allChns[sensorN-1]))
                print("ChN"+str(sensorN)+"- maxL="+str(maxL[sensorN-1])+"; maxA="+str(maxA[sensorN-1]))
                print("ChN"+str(sensorN)+"- minL="+str(minL[sensorN-1])+"; minA="+str(minA[sensorN-1]))
            #
            print("\nClustrers characteristics:")
            #print("clusters L: min L="+str(minL[sensorN-1])+" max L="+str(maxL[sensorN-1])+"; Ampl vals: min A="+str(minA[sensorN-1])+" max A="+str(maxA[sensorN-1]))
            clusters_Chars_AllChns=[]
            for sensorN in range(1, SensorsQuantity+1):
                clusters_Chars_chn=[]
                clustersQ=len(freqs_Clusters[sensorN-1])
                freqs_Clusters_chn=copy.deepcopy(freqs_Clusters[sensorN-1])
                ampls_Clusters_chn=copy.deepcopy(ampls_Clusters[sensorN-1])
                freqs_repres_chn=copy.deepcopy(freqs_repres_allChns[sensorN-1])
                ampls_repres_chn=copy.deepcopy(ampls_repres_allChns[sensorN-1])
                print("\nSensor (channel) N "+str(sensorN)+" - "+str(clustersQ)+" clustars of freqs")
                #print("clusters L: min L="+str(minL[sensorN-1])+" max L="+str(maxL[sensorN-1])+"; Ampl vals: min A="+str(minA[sensorN-1])+" max A="+str(maxA[sensorN-1]))
                print("clusters L: min L="+str(minL[sensorN-1])+" max L="+str(maxL[sensorN-1])+" last N of max L="+str(maxLN1[sensorN-1]))
                print("clusters A: min A="+str(minA[sensorN-1])+" max A="+str(maxA[sensorN-1])+" last N of max A="+str(maxAN1[sensorN-1]))
                #print("clusters L: min L="+str(minL[sensorN-1])+" max L="+str(maxL[sensorN-1])+"; Ampl vals: min A="+str(minA[sensorN-1])+" max A="+str(maxA[sensorN-1]))
                #minLNs=[]
                #maxLNs=[]
                #minANs=[]
                #maxANs=[]
                clusters_char_chn=[]
                for clusterN in range(1, clustersQ+1):
                    freqs_cluster=copy.deepcopy(freqs_Clusters_chn[clusterN-1])
                    ampls_cluster=copy.deepcopy(ampls_Clusters_chn[clusterN-1])
                    freq_repr=freqs_repres_chn[clusterN-1]
                    ampl_repr=ampls_repres_chn[clusterN-1]
                    clusterL=len(freqs_cluster)
                    cluster_char=[]
                    cluster_char.append(sensorN)#0
                    cluster_char.append(clusterN)#1
                    cluster_char.append((ampl_repr-minA[sensorN-1])/(maxA[sensorN-1]-minA[sensorN-1]))#2
                    cluster_char.append((clusterL-minL[sensorN-1])/(maxL[sensorN-1]-minL[sensorN-1]))#3
                    print("clusterN "+str(clusterN)+" values: "+str(clusterL)+" partL: ("+str(cluster_char[3])+"); mean freq val: "+str(freq_repr)+" repr val of Ampl: "+str(ampl_repr)+" (partA: "+str(cluster_char[2])+")")
                    clusters_char_chn.append(cluster_char)
                #for clusterN
                clusters_Chars_AllChns.append(clusters_char_chn)
            #for sensorN
        #if clustertize
    #
    print("Step3 (2026) finishes working")
        
