from MyPyVibroLib import *
#
#calc_ln_x_inRegr=False
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
ts, si2, en2 = read_SignalAndEnergy_csv(filenames[2-1])
print(filenames[2-1]+" done, "+str(len(si2))+" vals read")
#
tHBnd=4#0#4#7#if tHBnd==7 so len(en1)=67200, len(env1)=66800

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

#envelope - hilbert

env1, decr1 = analyze_signal1(ts, en1, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
env2, decr2 = analyze_signal1(ts, en2, method="mnk_lib", n_peaks=6, peak_thresh=0.3)
envS, decrS = analyze_signal1(ts, enS, method="mnk_lib", n_peaks=6, peak_thresh=0.3)

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

#envelope - lib - polynome by min quadrats

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

    #=============================================================================
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

do_ExcludeLowerPeaks=True

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
    #
    enve1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ts, type_Stairs0Line1=0)
    enve2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ts, type_Stairs0Line1=0)
    enveS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ts, type_Stairs0Line1=0)
    #
    print("linear interpolation calc'd successfully")
    #
    env1 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs1, trs1, ts, type_Stairs0Line1=1)
    env2 = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHs2, trs2, ts, type_Stairs0Line1=1)
    envS = MyEnvelopeBuilding_sumPart3of3_MakeEnvelopeCurveOfPeaksByRealT(peaksHsS, trsS, ts, type_Stairs0Line1=1)
    #
    print("stairs calc'd successfully")
    #
    print("Peaks of envelope: N, T, H1, H2, HS")
    for i in range(len(Hs1)):
        print(str(i+1)+" "+str(trs1[i])+" "+str(Hs1[i])+" "+str(Hs2[i])+" "+str(HsS[i])) 
    #
    GraphName="Энергия сигналов и огибающая (исключены провалы) - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
    #
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

print("Peaks of envelope")
for i in range(len(enve1)):
    print(str(i+1)+" "+str(enve1[i])) 

vsh=0

print("Approximating paks")

print("Signal Energy - Sensor 1")

#def MyEnvelopeBuilding_part4of3_CalcCoefs(signal, QSects, fs=1, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, do_lnT=False, do_lnX=True, vsh=0):

alfa1, beta1 = MyEnvelopeBuilding_part4of3_CalcCoefs(enve1, QSects, fs, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, do_lnT=False, do_lnX=True, vsh=0)

#A01=np.exp(alfa1)
delta1 = -beta1

print("alfa1="+str(alfa1)+" beta1="+str(beta1)+" A01="+str(A01)+" delta1="+str(delta1))

print("Signal Energy - Sensor 2")

alfa2, beta2 = MyEnvelopeBuilding_part4of3_CalcCoefs(enve2, QSects, fs, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, do_lnT=False, do_lnX=True, vsh=0)

#A02=np.exp(alfa2)
delta2 = -beta2

print("alfa2="+str(alfa2)+" beta2="+str(beta2)+" A02="+str(A02)+" delta2="+str(delta2))

print("Signal Energy - Sum")
alfaS, betaS = MyEnvelopeBuilding_part4of3_CalcCoefs(enveS, QSects, fs, vrnN_Integr1_SortedMaxs2_Max3=3, percent=1, do_lnT=False, do_lnX=True, vsh=0)

#A0S=np.exp(alfaS)
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


use_window=True
use_detrend=False
use_mean=False

freqs1, amps1 = compute_spectrum(en1, fs=fs, use_window=use_window)
freqs2, amps2 = compute_spectrum(en2, fs=fs, use_window=use_window)
freqsS, ampsS = compute_spectrum(enS, fs=fs, use_window=use_window)

QFreqs=len(freqs1)

GraphName="Спектр энергии сигнала - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

plot_several1([
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
    
print("Nu len(f1)="+str(len(freqs1))+" "+" len(f2)="+str(len(freqs2))+" "+" len(fS)="+str(len(freqsS)))

GraphName="Спектр энергии сигнала (корректированный)- файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]

plot_several1([
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

QForPeak=5#10#50#50

#
print("data 1")
peaksNs1, peakFreqs1, peaks1 = MyFindFreqsPeaks(freqs1, amps1, QForPeak=QForPeak, vsh=0)
QFreqPeaks1=len(peakFreqs1)
print("Peaks of freqs: "+str(QFreqPeaks1))
for i in range(1, QFreqPeaks1):
    print("peakN "+str(i)+" freq = "+str(peakFreqs1[i-1])+" freqN= "+str(peaksNs1[i-1])+" ampl= "+str(peaks1[i-1]))
#
print("data 2")
peaksNs2, peakFreqs2, peaks2 = MyFindFreqsPeaks(freqs2, amps2, QForPeak=QForPeak, vsh=0)
QFreqPeaks2=len(peakFreqs2)
print("Peaks of freqs: "+str(QFreqPeaks2))
for i in range(1, QFreqPeaks2):
    print("peakN "+str(i)+" freq = "+str(peakFreqs2[i-1])+" freqN= "+str(peaksNs2[i-1])+" ampl= "+str(peaks2[i-1]))
#
print("data S")
peaksNsS, peakFreqsS, peaksS = MyFindFreqsPeaks(freqsS, ampsS, QForPeak=QForPeak, vsh=0)
QFreqPeaksS=len(peakFreqsS)
print("Peaks of freqs: "+str(QFreqPeaksS))
for i in range(1, QFreqPeaksS):
    print("peakN "+str(i)+" freq = "+str(peakFreqsS[i-1])+" freqN= "+str(peaksNsS[i-1])+" ampl= "+str(peaksS[i-1]))

#use_window = True
#peak_min_height = 0.05
#peak_min_prominence = 0.01
#peak_min_distance_hz = 2.0
#bandwidth = 1.0

## сигнал и время
## t, signal = ... (массивы данных)
#signal=enS

## 1. огибающая
#envelope = compute_envelope(signal)

## 2. спектр

#def compute_spectrum(x, fs, use_window=False, use_mean=False, use_detrend=False, zero_padding_factor=1)


## 3. поиск пиков
#peak_freqs, peak_vals, _ = find_spectrum_peaks(freqs, amps,
#                                               min_height=peak_min_height,
#                                               min_prominence=peak_min_prominence,
#                                               min_distance_hz=peak_min_distance_hz)

## 4. выделение мод
#modes = extract_realistic_modes(signal, ts, fs, peak_freqs, envelope=envelope, bandwidth=bandwidth)

## 5. визуализация спектра с пиками
#plot_spectrum_with_peaks(freqs1, amps1, peak_freqs, peak_vals)
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

