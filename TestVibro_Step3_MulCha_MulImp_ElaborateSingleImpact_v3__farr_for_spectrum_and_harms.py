from MyPyVibroLib import *
from MyLib1 import *
#
#calc_ln_x_inRegr=False
#
fileEnding="_signal_whole.csv"#"_signal_SingleImpact.csv"

print("Step3 starts working")

#fileEnding="_SingleImpact.csv"

PathToNamesFiles="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"
PathToNamesFiles="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\data"

filePath2="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\results"
filePath2="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\results"

fileOwnNames=[]
#et in Step 3, ak in Step 2, V lir 2 sv files, #ma uz 1-channels nams o'csv-files s'al names o'wav-files, #et uz 2-channels nams o'csv-files atals name o'wav-file, #so S'ute lir atal file ut ved ir nams
with open(PathToNamesFiles+"\\FolderAndFiles.csv", newline='') as f:
    reader = csv.DictReader(f)
    LineN=0
    for row in reader:
        LineN+=1
        if LineN==1:
            filePath=row["Value"]
#
# ImpactBoundsFileOwnName="ImpactBounds.csv" # nu
#
SignalCharFileOwnName="FileChar.csv"

#fileOwnNames=["051_1_M", "051-2"]
#
#filePath="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav"
filePathIniData=filePath+"\\"+"data"#+"\\"+"IniData"
filePathResults=filePath+"\\"+"data"#+"\\"+"Results"
SignalCharFileFullName=filePathIniData+"\\"+SignalCharFileOwnName
filePath2=filePath+"\\"+"results"
#filePathIniData
#ImpactBoundsFileFullName=filePathIniData+"\\"+ImpactBoundsFileOwnName
#
fileEnding_toRead0="_signal_whole.csv"
fileEnding_toRead1="_ImpactsRanges.csv"
#
filenames =[]
ImpactLBs=[]
ImpactHBs=[]
#
ImpactBoundsFileOwnName=""
#
#fN, fNm, fs, tmax, es = ReadDiscretFreq(SignalCharFileFullName)
fileOwnNames,     fs, tms, ess = ReadIniDataNamesAndFreq(SignalCharFileFullName)
dt=1/fs
tmax=tms[0]#ob fs s'id'l
fN=0#
for fNm in fileOwnNames:#
    fN+=1#
    es=ess[fN-1]
    #tmax=tms[fN-1]#ob id'l uz je channel
    print("N "+str(fN)+" "+fNm+" fs="+str(fs)+" => dt=1/fs="+str(dt)+" tmax="+str(tmax)+" es="+str(es))
    #
    ImpactBoundsFileOwnName+=fNm
    if fN<2:
        ImpactBoundsFileOwnName+="_and_"
    else:
        ImpactBoundsFileOwnName+=fileEnding_toRead1#".csv"
    #
print("filePath2="+filePath2)            
ImpactBoundsFileName=filePathIniData+"\\"+ImpactBoundsFileOwnName
print("reading: "+ImpactBoundsFileOwnName+" : "+ImpactBoundsFileName)

imp_rngs=[]
impactNs=[]
#with open(filePathIniData+"\\"+ImpactBoundsFileName1, mode='r', newline='') as f:
with open(filePathIniData+"\\"+ImpactBoundsFileOwnName, mode='r', newline='') as f:
    #print("trying to read "+filePathIniData+"\\"+ImpactBoundsFileName1)
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
impactsCount=len(imp_rngs)
print("In all "+str(impactsCount)+" impacts")

for impactN in range(impactsCount):
    imp_rng=imp_rngs[impactN]
    tStart=imp_rng[1-1]
    tFin1=imp_rng[2-1][1-1]
    tFin2=imp_rng[2-1][2-1]
    ImpLB=tStart
    if tFin1<=tFin2:
        ImpHB=tFin1
    else:
        ImpHB=tFin2
    #
    print("Impact N "+str(impactN)+": "+"Impact N "+str(impactNs[impactN])+": "+str(imp_rng)+" ImpLB="+str(ImpLB)+" - ImpHB="+str(ImpHB))
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
decrs1=[]
decrs2=[]
decrsS=[]
#ImpactBoundsFileName=filePathIniData+"\\"+ImpactBoundsFileOwnName
countImpactsElaborated=0
#with open(src_path, mode='r', newline='', encoding='utf-8') as src_file, \
#open(dst_path, mode='w', newline='', encoding='utf-8') as dst_file:
src_path=filePathIniData+"\\"+ImpactBoundsFileOwnName
#dst_path=filePath2+"\\"+"ResultsMulty.csv"
dst_path_mul=filePath2+"\\"+"ResultsMulty.csv"
dst_path_sngl=filePath2+"\\"+"Results.csv"
#with open(filePathIniData+"\\"+ImpactBoundsFileOwnName, mode='r', newline='') as f:
#with open(src_path, mode='r', newline='', encoding='utf-8') as f, \
#     open(dst_path, mode='a', newline='', encoding='utf-8') as dst_f_mul, \
#     open(dst_path, mode='a', newline='', encoding='utf-8') as dst_f_sngl:
#    print("trying to read "+filePathIniData+"\\"+ImpactBoundsFileOwnName)
#    reader = csv.DictReader(f)
#    #
#    for row in reader:#=>for each impact
#        countImpactsElaborated+=1
print("reading saved impact ranges")
with open(dst_path_mul, mode='a', newline='', encoding='utf-8') as dst_f_mul:
    for impactN in range(impactsCount):
        countImpactsElaborated=impactN+1
        imp_rng=imp_rngs[impactN]
        print("impact "+str(impactN+1)+"="+str(impactNs[impactN])+" : ",imp_rng)
        tStart=imp_rng[1-1]
        tFin1=imp_rng[2-1][1-1]
        tFin2=imp_rng[2-1][1-2]
        #
        decrs1s=0
        decrs2s=0
        decrsSs=0
        #
        ImpLB=tStart
        if tFin1<=tFin2:
            ImpHB=tFin1
        else:
            ImpHB=tFin2
        #
        print("Анализ затухания без модального анализа")
        #
        print("Impact N "+str(impactN)+" "+" tStart="+str(tStart)+" tFin1="+str(tFin1)+" tFin2="+str(tFin2)+" ImpHB="+str(ImpHB))
        #
        ts=[]
        si1=[]
        si2=[]
        en1=[]
        en2=[]
        ensum=[]
        #siS=[]
        #    
        for i in range(1, len(tss)+1):#taks in python
            if tss[i-1]>=ImpLB and tss[i-1]<=ImpHB:
                ts.append(tss[i-1])
                si1.append(sis1[i-1])
                en1.append(ens1[i-1])
                si2.append(sis2[i-1])
                en2.append(ens2[i-1])
                ensum.append(ens1[i-1]+ens2[i-1])
                #siS.append(sis1[i-1]+sis2[i-1])
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
        enS=[]
        Qvals=len(en1)
        for i in range (1, Qvals+1):
            enS.append(en1[i-1]+en2[i-1])
        #
        print("len(enS)="+str(len(enS)))
        #
        do_ShowLibEnvelope=False
        if do_ShowLibEnvelope:
            #
            #envelope - hilbert
            #
            env1, decr1 = analyze_signal1(ts, en1, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
            env2, decr2 = analyze_signal1(ts, en2, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
            envS, decrS = analyze_signal1(ts, enS, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
            #
            GraphName="Энергия сигналов и огибающая - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            #
            plot_several1([
                [
                   [(ts, en1), (ts, env1)], 1
                ],
                [
                   [(ts, en2), (ts, env2)], 1
                ],
                [
                   [(ts, enS), (ts, envS)], 1
                ]
              ],
              [
                ["t, с", "Энергия сигнала", "Огибающая"],                  
                ["t, с", "Энергия сигнала", "Огибающая"],
                ["t, с", "Энергия сигнала", "Огибающая"]
              ],
              [
                [ {"color":"green"}, {"color":"red"}],
                [ {"color":"green"}, {"color":"red"}],
                [ {"color":"green"}, {"color":"red"}]
              ],
              GraphName
            )
            #            
            #envelope - lib - polynome by min quadrats 
            #            
            env1, decr1 = analyze_signal1(ts, en1, method="hilbert", n_peaks=6, peak_thresh=0.3)
            env2, decr2 = analyze_signal1(ts, en2, method="hilbert", n_peaks=6, peak_thresh=0.3)
            envS, decrS = analyze_signal1(ts, enS, method="hilbert", n_peaks=6, peak_thresh=0.3)
            #            
            print("len(envS)="+str(len(envS)))
            
            GraphName="Энергия сигналов и огибающая - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            
            plot_several1(
              [
                [
                   [(ts, en1), (ts, env1)], 1
                ],
                [
                   [(ts, en2), (ts, env2)], 1
                ],
                [
                   [(ts, enS), (ts, envS)], 1
                ]
              ],
              [
                ["t, с", "Энергия сигнала", "Огибающая"],                  
                ["t, с", "Энергия сигнала", "Огибающая"],
                ["t, с", "Энергия сигнала", "Огибающая"]
              ],
              [
                [ {"color":"green"}, {"color":"red"}],
                [ {"color":"green"}, {"color":"red"}],
                [ {"color":"green"}, {"color":"red"}]
              ],
              GraphName
             )
        # ce wa envelope libs
        print("len(en1="+str(len(en1))+" len(en2="+str(len(en2))+" len(enS="+str(len(enS)))
        #print("ts:")
        #for i in range(len(ts)):
        #    print(str(i)+") "+str(ts[i]))
        QPoints=len(en1)
        QSects=50#50#200
        vsh=0#1 this 67000, 67200, 66800

        trs1, peaksHs1 = MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(en1, ts, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
        trs2, peaksHs2 = MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(en2, ts, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
        trsS, peaksHsS = MyEnvelopeBuilding_sumPart2of3_DefinePeakVals(enS, ts, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)

        #envelopes

        enve1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ts, type_Stairs0Line1=0)
        enve2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ts, type_Stairs0Line1=0)
        enveS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ts, type_Stairs0Line1=0)

        print("linear interpolation calc'd successfully")

        if do_ShowLibEnvelope:#2nd case

            env1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ts, type_Stairs0Line1=1)
            env2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ts, type_Stairs0Line1=1)
            envS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ts, type_Stairs0Line1=1)

            print("stairs calc'd successfully")

            A01=enve1[0]
            A02=enve2[0]
            A0S=enveS[0]

            plot_several1([
                [
                   [(ts, en1), (ts, enve1), (ts, env1)], 1
                ],
                [
                   [(ts, en2), (ts, enve2), (ts, env2)], 1
                ],
                [
                   [(ts, enS), (ts, enveS), (ts, envS)], 1
                ]
              ],
              [
                ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"],                  
                ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"],
                ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"]
              ],
              [
                [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                [ {"color":"green"}, {"color":"red"}, {"color":"blue"}]
              ],
              GraphName
             )
        else:
            print("Show envelope partially turned off")
        #
        #if do_ShowLibEnvelope, 2.case
        do_ExcludeLowerPeaks=False

        if do_ExcludeLowerPeaks:
            Nps1, t2s1, Hs1 = ExcludeLowerPeaks(peaksHs1, trs1)
            Nps2, t2s2, Hs2 = ExcludeLowerPeaks(peaksHs2, trs2)
            NpsS, t2sS, HsS = ExcludeLowerPeaks(peaksHsS, trsS)
            #
            trs1=[]
            trs1=t2s1
            peaksHs1=[]
            peaksHs1=Hs1
            #
            trs2=[]
            trs2=t2s2
            peaksHs2=[]
            peaksHs2=Hs2
            #
            trsS=[]
            trsS=t2sS
            peaksHsS=[]
            peaksHsS=HsS
            #
            enve1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ts, type_Stairs0Line1=0)
            enve2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ts, type_Stairs0Line1=0)
            enveS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ts, type_Stairs0Line1=0)

            do_CalcStairsAndShowEnvelopedSections=False
            if do_CalcStairsAndShowEnvelopedSections:
                #
                print("linear interpolation calc'd successfully")
                #
                env1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ts, type_Stairs0Line1=1)
                env2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ts, type_Stairs0Line1=1)
                envS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ts, type_Stairs0Line1=1)
                #
                print("stairs calc'd successfully")
                #
                #print("Peaks of envelope: N, T, H1, H2, HS")
                #for i in range(len(Hs1)):
                #    print(str(i+1)+" "+str(trs1[i])+" "+str(Hs1[i])+" "+str(Hs2[i])+" "+str(HsS[i]))
                print("Peaks of envelope:")
                print("N, T1, H1")
                for i in range(len(Hs1)):
                    print(str(i+1)+" "+str(trs1[i])+" "+str(Hs1[i]))
                print("N, T2, H2")
                for i in range(len(Hs2)):
                    print(str(i+1)+" "+str(trs2[i])+" "+str(Hs2[i]))
                print("N, TS, HS")
                for i in range(len(HsS)):
                    print(str(i+1)+" "+str(trsS[i])+" "+str(HsS[i]))     #
                GraphName="Энергия сигналов и огибающая (исключены провалы) - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
                #
                plot_several1(
                  [ 
                    [
                       [(ts, en1), (ts, enve1), (ts, env1)], 1
                    ],
                    [
                       [(ts, en2), (ts, enve2), (ts, env2)], 1
                    ],
                    [
                       [(ts, enS), (ts, enveS), (ts, envS)], 1
                    ]
                  ],
                  [
                    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"],                  
                    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"],
                    ["t, с", "Энергия сигнала", "Огибающая1", "Огибающая2"]
                  ],
                  [
                    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                    [ {"color":"green"}, {"color":"red"}, {"color":"blue"}]
                  ],
                  GraphName
                )
            #if do_CalcStairsAndShowEnvelopedSections 
        # if do-ExcludePeaks  
        print("Approximating peaks")

        print("Signal Energy - Sensor 1")

        #def MyEnvelopeBuilding_part4of3_CalcCoefs   (signal, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, do_lnT=False, do_lnX=True, vsh=0)
        #def MyEnvelopeBuilding_part4of3_CalcCoefs_v1(Hs, Ts, QSects, do_lnT=False, do_lnX=True, vsh=0)

        alfa1, beta1 = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enve1, ts, do_lnT=False, do_lnY=True, vsh=0)

        A01=np.exp(alfa1)
        delta1 = -beta1

        print("alfa1="+str(alfa1)+" beta1="+str(beta1)+" A01="+str(A01)+" delta1="+str(delta1))

        print("Signal Energy - Sensor 2")

        #alfa2, beta2 = MyEnvelopeBuilding_part4of3_CalcCoefs(enve2, QSects, fs, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, do_lnT=False, do_lnX=True, vsh=0)
        alfa2, beta2 = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enve2, ts, do_lnT=False, do_lnY=True, vsh=0)

        A02=np.exp(alfa2)
        delta2 = -beta2

        print("alfa2="+str(alfa2)+" beta2="+str(beta2)+" A02="+str(A02)+" delta2="+str(delta2))

        print("Signal Energy - Sum")
        #alfaS, betaS = MyEnvelopeBuilding_part4of3_CalcCoefs(enveS, QSects, fs, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, do_lnT=False, do_lnX=True, vsh=0)
        alfaS, betaS = MyEnvelopeBuilding_part4of3_CalcCoefs_v1(enveS, ts, do_lnT=False, do_lnY=True, vsh=0)

        A0S=np.exp(alfaS)
        deltaS = -betaS

        print("alfaS="+str(alfaS)+" betaS="+str(betaS)+" A0S="+str(A0S)+" deltaS="+str(deltaS))

        print("alfa1="+str(alfa1)+" beta1="+str(beta1)+" A01="+str(A01)+" delta1="+str(delta1))
        print("alfa2="+str(alfa2)+" beta2="+str(beta2)+" A02="+str(A02)+" delta2="+str(delta2))
        print("alfaS="+str(alfaS)+" betaS="+str(betaS)+" A0S="+str(A0S)+" deltaS="+str(deltaS))

        env1=[]
        env2=[]
        envS=[]

        for i in range(len(ts)):
            t=ts[i]-ts[0]
            env1.append(A01*np.exp(-delta1*t))
            env2.append(A02*np.exp(-delta2*t))
            envS.append(A0S*np.exp(-delta2*t))
            #print(str(i)+" "+str(env1[i])+" "+str(env2[i])+" "+str(envS[i]))

        print("alfa1="+str(alfa1)+" beta1="+str(beta1)+" A01="+str(A01)+" delta1="+str(delta1))
        print("alfa2="+str(alfa2)+" beta2="+str(beta2)+" A02="+str(A02)+" delta2="+str(delta2))
        print("alfaS="+str(alfaS)+" betaS="+str(betaS)+" A0S="+str(A0S)+" deltaS="+str(deltaS))

        GraphName="Энергия сигналов, ступенчатая огибающая и аппроксимация экспонентой с вычислением и отображением декремента затухания - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

        plot_several1(
              [
                [
                   [(ts, en1), (ts, enve1), (ts, env1)], 1
                ],
                [
                   [(ts, en2), (ts, enve2), (ts, env2)], 1
                ],
                [
                   [(ts, enS), (ts, enveS), (ts, envS)], 1
                ]
              ],
              [
                ["t, с", "Энергия сигнала", "Огибающая", "Аппроксимация: decr="+str(-beta1)],                  
                ["t, с", "Энергия сигнала", "Огибающая", "Аппроксимация: decr="+str(-beta2)],
                ["t, с", "Энергия сигнала", "Огибающая", "Аппроксимация: decr="+str(-betaS)]
              ],
              [
                [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                [ {"color":"green"}, {"color":"red"}, {"color":"blue"}],
                [ {"color":"green"}, {"color":"red"}, {"color":"blue"}]
              ],
              GraphName
        )
        
        decr1=-beta1
        decr2=-beta2
        decrS=-betaS

        decrs1.append(decr1)
        decrs2.append(decr2)
        decrsS.append(decrS)

        decrs1s+=decr1
        decrs2s+=decr2
        decrsSs+=decrS

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

        print("results of impact"+str(impactN)+"("+str(countImpactsElaborated)+")"+": decr1="+str(decr1)+" decr2="+str(decr2)+" decrS="
              +str(decrS)+". Medium vals: decr1="+str(decR1)+" decr2="+str(decR2)+" decrS="+str(decRS)+" decrSs="+str(decrsSs))

        #lif kin file
        writer_mul = csv.writer(dst_f_mul)
        writer_mul.writerow([str(impactN), str(decr1), str(decr2), str(decrS), str(decR1), str(decR2), str(decRS), fileOwnNames[1-1], fileOwnNames[2-1]])
        print("Дописали строку текущих значений в .csv-файл")

        #

        do_ElaborateFreqs=True
        do_ElaborateImpactN=2#0

        #freq_st=[3.5,  9.5,  11.5,      20,     30,   32,    43,    50,    60] # pg7
        #freq_st=[  3, 9.75, 10.75,      19,     29, 31.5,  44.5,    47, 59.75] # pg8
        #freq_st=[  3,    9,    10,    18.75,   28.5,   31,  43.5,   46,  57.5] # etw pg9
        freqs_st=[   3,  9.5,  10.5,       19,     29, 31.5,  43.5,   47,  59.5] # pg10 aver
        #freq_st=[  3,  9.5,  10.5,       19,     29, 31.5, 43.75, 47.5,    59] # my try calc med
        #          F1    F2     C1        F3      C2    F4     T1    F5     C3  lis sdi dirs: F - flap, C - chord, T - torsion) 
        #           1     2      3         4       5     6      7     8      9
        # os ab TД 006.25
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

            print("Урезаем спектр до разумного набора.")
        
            freq_lim=66#66 - if less than 66, so by QForPeak==5 ne find f=62
        
            if freq_lim==0:
                freqLastNN=QFreqs
            else:
                QFreqs=len(freqs1)
                for i in range(1, QFreqs-1+1):
                    if freqs1[i-1]<=freq_lim and freqs1[i+1-1]>freq_lim:
                        freqLastNN=i
                    #
                #
            #
            if freq_lim>0:
                print("lim f["+str(freqLastNN)+"]="+str(freq_lim))
                #
                freqs1=freqs1[:freqLastNN]
                amps1 =amps1[:freqLastNN]
                freqs2=freqs2[:freqLastNN]
                amps2=amps2[:freqLastNN]
                #freqsS=freqsS[:freqLastNN]
                #ampsS=ampsS[:freqLastNN]
            #
               
            #print("Nu len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))
            print("Nu len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2)))
            
            GraphName="Спектр  сигнала (корректированный и сокращенный)- удар № "+str(impactN)+" - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            
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
        
            QForPeak=5#10#50#50

            #
            print("data 1")
            peaksNs1, peakFreqs1, peaks1 = MyFindFreqsPeaks(np.array(freqs1), np.array(amps1), QForPeak=QForPeak, vsh=0)
            QFreqPeaks1=len(peakFreqs1)
            print("Peaks of freqs: "+str(QFreqPeaks1))
            for i in range(1, QFreqPeaks1+1):
                print("peakN "+str(i)+" freq = "+str(peakFreqs1[i-1])+" freqN= "+str(peaksNs1[i-1])+" ampl= "+str(peaks1[i-1]))
            #
            print("data 2")
            peaksNs2, peakFreqs2, peaks2 = MyFindFreqsPeaks(np.array(freqs2), np.array(amps2), QForPeak=QForPeak, vsh=0)
            QFreqPeaks2=len(peakFreqs2)
            print("Peaks of freqs: "+str(QFreqPeaks2))
            for i in range(1, QFreqPeaks2+1):
                print("peakN "+str(i)+" freq = "+str(peakFreqs2[i-1])+" freqN= "+str(peaksNs2[i-1])+" ampl= "+str(peaks2[i-1]))
            #
            #print("data S")
            #peaksNsS, peakFreqsS, peaksS = MyFindFreqsPeaks(np.array(freqsS), np.array(ampsS), QForPeak=QForPeak, vsh=0)
            #QFreqPeaksS=len(peakFreqsS)
            #print("Peaks of freqs: "+str(QFreqPeaksS))
            #for i in range(1, QFreqPeaksS):
            #    print("peakN "+str(i)+" freq = "+str(peakFreqsS[i-1])+" freqN= "+str(peaksNsS[i-1])+" ampl= "+str(peaksS[i-1]))
            #
            # L'spectrum M etr f'signals, n'energy. So sum o'vals ab tbi senzs n'ha phys sdio. AI rat fy S (anal l'spectrum) deco f'je senz
            #
            amplPerCentApplicable=10
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
            print("Chosen frequences ("+str(QFreqPeaks1Chosen)+")of 1st sensor:")
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
            print("Chosen frequences ("+str(QFreqPeaks1Chosen)+")of 2nd sensor:")
            for i in range(QFreqPeaks2Chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs2_chosen[i])+" freq="+str(peakFreqs2_chosen[i])+" ampl="+str(peaks2_chosen[i]))
            #
            #
            vsh=0
            print("Sorted data 1 by amp descendence")
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
            print("Sorted data 1 by freq ascendence")
            #def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
            Sort3ArraysByOne_v2(peaksNs1, peakFreqs1, peaks1, by123=2, DescNotAsc=False, vsh=vsh)
            for i in range(QFreqPeaks1):
                print(str(i+1)+") "+" N: "+str(peaksNs1[i])+" freq="+str(peakFreqs1[i])+" ampl="+str(peaks1[i]))
            print("Again:")
            peaksNs1, peakFreqs1, peaks1=Sort3ArraysByOne_v3(peaksNs1, peakFreqs1, peaks1, by123=1, AscNotDesc=True, vsh=vsh)
            for i in range(QFreqPeaks1):
                print(str(i+1)+") "+" N: "+str(peaksNs1[i])+" freq="+str(peakFreqs1[i])+" ampl="+str(peaks1[i]))
            #
            print("Sorted data 2 by amp descendence")
            #def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
            Sort3ArraysByOne_v2(peaksNs2, peakFreqs2, peaks2, by123=3, DescNotAsc=True, vsh=vsh)
            for i in range(QFreqPeaks2):
                print(str(i+1)+") "+" N: "+str(peaksNs2[i])+" freq="+str(peakFreqs2[i])+" ampl="+str(peaks2[i]))
            print("Again:")
            peaksNs2, peakFreqs2, peaks2=Sort3ArraysByOne_v3(peaksNs2, peakFreqs2, peaks2, by123=3, AscNotDesc=False, vsh=vsh)
            for i in range(QFreqPeaks2):
                print(str(i+1)+") "+" N: "+str(peaksNs2[i])+" freq="+str(peakFreqs2[i])+" ampl="+str(peaks2[i]))
            #        
            print("Sorted data 2 by freq ascendence")
            #def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
            Sort3ArraysByOne_v2(peaksNs2, peakFreqs2, peaks2, by123=2, DescNotAsc=False, vsh=vsh)
            for i in range(QFreqPeaks2):
                print(str(i+1)+") "+" N: "+str(peaksNs2[i])+" freq="+str(peakFreqs2[i])+" ampl="+str(peaks2[i]))
            print("Again:")
            peaksNs2, peakFreqs2, peaks2=Sort3ArraysByOne_v3(peaksNs2, peakFreqs2, peaks2, by123=1, AscNotDesc=True, vsh=vsh)
            for i in range(QFreqPeaks2):
                print(str(i+1)+") "+" N: "+str(peaksNs2[i])+" freq="+str(peakFreqs2[i])+" ampl="+str(peaks2[i]))
            #    
            #
            #def ChooseFreqsBySetMemberN(Ns, Freqs, amps, FreqsSample, N, dFPercent=20):
            for frstN in range(1, QFreqsSt+1):
                print("Finding fitting frequences for frequency N"+str(frstN)+" = "+str(freqs_st[frstN-1]))
                freqBlock=ChooseFreqsBySetMemberN(peaksNs1, peakFreqs1, peaks1, freqs_st, frstN, dFPercent=20)
                if freqBlock!=[]:
                    N1=freqBlock[1-1]
                    freq1=freqBlock[2-1]
                    amp1=freqBlock[3-1]
                    print("for frequency N"+str(frstN)+" = "+str(freqs_st[frstN-1])+" chosen frequency (1st sensor) (max amplitude among nearest):")
                    print(str(N1)+") "+" freq="+str(freqs1[N1-1])+" ampl="+str(amps1[N1-1]))
                    #
                    peaksNs1_chosen.append(N1)
                    peakFreqs1_chosen.append(freq1)
                    peaks1_chosen.append(amp1)
                    
                else:
                    print("no freqs of sensor 1 fit this value")
                freqBlock=ChooseFreqsBySetMemberN(peaksNs2, peakFreqs2, peaks2, freqs_st, frstN, dFPercent=20)
                if freqBlock!=[]:
                    N2=freqBlock[1-1]
                    freq2=freqBlock[2-1]
                    amp2=freqBlock[3-1]
                    print("for frequency N"+str(frstN)+" = "+str(freqs_st[frstN-1])+" chosen frequency (2nd sensor) (max amplitude among nearest):")
                    print(str(N2)+") "+" freq="+str(freqs2[N2-1])+" ampl="+str(amps2[N2-1]))#wa N1 et S ecri err: name 'N1' is not defined - qob? S'def'd
                    #
                    peaksNs2_chosen.append(N2)
                    peakFreqs2_chosen.append(freq2)
                    peaks2_chosen.append(amp2)
                else:
                    print("no freqs of sensor 2 fit this value")
                #
            #
            print("\nFinaly - chosen frequences:")
            Q1_chosen=len(peakFreqs1_chosen)
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
            print("Sorted data of 1st sensor renewed by freq ascendence")
            Sort3ArraysByOne_v2(peaksNs2_chosen, peakFreqs2_chosen, peaks2_chosen, by123=2, DescNotAsc=False, vsh=vsh)
            for i in range(Q2_chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs2_chosen[i])+" freq="+str(peakFreqs2_chosen[i])+" ampl="+str(peaks2_chosen[i]))
            print("Again:")
            peaksNs2_chosen, peakFreqs2_chosen, peaks2_chosen= Sort3ArraysByOne_v3(peaksNs2_chosen, peakFreqs2_chosen, peaks2_chosen, by123=1, AscNotDesc=True, vsh=vsh)
            for i in range(Q2_chosen):
                print(str(i+1)+") "+" N: "+str(peaksNs2_chosen[i])+" freq="+str(peakFreqs2_chosen[i])+" ampl="+str(peaks2_chosen[i]))
            #
        #
    #for each impact#--------------------------------------------------------------------------------------------------------------------------

    with open(filePath2+"\\"+"Results.csv", mode='a', newline='') as dst_f_sngl:
        writer_sngl = csv.writer(dst_f_sngl)
        writer_sngl.writerow([fileOwnNames[1-1], fileOwnNames[2-1], str(decR1), str(decR2), str(decRS)])
    #
    print("Дописали строку средних значений в Results.csv")
    print ("\nВесь сигнал, все удары\n")

    ts=[]
    si1=[]
    si2=[]
    en1=[]
    en2=[]
    ensum=[]
    siS=[]
    # 
    for i in range(1, len(tss)+1):#taks in python
        #if tss[i-1]>=ImpLB and tss[i-1]<=ImpHB:
        ts.append(tss[i-1])
        si1.append(sis1[i-1])
        en1.append(ens1[i-1])
        si2.append(sis2[i-1])
        en2.append(ens2[i-1])
        ensum.append(ens1[i-1]+ens2[i-1])
        siS.append(sis1[i-1]+sis2[i-1])
    #
    
    print("read vals: ts:" +str(len(ts))+" vals, +si1: "+str(len(si1))+" vals, +en1: "+str(len(en1))+" +si2: "+str(len(si2))+" vals, +en2: "+str(len(en2))+" ")

    do_ElaborateFreqs=True
    do_ElaborateImpactN=2#0

    if do_ElaborateFreqs and (do_ElaborateImpactN==0 or impactN==do_ElaborateImpactN):
        
        use_window=True
        use_detrend=False
        use_mean=False

        freqs1, amps1 = compute_spectrum(en1, fs=fs, use_window=use_window)
        freqs2, amps2 = compute_spectrum(en2, fs=fs, use_window=use_window)
        freqsS, ampsS = compute_spectrum(enS, fs=fs, use_window=use_window)

        QFreqs=len(freqs1)
        
        GraphName="Спектр энергии сигнала - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
        
        plot_several1(
            [
                [
                    [(freqs1, amps1)], 1
                ],
                [
                    [(freqs2, amps2)], 1
                ],
                [
                   [(freqsS, ampsS)], 1
                ]
            ],
            [
                ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                ["Частота, Гц", "Амплитуда энергии сигнала"],
                ["Частота, Гц", "Амплитуда энергии сигнала"]
            ],
            None,
            GraphName
        )
        
        print("now len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))
        
        use_window=True
        use_detrend=True
        use_mean=False
        
        print("Корррекция 1 спектр - добавляем mean, detrend, zero_padding_factor")
        print("use_window="+str(use_window)+" use_detrend="+str(use_detrend)+" use_mean="+str(use_mean))

        #def compute_spectrum(x, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)
        
        freqs1, amps1 = compute_spectrum(si1, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
        freqs2, amps2 = compute_spectrum(si2, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
        freqsS, ampsS = compute_spectrum(siS, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
        
        GraphName="Спектр энергии сигнала (корректированный)- файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            
        plot_several1(
            [
                [
                    [(freqs1, amps1)], 1
                ],
                [
                    [(freqs2, amps2)], 1
                ],
                [
                    [(freqsS, ampsS)], 1
                ]
            ],
            [
                ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                ["Частота, Гц", "Амплитуда энергии сигнала"],
                ["Частота, Гц", "Амплитуда энергии сигнала"]
            ],
            None,
            GraphName
        )

        print("Урезаем спектр до разумного набора.")

        freq_lim=66#66 - if less than 66, so by QForPeak==5 ne find f=62
        
        if freq_lim==0:
            freqLastNN=QFreqs
        #
        else:
            for i in range(1, QFreqs-1+1):
                if freqs1[i-1]<=freq_lim and freqs1[i+1-1]>freq_lim:
                    freqLastNN=i
                #
            #
        #
        if freq_lim>0:
            print("lim f["+str(freqLastNN)+"]="+str(freq_lim))
            #
            freqs1=freqs1[:freqLastNN]
            amps1 =amps1[:freqLastNN]
            freqs2=freqs2[:freqLastNN]
            amps2=amps2[:freqLastNN]
            freqsS=freqsS[:freqLastNN]
            ampsS=ampsS[:freqLastNN]
        #
             
        print("Nu len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))
            
        GraphName="Спектр энергии сигнала (корректированный и сокращенный) - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            
        plot_several1(
            [
                [
                    [(freqs1, amps1)], 1
                ],
                [
                    [(freqs2, amps2)], 1
                ],
                [
                    [(freqsS, ampsS)], 1
                ]
            ],
            [
                ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                ["Частота, Гц", "Амплитуда энергии сигнала"],
                ["Частота, Гц", "Амплитуда энергии сигнала"]
            ],
            None,
            GraphName
        )
        
        QFreqsCut=len(freqs1)

        freqs1_refined=[]
        amps1_refined =[]
        freqs2_refined=[]
        amps2_refined =[]
        freqsS_refined=[]
        ampsS_refined =[]

        for k in range (QFreqsCut):
            freq1_refined, amp1_refined = refine_peak_parabolic(freqs1, amps1, k)
            freq2_refined, amp2_refined = refine_peak_parabolic(freqs2, amps2, k)
            freqS_refined, ampS_refined = refine_peak_parabolic(freqsS, ampsS, k)
            #
            freqs1_refined.append(freq1_refined)
            freqs2_refined.append(freq2_refined)
            freqsS_refined.append(freqS_refined)
            #
            amps1_refined.append(amp1_refined)
            amps2_refined.append(amp2_refined)
            ampsS_refined.append(ampS_refined)
        #

        plot_several1(
            [
                [
                   [(freqs1_refined, amps1_refined)], 1
                ],
                [
                    [(freqs2_refined, amps2_refined)], 1
                ],
                [
                   [(freqsS_refined, ampsS_refined)], 1
                ]
            ],
            [
                ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                ["Частота, Гц", "Амплитуда энергии сигнала"],
                ["Частота, Гц", "Амплитуда энергии сигнала"]
            ],
            None,
            GraphName
        )
        #
        QForPeak=5#10#50#50
        #
        print("data 1")
        peaksNs1, peakFreqs1, peaks1 = MyFindFreqsPeaks(np.array(freqs1), np.array(amps1), QForPeak=QForPeak, vsh=0)
        QFreqPeaks1=len(peakFreqs1)
        print("Peaks of freqs: "+str(QFreqPeaks1))
        for i in range(1, QFreqPeaks1):
            print("peakN "+str(i)+" freq = "+str(peakFreqs1[i-1])+" freqN= "+str(peaksNs1[i-1])+" ampl= "+str(peaks1[i-1]))
        #
        print("data 2")
        peaksNs2, peakFreqs2, peaks2 = MyFindFreqsPeaks(np.array(freqs2), np.array(amps2), QForPeak=QForPeak, vsh=0)
        QFreqPeaks2=len(peakFreqs2)
        print("Peaks of freqs: "+str(QFreqPeaks2))
        for i in range(1, QFreqPeaks2):
            print("peakN "+str(i)+" freq = "+str(peakFreqs2[i-1])+" freqN= "+str(peaksNs2[i-1])+" ampl= "+str(peaks2[i-1]))
        #
        print("data S")
        peaksNsS, peakFreqsS, peaksS = MyFindFreqsPeaks(np.array(reqsS), np.array(ampsS), QForPeak=QForPeak, vsh=0)
        QFreqPeaksS=len(peakFreqsS)
        print("Peaks of freqs: "+str(QFreqPeaksS))
        for i in range(1, QFreqPeaksS):
            print("peakN "+str(i)+" freq = "+str(peakFreqsS[i-1])+" freqN= "+str(peaksNsS[i-1])+" ampl= "+str(peaksS[i-1]))
        #
        
        
    #
#
print("done")
#-----------------------------------------------------

'''


do_ElaborateFreqs=True

if do_ElaborateFreqs:

    #
    ImpLB=tss[1-1]
    ImpHB=tmax
    #
    
    ts=[]
    si1=[]
    si2=[]
    en1=[]
    en2=[]
    ensum=[]
    #    
    for i in range(1, len(tss)+1):#taks in python
        if tss[i-1]>=ImpLB and tss[i-1]<=ImpHB:
            ts.append(tss[i-1])
            si1.append(sis1[i-1])
            en1.append(ens1[i-1])
            si2.append(sis2[i-1])
            en2.append(ens2[i-1])
            ensum.append(ens1[i-1]+ens2[i-1])
        #
    #
        
    #
    use_window=True
    use_detrend=False
    use_mean=False

    freqs1, amps1 = compute_spectrum(en1, fs=fs, use_window=use_window)
    freqs2, amps2 = compute_spectrum(en2, fs=fs, use_window=use_window)
    freqsS, ampsS = compute_spectrum(enS, fs=fs, use_window=use_window)

    QFreqs=len(freqs1)

    GraphName="Спектр _энергии сигнала - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

    plot_several1(
              [
                [
                   [(freqs1, amps1)], 1
                ],
                [
                    [(freqs2, amps2)], 1
                ],
                [
                   [(freqsS, ampsS)], 1
                ]
              ],
              [
                ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                ["Частота, Гц", "Амплитуда энергии сигнала"],
                ["Частота, Гц", "Амплитуда энергии сигнала"]
              ],
              None,
              GraphName
            )
    use_detrend=False
    use_mean=False

    freqs1, amps1 = compute_spectrum(en1, fs=fs, use_window=use_window)
    freqs2, amps2 = compute_spectrum(en2, fs=fs, use_window=use_window)
    freqsS, ampsS = compute_spectrum(enS, fs=fs, use_window=use_window)

    QFreqs=len(freqs1)

    GraphName="Спектр энергии_ сигнала - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

    plot_several1(
              [
                [
                   [(freqs1, amps1)], 1
                ],
                [
                    [(freqs2, amps2)], 1
                ],
                [
                   [(freqsS, ampsS)], 1
                ]
              ],
              [
                ["Частота, Гц", "Амплитуда энергии сигнала"],                  
                ["Частота, Гц", "Амплитуда энергии сигнала"],
                ["Частота, Гц", "Амплитуда энергии сигнала"]
              ],
              None,
              GraphName
             )

    print("now len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))

    use_window=True
    use_detrend=True
    use_mean=False
    
    #def compute_spectrum(x, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)

    freqs1, amps1 = compute_spectrum(en1, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
    freqs2, amps2 = compute_spectrum(en2, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
    freqsS, ampsS = compute_spectrum(enS, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)

    freq_lim=66#66 - if less than 66, so by QForPeak==5 ne find f=62

    if freq_lim==0:
        freqLastNN=QFreqs
    else:
        for i in range(1, QFreqs-1+1):
            if freqs1[i-1]<=freq_lim and freqs1[i+1-1]>freq_lim:
                freqLastNN=i
    if freq_lim>0:
        print("lim f["+str(freqLastNN)+"]="+str(freq_lim))
        #
        freqs1=freqs1[:freqLastNN]
        amps1 =amps1[:freqLastNN]
        freqs2=freqs2[:freqLastNN]
        amps2=amps2[:freqLastNN]
        freqsS=freqsS[:freqLastNN]
        ampsS=ampsS[:freqLastNN]
        #
    #
    
    print("Nu len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))

    GraphName="Спектр энергии _сигнала (корректированный)- файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

    plot_several1(
        [
            [
                [(freqs1, amps1)], 1
            ],
            [
                [(freqs2, amps2)], 1
            ],
            [
                [(freqsS, ampsS)], 1
            ]
        ],
        [
            ["Частота, Гц", "Амплитуда энергии сигнала"],                  
            ["Частота, Гц", "Амплитуда энергии сигнала"],
            ["Частота, Гц", "Амплитуда энергии сигнала"]
        ],
        None,
        GraphName
    )
    
    k_fr1=(freqs1[2-1]-freqs1[1-1])/(2-1-(1-1))
    k_fr2=(freqs2[2-1]-freqs2[1-1])/(2-1-(1-1))
    k_frS=(freqsS[2-1]-freqsS[1-1])/(2-1-(1-1))
                 
    
    print("now len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))
    
    use_window=True
    use_detrend=True
    use_mean=False
        
    #def compute_spectrum(x, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)
    
    freqs1, amps1 = compute_spectrum(en1, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
    freqs2, amps2 = compute_spectrum(en2, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
    freqsS, ampsS = compute_spectrum(enS, fs=fs, use_window=use_window,  use_mean=use_mean, use_detrend=use_detrend, zero_padding_factor=1)
    
    freq_lim=66#66 - if less than 66, so by QForPeak==5 ne find f=62
    
    if freq_lim==0:
        freqLastNN=QFreqs
    else:
        for i in range(1, QFreqs-1+1):
            if freqs1[i-1]<=freq_lim and freqs1[i+1-1]>freq_lim:
                freqLastNN=i
            #
        #
    #
    if freq_lim>0:
        print("lim f["+str(freqLastNN)+"]="+str(freq_lim))
        #
        freqs1=freqs1[:freqLastNN]
        amps1 =amps1[:freqLastNN]
        freqs2=freqs2[:freqLastNN]
        amps2=amps2[:freqLastNN]
        freqsS=freqsS[:freqLastNN]
        ampsS=ampsS[:freqLastNN]
        #
    #
    
    print("Nu len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))

    GraphName="Спектр энергии _сигнала_ (корректированный)- файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

    plot_several1(
        [   
            [
                [(freqs1, amps1)], 1
            ],
            [
                [(freqs2, amps2)], 1
            ],
            [
                [(freqsS, ampsS)], 1
            ]
        ],
        [
            ["Частота, Гц", "Амплитуда энергии сигнала"],                  
            ["Частота, Гц", "Амплитуда энергии сигнала"],
            ["Частота, Гц", "Амплитуда энергии сигнала"]
        ],
        None,
        GraphName
    )

    QFreqsCut=len(freqs1)

    for k in range (QFreqsCut):
        freqs1_refined, amps1_refined = refine_peak_parabolic(freqs1, amps1, k)
        freqs2_refined, amps2_refined = refine_peak_parabolic(freqs2, amps2, k)
        freqsS_refined, ampsS_refined = refine_peak_parabolic(freqsS, ampsS, k)
    #

    #k_fr1=(freqs1[2-1]-freqs1[1-1])/(2-1-(1-1))
    #k_fr2=(freqs2[2-1]-freqs2[1-1])/(2-1-(1-1))
    #k_frS=(freqsS[2-1]-freqsS[1-1])/(2-1-(1-1))

    QForPeak=5#10#50#50

    #
    print("data 1")
    peaksNs1, peakFreqs1, peaks1 = MyFindFreqsPeaks(np.array(freqs1), np.array(amps1), QForPeak=QForPeak, vsh=0)
    QFreqPeaks1=len(peakFreqs1)
    print("Peaks of freqs: "+str(QFreqPeaks1))
    for i in range(1, QFreqPeaks1):
        print("peakN "+str(i)+" freq = "+str(peakFreqs1[i-1])+" freqN= "+str(peaksNs1[i-1])+" ampl= "+str(peaks1[i-1]))
    #
    print("data 2")
    peaksNs2, peakFreqs2, peaks2 = MyFindFreqsPeaks(np.array(freqs2), np.array(amps2), QForPeak=QForPeak, vsh=0)
    QFreqPeaks2=len(peakFreqs2)
    print("Peaks of freqs: "+str(QFreqPeaks2))
    for i in range(1, QFreqPeaks2):
        print("peakN "+str(i)+" freq = "+str(peakFreqs2[i-1])+" freqN= "+str(peaksNs2[i-1])+" ampl= "+str(peaks2[i-1]))
    #
    print("data S")
    peaksNsS, peakFreqsS, peaksS = MyFindFreqsPeaks(np.array(reqsS), np.array(ampsS), QForPeak=QForPeak, vsh=0)
    QFreqPeaksS=len(peakFreqsS)
    print("Peaks of freqs: "+str(QFreqPeaksS))
    for i in range(1, QFreqPeaksS):
        print("peakN "+str(i)+" freq = "+str(peakFreqsS[i-1])+" freqN= "+str(peaksNsS[i-1])+" ampl= "+str(peaksS[i-1]))
    #

    #GraphName="Спектр энергии сигнала (лишь пики)- файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
    #
    #plot_several1(
    #   [   
    #        [
    #            [(freqs1, amps1)], 1
    #        ],
    #        [
    #            [(freqs2, amps2)], 1
    #        ],
    #        [
    #            [(freqsS, ampsS)], 1
    #        ]
    #    ],
    #    [
    #        ["Частота, Гц", "Амплитуда энергии сигнала"],                  
    #        ["Частота, Гц", "Амплитуда энергии сигнала"],
    #        ["Частота, Гц", "Амплитуда энергии сигнала"]
    #    ],
    #    None,
    #    GraphName
    #)
    #

    '''

print("Step3 finishes working")
