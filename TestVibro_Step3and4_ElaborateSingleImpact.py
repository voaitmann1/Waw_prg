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

bandwidth=2.0,
peak_thresh=0.1#0.1

   # Извлекаем моды
peaks, modes = extract_modes_and_save(ts, si1, fs,
                                          #save_dir="modes_results",
                                          #save_dir="D:\\MyFiles\\MyPrgs\\Python\\wav\\assets\\modes_results",
                                          save_dir="modes_results",
                                          bandwidth=2.0,#bandwidth, #if lif bandwidth=bandwidth, S lif err eiid as int alt tuple
                                          peak_thresh=0.03#0.1#peak_thresh
                                      )

#print("len(peaks)="+str(len(peaks)))
#for i in range(1, len(peaks)) :
#    print("len(peaks["+str(i-1)+"])="+str((peaks[i-1].size())))

# Визуализация
plt.figure(figsize=(10,6))
for f, sig_f in modes.items():
    plt.plot(ts, sig_f, label=f"{f:.1f} Hz")
plt.plot(ts, si1, "k--", alpha=0.4, label="Исходный")
plt.legend()
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.title("Выделенные моды колебаний")
plt.grid(True)
plt.show()
