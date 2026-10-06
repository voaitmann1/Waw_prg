from MyPyVibroLib1 import *# 1 is forscipy version more fresh than 1.7.3 which was for py 3.8. And this vrn is for py 3.10.
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

PathToNamesFiles="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"#win7 WmWare
PathToNamesFiles="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\data"
PathToNamesFiles="H:\MyFiles\MyPrgs\Python\Python1\\Wav\\data"

filePath2="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\results"
filePath2="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\results"
filePath2="H:\MyFiles\MyPrgs\Python\Python1\\Wav\\results"


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

do_refine_freqs=True

freqsStackIni1=[]
freqsStackIni2=[]
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
        print("freq_lim==0=> unlimited till end")
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
        # refining peaks
        freqs1_cut_rfnd=[]
        amps1_cut_rfnd=[]
        for freqN in range(QFreqs1cut):
            freq_refined, amp_refined = refine_peak_parabolic(freqs1_cut, amps1_cut, k)
            #
            freqs1_cut_rfnd.append(freqs1_cut_rfnd)
            amps1_cut_rfnd.append(amps1_cut_rfnd)
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
    #if frqLim==0
    #
    # refining peaks
    if do_refine_freqs:
        if frqLim==0:
            freqs1_rfnd=[]
            amps1_rfnd=[]
            for freqN in range(QFreqs1cut):
                freq_refined, amp_refined = refine_peak_parabolic(freqs1, amps1, freqN)
                #
                freqs1_rfnd.append(freq_refined)
                amps1_rfnd.append(amp_refined)
            #
            freqs2_rfnd=[]
            amps2_rfnd=[]
            for freqN in range(QFreqs2cut):
                freq_refined, amp_refined = refine_peak_parabolic(freqs2_cut, amps2_cut, freqN)
                #
                freqs2_rfnd.append(freq_refined)
                amps2_rfnd.append(amp_refined)
            #
        else:
            freqs1_cut_rfnd=[]
            amps1_cut_rfnd=[]
            for freqN in range(QFreqs1cut):
                freq_refined, amp_refined = refine_peak_parabolic(freqs1_cut, amps1_cut, freqN)
                #
                freqs1_cut_rfnd.append(freq_refined)
                amps1_cut_rfnd.append(amp_refined)
            #
            freqs2_cut_rfnd=[]
            amps2_cut_rfnd=[]
            for freqN in range(QFreqs2cut):
                freq_refined, amp_refined = refine_peak_parabolic(freqs2_cut, amps2_cut, freqN)
                #
                freqs2_cut_rfnd.append(freq_refined)
                amps2_cut_rfnd.append(amp_refined)
            #
        #
    #
    
    if freq_lim>0:
        if do_refine_freqs==True:
            freqs_impact_sensor1=copy.deepcopy(freqs1_cut_rfnd)
            amps_impact_sensor1=copy.deepcopy(amps1_cut_rfnd)
            freqs_impact_sensor2=copy.deepcopy(freqs2_cut_rfnd)
            amps_impact_sensor2=copy.deepcopy(amps2_cut_rfnd)
        else:
            freqs_impact_sensor1=copy.deepcopy(freqs1_cut)
            amps_impact_sensor1=copy.deepcopy(amps1_cut)
            freqs_impact_sensor2=copy.deepcopy(freqs2_cut)
            amps_impact_sensor2=copy.deepcopy(amps2_cut)
        #    
    else:
        if do_refine_freqs:
            freqs_impact_sensor1=copy.deepcopy(freqs1_rfnd)
            amps_impact_sensor1=copy.deepcopy(amps1_rfnd)
            freqs_impact_sensor2=copy.deepcopy(freqs2_rfnd)
            amps_impact_sensor2=copy.deepcopy(amps2_rfnd)
        else:
            freqs_impact_sensor1=copy.deepcopy(freqs1)
            amps_impact_sensor1=copy.deepcopy(amps1)
            freqs_impact_sensor2=copy.deepcopy(freqs2)
            amps_impact_sensor2=copy.deepcopy(amps2)
        #
    #
    freqsStackIni1.append(freqs_impact_sensor1)
    freqsStackIni2.append(freqs_impact_sensor2)
    ampsStacksIni1.append(amps_impact_sensor1)
    ampsStacksIni2.append(amps_impact_sensor2)
    #
    df=freqs_impact_sensor1[1]-freqs_impact_sensor1[0]
    if impactN==0 or (impactN>0 and df>dfmin):
        dfmin=df
    #
    # ut'je impact sha freqs et amps.
    # af impact cycle hado sort D.
#for je impact
fTol=0.3*dfmin#ut'cluster'g l'freqs
print("fTol="+str(fTol))
#
freqStackLen1=len(freqsStackIni1)
freqStackLen2=len(freqsStackIni2)
#
peak_Ns1=[]
peak_Ns2=[]
freq_clusters1=[]
freq_clusters2=[]
amps_clusters1=[]
amps_clusters2=[]
QForPeak=5
count_added1=0
#count_added2=0
print("Freqs (sensor 1) Ns:")
for impactN in range(impactsCount):
    print("impactN="+str(impactN))
    freqs_impact_sensor1=freqsStackIni1[impactN]
    amps_impact_sensor1=ampsStacksIni1[impactN]
    impactSpectrumL=len(freqs_impact_sensor1)
    if impactN==0:#ja copy erst impact's spectrum
        for impactFreqN in range(impactSpectrumL):
            clusterFreq=[]
            clusterAmp=[]
            impactFreq=freqs_impact_sensor1[impactFreqN]
            impactAmp=amps_impact_sensor1[impactFreqN]
            clusterFreq.append(impactFreq)
            clusterAmp.append(impactAmp)
            freq_clusters1.append(clusterFreq)
            amps_clusters1.append(clusterAmp)
            QClusters=len(freq_clusters1)
            clusterRepresentativeFreqs=[]
            for clusterFreqN in range(QClusters):
                clusterFreq=freq_clusters1[impactFreqN]#ob os nur 1. impact, cluster ha nur 1 member
                clusterRepresentativeFreqs.append(clusterFreq)
            #
            print("First Impact - Now freqs set is: ",clusterRepresentativeFreqs)
        #
    else:#impactN>0
        print("Impact N "+str(impactN+1))
        clusterRepresentativeFreqs=[]
        for impactFreqN in range(impactSpectrumL):
            impactFreq=freq_clusters1[impactFreqN]
            impactAmp=freq_clusters1[impactFreqN]
            print("N in impact spectrum" +str(impactFreqN+1)+" freq.="+str(impactFreq))
            #clusterRepresentativeFreqs.append(impactFreq)
            freqIsOfClusterN=0
            for clusterFreqN in range(1, freqStackLen1+1):
                clusterFreq=np.mean(np.array(freqs_impact_sensor1[clusterFreqN]))
                if abs(clusterFreq-impactFreq)<fTol:#belongs to this cluster
                    freqs_impact_sensor1[clusterFreqN-1].append(impactFreq)
                    amps_clusters1[clusterFreqN-1].append(impactAmp)
                    freqIsOfClusterN=clusterFreqN
                    clusterRepresentativeFreqs.append(clusterFreq)
                    #break#q'ver ce? break break't l'for? # break s'bad idea ob clusterRepresentativeFreqs wu n'full
                    print("inserted into cluster NN "+str(freqIsOfClusterN))
                #
            #
            #print("Cluster of "+str(impactN+1)+" is: "+str())
            if freqIsOfClusterN==0:
                newFreqCluster=[]
                newAmpCluster=[]
                newFreqCluster.append(impactFreq)
                newAmpCluster.append(impactAmp)
                poss=FindPosInSucc(clusterRepresentativeFreqs, clusterFreq)
                if poss.isLess==1:
                    arr1DIns(freq_clusters1, newFreqCluster, 1, vsh=0)
                    arr1DIns(amps_clusters1, newAmpCluster, 1, vsh=0)
                    print("added as 1st cluster")
                elif poss.isGreater==1:
                    freq_clusters1.append(newFreqCluster)
                    amps_clusters1.append(newAmpCluster)
                    print("added as last cluster")
                else:
                    freq_clusters1[poss.lessNN+1-1].append(freq)
                    amps_clusters1[poss.lessNN+1-1].append(amp)
                    print("inserted as new cluster N"+str(lessNN+1))
                #
                count_added1+=1
            #
            QClusters=len(freq_clusters1)
            print("Now clusters are")
            for clusterN in range(QClusters):
                print(str(freq_clusters1[clusterN]))
            #
        #
    #
#
#count_added1=0
count_added2=0
print("Freqs (sensor 2) Ns:")
for impactN in range(impactsCount):
    print("impactN="+str(impactN))
    freqs_impact_sensor2=freqsStackIni2[impactN]
    amps_impact_sensor2=ampsStacksIni2[impactN]
    impactSpectrumL=len(freqs_impact_sensor2)
    if impactN==0:#ja copy erst impact's spectrum
        for impactFreqN in range(impactSpectrumL):
            clusterFreq=[]
            clusterAmp=[]
            impactFreq=freqs_impact_sensor2[impactFreqN]
            impactAmp=amps_impact_sensor2[impactFreqN]
            clusterFreq.append(impactFreq)
            clusterAmp.append(impactAmp)
            freq_clusters2.append(clusterFreq)
            amps_clusters2.append(clusterAmp)
            QClusters=len(freq_clusters2)
            clusterRepresentativeFreqs=[]
            for clusterFreqN in range(QClusters):
                clusterFreq=freq_clusters1[impactFreqN]#ob os nur 1. impact, cluster ha nur 1 member
                clusterRepresentativeFreqs.append(clusterFreq)
            #
            print("First Impact - Now freqs set is: ",clusterRepresentativeFreqs)
        #
    else:#impactN>0
        print("Impact N "+str(impactN+1))
        clusterRepresentativeFreqs=[]
        for impactFreqN in range(impactSpectrumL):
            impactFreq=freq_clusters2[impactFreqN]
            impactAmp=freq_clusters2[impactFreqN]
            print("N in impact spectrum" +str(impactFreqN+1)+" freq.="+str(impactFreq))
            #clusterRepresentativeFreqs.append(impactFreq)
            freqIsOfClusterN=0
            for clusterFreqN in range(1, freqStackLen2+1):
                clusterFreq=np.mean(np.array(freqs_impact_sensor2[clusterFreqN]))
                if abs(clusterFreq-impactFreq)<fTol:#belongs to this cluster
                    freqs_impact_sensor2[clusterFreqN-1].append(impactFreq)
                    amps_clusters2[clusterFreqN-1].append(impactAmp)
                    freqIsOfClusterN=clusterFreqN
                    clusterRepresentativeFreqs.append(clusterFreq)
                    #break#q'ver ce? break break't l'for? # break s'bad idea ob clusterRepresentativeFreqs wu n'full
                    print("inserted into cluster NN "+str(freqIsOfClusterN))
                #
            #
            #print("Cluster of "+str(impactN+1)+" is: "+str(clusterRepresentativeFreqs))
            if freqIsOfClusterN==0:
                newFreqCluster=[]
                newAmpCluster=[]
                newFreqCluster.append(impactFreq)
                newAmpCluster.append(impactAmp)
                poss=FindPosInSucc(clusterRepresentativeFreqs, clusterFreq)
                if poss.isLess==1:
                    arr1DIns(freq_clusters2, newFreqCluster, 1, vsh=0)
                    arr1DIns(amps_clusters2, newAmpCluster, 1, vsh=0)
                    print("added as 1st cluster")
                elif poss.isGreater==1:
                    freq_clusters2.append(newFreqCluster)
                    amps_clusters2.append(newAmpCluster)
                    print("added as last cluster")
                else:
                    freq_clusters2[poss.lessNN+1-1].append(freq)
                    amps_clusters2[poss.lessNN+1-1].append(amp)
                    print("inserted as new cluster N"+str(lessNN+1))
                #
                count_added2+=1
            #
            QClusters=len(freq_clusters2)
            print("Now clusters are")
            for clusterN in range(QClusters):
                print(str(freq_clusters2[clusterN]))
            #
        #
    #
#
count_added=count_added1+count_added2
print("Ns added (for both): "+str(count_added))
#
freq_clusters1_med=[]
amp_clusters1_med=[]
QClusters1=len(freq_clusters1)
for clusterN in range(QClusters):
    clusterFreq=freq_clusters1[clusterN]
    clusterAmp=amp_clusters1[clusterN]
    freq_ofCluster=np.mean(np.array(clusterFreq))
    amp_ofCluster= np.sqrt(np.mean(np.array(amps_clusters1[clusterN])**2))
    freq_clusters1_med.append(freq_ofCluster)
    amp_clusters1_med.append(amp_ofCluster)
#
freq_clusters2_med=[]
amp_clusters2_med=[]
QClusters2=len(freq_clusters2)
for clusterN in range(QClusters):
    clusterFreq=freq_clusters2[clusterN]
    clusterAmp=amp_clusters2[clusterN]
    freq_ofCluster=np.mean(np.array(clusterFreq))
    amp_ofCluster= np.sqrt(np.mean(np.array(amps_clusters2[clusterN])**2))
    freq_clusters2_med.append(freq_ofCluster)
    amp_clusters1_med.append(amp_ofCluster)
#
print("average values")
print("Step4 finishes working")
