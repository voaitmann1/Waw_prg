from MyPyVibroLib import *

if __name__ == "__main__":
    SignalCharFileOwnName="FileChar.csv"
    fileOwnNames=["051_1_M_signal_whole.csv", "051-2_signal_whole.csv"]
    filePath="D:\\MyFilesCur\\MyPrgs\\Python\\Wav"
    filePathIniData=filePath+"\\"+"assets"#+"\\"+"IniData"
    filePathResults=filePath+"\\"+"assets"#+"\\"+"Results"
    SignalCharFileFullName=filePathIniData+"\\"+SignalCharFileOwnName
    filenames =[]
    #
    fN, fNm, fs, tmax, es = ReadDiscretFreq(SignalCharFileFullName)
    dt=1/fs
    print("N "+str(fN)+fNm+" fs="+str(fs)+" => dt=1/fs="+str(dt)+" tmax="+str(tmax)+" es="+str(es))
    
    #
    ImpLB=1.6819791666666666
    ImpHB=12.466979166666667-dt

    ImpLB=1.6819791666666666
    ImpHB=12.16#12.466979166666667-175*dt
    #uuper first - ab 1 dt., lower first - 40, sanme wa 45 et 60, ce 80-100 gut
    #150-154 - same ma kurz
    #170 - as 150 ma less
    #175 - gut, qam s'ini& -
    #174 alm gut, ma tams range, ute detrend

    #ImpLB=1.6819791666666666-2*dt
    #ImpHB=ImpLB+4*dt
    #impacts = [
    #    (1, ImpLB, ImpHB)#for flap dir (1st dir) # lif err: tuple sn'callable. Mab sdi tuple n'abl ha var vals, S abl ha nur const vaks?
    #    (2, 1.23, 5.67)#for rest, rot, dir
    #]
    impacts = [
        [1, ImpLB, ImpHB],#for flap dir (1st dir) 
        [2, 1.23, 5.67]#for rest, rot, dir
    ]
    #
    for fileOwnName in fileOwnNames:
        fname=filePathIniData+"\\"+fileOwnName
        filenames.append(fname)

        #nu read csvs: FileChar uz fs et *_signal_whole uz [t, signal]
        t, signal = read_signal_csv(fname)
        
        #plot geq signal, lir'd tnu ab csv
        #plot_signal(t, signal, title="Сигнал "+fileOwnName, t_start=None, t_end=None)

        t_sngl=[]
        x_sngl=[]

        t_sngl1=[]
        x_sngl1=[]
        
        for i in range(1, len(t)+1):
            if t[i-1]>=ImpLB and t[i-1]<=ImpHB:
                t_sngl.append(t[i-1])
                x_sngl.append(signal[i-1])
                t_sngl1.append(t[i-1]-ImpLB)
                x_sngl1.append(signal[i-1])
        
        
        #nu plot fragms

        plot_signal(t, signal, title="Единичный удар . "+fileOwnName, t_start=ImpLB, t_end=ImpHB)
        plot_signal(t_sngl, x_sngl, title="Единичный удар .. "+fileOwnName)
        plot_signal(t_sngl1, x_sngl1, title="Единичный удар ... "+fileOwnName)
    
        print(fileOwnName+" "+fileOwnName[:-10])
            
        csv_filename=fname[:-10]+"_SingleImpactRange"+".csv"
    
        with open(csv_filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(["Time_s", "Signal"])
            writer.writerow(["Time_s", "Signal", "Energy"])
            for i in range(1, len(t_sngl)+1):
                writer.writerow([t_sngl[i-1], x_sngl[i-1], x_sngl[i-1]*x_sngl[i-1]])
        print(csv_filename+" file for single impact process is written")

   
        
