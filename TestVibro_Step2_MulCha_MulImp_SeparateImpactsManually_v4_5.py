# based on vrn 4_4 - arb'n vrn
# 4_4 s'diqal'd in C
# no reg l'impacts bounds
# HaDo:
# - clasterize l'smooth'd freqs
# - reg l'impacts bounds,
# - lir et lif l'spectrum
# - full harm anal
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
    do_ShowWholeSignal_AfterNorm=False#True
    do_ShowWholeSignal_AfterDetrend=False#True
    do_ShowSingleSignal_AfterNorm=False
    do_ShowSingleSignal_AfterDetrend=False
    do_CheckAllSingleSignals=True
    do_showSingleSignals_TogetherFromAllSensors=True
    do_showSingleSignals_SeparatelyFromEachSensor=False
    do_checkSingleSigmnalsWithGraphAtOnce=False
    do_ifImpactTimeRangeNotGiven_ReadFileNotStopAndRepoirtyError=False# nrewe, n'arb
    do_clustrerizeSpectrum=True
    showCurFreqCluster_NeededFragmentOnlyNotWhole=False#True
    do_Smoothing_Extremums=True
    #
    _chn_N_=2
    _impN_=2#5
    #
    freqHB_Smooth=65
    freqHB_TryClust=4
    #
    #freqHB=30 #4 #19#65
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
                t_sngl_chn, x_sngl_chn = GetSingleImpactSignal(ts, signal_chn, impLB, impHB) 
                t_sngl.append(t_sngl_chn)
                x_sngl.append(x_sngl_chn)
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
                    #
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
                #
            #
        #for
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
    print("Step2 finishes working")
        
