from MyPyVibroLib import *

if __name__ == "__main__":

    print("Step2 starts working")

    fileEnding_toRead="_signal_whole.csv"
    fileEnding_toWrite="_SingleImpactRange"+".csv"
    PathToNamesFile="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"
    #fileOwnNames=[]
    #fileIniNames=[]
    with open(PathToNamesFile+"\\FolderAndFiles.csv", newline='') as f:
        reader = csv.DictReader(f)
        LineN=0
        for row in reader:
            LineN+=1
            if LineN==1:
                #filePath=row[2-1]#di key err. I efcog 
                filePath=row["Value"]
            elif LineN==2:
                #QFiles=int(row[2-1])
                QFiles=int(row["Value"])
            #elif LineN>2:
            #    #fileOwnNames.append(row[2-1]+".csv")
            #    fileIniNames.append(row["Value"])
            #    fileOwnNames.append(row["Value"]+fileEnding_toRead)

    #print("Must work with")
    #print("path: C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav")
    #print("files: 051_1_M_signal_whole.csv, 051-2_signal_whole.csv")
    #print("Working with:")
    print("path: "+filePath)
    print("Files: "+str(QFiles))
    #for i in range(QFiles):
     #   print(fileOwnNames[i])
    
    SignalCharFileOwnName="FileChar.csv"
    #fileOwnNames=["051_1_M_signal_whole.csv", "051-2_signal_whole.csv"]
    #filePath="D:\\MyFilesCur\\MyPrgs\\Python\\Wav"
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
    fN=0#
    for fNm in fileOwnNames:#
        fN+=1#
        es=ess[fN-1]
        tmax=tms[fN-1]
        print("N "+str(fN)+" "+fNm+" fs="+str(fs)+" => dt=1/fs="+str(dt)+" tmax="+str(tmax)+" es="+str(es))
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
    elif fileOwnNames[1-1]=="044-1" and fileOwnNames[2-1]=="044-2":# !! 040-1  nabls zli ety!
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
    elif fileOwnNames[1-1]=="043-1" and fileOwnNames[2-1]=="043-2":
        ImpLB=43.62#43.3
        ImpHB=57
    #--------------------------------
    elif fileOwnNames[1-1]=="045-1" and fileOwnNames[2-1]=="045-2_M":# !! 040-1  nabls zli ety!
        ImpLB=70.30
        ImpHB=74.38
    #--------------------------------
    elif fileOwnNames[1-1]=="047-1" and fileOwnNames[2-1]=="047-2":# !! 040-1  nabls zli ety!
        ImpLB=29#74.7 
        ImpHB=36.8
    #--------------------------------
    elif fileOwnNames[1-1]=="048-1" and fileOwnNames[2-1]=="048-2":# !! 040-1  nabls zli ety!
        ImpLB=32.12#32 #v2 #v1
        ImpHB=43.3
    #--------------------------------
    else:
        print("other files nsmes: ")
        #for i in range(len(fileIniNames)):
        #    print(fileIniNames[i])
        for i in range(len(fileOwnNames)):
            print(fileOwnNames[i])
    print(str(ImpLB)+" ... "+str(ImpHB))
    #
    impacts = [
        [1, ImpLB, ImpHB],#for flap dir (1st dir) 
        [2, 1.23, 5.67]#for rest, rot, dir
    ]
    #
    filenames=[]
    for fileOwnName in fileOwnNames:
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
        
        #nu plot fragms

        plot_signal(t, signal, title="Единичный удар . "+fileOwnName, t_start=ImpLB, t_end=ImpHB)
        #plot_signal(t_sngl, x_sngl, title="Единичный удар .. "+fileOwnName)
        #plot_signal(t_sngl1, x_sngl1, title="Единичный удар ... "+fileOwnName)
    
        print(fileOwnName+" => "+fileOwnName[:-10])
            
        #csv_filename=fname[:-10]+"_SingleImpactRange"+".csv"
        #csv_filename="data"+"\\"+fileIniName+fileEnding_toWrite
        csv_filename="data"+"\\"+fileOwnName+fileEnding_toWrite
        #csv_filename=filePathData+"\\"+fileIniName+"_SingleImpactRange"+".csv"#
    
        with open(csv_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(["Time_s", "Signal"])
            writer.writerow(["Time_s", "Signal", "Energy"])
            for i in range(1, len(t_sngl)+1):
                writer.writerow([t_sngl[i-1], x_sngl[i-1], x_sngl[i-1]*x_sngl[i-1]])
        print(csv_filename+" file for single impact process is written")

    print("Step2 finishes working")
        
