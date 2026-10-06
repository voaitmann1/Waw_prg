from MyPyVibroLib import *
from MyLib1 import *
#
#freq_st=[3.5,  9.5,  11.5,      20,     30,   32,    43,    50,    60] # pg7
#freq_st=[  3, 9.75, 10.75,      19,     29, 31.5,  44.5,    47, 59.75] # pg8
#freq_st=[  3,    9,    10,    18.75,   28.5,   31,  43.5,   46,  57.5] # etw pg9
freqs_st=[   3,  9.5,  10.5,       19,     29, 31.5,  43.5,   47,  59.5] # pg10 aver
#freq_st=[  3,  9.5,  10.5,       19,     29, 31.5, 43.75, 47.5,    59] # my try calc med
#          F1    F2     C1        F3      C2    F4     T1    F5     C3  lis sdi dirs: F - flap, C - chord, T - torsion) 
#           1     2      3         4       5     6      7     8      9
#
#calc_ln_x_inRegr=False
#
fileEnding="_signal_whole.csv"#"_signal_SingleImpact.csv"
fileEnding_toRead1="_ImpactsRanges.csv"

print("Step4 starts working")

PathToNamesFiles="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"
PathToNamesFiles="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\data"


filePath2="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\results"
filePath2="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\results"


#et in Step 3, ak in Step 2, V lir 2 sv files, #ma uz 1-channels nams o'csv-files s'al names o'wav-files, #et uz 2-channels nams o'csv-files atals name o'wav-file, #so S'ute lir atal file ut ved ir nams
with open(PathToNamesFiles+"\\FolderAndFiles.csv", newline='') as f:
    reader = csv.DictReader(f)
    LineN=0
    for row in reader:
        LineN+=1
        if LineN==1:
            filePath=row["Value"]
        #
    #
#
filePathIniData=filePath+"\\"+"data"#+"\\"+"IniData"
SignalCharFileOwnName="FileChar.csv"
SignalCharFileFullName=filePathIniData+"\\"+SignalCharFileOwnName
filePathIniData=filePath+"\\"+"data"#+"\\"+"IniData"
filePathResults=filePath+"\\"+"data"#+"\\"+"Results"
filePath2=filePath+"\\"+"results"
#
fileOwnNames,     fs, tms, ess = ReadIniDataNamesAndFreq(SignalCharFileFullName)
#
filenames =[]
ImpactLBs=[]
ImpactHBs=[]
#
ImpactBoundsFileOwnName=""

fN=0#
for fNm in fileOwnNames:#
    fN+=1#
    #es=ess[fN-1]
    ##tmax=tms[fN-1]#ob id'l uz je channel
    #print("N "+str(fN)+" "+fNm+" fs="+str(fs)+" => dt=1/fs="+str(dt)+" tmax="+str(tmax)+" es="+str(es))
    #
    ImpactBoundsFileOwnName+=fNm
    if fN<2:
        ImpactBoundsFileOwnName+="_and_"
    else:
        ImpactBoundsFileOwnName+=fileEnding_toRead1#".csv"
    #
#
print("filePath2="+filePath2)            
ImpactBoundsFileName=filePathIniData+"\\"+ImpactBoundsFileOwnName
print("reading: "+ImpactBoundsFileOwnName+" : "+ImpactBoundsFileName)
#
print("reading impacts bounds from: "+filePathIniData+"\\"+ImpactBoundsFileOwnName)
imp_rngs=[]
impactNs=[]
with open(filePathIniData+"\\"+ImpactBoundsFileOwnName, mode='r', newline='') as f:
    print("trying to read "+filePathIniData+"\\"+ImpactBoundsFileName)
    reader = csv.DictReader(f)
    for row in reader:
        imp_rng=[]
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
        imp_rng=[tStart, [tFin1, tFin2]]
        imp_rngs.append(imp_rng)
        #
        impactNs.append(impactN)
        #
        print("Impact N "+str(impactN)+": "+str(imp_rng)+" ImpLB="+str(ImpLB)+" - ImpHB="+str(ImpHB))
    #
#
for fileOwnName in fileOwnNames:
    fileFullName = filePathIniData +"\\"+ fileOwnName+fileEnding
    filenames.append(fileFullName)
    print("reading "+fileFullName)
#
print("trying to read "+filenames[1-1])
#s, si1, en1 = read_SignalAndEnergy_csv(filenames[1-1])
#print(filenames[1-1]+" done, "+str(len(si1))+" vals read")
tss, sis1, ens1 = read_SignalAndEnergy_csv(filenames[1-1])
print(filenames[1-1]+" done, "+str(len(sis1))+" vals read")
print("trying to read "+filenames[2-1])
#ts, si2, en2 = read_SignalAndEnergy_csv(filenames[2-1])
#print(filenames[2-1]+" done, "+str(len(si2))+" vals read")
tss, sis2, ens2 = read_SignalAndEnergy_csv(filenames[2-1])
print(filenames[2-1]+" done, "+str(len(sis2))+" vals read")
#
impactsCount=len(imp_rngs)
print("In all "+str(impactsCount)+" impacts")

print("trying to read "+filenames[1-1])
tss, sis1, ens1 = read_SignalAndEnergy_csv(filenames[1-1])
print(filenames[1-1]+" done, "+str(len(sis1))+" vals read")
print("trying to read "+filenames[2-1])
tss, sis2, ens2 = read_SignalAndEnergy_csv(filenames[2-1])
print(filenames[2-1]+" done, "+str(len(sis2))+" vals read")
#ob tss s'idy in tbi files

with open(PathToNamesFiles+"\\"+"Frequences.csv", mode='w', newline='') as ff:
    writer_ff=csv.writer(ff)
    #writer_ff.writerow(["tStart", "tFin", "Freq", "Amp", "ImpactN", "SensorN"])
    writer_ff.writerow(['N', 'Freq', "ampl", "sensorN", "impactN"])

for impactN in range(impactsCount):
    countImpactsElaborated=impactN+1
    imp_rng=imp_rngs[impactN]
    print("impact "+str(impactN+1)+"="+str(impactNs[impactN])+" : ",imp_rng)
    tStart=imp_rng[1-1]
    tFin1=imp_rng[2-1][1-1]
    tFin2=imp_rng[2-1][1-2]
    #
    ImpLB=tStart
    if tFin1 <= tFin2:
        ImpHB=tFin1
    else:
        ImpHB=tFin2
    #
    print("tmin="+str(tss[0])+" tmax="+str(tss[-1])+" ImpLB="+str(ImpLB)+" ImpHB="+str(ImpHB))
    #
    ts=[]
    si1=[]
    si2=[]
    #
    en1=[]
    en2=[]
    ensum=[]
    #
    for i in range(1, len(tss)+1):#taks in python
        if tss[i-1]>=ImpLB and tss[i-1]<=ImpHB:
            ts.append(tss[i-1])
            si1.append(sis1[i-1])
            si2.append(sis2[i-1])
            #
            en1.append(ens1[i-1])
            en2.append(ens2[i-1])
            ensum.append(ens1[i-1]+ens2[i-1])
            #siS.append(sis1[i-1]+sis2[i-1])
            #
            #print(str(i)+") t="+str(tss[i-1])+" IS in ["+str(ImpLB)+"..."+str(ImpHB)+"]")
        else:
            #print(str(i)+") t="+str(tss[i-1])+" NOT in ["+str(ImpLB)+"..."+str(ImpHB)+"]")
            pass#ob to else wa ut'print
        #
    #
    print("read vals: ts:" +str(len(ts))+" vals, +si1: "+str(len(si1))+" vals, +en1: "+str(len(en1))+" +si2: "+str(len(si2))+" vals, +en2: "+str(len(en2))+" ") 
    #
    print("read vals: ts:" +str(len(ts))+" vals, +si1: "+str(len(si1))+" vals, +en1: "+str(len(en1))+" +si2: "+str(len(si2))+" vals, +en2: "+str(len(en2))+" ") 
    GraphName="Сигналы и их энергия обоих датчиков - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
    plot_several1([
                [
                   [(ts, si1), (ts, en1)], 2
                ],
                [
                   [(ts, si2), (ts, en2)], 2#[(ts, si1), (ts, en1)], 2
                ],
                [
                   #[(ts, en1+en2)], 1
                   [(ts, ensum)], 1
                ]
              ],
              [
                ["t, с", "Сигнал", "Энергия сигнала"],                  
                ["t, с", "Сигнал", "Энергия сигнала"],
                ["t, с", "Энергия"]
              ],
              [
                [ {"color":"blue"}, {"color":"green"}],
                [ {"color":"blue"}, {"color":"green"}],
                [ {"color":"green"}]
              ],
              GraphName)
        #
    #
    do_ElaborateFreqs=True
    do_ElaborateImpactN=2#0
    #
    QFreqsSt=len(freqs_st)

    if do_ElaborateFreqs and (do_ElaborateImpactN==0 or impactN==do_ElaborateImpactN):
        
        use_window=True
        use_detrend=False
        use_mean=True#False

        freqs1, amps1 = compute_spectrum(si1, fs=fs, use_window=use_window)
        freqs2, amps2 = compute_spectrum(si2, fs=fs, use_window=use_window)
        #freqsS, ampsS = compute_spectrum(siS, fs=fs, use_window=use_window)

        GraphName="_Спектр_  сигнала - удар № "+str(impactN)+" - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
        
        plot_several1(
                [
                    [
                       [(freqs1, amps1)], 1
                    ],
                    [
                        [(freqs2, amps2)], 1
                    ]
                    #,
                    #[
                    #   [(freqsS, ampsS)], 1
                    #]
                ],
                [
                    ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                    ["Частота, Гц", "Амплитуда энергии сигнала"],
                    #["Частота, Гц", "Амплитуда энергии сигнала"]
                ],
                None,
                GraphName
            )
        
        #print("now len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))
        print("now len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2)))
        
        use_window=True
        use_detrend=True
        use_mean=False#True#False

        #def compute_spectrum(x, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)

        print("Корррекция _1_ спектр - добавляем mean, detrend, zero_padding_factor")
        print(" use_window="+str(use_window)+" use_detrend="+str(use_detrend)+" use_mean="+str(use_mean)+"zero_padding_factor"+"=1")
        
        freqs1, amps1 = compute_spectrum(si1, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
        freqs2, amps2 = compute_spectrum(si2, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
        #freqsS, ampsS = compute_spectrum(siS, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)

        GraphName="Спектр  сигнала (корректированный)- удар № "+str(impactN)+" - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            
        plot_several1(
                [
                    [   
                        [(freqs1, amps1)], 1
                    ],
                    [
                        [(freqs2, amps2)], 1
                    ]
                    #,
                    #[
                    #    [(freqsS, ampsS)], 1
                    #]
                ],
                [
                    ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                    ["Частота, Гц", "Амплитуда энергии сигнала"],
                    #["Частота, Гц", "Амплитуда энергии сигнала"]
                ],
                None,
                GraphName
            )
        #
        # ma no interp m'spline/parabola
        #
        print("Урезаем спектр до разумного набора.")
        
        freq_lim=66#66 - if less than 66, so by QForPeak==5 ne find f=62
        
        if freq_lim==0:
            #freqLastNN=QFreqs
            pass
        else:
            QFreqs=len(freqs1)
            for i in range(1, QFreqs-1+1):
                if freqs1[i-1]<=freq_lim and freqs1[i+1-1]>freq_lim:
                    freqLastNN=i
                #
            #
            freqs1_cut=freqs1[:freqLastNN]
            amps1_cut =amps1[:freqLastNN]
            #
            QFreqs1cut=len(freqs1_cut)
            #
            print("sensor 1: lim f["+str(freqLastNN)+"]="+str(freqs1_cut[freqLastNN-1])+"<="+str(freq_lim)+", in all "+str(QFreqs1cut)+" vals")
            #
            QFreqs=len(freqs2)
            for i in range(1, QFreqs-1+1):
                if freqs1[i-1]<=freq_lim and freqs1[i+1-1]>freq_lim:
                    freqLastNN=i
                #
            #
            freqs2_cut=freqs2[:freqLastNN]
            amps2_cut =amps2[:freqLastNN]
            #
            QFreqs2cut=len(freqs2_cut)
            #
            print("sensor 2: lim f["+str(freqLastNN)+"]="+str(freqs2_cut[freqLastNN-1])+"<="+str(freq_lim)+", in all "+str(QFreqs2cut)+" vals")
            #
            #if freq_lim>0:
            #    print("lim f["+str(freqLastNN)+"]="+str(freq_lim))
            #    #
            #    freqs1=freqs1[:freqLastNN]
            #    amps1 =amps1[:freqLastNN]
            #    freqs2=freqs2[:freqLastNN]
            #    amps2=amps2[:freqLastNN]
            #    #freqsS=freqsS[:freqLastNN]
            #    #ampsS=ampsS[:freqLastNN]
            #
            #print("Nu len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))
            print("Nu len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2)))
            
            GraphName="Спектр  сигнала (корректированный и сокращенный)- удар № "+str(impactN)+" - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            
            plot_several1(
                [
                    [
                        #[(freqs1, amps1)], 1 
                        [(freqs1_cut, amps1_cut)], 1
                    ],
                    [
                        #[(freqs2, amps2)], 1 
                        [(freqs2_cut, amps2_cut)], 1 
                    ]
                    #,
                    #[
                    #    [(freqsS, ampsS)], 1
                    #]
                ],
                [
                    ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                    ["Частота, Гц", "Амплитуда энергии сигнала"],
                    #["Частота, Гц", "Амплитуда энергии сигнала"]
                ],
                None,
                GraphName
            )
            #
            QForPeak=5#10#50#50
            #
            print("data 1")
            #peaksNs1, peakFreqs1, peaks1 = MyFindFreqsPeaks(np.array(freqs1), np.array(amps1), QForPeak=QForPeak, vsh=0)
            peaksNs1, peakFreqs1, peaks1 = MyFindFreqsPeaks(np.array(freqs1_cut), np.array(amps1_cut), QForPeak=QForPeak, vsh=0)
            QFreqPeaks1=len(peakFreqs1)
            print("Peaks of freqs: "+str(QFreqPeaks1))
            for i in range(1, QFreqPeaks1+1):
                print("peakN "+str(i)+" freq = "+str(peakFreqs1[i-1])+" freqN= "+str(peaksNs1[i-1])+" ampl= "+str(peaks1[i-1]))
            #
            print("data 2")
            #peaksNs2, peakFreqs2, peaks2 = MyFindFreqsPeaks(np.array(freqs2), np.array(amps2), QForPeak=QForPeak, vsh=0)
            peaksNs2, peakFreqs2, peaks2 = MyFindFreqsPeaks(np.array(freqs2_cut), np.array(amps2_cut), QForPeak=QForPeak, vsh=0)
            QFreqPeaks2=len(peakFreqs2)
            print("Peaks of freqs: "+str(QFreqPeaks2))
            for i in range(1, QFreqPeaks2+1):
                print("peakN "+str(i)+" freq = "+str(peakFreqs2[i-1])+" freqN= "+str(peaksNs2[i-1])+" ampl= "+str(peaks2[i-1]))
            #
            #
            amplPerCentApplicable=10
            dAPercentForStFreqs1=5
            dAPercentForStFreqs2=5
            MaxQFreqs1=2
            MaxQFreqs2=4
            #
            print("\nAbove peaks are chosen. Below choosing ones with amplitude big enough\n")
            #
            peakFreqs1_chosen=[]
            peaks1_chosen=[]
            peaksNs1_chosen=[]
            #
            for i in range (1, QFreqPeaks1+1):
                cur_peak=peaks1[i-1]
                if i==1 or (i>1 and cur_peak>max_peak1):
                    max_peakN1=peaksNs1[i-1]
                    max_peak1=cur_peak
                    maxpeak_Freq1=peakFreqs1[i-1]
                    print(str(i)+" cur_peak="+str(cur_peak)+" max_peak1="+str(max_peak1)+" - this is cur max")
                else:
                    print(str(i)+" cur_peak="+str(cur_peak)+" max_peak1="+str(max_peak1)+" - tis is NOT curmax")
                #
            #
            print("max_peak1="+str(max_peak1))
            print("choosing")
            for i in range (1, QFreqPeaks1+1):
                cur_peak=peaks1[i-1]
                perCentCompared=(max_peak1-cur_peak)/max_peak1*100
                if perCentCompared<=amplPerCentApplicable:
                    peakFreqs1_chosen.append(peakFreqs1[i-1])
                    peaks1_chosen.append(cur_peak)
                    peaksNs1_chosen.append(peaksNs1[i-1])
                    print(str(i)+") "+"cur_peak="+str(cur_peak)+" max peak="+str(max_peak1)+" %diff="+str(perCentCompared)+" < "+str(amplPerCentApplicable)+" - chosen!")
                else:
                    print(str(i)+") "+"cur_peak="+str(cur_peak)+" max peak="+str(max_peak1)+" %diff="+str(perCentCompared)+" > "+str(amplPerCentApplicable)+" - NOT chosen")
                #
            #
            QFreqPeaks1Chosen=len(peakFreqs1_chosen)
            if QFreqPeaks1Chosen<MaxQFreqs1:
                for i in range(QFreqPeaks1Chosen+1, MaxQFreqs1+1):
                    peakFreqs1_chosen.append(peakFreqs1[i-1])
                    peaks1_chosen.append(peaks1[i-1])
                    peaksNs1_chosen.append(peaksNs1[i-1])
                #
            #
            print("Chosen (by amp) frequences ("+str(QFreqPeaks1Chosen)+") of 1st sensor:")
            for i in range(QFreqPeaks1Chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs1_chosen[i])+" freq="+str(peakFreqs1_chosen[i])+" ampl="+str(peaks1_chosen[i]))
            #
            peakFreqs2_chosen=[]
            peaks2_chosen=[]
            peaksNs2_chosen=[]
            #
            for i in range (1, QFreqPeaks2+1):
                cur_peak=peaks2[i-1]
                if i==1 or (i>1 and cur_peak>max_peak2):
                    max_peakN2=peaksNs2[i-1]
                    max_peak2=cur_peak
                    maxpeak_Freq2=peakFreqs2[i-1]
                    print(str(i)+" cur_peak="+str(cur_peak)+" max_peak1="+str(max_peak2)+" - this is cur max")
                else:
                    print(str(i)+" cur_peak="+str(cur_peak)+" max_peak1="+str(max_peak2)+" - tis is NOT curmax")
                #
            #
            print("max_peak2="+str(max_peak2))
            for i in range (1, QFreqPeaks2+1):
                cur_peak=peaks2[i-1]
                perCentCompared=(max_peak2-cur_peak)/max_peak2*100
                if perCentCompared<=amplPerCentApplicable:
                    peakFreqs2_chosen.append(peakFreqs2[i-1])
                    peaks2_chosen.append(cur_peak)
                    peaksNs2_chosen.append(peaksNs2[i-1])
                    print(str(i)+") "+"cur_peak="+str(cur_peak)+" max peak2="+str(max_peak2)+" %diff="+str(perCentCompared)+" < "+str(amplPerCentApplicable)+" - chosen!")
                else:
                    print(str(i)+") "+"cur_peak="+str(cur_peak)+" max peak2="+str(max_peak2)+" %diff="+str(perCentCompared)+" > "+str(amplPerCentApplicable)+" - NOT chosen")
                #
            #
            QFreqPeaks2Chosen=len(peakFreqs2_chosen)
            if QFreqPeaks2Chosen<MaxQFreqs2:
                for i in range(QFreqPeaks2Chosen+1, MaxQFreqs2+1):
                    peakFreqs2_chosen.append(peakFreqs2[i-1])
                    peaks2_chosen.append(peaks2[i-1])
                    peaksNs2_chosen.append(peaksNs2[i-1])
                #
            #
            print("Chosen (by amp) frequences ("+str(QFreqPeaks2Chosen)+") of 2nd sensor:")
            for i in range(QFreqPeaks2Chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs2_chosen[i])+" freq="+str(peakFreqs2_chosen[i])+" ampl="+str(peaks2_chosen[i]))
            #
            #
            vsh=0
            print("Sorted data of sensor 1 by amp descendence")
            #def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
            Sort3ArraysByOne_v2(peaksNs1, peakFreqs1, peaks1, by123=3, DescNotAsc=True, vsh=vsh)
            for i in range(QFreqPeaks1):
                print(str(i+1)+") "+" N: "+str(peaksNs1[i])+" freq="+str(peakFreqs1[i])+" ampl="+str(peaks1[i]))
            #
            print("Again:")
            peaksNs1, peakFreqs1, peaks1=Sort3ArraysByOne_v3(peaksNs1, peakFreqs1, peaks1, by123=3, AscNotDesc=False, vsh=vsh)
            for i in range(QFreqPeaks1):
                print(str(i+1)+") "+" N: "+str(peaksNs1[i])+" freq="+str(peakFreqs1[i])+" ampl="+str(peaks1[i]))
            #
            #
            print("Sorted data of sensor 1 by freq ascendence")
            #def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
            Sort3ArraysByOne_v2(peaksNs1, peakFreqs1, peaks1, by123=2, DescNotAsc=False, vsh=vsh)
            for i in range(QFreqPeaks1):
                print(str(i+1)+") "+" N: "+str(peaksNs1[i])+" freq="+str(peakFreqs1[i])+" ampl="+str(peaks1[i]))
            print("Again:")
            peaksNs1, peakFreqs1, peaks1=Sort3ArraysByOne_v3(peaksNs1, peakFreqs1, peaks1, by123=1, AscNotDesc=True, vsh=vsh)
            for i in range(QFreqPeaks1):
                print(str(i+1)+") "+" N: "+str(peaksNs1[i])+" freq="+str(peakFreqs1[i])+" ampl="+str(peaks1[i]))
            #
            print("Sorted data of sensor 2 by amp descendence")
            #def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
            Sort3ArraysByOne_v2(peaksNs2, peakFreqs2, peaks2, by123=3, DescNotAsc=True, vsh=vsh)
            for i in range(QFreqPeaks2):
                print(str(i+1)+") "+" N: "+str(peaksNs2[i])+" freq="+str(peakFreqs2[i])+" ampl="+str(peaks2[i]))
            print("Again:")
            peaksNs2, peakFreqs2, peaks2=Sort3ArraysByOne_v3(peaksNs2, peakFreqs2, peaks2, by123=3, AscNotDesc=False, vsh=vsh)
            for i in range(QFreqPeaks2):
                print(str(i+1)+") "+" N: "+str(peaksNs2[i])+" freq="+str(peakFreqs2[i])+" ampl="+str(peaks2[i]))
            #        
            print("Sorted data of sensor 2 by freq ascendence")
            #def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
            Sort3ArraysByOne_v2(peaksNs2, peakFreqs2, peaks2, by123=2, DescNotAsc=False, vsh=vsh)
            for i in range(QFreqPeaks2):
                print(str(i+1)+") "+" N: "+str(peaksNs2[i])+" freq="+str(peakFreqs2[i])+" ampl="+str(peaks2[i]))
            print("Again:")
            peaksNs2, peakFreqs2, peaks2=Sort3ArraysByOne_v3(peaksNs2, peakFreqs2, peaks2, by123=1, AscNotDesc=True, vsh=vsh)
            for i in range(QFreqPeaks2):
                print(str(i+1)+") "+" N: "+str(peaksNs2[i])+" freq="+str(peakFreqs2[i])+" ampl="+str(peaks2[i]))
            #
            print("\nAbove freqs with big ampls are chosen - below choosing vals close to standard vals")
            #
            #def ChooseFreqsBySetMemberN(Ns, Freqs, amps, FreqsSample, N, dFPercent=20):
            #print("\nChoosing freqs:")
            for frstN in range(1, QFreqsSt+1):
                print("Finding fitting frequences for frequency N"+str(frstN)+" = "+str(freqs_st[frstN-1]))
                print("\nFor sensor 1:")
                freqBlock=ChooseFreqsBySetMemberN(peaksNs1, peakFreqs1, peaks1, freqs_st, frstN, dFPercent=20, dAPercent=dAPercentForStFreqs1)
                if freqBlock!=[]:
                    N1=freqBlock[1-1]
                    freq1=freqBlock[2-1]
                    amp1=freqBlock[3-1]
                    print("for frequency N"+str(frstN)+" = "+str(freqs_st[frstN-1])+" chosen frequency (1st sensor) (max amplitude among nearest):")
                    #print(str(N1)+") "+" freq="+str(freqs1[N1-1])+" ampl="+str(amps1[N1-1]))
                    #print(str(N1)+") "+" freq="+str(freqs1_cut[N1-1])+" ampl="+str(amps1_cut[N1-1]))
                    print(str(peaksNs1[N1-1])+") "+" freq="+str(freqs1[peaksNs1[N1-1]-1])+" ampl="+str(amps1[peaksNs1[N1-1]-1]))
                    #
                    if isInArrayAtPosN(peaksNs1_chosen, peaksNs1[N1-1])==[]:
                        peaksNs1_chosen.append(peaksNs1[N1-1])
                        peakFreqs1_chosen.append(freq1)
                        peaks1_chosen.append(amp1)
                        print("adding val")
                    else:
                        print("val "+str(freq1)+" is suitable, but is already present in arr at ", isInArrayAtPosN(peaksNs1_chosen, peaksNs1[N1-1]))
                    #
                else:
                    print("no freqs of sensor 1 fit this value")
                #
                print("now frequences for sensor 1 chosen:")
                print(str(peakFreqs1_chosen))
                print("Ns:" ,peaksNs1_chosen)
                print("amps:" ,peaksNs1_chosen)
                #
                print("\nFor sensor 2:")    
                freqBlock=ChooseFreqsBySetMemberN(peaksNs2, peakFreqs2, peaks2, freqs_st, frstN, dFPercent=20, dAPercent=dAPercentForStFreqs2)
                if freqBlock!=[]:
                    N2=freqBlock[1-1]
                    freq2=freqBlock[2-1]
                    amp2=freqBlock[3-1]
                    print("for frequency N"+str(frstN)+" = "+str(freqs_st[frstN-1])+" chosen frequency (2nd sensor) (max amplitude among nearest):")
                    print(str(peaksNs2[N2-1])+") "+" freq="+str(freqs2[peaksNs2[N2-1]-1])+" ampl="+str(amps2[peaksNs2[N2-1]-1]))
                    #
                    if isInArrayAtPosN(peaksNs2_chosen, peaksNs2[N2-1])==[]:
                        peaksNs2_chosen.append(peaksNs2[N2-1])
                        peakFreqs2_chosen.append(freq2)
                        peaks2_chosen.append(amp2)
                        print("adding val")
                    else:
                        print("val "+str(freq2)+" is suitable, but is already present in arr at ",isInArrayAtPosN(peaksNs2_chosen, peaksNs2[N2-1]))
                    #
                    print("now frequences chosen:")
                    print(peakFreqs2_chosen)
                else:
                    print("no freqs of sensor 2 fit this value")
                #
                print("now frequences for sensor 2 chosen:")
                print(str(peakFreqs2_chosen))
                print("Ns:" ,peaksNs2_chosen)
                print("amps:" ,peaksNs2_chosen)
            #
            #
            print("\nFinaly - chosen frequences:")
            Q1_chosen=len(peakFreqs1_chosen)
            print("For 1st sensor: "+str(Q1_chosen))
            print("Ns: ", peaksNs1_chosen)
            print("freqs: ", peakFreqs1_chosen)
            print("ampls: ", peaks1_chosen)
            print("Sorted data of 1st sensor renewed by freq ascendence")
            Sort3ArraysByOne_v2(peaksNs1_chosen, peakFreqs1_chosen, peaks1_chosen, by123=2, DescNotAsc=False, vsh=vsh)
            for i in range(Q1_chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs1_chosen[i])+" freq="+str(peakFreqs1_chosen[i])+" ampl="+str(peaks1_chosen[i]))
            #
            print("Again:")
            peaksNs1_chosen, peakFreqs1_chosen, peaks1_chosen= Sort3ArraysByOne_v3(peaksNs1_chosen, peakFreqs1_chosen, peaks1_chosen, by123=1, AscNotDesc=True, vsh=vsh)
            for i in range(Q1_chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs1_chosen[i])+" freq="+str(peakFreqs1_chosen[i])+" ampl="+str(peaks1_chosen[i]))
            #
            Q2_chosen=len(peakFreqs2_chosen)
            print("For 2nd sensor: "+str(Q2_chosen))
            print("Ns: ", peaksNs2_chosen)
            print("freqs: ", peakFreqs2_chosen)
            print("ampls: ", peaks2_chosen)
            print("Sorted data of 2nd sensor renewed by freq ascendence")
            Sort3ArraysByOne_v2(peaksNs2_chosen, peakFreqs2_chosen, peaks2_chosen, by123=2, DescNotAsc=False, vsh=vsh)
            for i in range(Q2_chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs2_chosen[i])+" freq="+str(peakFreqs2_chosen[i])+" ampl="+str(peaks2_chosen[i]))
            print("Again:")
            peaksNs2_chosen, peakFreqs2_chosen, peaks2_chosen= Sort3ArraysByOne_v3(peaksNs2_chosen, peakFreqs2_chosen, peaks2_chosen, by123=1, AscNotDesc=True, vsh=vsh)
            for i in range(Q2_chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs2_chosen[i])+" freq="+str(peakFreqs2_chosen[i])+" ampl="+str(peaks2_chosen[i]))
            #
            #def refine_peak_parabolic(freqs, amps, k): # return freqs[k], amps[k] # ab MyPyVibroLib
            for k in range (Q1_chosen):
                freq1_refined, amp1_refined = refine_peak_parabolic(peakFreqs1_chosen, peaks1_chosen, k)
            with open(PathToNamesFiles+"\\"+"Frequences.csv", mode='a', newline='') as ff:
                writer_ff = csv.writer(ff)
                #writer.writerow(['N', 'Freq', "ampl", "sensorN", "impactN"])
                for i in range(Q1_chosen):
                    writer_ff.writerow([str(i+1), str(peakFreqs1_chosen[i]), str(peaks1_chosen[i]), "1", str(impactN)])
                #
                for i in range(Q2_chosen):
                    writer_ff.writerow([str(i+1+Q1_chosen), str(peakFreqs2_chosen[i]), str(peaks2_chosen[i]), "2", str(impactN)])
                #
            #
            print("Frequences.csv written successfully")
            #$print("Reading Frequences.csv")
            #with open(PathToNamesFiles+"\\"+"Frequences.csv", mode='a', newline='') as ff:
            #    writer_ff=csv.writer(ff)
            #    writer_ff.writerow(s
            print("\nUnited freqs list (For both sensors. Sorted by Freqs accendance):\n")
            #
            peaksNs_united_chosen=copy.deepcopy(peaksNs2_chosen)
            peaksFreqs_united_chosen=copy.deepcopy(peakFreqs2_chosen)
            peaks_united_chosen=copy.deepcopy(peaks2_chosen)
            QUnited=len(peaksFreqs_united_chosen)
            for i in range(1, Q1_chosen+1):
                #cur_peak_1_chosen=peakFreqs1_chosen[i-1]
                poss=valIsAtPos(peaksFreqs_united_chosen, peakFreqs1_chosen[i-1], vsh=1)
                print(str(i)+"/"+str(Q1_chosen)+": fr="+str(peakFreqs1_chosen[i-1])+": ",poss)
                #poss1=valIsAtPos(peaksNs_united_chosen, peakNs1_chosen[i-1], vsh=1)
                #if poss1.equalNN>0:
                if poss.equalNN>0:
                    print("same freq, not added")
                else:
                    if poss.isLess:
                        arr1DIns(peaksNs_united_chosen, peaksNs1_chosen[i-1], 1, vsh=0)
                        arr1DIns(peaksFreqs_united_chosen, peakFreqs1_chosen[i-1], 1, vsh=0)
                        arr1DIns(peaks_united_chosen, peaks1_chosen[i-1], 1, vsh=0)
                        QUnited=len(peaksFreqs_united_chosen)
                    elif poss.isGreater:
                        #arr1DIns(peaksNs_united_chosen, peaksNs1_chosen[i-1], QUnited, vsh=0)
                        #arr1DIns(peaksFreqs_united_chosen, peakFreqs1_chosen[i-1], QUnited, vsh=0)
                        #arr1DIns(peaks_united_chosen, peaks1_chosen[i-1], QUnited, vsh=0)
                        peaksNs_united_chosen.append(peaksNs1_chosen[i-1])
                        peaksFreqs_united_chosen.append(peakFreqs1_chosen[i-1])
                        peaks_united_chosen.append(peaks1_chosen[i-1])
                        QUnited=len(peaksFreqs_united_chosen)
                    else:
                        arr1DIns(peaksNs_united_chosen, peaksNs1_chosen[i-1], poss.lessNN+1, vsh=0)
                        arr1DIns(peaksFreqs_united_chosen, peakFreqs1_chosen[i-1], poss.lessNN+1, vsh=0)
                        arr1DIns(peaks_united_chosen, peaks1_chosen[i-1], poss.lessNN+1, vsh=0)
                        QUnited=len(peaksFreqs_united_chosen)
                        #
                        print("now: ")
                        print("Ns: ", peaksNs_united_chosen)
                        print("freqs: ", peaksFreqs_united_chosen)
                        print("ampls: ", peaks_united_chosen)
                    #
                #
            #
            print("_Finally: ")
            for i in range(QUnited):
                print(str(i+1)+") "+" N: "+str(peaksNs_united_chosen[i])+" freq="+str(peaksFreqs_united_chosen[i])+" ampl="+str(peaks_united_chosen[i]))
            #
            #
        #
    #for each impact#-
    

print("Step4 finishes working")
