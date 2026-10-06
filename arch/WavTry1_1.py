print ("wait a bit - configuring...")#cp1251 UTF-8

import numpy as np

#import builti

import matplotlib.pyplot as plt
from scipy.io import wavfile
import wave
#
from scipy.fft import rfft, rfftfreq
from scipy.signal import hilbert

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
plot_signal(data, fs, channel=0, start=0.0, duration=190.0)
plot_signal(data, fs, channel=0, start=0.0, duration=129.0)
plot_signal(data, fs, channel=0, start=60, duration=30)
plot_signal(data, fs, channel=0, start=0, duration=70)
plot_signal(data, fs, channel=0, start=0, duration=90)

#-----------------------------------------------------------------------------

def harmonic_analysis_with_envelopes(y, fs, n_harmonics=10):#5):
    """
    Анализ сигнала с построением огибающих для гармоник и суммарного сигнала.
    """
    N = len(y)
    t = np.arange(N) / fs

    Y = rfft(y)
    freqs = rfftfreq(N, 1/fs)

    results = []
    total_energy = 0

    # список огибающих для визуализации
    envelopes = []

    for k in range(1, n_harmonics+1):
        idx = np.argmax(np.abs(Y))
        freq = freqs[idx]
        comp = np.abs(Y[idx]) * np.cos(2*np.pi*freq*t + np.angle(Y[idx]))

        # энергия
        energy = np.sum(comp**2)
        total_energy += energy

        # огибающая
        env = np.abs(hilbert(comp))
        envelopes.append((t, comp, env, freq))

        # декремент и добротность
        env_valid = env[env > 1e-6]
        if len(env_valid) > 10:
            log_env = np.log(env_valid)
            slope, _ = np.polyfit(np.arange(len(log_env)), log_env, 1)
            delta = -slope
            Q = np.pi / delta if delta > 0 else np.inf
        else:
            delta, Q = np.nan, np.nan

        results.append({
            "freq": freq,
            "energy": energy,
            "delta": delta,
            "Q": Q
        })

        Y[idx] = 0

    # суммарный сигнал
    env_total = np.abs(hilbert(y))
    env_valid = env_total[env_total > 1e-6]
    if len(env_valid) > 10:
        log_env = np.log(env_valid)
        slope, _ = np.polyfit(np.arange(len(log_env)), log_env, 1)
        delta_total = -slope
        Q_total = np.pi / delta_total if delta_total > 0 else np.inf
    else:
        delta_total, Q_total = np.nan, np.nan

    summary = {
        "energy_total": total_energy,
        "delta_total": delta_total,
        "Q_total": Q_total,
        "env_total": (t, y, env_total)
    }

    return results, summary, envelopes


def plot_harmonics_with_envelopes(results, summary, envelopes):
    #"""
    #Строит графики огибающих гармоник и суммарного сигнала.
    #"""
    plt.figure(figsize=(12,8))

    # гармоники
    for i, (t, comp, env, freq) in enumerate(envelopes):
        plt.subplot(len(envelopes)+1, 1, i+1)
        #plt.plot(t, comp, label=f"Гармоника {freq:.1f} Гц", alpha=0.6)#mab py2.7 n'int tic syntax
        plt.plot(t, comp, label=f"Гармоника {freq:.1f} Гц", alpha=0.6)
        plt.plot(t, env, "r--", label="Огибающая")
        #del str
        #print(">>> str(123)="+str(123))
        #plt.xlabel("Время, с")
        #plt.ylabel("Амплитуда")
        #plt.legend()
        plt.grid(True)

    # суммарный сигнал
    t, y, env_total = summary["env_total"]
    plt.subplot(len(envelopes)+1, 1, len(envelopes)+1)
    plt.plot(t, y, label="Суммарный сигнал", alpha=0.6)
    plt.plot(t, env_total, "r--", label="Огибающая")
    
    #plt.xlabel("Время, с")
    #plt.ylabel("Амплитуда")
    #plt.legend()
    plt.grid(True)
    plt.title(f"Суммарно: δ={summary['delta_total']:.4f}, Q={summary['Q_total']:.2f}")

    plt.tight_layout()
    plt.show()
    

#-------------------------------------------------------------

#fs, data = read_wav("test.wav")
#fs,
    data = read_wav_safe(fullFileName, max_seconds=190)
# V ha nua fs et data
y = data[:,0] if data.ndim > 1 else data
print("Step2")

results, summary, envelopes = harmonic_analysis_with_envelopes(y, fs, n_harmonics=3)
#del str
plot_harmonics_with_envelopes(results, summary, envelopes)
print("That's all")

