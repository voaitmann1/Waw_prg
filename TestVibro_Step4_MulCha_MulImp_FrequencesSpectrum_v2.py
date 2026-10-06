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
#
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

#freqStacks1=[]
#ampsStacks1=[]
#freqStacks2=[]
#ampsStacks2=[]

fresqStackIni=[]
ampsStacksIni1=[]
ampsStacksIni2=[]

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
    #do_ElaborateFreqs=True
    #do_ElaborateImpactN=2#0
    #
    QFreqsSt=len(freqs_st)

    #if do_ElaborateFreqs and (do_ElaborateImpactN==0 or impactN==do_ElaborateImpactN):#all impacts et alum arbf
    #if True:
        
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
                    #
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
    use_mean=False#False

    #def compute_spectrum(x, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)

    print("Корррекция _1_ спектр - добавляем mean, detrend, zero_padding_factor")
    print(" use_window="+str(use_window)+" use_detrend="+str(use_detrend)+" use_mean="+str(use_mean)+"zero_padding_factor"+"=1")
        
    freqs1, amps1 = compute_spectrum(si1, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
    freqs2, amps2 = compute_spectrum(si2, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
    #freqsS, ampsS = compute_spectrum(siS, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)

    print("_now _len(f1)="+str(len(freqs1))+" "+" _len(f2)="+str(len(freqs2)))
    
    GraphName="Спектр  сигнала (корректированный)- удар № "+str(impactN)+" - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            
    plot_several1
    (
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
    )#so ne show graph ob osn'fun call, ossd ref ad fun - loc o''(' vikts!
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
    print("Урезаем спектр до разумного набора.")
        
    freq_lim=66#66 - if less than 66, so by QForPeak==5 ne find f=62
        
    if freq_lim==0:
        #pass
        print("freq_lim==0")
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
            if freqs2[i-1]<=freq_lim and freqs2[i+1-1]>freq_lim:
                freqLastNN=i
            #
        #
        freqs2_cut=freqs2[:freqLastNN]
        amps2_cut =amps2[:freqLastNN]
        #
        QFreqs2cut=len(freqs2_cut)
        #
        print("sensor 2: lim f["+str(freqLastNN)+"]="+str(freqs2_cut[freqLastNN-1])+"<="+str(freq_lim)+", in all "+str(QFreqs2cut)+" vals")
                    
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
    #if arbf l'freqs - Nu no cond: if true 
    #freqStacks1=copy.deepcopy(freqs1_cut)
    #freqStacks2=copy.deepcopy(freqs2_cut)# or mab os idy ress?
    freqsStackIni=copy.deepcopy(freqs1_cut)# S'sim freqs1 et freqs2 s'idy ob idq points
    ampsStacksIni1.append(amps1_cut)
    ampsStacksIni2.append(amps2_cut)
    #
    # ut'je impact sha freqs et amps.
    # af impact cycle hado sort D.
#for je impact
#
# Формируем (на 1-м ударе) и уточняем (на последующих) список номеров пиков.
# Если в некотором ударе есть пики, каких не было в списке - вставляем - и сразу в нужную позицию
#
QFreqs=len(freqsStackIni)
peak_Ns1=[]
peak_Ns2=[]
freq_peaks1=[]
freq_peaks2=[]
peak_amps1=[]
peak_amps2=[]
QForPeak=5
count_added=0
for impactN in range(impactsCount):
    print("impactN="+str(impactN))
    #print("Sensor N 1")
    peak_Ns1_cur = MyFindFreqsPeaks_onlyNs(np.array(freqs1_cut), np.array(amps1_cut), QForPeak=QForPeak, vsh=0)
    print("Freqs (sensor 1) Ns:")
    if impactN==0:
        peak_Ns1=copy.deepcopy(peak_Ns1_cur)
        print("Ini:")
        print(peak_Ns1)
    else:
        print("Now:")
        countPeaks_cur=len(peak_Ns1_cur)
        countPeaks_1=len(peak_Ns1)
        print(peak_Ns1_cur)
        for i in range(countPeaks_cur):
            count_found1=0
            for j in range(countPeaks_1):
                if peak_Ns1[j] == peak_Ns1_cur[i]:
                    count_found1+=1
                #
            #
            if count_found1==0:
                print("New peak N found: "+str(peak_Ns1_cur[i]))
                arr1DComparableInsByOrder(peak_Ns1, peak_Ns1_cur[i])
                #
                print("Now:")
                print(peak_Ns1)
                count_added+=1
            #
        #
    #
    print("Freqs (sensor 2) Ns:")
    peak_Ns2_cur = MyFindFreqsPeaks_onlyNs(np.array(freqs2_cut), np.array(amps2_cut), QForPeak=QForPeak, vsh=0)
    if impactN==0:
        peak_Ns2=copy.deepcopy(peak_Ns2_cur)
        print("Ini:")
        print(peak_Ns2)
    else:
        print("Now:")
        countPeaks_cur=len(peak_Ns2_cur)
        countPeaks_2=len(peak_Ns2)
        print(peak_Ns2_cur)
        for i in range(countPeaks_cur):
            count_found2=0
            for j in range(countPeaks_2):
                if peak_Ns2[j] == peak_Ns2_cur[i]:
                    count_found2+=1
                #
            #
            if count_found2==0:
                print("New peak N found: "+str(peak_Ns2_cur[i]))
                arr1DComparableInsByOrder(peak_Ns2, peak_Ns2_cur[i])
                #
                print("Now:")
                print(peak_Ns2)
                count_added+=1
            #
        #
    #
#
print("Ns added: "+str(count_added))
#
# формируем 1D список частот и 2D список амплитуд: (частота, удар)
#
# freqs list = freqs1 = freqs2 (D s'idq ob idq dots of data of tbi senzs)
#
freqs_peak1=[]
freqs_peak2=[]
amps_avg_peak1=[]
amps_avg_peak2=[]
ampSumOfPow2=0
for freqN in range(len(peak_Ns1)):
    N=peak_Ns1[freqN]
    freq=freqs1_cut[N]
    freqs_peak1.append(freq)
    ampsOfpow2=[]
    amps=[]
    for impactN in range(impactsCount):
        amp=ampsStacksIni1[impactN][N]
        amps.append(amp)
        amp_pow2=amp*amp
        ampSumOfPow2+=amp_pow2
        ampsOfpow2.append(amp_pow2)
    #
    print("peak N"+str(freqN+1)+" freq1="+str(freq)+" Amps:")
    print(amps)
    #
    amp_avg=np.sqrt(np.mean(ampsOfpow2, axis=0))
    print("am avg="+str(amp_avg))
    amps_avg_peak1.append(amp_avg)
#
for freqN in range(len(peak_Ns2)):
    N=peak_Ns2[freqN]
    freq=freqs2_cut[N]
    freqs_peak2.append(freq)
    ampsOfpow2=[]
    amps=[]
    for impactN in range(impactsCount):
        amp=ampsStacksIni2[impactN][N]
        amps.append(amp)
        amp_pow2=amp*amp
        ampSumOfPow2+=amp_pow2
        ampsOfpow2.append(amp_pow2)
    #
    print("peak N"+str(freqN+1)+" freq1="+str(freq)+" Amps:")
    print(amps)
    amp_avg=np.sqrt(np.mean(ampsOfpow2, axis=0))
    print("am avg="+str(amp_avg))
    amps_avg_peak1.append(amp_avg)
#
print("Step4 finishes working")
