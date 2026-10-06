print ("wait a bit - configuring...")#cp1251 UTF-8

import numpy as np

#import builti

import matplotlib.pyplot as plt
from scipy.io import wavfile
import wave
#
from scipy.fft import rfft, rfftfreq
from scipy.signal import hilbert, find_peaks

#pathToFile="D:\\MyFilesCur\\W37_Blades\\W37_3_Decrement\\wavs\\assets"
pathToFile="D:\\MyFilesCur\\MyPrgs\\Python\\Wav\\assets"
#pathToFile="H:\\MyFiles\\MyPrgs\\Python\\Python1\\Wavs"
FileOwnName="051_1_M.wav"
fullFileName=pathToFile+"\\"+FileOwnName

print("config ok")

def read_wav(fullFileName):
    fs, data = wavfile.read(fullFileName)
    if np.issubdtype(data.dtype, np.integer):
        max_val=np.info(data.dtype).max
        data=data.astype(np.float32)/max_val
    return(fs, data)

def read_wav_safe(fullFileName, max_seconds=None):
    try:
        fs, data=wavfile.read(fullFileName)
        #norm'g if data s'numoz
        if np.issubdtype(data.dtype, np.integer):
            max_val= np.iinfo(data.dtype).max
            data=data.astype(np.float32)
        return fs, data
    except Exception as e:
        print("Error reading file "+str(e))
        print("trying to read via wave")
        #with wave.open(fileName, "rb") as wf:#os not l'methods __enter__ et __exit__, so n'arb
        wf=wave.open(fullFileName, "rb")
        fs=wf.getframerate()
        n_channels = wf.getnchannels()
        n_frames = wf.getnframes()

        if max_seconds is not None:
            #data = data.reshape(-1, n_channels)
            n_frames = min(n_frames, int(fs * max_seconds))

        raw = wf.readframes(n_frames)

        wf.close()#ute nur uz py 2.7 ob in py 3 to obj ha attr __exit__
          
        data = np.frombuffer(raw,dtype = np.int16)

        if n_channels >1:
            data = data.reshape(-1, n_channels)
            #print(str(n_channels)+" channels")
        else:
            pass
            #print(str(n_channels)+" channels")

        data = data.astype(np.float32)/ np.iinfo(np.int16).max
        return fs, data
       
    

#def plot_signal(data, fs, channel=0, duration=None):
#    if data.ndim==1:
#        y=data
#    else:
#        y=data[:, channel]
#        pass
#    t=np.arange(len(y))/float(fs)
#    if duration:
#        mask=t<duration
#        t=t[mask]
#        y=y[mask]
#
#    plt.figure(figsize=(10,4))
#    plt.plot(t,y,linewidth=0.8)
#    plt.xlabel="Время, с"
#    plt.ylabel="сигнал (канал{channel})"
#    plt.grid(True)
#    plt.show()

def plot_signal(data, fs, channel=0, start=0.0, duration=None):
    if data.ndim==1:
        y=data
    else:
        y=data[:, channel]
        pass
    start_index=int(start*fs)
    if duration is None:
        end_index=len(y)
    else:
        end_index=int(start_index +duration*fs)
    y=y[start_index:end_index]
    t=np.arange(len(y))/float(fs)+start
    #if duration:
    #    mask=t<duration
    #    t=t[mask]
    #    y=y[mask]

    plt.figure(figsize=(10,4))
    plt.plot(t,y,linewidth=0.8)
    plt.xlabel="Время, с"
    plt.ylabel="сигнал (канал{channel})"
    plt.grid(True)
    plt.show()
    #plt.savefig("graph.png")#so arb bad-tak: show graph am window Figure2 et empty window Figure1, l'ic lif ad .png-file

#fileName="D:\\MyFilesCur\\W37_Blades\\W37_3_Decrement\\wavs\\051_1.wav"
#fs, data = read_wav_safe(fileName, max_seconds=5)#arb gur ma show zu miq
#plot_signal(data, fs, channel=0, duration=2.0)#arb gur ma show zu miq
#fs, data = read_wav_safe(fileName, max_seconds=60)#arb gut et show 7 blows
#plot_signal(data, fs, channel=0, duration=60.0)#arb gut et show 7 blows
#fs, data = read_wav_safe(fileName, max_seconds=130)#arb gut et show 15 blows
#plot_signal(data, fs, channel=0, duration=130.0)#arb gut et show 15 blows
#fs, data = read_wav_safe(fileName, max_seconds=190)#works!
fs, data = read_wav_safe(fullFileName, max_seconds=190)
#plot_signal(data, fs, channel=0, duration=190.0)#arb gut et show 15 blows, et last N ecri 120, I n'int qob
#HighBound=800
#data1=data[0:HighBound]
#plot_signal(data, HighBound, channel=0, duration=190.0)#arb, show 1,5 blows
#plot_signal(data1, HighBound, channel=0, duration=190.0)#arb, show mic fragm
#plot_signal(data, HighBound, channel=0)#arb, show all
#plot_signal(data1, HighBound, channel=0)#arb, show mic fragm
#HighBound=800
#data1=data[0:HighBound]
#print("L(data="+str(len(data))+", L(data1)="+str(len(data1))+", fs="+str(fs))
print("L(data="+str(len(data))+", fs="+str(fs))
#plot_signal(data1, HighBound, channel=0)#arb, show mic fragm, ety if HighBound=fs, ma > HighBound - > data in mic fragm, last N ecri 1 by HighBound = 800, I n'int qob
#plot_signal(data, HighBound, channel=0)#arb, show all, 15 blows, ma last N ecri 1600 by HighBound = 800, N = 160 by HighBound = 8000, I n'int qob
#print("data 0-"+str(800),data[0:800])
#print(data), start=0, duration=190.0)
plot_signal(data, fs, channel=0)
#plot_signal(data, fs, channel=0, start=0.0, duration=190.0)
#plot_signal(data, fs, channel=0, start=0.0, duration=129.0)
plot_signal(data, fs, channel=0, start=60, duration=30)
#plot_signal(data, fs, channel=0, start=0, duration=70)
#plot_signal(data, fs, channel=0, start=0, duration=90)

#-----------------------------------------------------------------------------



time=np.arange(len(data))/float(fs)

def plot_envelope(time, data, method="hilbert", poly_order=3):
    """
    Рисует сигнал и его огибающую
    
    method:
        "hilbert" – через преобразование Гильберта
        "peaks"   – через пики + аппроксимацию полиномом
    poly_order:
        порядок полинома для аппроксимации пиков (по умолчанию кубический)
    """
    
    plt.figure(figsize=(12, 4))
    plt.plot(time, data, label="Сигнал", alpha=0.7)
    
    if method == "hilbert":
        # Преобразование Гильберта
        analytic_signal = hilbert(data)
        envelope = np.abs(analytic_signal)
        plt.plot(time, envelope, "r", label="Огибающая (Гильберт)")
    
    elif method == "peaks":
        # Поиск пиков
        peaks, _ = find_peaks(np.abs(data))
        peak_times = time[peaks]
        peak_values = np.abs(data[peaks])
        
        # Аппроксимация по методу МНК (полином)
        coeffs = np.polyfit(peak_times, peak_values, poly_order)
        envelope = np.polyval(coeffs, time)
        
        plt.plot(time, envelope, "g", label=f"Огибающая (пики+МНК, n={poly_order})")
    
    else:
        raise ValueError("method должен быть 'hilbert' или 'peaks'")
    
    #plt.xlabel("Время [с]")
    #plt.ylabel("Амплитуда")
    plt.title(f"Сигнал и огибающая ({method})")
    plt.legend()
    plt.grid(True)
    plt.show()

#-------------------------------------------------------------

#fs, data = read_wav("test.wav")
#fs,
    data = read_wav_safe(fullFileName, max_seconds=190)
# V ha nua fs et data
y = data[:,0] if data.ndim > 1 else data
print("Step2 - envelopes")

plot_envelope(time, data, method="hilbert")
plot_envelope(time, data, method="peaks", poly_order=3)

results, summary, envelopes = harmonic_analysis_with_envelopes(y, fs, n_harmonics=3)
#del str
plot_harmonics_with_envelopes(results, summary, envelopes)
print("That's all")

