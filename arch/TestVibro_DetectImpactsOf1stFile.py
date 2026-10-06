from MyPyVibroLib import *
#import pandas as pd

#pathToFile="D:\\MyFilesCur\\W37_Blades\\W37_3_Decrement\\wavs\\assets"
pathToFile="D:\\MyFilesCur\\MyPrgs\\Python\\Wav\\assets"
#pathToFile="H:\\MyFiles\\MyPrgs\\Python\\Python1\\Wavs"
FileOwnName="051_1_M.wav"
fullFileName=pathToFile+"\\"+FileOwnName

config_plotSelect_Vrn=0
#0 - do not plot, 1- mask val sel, 2 - usual val sel

t, data, fs = read_wav_and_calc_t(fullFileName)

plot_signal(t, data)

peaks_time, segments = detect_impacts_segments(data, fs=fs, min_distance=0.05, threshold_ratio=0.66)

QImpacts=len(peaks_time)
print("impact time ranges:")
for i in range(1, QImpacts+1):
    t_plt=[]
    x_plt=[]
    print("t1="+str(peaks_time[i-1])+"="+str(segments[i-1][1-1])+"...t2="+str(segments[i-1][2-1])+" (duration="+str(segments[i-1][2-1]-segments[i-1][1-1]))
    #
    if config_plotSelect_Vrn==1:
        for j in range(1, len(t)+1):
            if( (t[j-1]>=peaks_time[i-1]) and (t[j-1]<=segments[i-1][2-1]) ):
                t_plt.append(t[j-1])
                x_plt.append(data[j-1])
        plt.plot(t_plt, x_plt)
    elif config_plotSelect_Vrn==2:
        mask = (t >= peaks_time[i-1]) & (t <= segments[i-1][2-1])
        plt.plot(t[mask], data[mask])
    #
    if(config_plotSelect_Vrn==1 or config_plotSelect_Vrn==2):
        plt.xlabel("Время, с")
        plt.ylabel("Амплитуда")
        plt.title(f"Затухающий процесс от удара N{i}")
        plt.grid()
        plt.show()

