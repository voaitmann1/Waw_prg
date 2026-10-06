from MyPyVibroLib import *

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

    #=============================================================================



use_window = True
peak_min_height = 0.05
peak_min_prominence = 0.01
peak_min_distance_hz = 2.0
bandwidth = 1.0

# сигнал и время
# t, signal = ... (массивы ваших данных)
signal=enS

# 1. огибающая
envelope = compute_envelope(signal)

# 2. спектр
freqs, amps = compute_spectrum(signal, fs=fs, use_window=use_window)

# 3. поиск пиков
peak_freqs, peak_vals, _ = find_spectrum_peaks(freqs, amps,
                                               min_height=peak_min_height,
                                               min_prominence=peak_min_prominence,
                                               min_distance_hz=peak_min_distance_hz)

# 4. выделение мод
modes = extract_realistic_modes(signal, ts, fs, peak_freqs, envelope=envelope, bandwidth=bandwidth)

# 5. визуализация спектра с пиками
plot_spectrum_with_peaks(freqs, amps, peak_freqs, peak_vals)

# 6. визуализация мод
plt.figure(figsize=(10,5))
plt.plot(ts, signal, label="Исходный сигнал")
plt.plot(ts, envelope, 'k--', label="Огибающая")
for f, mode in modes.items():
    plt.plot(ts, mode, label=f"Мода {f:.2f} Гц")
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.legend()
plt.show()
