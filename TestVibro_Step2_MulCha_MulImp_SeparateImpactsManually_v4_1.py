# based on vrn 4, vrn 4 s'diqal'd in C.
# Amda s'real'd reading l'file o'bounds, calc l'ranges, separ'fg l'signal by to bounds ad un impacts,
# show l'signal: ini, norm'd et detrend'd et su spectrum: o'ge signal (nout, sflu, exnot) et je impact
# Ma ce n'arb ut if sensors Q !=2
# So in next vrn s'ute do cycle ut form l'data ut'graph
# et wu gut ha separ var ut'time range uz je channel, et calc S separ'y by n'id'l tFin - so swu V abl calc impacts co n'idq'l len
# Et algorythm, id let ignore l'arr of bounds, if S ns'dat'd, et lir S ab file, ns'real'd, et msb real'd in next vrn.
# Ut'extract time bounds utf'tc fun ExtractBounds; ut'2 (tStart, tFin) - utf'tc ExtractBounds2, ma
# ut'3 (tStart, tFin1, tFin2) - es ExtractBounds3 
# Code, utf'd ut'iqv l'file o'bounds et single signal, ablb utf'd in next step
# 

from MyPyVibroLib import *

if __name__ == "__main__":

    print("Step2 starts working")

    do_ShowReadSignal=True#False#True
    do_computeSpectrum=True
    do_detrend=True
    do_normalizeByMean=True
    do_ShowWholeSignal=True
    do_ShowSingleSignal=True
    do_ShowWholeSignal_AfterNorm=True
    do_ShowWholeSignal_AfterDetrend=True
    do_ShowSingleSignal_AfterNorm=False
    do_ShowSingleSignal_AfterDetrend=False
    do_CheckAllSingleSignals=True
    do_showSingleSignals_TogetherFromAllSensors=True
    do_showSingleSignals_SeparatelyFromEachSensor=False
    do_checkSingleSigmnalsWithGraphAtOnce=False
    do_ifImpactTimeRangeNotGiven_ReadFileNotStopAndRepoirtyError=False# nrewe, n'arb
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
    #
    print("-------------  now impacts bounds ----------")
    #tmax=ts[-1]
    #ImpLB=0
    #ImpHB=tmax   
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
        ImpLB=118.4#8.103020833333334
        ImpHB=136.0#26.904583333333335 
    #--------------------------------
    elif fileOwnNames[1-1]=="0005_chN0" and fileOwnNames[2-1]=="0005_chN1":
        ImpLB=81.5
        ImpHB=87.9#86.3#commented s'ab 0th chn, to vibrs damp kq mox, et vibrs o'1. chN damp kq diu, tic, kq, time s'jq n'noise
    #--------------------------------
    elif fileOwnNames[1-1]=="022_chN0" and fileOwnNames[2-1]=="022_chN1":
        ImpLB=36.49
        ImpHB=41.43#hic chN0 exda atal prev chN0
    #--------------------------------
    elif fileOwnNames[1-1]=="022_chN0" and fileOwnNames[2-1]=="022_chN1":
        ImpLB=36.49
        ImpHB=41.430
    #--------------------------------
    elif fileOwnNames[1-1]=="023_chN0" and fileOwnNames[2-1]=="023_chN1":
        ImpLB=25.87
        ImpHB=30.0
    #--------------------------------
    elif fileOwnNames[1-1]=="020_chN0" and fileOwnNames[2-1]=="020_chN1":
        ImpLB=35.796875#last.N'lim'd m'af-impact
        ImpHB=40.45
    #--------------------------------
    elif fileOwnNames[1-1]=="021_chN0" and fileOwnNames[2-1]=="021_chN1":
        ImpLB=25.33
        ImpHB=27.3#28.92#ob in chN0 os end o'imp, ics ha kq period et starts noise of ety mer freq
    #--------------------------------
    elif fileOwnNames[1-1]=="021_chN0" and fileOwnNames[2-1]=="021_chN1":
        ImpLB=25.33
        ImpHB=27.3#28.92#ob in chN0 os end o'imp, ics ha kq period et starts noise of ety mer freq
    #--------------------------------
    elif fileOwnNames[1-1]=="026_chN0" and fileOwnNames[2-1]=="026_chN1":
        ImpLB=5.1
        ImpHB=7.32
    #--------------------------------
    elif fileOwnNames[1-1]=="027_chN0" and fileOwnNames[2-1]=="027_chN1":
        ImpLB=21.62
        ImpHB=25.21
    #--------------------------------
    elif fileOwnNames[1-1]=="39_2ТЭ30451_chN0" and fileOwnNames[2-1]=="39_2ТЭ30451_chN1":
        ImpLB=54.6
        ImpHB=62.3#63.3 uz chN1
    #--------------------------------
    elif fileOwnNames[1-1]=="40_2ТЭ30451_chN0" and fileOwnNames[2-1]=="40_2ТЭ30451_chN1":
        ImpLB=128.3
        ImpHB=137.8
    #--------------------------------
    elif fileOwnNames[1-1]=="41_2ТЭ33451_chN0" and fileOwnNames[2-1]=="41_2ТЭ33451_chN1":
        ImpLB=35.5
        ImpHB=45.3
    #--------------------------------
    elif fileOwnNames[1-1]=="42_2ТЭ33451_chN0" and fileOwnNames[2-1]=="42_2ТЭ33451_chN1":
        ImpLB=89.0
        ImpHB=100
    #--------------------------------
    elif fileOwnNames[1-1]=="43_1ТЭ17441_chN0" and fileOwnNames[2-1]=="43_1ТЭ17441_chN1":
        ImpLB=106.1
        ImpHB=116#120
    #--------------------------------
    elif fileOwnNames[1-1]=="44_1ТЭ17441_chN0" and fileOwnNames[2-1]=="44_1ТЭ17441_chN1":
        ImpLB=100
        ImpHB=108.1
    #--------------------------------
    elif fileOwnNames[1-1]=="45_1ТЭ18441_chN0" and fileOwnNames[2-1]=="45_1ТЭ18441_chN1":
        ImpLB=106.2
        ImpHB=120
    #--------------------------------
    elif fileOwnNames[1-1]=="46_1ТЭ18441_chN0" and fileOwnNames[2-1]=="46_1ТЭ18441_chN1":
        ImpLB=52.851#52.851#52.6  # v3 # v2 # v1
        ImpHB=68.9#57#60          # v3 # v2 # v1
    #--------------------------------
    elif fileOwnNames[1-1]=="47_1ТЭ20441_chN0" and fileOwnNames[2-1]=="47_1ТЭ20441_chN1":
        ImpLB=108.3
        ImpHB=123.8
    #--------------------------------
    elif fileOwnNames[1-1]=="48_1ТЭ20441_chN0" and fileOwnNames[2-1]=="48_1ТЭ20441_chN1":
        ImpLB=128.78
        ImpHB=137.40
    #--------------------------------
    elif fileOwnNames[1-1]=="49_2ТЭ32451_chN0" and fileOwnNames[2-1]=="49_2ТЭ32451_chN1":
        ImpLB=86.8
        ImpHB=100
    #--------------------------------
    elif fileOwnNames[1-1]=="50_2ТЭ32451_chN0" and fileOwnNames[2-1]=="50_2ТЭ32451_chN1":
        ImpLB=72.8#72.7#72.8
        ImpHB=83.8
    #--------------------------------
    elif fileOwnNames[1-1]=="049-1" and fileOwnNames[2-1]=="049-2":
        ImpLB=65.56#65.4 #v2 #v1
        ImpHB=74.3
    #--------------------------------
    elif fileOwnNames[1-1]=="050-1" and fileOwnNames[2-1]=="050-2":
        ImpLB=75.22#75.2
        ImpHB=84.9
    #--------------------------------
    elif fileOwnNames[1-1]=="043-1" and fileOwnNames[2-1]=="043-2":
        ImpLB=43.62#43.3
        ImpHB=57
    #--------------------------------
    elif fileOwnNames[1-1]=="045-1" and fileOwnNames[2-1]=="045-2_M":# !! 040-1  nabls zli ety!
        ImpLB=70.30
        ImpHB=74.38
    #--------------------------------
    elif fileOwnNames[1-1]=="039-1" and fileOwnNames[2-1]=="039-2":
        ImpLB=101.8
        ImpHB=118.3
    #--------------------------------
    elif fileOwnNames[1-1]=="039-1_M" and fileOwnNames[2-1]=="039-2":
        ImpLB=85.4
        ImpHB=101.5
    #--------------------------------
    elif fileOwnNames[1-1]=="040-1" and fileOwnNames[2-1]=="040-2":
        ImpLB=74.539#74.5#85.457
        ImpHB=87.4
    #--------------------------------
    elif fileOwnNames[1-1]=="041-1" and fileOwnNames[2-1]=="041-2":
        ImpLB=93.07#92.9 #v2 v1
        ImpHB=105.2
    #--------------------------------
    elif fileOwnNames[1-1]=="042-1" and fileOwnNames[2-1]=="042-2":
        ImpLB=18
        ImpHB=28.9
    #--------------------------------
    elif fileOwnNames[1-1]=="044-1" and fileOwnNames[2-1]=="044-2":# No tal file in xls! !! 040-1 nabls zli! # no tic file in xls file!! 
        ImpLB=74.5
        ImpHB=51.2#87.7#70.30 74.38
    #--------------------------------
      # !! 044-1  nabls arbf. S lif: wrirer.writerow(signal[i], signal[i]**2) - no space left on device
        #et file whole_signal.csv, ics'lir'd kum to time, ha 230 MB. Ja, es warn:
        #Warning (from warnings module):
        #File "C:\Users\V\Documents\MyPrgs\Python\Wav\MyPyVibroLib.py", line 270
        #fs, data=wavfile.read(fullFileName)
        #WavFileWarning: Reached EOF prematurely; finished at 13256496 bytes, expected 13256498 bytes from header.
        #
        #mab zu mag file?
    #--------------------------------
    #elif fileOwnNames[1-1]=="043-1" and fileOwnNames[2-1]=="043-2":
    #    ImpLB=43.62#43.3
    #    ImpHB=57
    #--------------------------------
    #elif fileOwnNames[1-1]=="045-1" and fileOwnNames[2-1]=="045-2_M":# !! 040-1  nabls zli ety!
    #    ImpLB=70.30
    #    ImpHB=74.38
    #--------------------------------
    elif fileOwnNames[1-1]=="047-1" and fileOwnNames[2-1]=="047-2":# !! 040-1  nabls zli ety!
        ImpLB=29#74.7 
        ImpHB=36.8
    #--------------------------------
    elif fileOwnNames[1-1]=="048-1" and fileOwnNames[2-1]=="048-2":# !! 040-1  nabls zli ety!
        ImpLB=32.12#32 #v2 #v1
        ImpHB=43.3
    #--------------------------------
    #elif fileOwnNames[1-1]=="041-1" and fileOwnNames[2-1]=="041-2":
    #    ImpLB=93.07#92.9 #v2 v1
    #    ImpHB=105.2
    #--------------------------------
    #elif fileOwnNames[1-1]=="042-1" and fileOwnNames[2-1]=="042-2":
    #    ImpLB=18
    #    ImpHB=28.9
    #--------------------------------
    elif fileOwnNames[1-1]=="0035_chN0" and fileOwnNames[2-1]=="0035_chN1":
        ImpLB=27.5
        ImpHB=44.4
    #--------------------------------
    elif fileOwnNames[1-1]=="0036_chN0" and fileOwnNames[2-1]=="0036_chN1":
        ImpLB=172.5
        ImpHB=189.4
    #--------------------------------
    elif fileOwnNames[1-1]=="0037_chN0" and fileOwnNames[2-1]=="0037_chN1":
        ImpLB=52.55
        ImpHB=62.4

        impacts=[
                   [1, [12.6, [13.3]]],#a'chN1 os noise, n'impact
                   [2, [31.0, [40.0, 38.5]]],
                   [3, [42.8, [51.7, 51.3]]],
                   [4, [52.4, [61.2, 59.9]]],
                   [5, [62.8, [71.8, 69.9]]],
                   [6, [72.8, [82.0, 91.8]]],
                   [7, [83.1, [92.1, 92.5]]],
                   [8, [93.0, [101.3, 100.3]]],
                   [9, [102.9, [111.7, 112.1]]],
                   [10, [112.8, [120.5, 121.6]]],
                   [11, [123.0, [130.7, 131.5]]],
                   [12, [133.3, [140.3, 142.6]]]
                ]
    #--------------------------------
    elif fileOwnNames[1-1]=="0038_chN0" and fileOwnNames[2-1]=="0038_chN1":
        ImpLB=28.8#29.12
        ImpHB=43.9
    #--------------------------------
    elif fileOwnNames[1-1]=="0038-03.12.25-МС0042511-1_chN0" and fileOwnNames[2-1]=="0038-03.12.25-МС0042511-1_chN1":
        ImpLB=44.8#29.12
        ImpHB=54.9
        #
        impacts=[#2026-08-05, was ac ce, nur ImpLB ety ImpHB
            [1, [4.2, [9.1, 10.9]]],#
            [2, [15.6, [21.0, 23.4]]],#
            [3, [24.7, [30.1, 31.1]]],#
            [4, [35.1, [39.7, 41.9]]],#
            [5, [44.8, [50.0, 51.6]]],#
            [6, [55.0, [60.0, 62.0]]],#
            [7, [65.1, [74.9, 73.2]]],#
            [8, [75.1, [80.9, 83.3]]],#
            [9, [85.3, [92.0, 91.6]]],#
        ]
    #--------------------------------
    elif fileOwnNames[1-1]=="0039-03.12.25-МС0042511-2_chN0" and fileOwnNames[2-1]=="0039-03.12.25-МС0042511-2_chN1":
        ImpLB=63.1
        ImpHB=73.3
    #--------------------------------
    elif fileOwnNames[1-1]=="0040-03.12.25-МС0032510-1_chN0" and fileOwnNames[2-1]=="0040-03.12.25-МС0032510-1_chN1":#iqv!
        ImpLB=39.1#98.7
        ImpHB=48.8#108.8
    #--------------------------------
    elif fileOwnNames[1-1]=="0041-03.12.25-МС0032510-2_chN0" and fileOwnNames[2-1]=="0041-03.12.25-МС0032510-2_chN1":
        ImpLB=73.8
        ImpHB=83.7
    #--------------------------------
    elif fileOwnNames[1-1]=="0042-03.12.25-МС0022510-1_chN0" and fileOwnNames[2-1]=="0042-03.12.25-МС0022510-1_chN1":
        ImpLB=42.0
        ImpHB=53.1
    #--------------------------------
    elif fileOwnNames[1-1]=="0043-03.12.25-МС0022510-2_chN0" and fileOwnNames[2-1]=="0043-03.12.25-МС0022510-2_chN1":
        ImpLB=31.2
        ImpHB=42.9
    #--------------------------------                
    elif fileOwnNames[1-1]=="0044-03.12.25-МС0012509-1_chN0" and fileOwnNames[2-1]=="0044-03.12.25-МС0012509-1_chN1":   
        ImpLB=45.25#41.4
        ImpHB=54.7
    #--------------------------------                
    elif fileOwnNames[1-1]=="0045-03.12.25-МС0012509-2_chN0" and fileOwnNames[2-1]=="0045-03.12.25-МС0012509-2_chN1":   
        ImpLB=12.9
        ImpHB=18.9
    #--------------------------------
        # all files mentioned in ord D s'in xls
    #--------------------------------
    elif fileOwnNames[1-1]=="01_ДВ_1_1канал" and fileOwnNames[2-1]=="02_ДВ_2_2канал":
        ImpLB=41.0
        ImpHB=50.7
        #
        impacts=[
            [1, [19.1, [27.6, 24.4]]],
            [2, [32.8, [39.8, 36.9]]],
            [3, [41.3, [50.6, 47.3]]],
            [4, [51.2, [59.0, 56.0]]],
            [5, [61.3, [70.3, 66.6]]],
            [6, [71.1, [78.8, 78.4]]],
            [7, [81.6, [89.8, 85.8]]],
            [8, [90.5, [98.2, 95.5]]],
            [9, [98.5, [105.4, 13.1]]],
            [10, [107.7, [115.4, 111.7]]],
            [11, [118.5, [119.4]]]
        ]
    #--------------------------------
    elif fileOwnNames[1-1]=="20251218Сер1__01_ДВ_1_1канал" and fileOwnNames[2-1]=="20251218Сер1__02_ДВ_2_2канал":
        ImpLB=41.0
        ImpHB=50.7
        #
        impacts=[
           [1, [19.1, [27.6, 24.4]]],
           [2, [32.8, [39.8, 36.9]]],
           [3, [41.3, [50.6, 47.3]]],
           [4, [51.2, [59.0, 56.0]]],
           [5, [61.3, [70.3, 66.6]]],
           [6, [71.1, [78.8, 78.4]]],
           [7, [81.6, [89.8, 85.8]]],
           [8, [90.5, [98.2, 95.5]]],
           [9, [98.5, [105.4, 13.1]]],
           [10, [107.7, [115.4, 111.7]]],
           [11, [118.5, [119.4]]]
        ]
    #--------------------------------
    elif fileOwnNames[1-1]=="20251218Сер2__01_ДВ_1_1канал" and fileOwnNames[2-1]=="20251218Сер2__02_ДВ_2_2 канал":
        #                    20251218Сер2__01_ДВ_1_1канал                          20251218Сер2__02_ДВ_2_2_канал
        ImpLB=71.3        #                                                        20251218Сер2__02_ДВ_2_2 канал 
        ImpHB=75.8
        #
        impacts=[
            [1, [9.5, [12.9, 24.4]]],
            [2, [17.6, [23.6, 36.9]]],
            [3, [27.7, [31.6, 47.3]]],
            #[4, [41.2, [46.1, 56.0]]],#
            #[5, [51.2, [67.2, 66.6]]],#
            #[6, [59.9, [78.8, 78.4]]],#
            #[7, [71.4, [76.8, 85.8]]],#
            [8, [85.3, [90.7, 95.5]]],
            [9, [97.9, [101.1, 103.1]]],
            [10, [107.0, [113.5, 111.7]]],
            [11, [120.2, [125.7]]],
            [12, [132.7, [136.3]]]
        ]
    #--------------------------------
    else:
        print("other files nsmes: ")
        #for i in range(len(fileIniNames)):
        #    print(fileIniNames[i])
        for i in range(len(fileOwnNames)):
            print(fileOwnNames[i])
        #
    #
    print(str(ImpLB)+" ... "+str(ImpHB))
    #
    #impacts = [
    #    [1, ImpLB, ImpHB],#for flap dir (1st dir) 
    #    [2, 1.23, 5.67]#for rest, rot, dir
    #]
    #
    do_WriteAllImpactsNotSingle=True
    #
    print("Impacts are defined")
    print("Impacts (initially given")
    print(impacts)
    if do_WriteAllImpactsNotSingle==False:
        impacts=[]
        impacts.append(ImpLB)
        impacts.append(ImpHB)
    print("Impacts (after correction)")
    print(impacts)
    impactsBounds_fileName=dataRead.Folder+"\\"+dataRead.SubFolder_IntermediateData+"\\"+dataRead.File[0]+dataRead.fileNameEnding_ImpactBounds
    print("writing file of impacts bounds "+impactsBounds_fileName)
    #impactsQ=len(impacts)
    #elaboratedImpactN=0
    #with open(filePathResults+"\\"+ImpactBoundsFileName, mode='a', newline='') as f:
    with open(impactsBounds_fileName, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["impactN", "tStart", "tFin1", "tFin2"])
        print("header is written to file")
        if do_WriteAllImpactsNotSingle:
            print("writing impacts bounds to file")
            impactsQ=len(impacts)
            print("impactsQ="+str(impactsQ))
            print("impacts:")
            print(impacts)
            elaboratedImpactN=0
            for impact in impacts:
                elaboratedImpactN+=1
                impactN=impact[1-1] # mut r'ef v
                tsOfImpact=impact[2-1] # mut r'ef v
                tStart, tsFin = tsOfImpact # mut r'ef v
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
                writer.writerow([str(impactN), str(tStart), str(tFin1), str(tFin2)])
            #
        else:
            print("writing  Single impact bounds to file")
            writer.writerow([str(1), str(ImpLB), str(ImpHB), str(ImpHB)])
        #
    #
    #print(impactsBounds_fileName+ " записан (окончательно)")
    print(impactsBounds_fileName+ " записан (!)")
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
                t_sngl, x_sngl_chn = GetSingleImpactSignal(ts, signal_chn, impLB, impHB) 
                x_sngl.append(x_sngl_chn)
                #x_sngl.append(copy.deepcopy(x_sngl_chn))
                #
                if do_checkSingleSigmnalsWithGraphAtOnce:
                    fileOwnName=fileOwnNames[sensorN-1]
                    plot_signal(t_sngl, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар {impLB} ... {impHB} (исходный), канал"+str(sensorN-1))
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
            impLB=t_sngl[0]
            impHB=t_sngl[-1]
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
                #t_sngl=ts_sngl[impN]
                #x_sngl=xs_sngl[impN]
                if do_showSingleSignals_SeparatelyFromEachSensor:
                    for sensorN in range(1, SensorsQuantity+1):
                        x_sngl_chn=copy.deepcopy(x_sngl[sensorN-1])
                        fileOwnName=fileOwnNames[sensorN-1]
                    
                        plot_signal(t_sngl, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар {impLB} ... {impHB} (исходный), канал"+str(sensorN-1))
                    #for
                #if
                #print("data include points: t: "+str(len(t_sngl))+" x1: "+str(len(x_sngl[1-1]))+" x2: "+str(len(x_sngl[2-1])))
                if do_showSingleSignals_TogetherFromAllSensors:
                    GraphName=f"сигнал 1 удар t={impLB} ... {impHB}(исходный.)"
                    plot_several1([
                     
                        [
                           [(t_sngl, x_sngl[1-1])], 1
                        ],
                        [
                           [(t_sngl, x_sngl[2-1])], 1
                        ]
                        
                      ],
                      [
                        ["t, с", "Сигнал", "Канал 0"],                  
                        ["t, с", "Сигнал", "Канал 1"]
                        
                      ],
                      [
                        [ {"color":"blue"}],
                        [ {"color":"blue"}]
                      ],
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
                        plot_signal(t_sngl, x_sngl, title=f"{fileOwnName} - сигнал 1 удар t={impLB} ... {impHB}(нормализация.), канал"+str(sensorN-1))
                    #
                #
                if do_showSingleSignals_TogerherForAllSensors:
                    GraphName=f"сигнал 1 удар t={impLB} ... {impHB}(нормализация.)"
                    plot_several1([
                     
                        [
                           [(t_sngl, x_sngl[1-1])], 1
                        ],
                        [
                           [(t_sngl, x_sngl[2-1])], 1
                        ]
                        
                      ],
                      [
                        ["t, с", "Сигнал", "Канал 0"],                  
                        ["t, с", "Сигнал", "Канал 1"]
                        
                      ],
                      [
                        [ {"color":"blue"}],
                        [ {"color":"blue"}]
                      ],
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
                        plot_signal(t_sngl, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар t={impLB} ... {impHB} (детренд), канал"+str(sensorN-1))
                    #               
                #
                if do_showSingleSignals_TogerherForAllSensors:                
                    GraphName=f"сигнал 1 удар t={impLB} ... {impHB}(детренд.)"
                    plot_several1([
                     
                        [
                           [(t_sngl, x_sngl[1-1])], 1
                        ],
                        [
                           [(t_sngl, x_sngl[2-1])], 1
                        ]
                        
                      ],
                      [
                        ["t, с", "Сигнал", "Канал 0"],                  
                        ["t, с", "Сигнал", "Канал 1"]
                        
                      ],
                      [
                        [ {"color":"blue"}],
                        [ {"color":"blue"}]
                      ],
                      GraphName
                    )
                #
            #
        #for
    #---------------------------------------------------------------------------------------
    if do_computeSpectrum:
        fs=dataRead.fs[0]
        #
        print("for whole spectrum")
        for sensorN in range(1, SensorsQuantity+1):
            fileOwnName=fileOwnNames[sensorN-1]
            signal_chn=copy.deepcopy(signals[sensorN-1])
            print("spectrum (for each impasct)")
            freqs, amps = compute_spectrum(signal_chn, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)
            print(" spectrum: fs="+str(fs)+"; values of frequencies: "+str(len(freqs))+", values of amplitude: "+str(len(amps)))
            GraphName="Спектр колебаний (whole signal chN "+str(sensorN)+") - файл "+fileOwnName
            GraphName=f"Спектр колебаний (single impact N "+str(impN+1)+" (t={impLB}...{impHB}) signal chN "+str(sensorN)+") - файл "+fileOwnName
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
        if do_CheckAllSingleSignals:
            for impN in range(len(impacts)):
                impNf, impLB, impHB = ExtractImpactBounds2(impacts, impN+1)
                print(str(impN+1)+") impact N "+str(impNf)+" impLB="+str(impLB)+" impHB="+str(impHB))
                t_sngl=[]
                x_sngl=[]
                for sensorN in range(1, SensorsQuantity+1):
                    signal_chn=copy.deepcopy(signals[sensorN-1])
                    t_sngl, x_sngl_chn = GetSingleImpactSignal(ts, signal_chn, impLB, impHB) 
                    x_sngl.append(x_sngl_chn)
                #
                for sensorN in range(1, SensorsQuantity+1):
                    fileOwnName=fileOwnNames[sensorN-1]
                    x_sngl=copy.deepcopy(xs_sngl[sensorN-1])
                    #
                    if do_showSingleSignals_SeparatelyFromEachSensor:
                        plot_signal(t_sngl, x_sngl_chn, title=f"{fileOwnName} - сигнал 1 удар {impLB} ... {impHB} (исходный), канал"+str(sensorN-1))
                    #
                    print("spectrum (for each impasct)")
                    freqs, amps = compute_spectrum(x_sngl, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)
                    print(" spectrum: fs="+str(fs)+"; values of frequencies: "+str(len(freqs))+", values of amplitude: "+str(len(amps)))
                    GraphName=f"Спектр колебаний (single impact N "+str(impN+1)+" (t={impLB}...{impHB}) signal chN "+str(sensorN)+") - файл "+fileOwnName
                    plot_signal(freqs, amps, title=f"Спектр-удар {impN} N {impNf} t={impLB}..{impHB} ). "+fileOwnName)
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
                #for sensorN
            #for impact N
        # if do_CheckAllSingleSignals
    #if compute spectrum

    
    
    print("Step2 finishes working")
        
