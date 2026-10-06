from MyPyVibroLib import *
#
SignalCharFileOwnName="FileChar.csv"
fileOwnNames=["051_1_M", "051-2"]
fileEnding="_signal_SingleImpactRange.csv"
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
for fileOwnName in fileOwnNames:
    fileFullName = filePathIniData +"\\"+ fileOwnName+fileEnding
    filenames.append(fileFullName)
    print("reading "+fileFullName)
#
print("trying to read "+filenames[1-1])
ts, si1, en1 = read_SignalAndEnergy_csv(filenames[1-1])
print(filenames[1-1]+" done, "+str(len(si1))+" vals read")
print("trying to read "+filenames[2-1])
ts, si2, en2  = read_SignalAndEnergy_csv(filenames[2-1])
print(filenames[2-1]+" done, "+str(len(si2))+" vals read")
#
tHBnd=4#0#4#7#if tHBnd==7 so len(en1)=67200, len(env1)=66800
# 67000=67000 - ignoring this point
# 67200=6700 - ignoring this point  - this was written thrice
if tHBnd!=0:
    indexHB=int(tHBnd*fs)
    print("indexHB="+str(indexHB))
    ts=ts[:indexHB]
    si1=si1[:indexHB]
    si2=si2[:indexHB]
    en1=en1[:indexHB]
    en2=en2[:indexHB]
#
data_to_plot=[((ts, si1), (ts, en1)), ((ts, si2), (ts, en2))]
dataNames=[""]
#data_to_plot=[((ts,x1), (ts, y1)), (ts, y1)]

#   
GraphName="Сигналы и их энергия обоих датчиков - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
#
#plot_several(data_to_plot, labels=None, title=GraphName)
plot_several1([
                [
                   [(ts, si1), (ts, en1)], 2
                ],
                [
                   [(ts, si1), (ts, en1)], 2
                ],
                [
                   [(ts, en1+en2)], 1
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
print("len(enS)="+str(len(enS)))

#env1, decr1 = analyze_signal(ts, en1, method="mnk_manual")
#env2, decr2 = analyze_signal(ts, en2, method="mnk_manual")
#envS, decrS = analyze_signal(ts, enS, method="mnk_manual")
#env1, decr1 = analyze_signal(ts, en1, method="mnk_lib")
#env2, decr2 = analyze_signal(ts, en2, method="mnk_lib")
#envS, decrS = analyze_signal(ts, enS, method="mnk_lib")
#env1, decr1 = analyze_signal(ts, en1, method="hilbert")
#env2, decr2 = analyze_signal(ts, en2, method="hilbert")
#envS, decrS = analyze_signal(ts, enS, method="hilbert")

#env1, decr1 = analyze_signal1(ts, en1, method="mnk_manual")
#env2, decr2 = analyze_signal1(ts, en2, method="mnk_manual")
#envS, decrS = analyze_signal1(ts, enS, method="mnk_manual")
#env1, decr1 = analyze_signal1(ts, en1, method="mnk_lib")
#env2, decr2 = analyze_signal1(ts, en2, method="mnk_lib")
#envS, decrS = analyze_signal1(ts, enS, method="mnk_lib")
#env1, decr1 = analyze_signal1(ts, en1, method="hilbert")
#env2, decr2 = analyze_signal1(ts, en2, method="hilbert")
#envS, decrS = analyze_signal1(ts, enS, method="hilbert")

#env1, decr1 = analyze_signal1(ts, en1, method="mnk_manual", n_peaks=6, peak_thresh=0.3)
#env2, decr2 = analyze_signal1(ts, en2, method="mnk_manual", n_peaks=6, peak_thresh=0.3)
#envS, decrS = analyze_signal1(ts, enS, method="mnk_manual", n_peaks=6, peak_thresh=0.3)
#env1, decr1 = analyze_signal1(ts, en1, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
#env2, decr2 = analyze_signal1(ts, en2, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
#envS, decrS = analyze_signal1(ts, enS, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
env1, decr1 = analyze_signal1(ts, en1, method="hilbert", n_peaks=6, peak_thresh=0.3)
env2, decr2 = analyze_signal1(ts, en2, method="hilbert", n_peaks=6, peak_thresh=0.3)
envS, decrS = analyze_signal1(ts, enS, method="hilbert", n_peaks=6, peak_thresh=0.3)



print("len(envS)="+str(len(envS)))

GraphName="Энергия сигналов и огибающая - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

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

env1, decr1 = analyze_signal1(ts, en1, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
env2, decr2 = analyze_signal1(ts, en2, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
envS, decrS = analyze_signal1(ts, enS, method="mnk_lib", n_peaks=6, peak_thresh=0.3)



print("len(envS)="+str(len(envS)))

GraphName="Энергия сигналов и огибающая - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

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

    #=============================================================================
print("len(en1="+str(len(en1))+" len(en2="+str(len(en2))+" len(enS="+str(len(enS)))
QPoints=len(en1)
QSects=50#200
vsh=0#1 this 67000, 67200, 66800
#Ns=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, vsh=0)
#Hs=MyEnvelopeBuilding_part3of3_BuildingStairs(en1, QSects)#, fs)
#print("len(en1="+str(len(en1))+" len(en2="+str(len(en2))+" len(enS="+str(len(enS))+" len(Hs)="+str(len(Hs)))#+" len(Hs[0])="+str(len(Hs[0])))

#Hs1=

enve1=MyEnvelopeBuilding_part3of3_BuildingStairs(en1, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh) # True False
#enve1 = MyEnvelopeBuilding_part3of3_BuildingCurveLinApprox(en1, QSects, fs)
enve2=MyEnvelopeBuilding_part3of3_BuildingStairs(en2, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
#enve2 = MyEnvelopeBuilding_part3of3_BuildingCurveLinApprox(en2, QSects, fs)
enveS=MyEnvelopeBuilding_part3of3_BuildingStairs(enS, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, vsh=vsh)
#enveS = MyEnvelopeBuilding_part3of3_BuildingCurveLinApprox(en2, QSects, fs)
print("len(en1="+str(len(en1))+" len(env1="+str(len(env1)))

A01=enve1[0]
A02=enve2[0]
A0S=enveS[0]

plot_several1([
                [
                   [(ts, en1), (ts, enve1)], 1
                ],
                [
                   [(ts, en2), (ts, enve2)], 1
                ],
                [
                   [(ts, enS), (ts, enveS)], 1
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


vsh=0

print("Signal Energy - Sensor 1")

alfa1, beta1 = MyEnvelopeBuilding_part4of3_CalcCoefs(enve1, QSects, fs)

#A01=np.exp(alfa1)
delta1 = -beta1

print("alfa1="+str(alfa1)+" beta1="+str(beta1)+" A01="+str(A01)+" delta1="+str(delta1))

print("Signal Energy - Sensor 2")

alfa2, beta2 = MyEnvelopeBuilding_part4of3_CalcCoefs(enve2, QSects, fs)

#A02=np.exp(alfa2)
delta2 = -beta2

print("alfa2="+str(alfa2)+" beta2="+str(beta2)+" A02="+str(A02)+" delta2="+str(delta2))

print("Signal Energy - Sum")
alfaS, betaS = MyEnvelopeBuilding_part4of3_CalcCoefs(enveS, QSects, fs)

#A0S=np.exp(alfaS)
deltaS = -betaS

print("alfaS="+str(alfaS)+" betaS="+str(betaS)+" A0S="+str(A0S)+" deltaS="+str(deltaS))

#A01=exp(alfa1)
#A02=exp(alfa2)
#A0S=exp(alfaS)
#delta1 = -beta1
#delta2 = -beta2
#deltaS = -betaS

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

      
#plot_several1([
#                [
#                   [(ts, en1), (ts, env1)], 1
#                ],
#                [
#                   [(ts, en2), (ts, env2)], 1
#                ],
#                [
#                   [(ts, enS), (ts, envS)], 1
#                ]
#              ],
#              [
#                ["t, с", "Энергия сигнала", "Огибающая"],                  
#                ["t, с", "Энергия сигнала", "Огибающая"],
#                ["t, с", "Энергия сигнала", "Огибающая"]
#              ],
#             [
#               [ {"color":"green"}, {"color":"red"}],
#                [ {"color":"green"}, {"color":"red"}],
#                [ {"color":"green"}, {"color":"red"}]
#              ],
#              GraphName
#             )


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



#use_window = True
#peak_min_height = 0.05
#peak_min_prominence = 0.01
#peak_min_distance_hz = 2.0
#bandwidth = 1.0

## сигнал и время
## t, signal = ... (массивы ваших данных)
#signal=enS

## 1. огибающая
#envelope = compute_envelope(signal)

## 2. спектр
#freqs, amps = compute_spectrum(signal, fs=fs, use_window=use_window)

## 3. поиск пиков
#peak_freqs, peak_vals, _ = find_spectrum_peaks(freqs, amps,
#                                               min_height=peak_min_height,
#                                               min_prominence=peak_min_prominence,
#                                               min_distance_hz=peak_min_distance_hz)

## 4. выделение мод
#modes = extract_realistic_modes(signal, ts, fs, peak_freqs, envelope=envelope, bandwidth=bandwidth)

## 5. визуализация спектра с пиками
#plot_spectrum_with_peaks(freqs, amps, peak_freqs, peak_vals)
#
## 6. визуализация мод
#plt.figure(figsize=(10,5))
#plt.plot(ts, signal, label="Исходный сигнал")
#plt.plot(ts, envelope, 'k--', label="Огибающая")
#for f, mode in modes.items():
#    plt.plot(ts, mode, label=f"Мода {f:.2f} Гц")
#plt.xlabel("Время, с")
#plt.ylabel("Амплитуда")
#plt.grid(True)
#plt.legend()
#plt.show()
