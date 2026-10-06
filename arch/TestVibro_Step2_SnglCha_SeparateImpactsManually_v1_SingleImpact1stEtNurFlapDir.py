from MyPyVibroLib import *

if __name__ == "__main__":

    print("Step2 starts working")

    fileEnding_toRead="_signal_whole.csv"
    fileEnding_toWrite="_SingleImpactRange"+".csv"
    PathToNamesFile="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"
    fileOwnNames=[]
    fileIniNames=[]
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
            elif LineN>2:
                #fileOwnNames.append(row[2-1]+".csv")
                fileIniNames.append(row["Value"])
                fileOwnNames.append(row["Value"]+fileEnding_toRead)

    #print("Must work with")
    #print("path: C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav")
    #print("files: 051_1_M_signal_whole.csv, 051-2_signal_whole.csv")
    #print("Working with:")
    print("path: "+filePath)
    print("Files: "+str(QFiles))
    for i in range(QFiles):
        print(fileOwnNames[i])
    
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
    fN, fNm, fs, tmax, es = ReadDiscretFreq(SignalCharFileFullName)
    #fileOwnNames,     fs, tms, ess = ReadIniDataNamesAndFreq(SignalCharFileFullName)#ml
    dt=1/fs
    #tmax=tms[0]#ob fs s'id'l
    #fN=0#
    #for fNm in fileOwnNames:#
    #    fN+=1#
    #    es=ess[fN-1]
    #    tmax=tms[fN-1]
    #    print("N "+str(fN)+" "+fNm+" fs="+str(fs)+" => dt=1/fs="+str(dt)+" tmax="+str(tmax)+" es="+str(es))
    #
    print("N "+str(fN)+" "+fNm+" fs="+str(fs)+" => dt=1/fs="+str(dt)+" tmax="+str(tmax)+" es="+str(es))
    #
    #-----------------------------------------
    if fileIniNames[1-1]=="051-1_M" and fileIniNames[2-1]=="051-2":
    
        ImpLB=1.6819791666666666#051_1_M, 051-2
        ImpHB=12.466979166666667-dt#051_1_M, 051-2
        #
        ImpLB=1.6819791666666666 #051_1_M, 051-2
        ImpHB=12.16#12.466979166666667-175*dt #051_1_M, 051-2
    #--------------------------------
    elif fileIniNames[1-1]=="021-1" and fileIniNames[2-1]=="021-2":
   
        ImpLB=21.17125#021-1, #021-2
        #ImpHB=28.011125#021-1, #021-2
        #ImpHB=28.011125-1199*dt#27.86125#021-1, #021-2
        ImpHB=27.86125
    #----------------------------------
    elif fileIniNames[1-1]=="020-1" and fileIniNames[2-1]=="020-2":
    
        ImpLB=61.589875##020-1, #020-2 
        ImpHB=68.7#68.994125
    #--------------------------------
    elif fileIniNames[1-1]=="022-1" and fileIniNames[2-1]=="022-2":
    
        ImpLB=55.148375
        #ImpHB=63.661875
        ImpHB=63.5
    #-------------------------------
    elif fileIniNames[1-1]=="023-1" and fileIniNames[2-1]=="023-2":
    
        ImpLB=3.76575
        #ImpHB=10.80575
        ImpHB=10.7
    #--------------------------------
    elif fileIniNames[1-1]=="024-1" and fileIniNames[2-1]=="024-2":
    
        ImpLB=28.443125
        #ImpHB=40.5145
        ImpHB=34.7
    #--------------------------------
    elif fileIniNames[1-1]=="025-1" and fileIniNames[2-1]=="025-2":
    
        ImpLB=47.7
        ImpHB=53.5
    #--------------------------------
    elif fileIniNames[1-1]=="029-1 8kHz-01" and fileIniNames[2-1]=="029-2 8kHz-02":
    
        ImpLB=20.652375
        ImpHB=29.600625
        ImpHB=29.45625
    #--------------------------------
    elif fileIniNames[1-1]=="030-1 8kHz-03" and fileIniNames[2-1]=="030-2 8kHz-04":
    
        ImpLB=56.97275
        ImpHB=67.703125
        ImpHB=63.7
    #--------------------------------
    elif fileIniNames[1-1]=="033-1" and fileIniNames[2-1]=="033-2":
    
        ImpLB=8.483125
        #ImpHB=17.174
        ImpHB=17.0
    #--------------------------------
    elif fileIniNames[1-1]=="034-1" and fileIniNames[2-1]=="034-2":
    
        ImpLB=31.1935
        ImpLB=31.125#small tail amef. 
        ImpHB=38.38725
        ImpHB=38.1
    #--------------------------------

    elif fileIniNames[1-1]=="026-1" and fileIniNames[2-1]=="026-2":
    
        ImpLB=12.98275
        ImpHB=22.8235
        #ImpLB=13
        ImpHB=23
        ImpHB=22.7
    #--------------------------------
    elif fileIniNames[1-1]=="028-1" and fileIniNames[2-1]=="028-2":
    
        ImpLB=69.42525
        ImpHB=80.399875
    #--------------------------------
    elif fileIniNames[1-1]=="035-1" and fileIniNames[2-1]=="035-2":
    
        ImpLB=26.34875
        ImpHB=35.1715
        ImpHB=34.91#so left ei or 1 numom peak(s): I efcog - n'vikt
    #--------------------------------
    elif fileIniNames[1-1]=="036-1" and fileIniNames[2-1]=="036-2":
    
        ImpLB=17.906375
        #ImpHB=25.398625
        ImpHB=25.2#so left ei or 1 numom peak(s): I efcog - n'vikt
    #--------------------------------
    elif fileIniNames[1-1]=="031-1" and fileIniNames[2-1]=="031-2":
    
        ImpLB=2.992375
        ImpHB=12.217375
        ImpHB=12.15
    #--------------------------------
    elif fileIniNames[1-1]=="032-1" and fileIniNames[2-1]=="032-2":
    
        ImpLB=22.9925
        ImpHB=30.646875
        ImpHB=30.605
    #--------------------------------
    elif fileIniNames[1-1]=="037-1" and fileIniNames[2-1]=="037-2":
    
        ImpLB=89.247375
        ImpHB=105.899875
    #--------------------------------
    elif fileIniNames[1-1]=="038-1" and fileIniNames[2-1]=="038-2":
    
        ImpLB=19.790375
        ImpHB=27.981125
        ImpHB=27.94 #remains mic tail o'impact at 2. graph - I ha experience S n'badf l'gefas
    #--------------------------------
    elif fileIniNames[1-1]=="051-1" and fileIniNames[2-1]=="051-2":
    
        ImpLB=12.458333333333334
        ImpHB=20.5 
    #--------------------------------
    elif fileIniNames[1-1]=="052-1" and fileIniNames[2-1]=="052-2":
    
        ImpLB=99.5
        ImpHB=106.5 
    #--------------------------------
    elif fileIniNames[1-1]=="053-1" and fileIniNames[2-1]=="053-2":
    
        ImpLB=2
        ImpHB=11.2 
    #--------------------------------
    elif fileIniNames[1-1]=="054-1" and fileIniNames[2-1]=="055-2":#so
    
        ImpLB=9.5
        ImpHB=15.5 
    #--------------------------------
    elif fileIniNames[1-1]=="024_chN0" and fileIniNames[2-1]=="024_chN1":#so
    
        ImpLB=20.647#18.435625
        ImpHB=23.28#25.524375 
    
    #--------------------------------
    else:
        print("other files nsmes: ")
        for i in range(len(fileIniNames)):
            print(fileIniNames[i])
        #for i in range(len(fileOwnNames)):
        #    print(fileOwnNames[i])
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
        
