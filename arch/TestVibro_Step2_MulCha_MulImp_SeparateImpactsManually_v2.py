from MyPyVibroLib import *

if __name__ == "__main__":

    print("Step2 starts working")

    do_WriteAllImpactsNotSingle=True
    
    fileEnding_toRead="_signal_whole.csv"
    #fileEnding_toWrite="_SingleImpact"+".csv
    fileEnding_toWrite0="_SingleImpactSignal"+".csv"
    fileEnding_toWrite1="_ImpactsRanges"+".csv"
    #
    PathToNamesFile="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\data"
    #
    with open(PathToNamesFile+"\\FolderAndFiles.csv", newline='') as f:
        reader = csv.DictReader(f)
        LineN=0
        for row in reader:
            LineN+=1
            if LineN==1:
                filePath=row["Value"]
            elif LineN==2:
                QFiles=int(row["Value"])

    print("path: "+filePath)
    print("Files: "+str(QFiles))
    
    SignalCharFileOwnName="FileChar.csv"
    #
    filePathIniData=filePath+"\\"+"data"#+"\\"+"IniData"
    filePathResults=filePath+"\\"+"data"#+"\\"+"Results"
    filePathData=filePath+"\\"+"data"#+"\\"+"Results"
    SignalCharFileFullName=filePathIniData+"\\"+SignalCharFileOwnName
    #filenames =[]
    #
    #reading FileChar.csv all
    #ef maq-channel the file wa ute nur uz fs, 2 id'l senzs lif'te id'l process ain 2 files, so tic file s'not uz fs nur et nur 1 line can b lir'd, et file
    #um maq-channel the file s'ute uz fs et names, ob by 1-channel wa 2 .wav-files et 2 csv files, et nu es 1 .wav file et 2 csv files uz je channel
    #so uz 1-channel es 2 .wav-files et 2 .csv-files co id'l names, et uz 2-channel es 1 .wav-file et 2 .csv-files.
    #et efce ef maq-channel own names o' .csv-files wa al o' .wav-files, et nu by maq-channel uz arbf data s'ute nur 2 .csv-files, so nu ini data s'csv-files co channel N in names
    #
    #fN, fNm, fs, tmax, es = ReadDiscretFreq(SignalCharFileFullName)
    fileOwnNames,     fs, tms, ess = ReadIniDataNamesAndFreq(SignalCharFileFullName)
    dt=1/fs
    tmax=tms[0]#ob fs s'id'l
    #
    #ImpactBoundsFileName0=""
    ImpactBoundsFileName1=""
    #
    fN=0#
    for fNm in fileOwnNames:#
        fN+=1#
        es=ess[fN-1]
        tmax=tms[fN-1]
        print("N "+str(fN)+" "+fNm+" fs="+str(fs)+" => dt=1/fs="+str(dt)+" tmax="+str(tmax)+" es="+str(es))
        #
        #ImpactBoundsFileName0+=fNm
        ImpactBoundsFileName1+=fNm
        if fN<2:#QFiles:
            #ImpactBoundsFileName0+="_and_"
            ImpactBoundsFileName1+="_and_"
        #    
    #
    #ImpactBoundsFileName0+=fileEnding_toWrite0
    ImpactBoundsFileName1+=fileEnding_toWrite1
    #
    # ----------------------------------------------------------------------------------
    #with open(filePathResults+"\\"+ImpactBoundsFileName, mode='w', newline='') as f:
    #    writer = csv.writer(f)
    #    #writer.writerow(["ImpactID", "StartTime_s", "EndTime_s"])
    #    writer.writerow(["ImpactID", "tStart", "tFin1", "tFin2"])
    #
    #print("file of impact bounds: "+ImpactBoundsFileName+" создан (заготовка)")
    # ----------------------------------------------------------------------------------
    #
    
    #
    #print("N "+str(fN)+" "+fNm+" fs="+str(fs)+" => dt=1/fs="+str(dt)+" tmax="+str(tmax)+" es="+str(es))
    #
    #-----------------------------------------
    #if fileIniNames[1-1]=="051_1_M" and fileIniNames[2-1]=="051-2":
    #if fileOwnNames[1-1]=="051_1_M" and fileOwnNames[2-1]=="051-2":so D exha locs
    if fileOwnNames[1-1]=="051-1_M" and fileOwnNames[2-1]=="051-2":    
        ImpLB=1.6819791666666666#051_1_M, 051-2
        ImpHB=12.466979166666667-dt#051_1_M, 051-2
        #
        ImpLB=1.6819791666666666 #051_1_M, 051-2
        ImpHB=12.16#12.466979166666667-175*dt #051_1_M, 051-2
    #--------------------------------
    #elif fileIniNames[1-1]=="021-1" and fileIniNames[2-1]=="021-2":
    elif fileOwnNames[1-1]=="021-1" and fileOwnNames[2-1]=="021-2":
        ImpLB=21.17125#021-1, #021-2
        #ImpHB=28.011125#021-1, #021-2
        #ImpHB=28.011125-1199*dt#27.86125#021-1, #021-2
        ImpHB=27.86125
    #---------------------------------------
    #elif fileIniNames[1-1]=="020-1" and fileIniNames[2-1]=="020-2":
    elif fileOwnNames[1-1]=="020-1" and fileOwnNames[2-1]=="020-2":
        ImpLB=61.589875##020-1, #020-2 
        ImpHB=68.7#68.994125
    #--------------------------------
    #elif fileIniNames[1-1]=="022-1" and fileIniNames[2-1]=="022-2":
    elif fileOwnNames[1-1]=="022-1" and fileOwnNames[2-1]=="022-2":
        ImpLB=55.148375
        #ImpHB=63.661875
        ImpHB=63.5
    #--------------------------------
    #elif fileIniNames[1-1]=="023-1" and fileIniNames[2-1]=="023-2":
    elif fileOwnNames[1-1]=="023-1" and fileOwnNames[2-1]=="023-2":
        ImpLB=3.76575
        #ImpHB=10.80575
        ImpHB=10.7
    #--------------------------------
    #elif fileIniNames[1-1]=="024-1" and fileIniNames[2-1]=="024-2":
    elif fileOwnNames[1-1]=="024-1" and fileOwnNames[2-1]=="024-2":
        ImpLB=28.443125
        #ImpHB=40.5145
        ImpHB=34.7
    #--------------------------------
    #elif fileIniNames[1-1]=="025-1" and fileIniNames[2-1]=="025-2":
    elif fileOwnNames[1-1]=="025-1" and fileOwnNames[2-1]=="025-2":
        ImpLB=47.7
        ImpHB=53.5
    #--------------------------------
    #elif fileIniNames[1-1]=="029-1 8kHz-01" and fileIniNames[2-1]=="029-2 8kHz-02":
    elif fileOwnNames[1-1]=="029-1 8kHz-01" and fileOwnNames[2-1]=="029-2 8kHz-02":
        ImpLB=20.652375
        ImpHB=29.600625
        ImpHB=29.45625
    #--------------------------------
    #elif fileIniNames[1-1]=="030-1 8kHz-03" and fileIniNames[2-1]=="030-2 8kHz-04":
    elif fileOwnNames[1-1]=="030-1 8kHz-03" and fileOwnNames[2-1]=="030-2 8kHz-04":
        ImpLB=56.97275
        ImpHB=67.703125
        ImpHB=63.7
    #--------------------------------
    #elif fileIniNames[1-1]=="033-1" and fileIniNames[2-1]=="033-2":
    elif fileOwnNames[1-1]=="033-1" and fileOwnNames[2-1]=="033-2":
        ImpLB=8.483125
        #ImpHB=17.174
        ImpHB=17.0
    #--------------------------------
    #elif fileIniNames[1-1]=="034-1" and fileIniNames[2-1]=="034-2":
    elif fileOwnNames[1-1]=="034-1" and fileOwnNames[2-1]=="034-2":
        ImpLB=31.1935
        ImpLB=31.125#small tail amef. 
        ImpHB=38.38725
        ImpHB=38.1
    #--------------------------------
    #elif fileIniNames[1-1]=="026-1" and fileIniNames[2-1]=="026-2":
    elif fileOwnNames[1-1]=="026-1" and fileOwnNames[2-1]=="026-2":
        ImpLB=12.98275
        ImpHB=22.8235
        #ImpLB=13
        ImpHB=23
        ImpHB=22.7
    #--------------------------------
    #elif fileIniNames[1-1]=="028-1" and fileIniNames[2-1]=="028-2":
    elif fileOwnNames[1-1]=="028-1" and fileOwnNames[2-1]=="028-2":
        ImpLB=69.42525
        ImpHB=80.399875
    #--------------------------------
    #elif fileIniNames[1-1]=="035-1" and fileIniNames[2-1]=="035-2":
    elif fileOwnNames[1-1]=="035-1" and fileOwnNames[2-1]=="035-2":
        ImpLB=26.34875
        ImpHB=35.1715
        ImpHB=34.91#so left ei or 1 numom peak(s): I efcog - n'vikt
    #--------------------------------
    #elif fileIniNames[1-1]=="036-1" and fileIniNames[2-1]=="036-2":
    elif fileOwnNames[1-1]=="036-1" and fileOwnNames[2-1]=="036-2":
        ImpLB=17.906375
        #ImpHB=25.398625
        ImpHB=25.2#so left ei or 1 numom peak(s): I efcog - n'vikt
    #--------------------------------
    #elif fileIniNames[1-1]=="031-1" and fileIniNames[2-1]=="031-2":
    elif fileOwnNames[1-1]=="031-1" and fileOwnNames[2-1]=="031-2":
        ImpLB=2.992375
        ImpHB=12.217375
        ImpHB=12.15
    #--------------------------------
    #elif fileIniNames[1-1]=="032-1" and fileIniNames[2-1]=="032-2":
    elif fileOwnNames[1-1]=="032-1" and fileOwnNames[2-1]=="032-2":
        ImpLB=22.9925
        ImpHB=30.646875
        ImpHB=30.605
    #--------------------------------
    #elif fileIniNames[1-1]=="037-1" and fileIniNames[2-1]=="037-2":
    elif fileOwnNames[1-1]=="037-1" and fileOwnNames[2-1]=="037-2":
        ImpLB=89.247375
        ImpHB=105.899875
    #--------------------------------
    #elif fileIniNames[1-1]=="038-1" and fileIniNames[2-1]=="038-2":
    elif fileOwnNames[1-1]=="038-1" and fileOwnNames[2-1]=="038-2":
        ImpLB=19.790375
        ImpHB=27.981125
        ImpHB=27.94 #remains mic tail o'impact at 2. graph - I ha experience S n'badf l'gefas
    #--------------------------------
    #elif fileIniNames[1-1]=="051-1" and fileIniNames[2-1]=="051-2":
    elif fileOwnNames[1-1]=="051-1" and fileOwnNames[2-1]=="051-2":
        ImpLB=12.458333333333334
        ImpHB=20.5 
    #--------------------------------
    #elif fileIniNames[1-1]=="052-1" and fileIniNames[2-1]=="052-2":
    elif fileOwnNames[1-1]=="052-1" and fileOwnNames[2-1]=="052-2":
        ImpLB=99.5
        ImpHB=106.5 
    #--------------------------------
    #elif fileIniNames[1-1]=="053-1" and fileIniNames[2-1]=="053-2":
    elif fileOwnNames[1-1]=="053-1" and fileOwnNames[2-1]=="053-2":
        ImpLB=2
        ImpHB=11.2 
    #--------------------------------
    #elif fileIniNames[1-1]=="054-1" and fileIniNames[2-1]=="055-2":#so
    elif fileOwnNames[1-1]=="054-1" and fileOwnNames[2-1]=="055-2":#so
        ImpLB=9.5
        ImpHB=15.5 
    #--------------------------------
    #elif fileIniNames[1-1]=="024_chN0" and fileIniNames[2-1]=="024_chN1":#so
    elif fileOwnNames[1-1]=="024_chN0" and fileOwnNames[2-1]=="024_chN1":#so
        ImpLB=20.647#18.435625
        ImpHB=23.28#25.524375 
    #--------------------------------
    #elif fileIniNames[1-1]=="025_chN0" and fileIniNames[2-1]=="025_chN1":#so
    elif fileOwnNames[1-1]=="025_chN0" and fileOwnNames[2-1]=="025_chN1":#so
        ImpLB=10.68#8.103020833333334
        ImpHB=13.10#26.904583333333335 
    #--------------------------------
    elif fileOwnNames[1-1]=="0002_chN0" and fileOwnNames[2-1]=="0002_chN1":#so
        impacts0=[
            [7.4, 13.9],
            [29.1, 41.2],
            [41.4, 50.0],
            [61.5, 75.0],
            [92.1, 100.0],
            [106.6, 118.4],
            [118.4, 130.0],
            [135.8, 146.4],
            [158.0, 168.1],
            [170.0, 177.0],
            [181.4, 191.5]
                    ]
        impacts=[
            [7.4, [18.1, 18.5]],
            [29.1, [41.0, 41.4]],
            [41.4, [50.9, 54.7]],
            [61.5, [61.9, 75.0]],
            [80.3, [82.3, 89.9]],
            [92.1, [100.2, 103.4]],
            [106.6, [115.5, 118.4]],
            [118.4, [128.8, 131.7]],
            [135.8, [140.9, 147.6]],
            [158.0, [165.5, 170.0]],
            [170.0, [175.5, 180.7]],
            [181.4, [187.8, 194.7]]
        ]
    #--------------------------------                ]
    elif fileOwnNames[1-1]=="0044-03.12.25-МС0012509-1_chN0" and fileOwnNames[2-1]=="0044-03.12.25-МС0012509-1_chN1":   
        ImpLB=41.4
        ImpHB=54.7
        #
        impacts=[
            [5.9, [6.8, 6.8]],
            [10.5, [14.7, 14.7]],
            [23.2, [27.8, 27.4]],
            [34.1, [38.0, 38.3]],
            [45.2, [49.7, 50.0]],
            [59.0, [63.4, 63.0]],
            [67.5, [71.3, 71.4]],
            [76.8, [78.7, 80.0]],
            [85.4, [89.7, 88.6]],
            [107.6, [109.2, 111.5]],
            [117.9, [121.3, 122.5]],#123.3
          ]

    #--------------------------------                ]
    elif fileOwnNames[1-1]=="0045-03.12.25-МС0012509-2_chN0" and fileOwnNames[2-1]=="0045-03.12.25-МС0012509-2_chN1":   
        ImpLB=12.9
        ImpHB=18.9
        #
        impacts=          [
            [2.5, [5.2, 7.0]],
            [12.9, [16.2, 16.0]],
            [21.9, [24.6, 32.0]],#32.0 - best
            [33.3, [37.1, 40.0]],#hard def range b S'n'lin
            [45.2, [52.9, 54.2]],
            [59.0, [63.0, 67.2]],
            [68.4, [71.9, 73.3]],
            [87.7, [89.7, 93.5]],
            [99.6, [104.9, 109.4]],
            [113.5, [116.2, 121.6]],#hard def range b S'n'lin
            [127.4, [129.7, 139.1]],#123.3
            [146.3, [148.7, 150.3]]
          ]
        
    #--------------------------------
    elif fileOwnNames[1-1]=="01_ДВ_1_1канал" and fileOwnNames[2-1]=="02_ДВ_2_2канал":
        ImpLB=41.0
        ImpHB=50.7
        #
        impacts=[
            [19.1, [27.6, 24.4]],
            [32.8, [39.8, 36.9]],
            [41.3, [50.6, 47.3]],
            [51.2, [59.0, 56.0]],
            [61.3, [70.3, 66.6]],
            [71.1, [78.8, 78.4]],
            [81.6, [89.8, 85.8]],
            [90.5, [98.2, 95.5]],
            [98.5, [105.4, 13.1]],
            [107.7, [115.4, 111.7]],
            [118.5, [119.4]]
        ]
    else:
        print("other files nsmes: ")
        #for i in range(len(fileIniNames)):
        #    print(fileIniNames[i])
        for i in range(len(fileOwnNames)):
            print(fileOwnNames[i])
    print(str(ImpLB)+" ... "+str(ImpHB))
    #
    #impacts = [
    #    [1, ImpLB, ImpHB],#for flap dir (1st dir) 
    #    [2, 1.23, 5.67]#for rest, rot, dir
    #]
    #

    
                         
    print("writing file of impacts bounds "+filePathResults+"\\"+ImpactBoundsFileName1)
    impactsQ=len(impacts)
    impactN=0
    #with open(filePathResults+"\\"+ImpactBoundsFileName, mode='a', newline='') as f:
    with open(filePathResults+"\\"+ImpactBoundsFileName1, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["impactN", "tStart", "tFin1", "tFin2"])
        if do_WriteAllImpactsNotSingle:
            for impact in impacts:
                impactN+=1
                tStart, tsFin= impact
                if len(tsFin)==2:
                    tFin1=tsFin[1-1]
                    tFin2=tsFin[2-1]
                elif  len(tsFin)==1 or tsFin[2-1]==0:
                    tFin1=tsFin[1-1]
                    tFin2=tFin1
                elif len(tsFin)==0:
                    if(impactN==impactsQ):
                        tFin1=tmax-2-dt
                        tFin2=tFin1
                    else:
                        tFin1=impacts[impactN+1-1][1-1]-dt
                        tFin2=tFin1
                    #
                #
                writer.writerow([str(impactN), str(tStart), str(tFin1), str(tFin2)])
            #
        else:
            writer.writerow([str(1), str(ImpLB), str(ImpHB), str(ImpHB)])
                             
    print(ImpactBoundsFileName1+ " записан (окончательно)")
    #
    do_computeSpectrum=True
    #
    filenames=[]
    for fileOwnName in fileOwnNames:#must be 2
        fname=filePathIniData+"\\"+fileOwnName+fileEnding_toRead
        filenames.append(fname)
        #nu read csvs: FileChar uz fs et *_signal_whole uz [t, signal]
        t, signal = read_signal_csv(fname)
        #plot geq signal, lir'd tnu ab csv
        #plot_signal(t, signal, title="Сигнал "+fileOwnName, t_start=None, t_end=None)
        t_sngl=[]
        x_sngl=[]
        #
        #t_sngl1=[]
        #x_sngl1=[]
        #
        do_detrend=True
        do_normalizeByMean=True
        #
        if do_detrend:
            detrend(signal)

        if do_normalizeByMean:
            md=np.mean(signal)
            for i in range(len(signal)):
                signal[i]-=md
        
        for i in range(1, len(t)+1):
            if t[i-1]>=ImpLB and t[i-1]<=ImpHB:
                t_sngl.append(t[i-1])
                x_sngl.append(signal[i-1])
                #t_sngl1.append(t[i-1]-ImpLB)
                #x_sngl1.append(signal[i-1])
            #
        #
        if do_computeSpectrum:
            print("spectrum")
            #print("trying to read: "+fname)
            #t, n_channels, signal, fs = read_wav_and_calc_t_1(fname, max_seconds=None)
            #compute_spectrum(signal, fs, method='fft', use_window=False, plot=True) - n'last
            #def compute_spectrum(x, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1):
            freqs, amps = compute_spectrum(signal, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)
            print(" spectrum: fs="+str(fs)+"; values of frequencies: "+str(len(freqs))+", values of amplitude: "+str(len(amps)))
            #plot 'em all!
            #GraphName="Спектр колебаний - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            GraphName="Спектр колебаний - файл "+fileOwnName
            #
            #plot_several(data_to_plot, labels=None, title=GraphName)
            plot_signal(freqs, amps, title="Спектр . "+fileOwnName)
            print("graph of spectrum was displayed")
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
            print("graph of spectrum was displayed")
        else:
            print("spectrum not needed")
        #
        #nu plot fragms
        print("Единичный удар:")
        plot_signal(t, signal, title="Единичный удар . "+fileOwnName, t_start=ImpLB, t_end=ImpHB)

        do_checkHere=True#False#True
        
        
        if do_checkHere:
            print("Все удары:")
            with open(filePathIniData+"\\"+ImpactBoundsFileName1, mode='r', newline='') as f:
            #with open(filePathResults+"\\"+ImpactBoundsFileName, newline='') as f:
                print("trying to read "+filePathIniData+"\\"+ImpactBoundsFileName1)
                reader = csv.DictReader(f)
                for row in reader:
                    impactN=int(row["impactN"])
                    tStart=float(row["tStart"])
                    tFin1=float(row["tFin1"])
                    tFin2=float(row["tFin2"])
                    ImpLB=tStart
                    if tFin1<=tFin2:
                        ImpHB=tFin1
                    else:
                        ImpHB=tFin2
                    #
                    print("Impact N "+str(impactN)+" "+" tStart="+str(tStart)+" tFin1="+str(tFin1)+" tFin2="+str(tFin2)+" tFin2="+str(tFin2))
                    #
                    es=0
                    t_sngl=[]
                    x_sngl=[]
                    y_energ=[]
                    for i in range(1, len(t)+1):
                        
                        if t[i-1]>=ImpLB and t[i-1]<=ImpHB:
                            t_sngl.append(t[i-1])
                            x_sngl.append(signal[i-1])
                            y_energ.append(signal[i-1]*signal[i-1])
                        #
                    #
                    GraphName="Сигнал и энергия сигнала: удар "+str(impactN)
                    #plot_several1([
                    #  [
                    #     [(t_sngl, x_sngl), (t_sngl, y_energ)], 1
                    #  ]
                    #     
                    #],
                    #[
                    #  ["t, с", "Сигнал", "Энергия сигнала"],                  
                    #  
                    #],
                    #[
                    #  [ {"color":"blue"}, {"color":"red"}],
                    # 
                    #],
                    #GraphName
                    #)
                    
                    plot_several1([
                      [
                         [(t_sngl, x_sngl), (t_sngl, y_energ)], 2
                      ]
                         
                    ],
                    [
                      ["t, с", "Сигнал", "Энергия сигнала"],                  
                      
                    ],
                    [
                      [ {"color":"blue"}, {"color":"green"}],
                     
                    ],
                    GraphName
                    )
                #for ecch impact
            #with
        else:
            print("task to display all ranges was not given")
        #
                
                            
    print("Step2 finishes working")
        
