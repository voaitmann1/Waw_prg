from MyPyVibroLib import *
from MyLib1 import *
#
fileEnding="_signal_whole.csv"#"_signal_SingleImpact.csv"
fileEnding_toRead1="_ImpactsRanges.csv"
#fileEnding_toRead1="_ImpactsRanges.csv"

print("Step5 starts working")

PathToNamesFiles="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\data"
PathToNamesFiles="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\data"

filePath2="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\results"
filePath2="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav\\results"

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
filenames=[]
ImpactLBs=[]
ImpactHBs=[]
#
ImpactBoundsFileOwnName=""

fN=0#
for fNm in fileOwnNames:#
    fN+=1#
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
tss, sis1, ens1 = read_SignalAndEnergy_csv(filenames[1-1])
print(filenames[1-1]+" done, "+str(len(sis1))+" vals read")
print("trying to read "+filenames[2-1])
tss, sis2, ens2 = read_SignalAndEnergy_csv(filenames[2-1])
print(filenames[2-1]+" done, "+str(len(sis2))+" vals read")
#
impactsCount=len(imp_rngs)
print("In all "+str(impactsCount)+" impacts")
#
ImpactToAnalyzeN=2
freqs1=[]
amps1=[]
freqs2=[]
amps2=[]
#
# writer.writerow(['N', 'Freq', "ampl", "sensorN", "impactN"])
#
with open(PathToNamesFiles+"\\"+"Frequences.csv", mode='r', newline='') as ff:
    reader = csv.DictReader(ff)
    for row in reader:
        recN=int(row["N"])
        freq=float(row["Freq"])
        ampl=float(row["ampl"])
        sensorN=int(row["sensorN"])
        impactN=int(row["impactN"])
        #
        if impactN==ImpactToAnalyzeN:
            if sensorN==1:
                freqs1.append(freq)
                amps1.append(ampl)
                #
                #print(str(recN)+" freq="+str(freq)+" ampl="+str(ampl)+" sensorN="+str(sensorN)+" impactN="+str(impactN))
            elif sensorN==2:
                freqs2.append(freq)
                amps2.append(ampl)
                #
                #print(str(recN)+" freq="+str(freq)+" ampl="+str(ampl)+" sensorN="+str(sensorN)+" impactN="+str(impactN))
            else:
                pass
                #print(str(recN)+" impactN="+str(impactN)+" sensorN="+str(sensorN)+" - incorrect SensorN")
            #
        #
    #
#
QFreqs1=len(freqs1)#vikt: hin wa err: irr indent - ma indent wa ver, et err wa ob af else ov nah print wa comment'd ma ns'da pass 
print("Frequences ("+str(QFreqs1)+") of 1st sensor:")
for i in range(QFreqs1):
    print(str(i+1)+") freq="+str(freqs1[i])+" ampl="+str(amps1[i]))
#
QFreqs2=len(freqs2)
print("Frequences ("+str(QFreqs2)+") of 2nd sensor:")
for i in range(QFreqs2):
    print(str(i+1)+") freq="+str(freqs2[i])+" ampl="+str(amps2[i]))
#
print("Working with spectrum")
GraphName="Спектр сигнала (Избранные значения)- удар № "+str(impactN)+" - файлы "+fileOwnNames[1-1]+" и "+fileOwnNames[2-1]
            
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
print("starting harmomic analysis....")
#
for i in range(QFreqs1):
    freq=freqs1[i]
    print(str(i+1)+") freq="+str(freq))
    params=make_params(freq, fs)#fs s'lir'd ov
    print("params of finding harmonics:")
    print(params)
    x_filt_harm, t = process_mode(sis1, tss, fs, params)
    #
    plot_several1(
        [
            [
                [(t, si1)], 1
            ]
            ,
            [
                [(t, x_filt_harm)], 1
            ]
            #,
            #[
            #   #[(ts, en1+en2)], 1
            #   [(ts, ensum)], 1
            #]
        ],
        [
            ["t, с", "Сигнал (весь)"],                  
            ["t, с", "Сигнал (гармоника частотой "+str(freq)+")"]
            
        ],
        [
            [ {"color":"green"}],
            [ {"color":"blue"}]
        ],
        GraphName
    )
    #
#
print("Step5 finishes working")
