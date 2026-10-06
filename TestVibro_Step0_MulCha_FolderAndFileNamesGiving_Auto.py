print("Step0 starts working")
#fileOwnNames=["020-1", "020-2", "021-1", "021-2"]#, "052-1", "052-2"]
filePath="C:\\Users\\user\\Documents\\MyPrgs\\Python\\Wav"
filePath1=filePath+"\\data"
#fileOwnNames=["051_1_M.wav", "051-2.wav", "052-1.wav", "052-2.wav"]


from MyPyVibroLib import *
import os

try:
    if not os.path.exists(filePath1):
        print("Incorrect path!")
    else:
        all_items=os.listdir(filePath1)
        fileOwnNames=[f for f in all_items]
        print("folder viewed")
except Exception as e:
    print("Error: {e}")
    

#for f in fileOwnNames:
#    fo=f[:-4]
#    print(f+" -> "+fo)
    


with open(filePath1+"\\"+"FolderAndFiles.csv", mode='a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name:", "Value"])
    writer.writerow(["Folder:", filePath])
    writer.writerow(["Files:", str(len(fileOwnNames))])
    for fileOwnName in fileOwnNames:
        fileOwnName_noExt=fileOwnName[:-4]
        writer.writerow(["File:", fileOwnName_noExt])
        #
        t, n_channels, data, fs=read_wav_and_calc_t_1(filePath1+"\\"+fileOwnName, max_seconds=None)
        writer.writerow(["Channels:", str(n_channels)])
        #
        print("File:"+" "+fileOwnName+" -> "+fileOwnName_noExt)
        print("Файл:"+" "+fileOwnName+" Каналов: "+str(n_channels))

print(filePath1+"\\"+"FolderAndFiles.csv successfully created")

with open(filePath1+"\\"+"FolderAndFiles_1_Full.csv", mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name:", "Value"])
    writer.writerow(["Folder:", filePath])
    writer.writerow(["Files:", str(len(fileOwnNames))])
    writer.writerow(["fileNameEnding_Signal", "_signal_whole.csv"])
    writer.writerow(["fileNameEnding_ImpactBounds", "_ImpactsRanges.csv"])
    writer.writerow(["fileNameEnding_Spectrum", "_spectrum.csv"])
    writer.writerow(["SubFolder_IniData", "data"])
    writer.writerow(["SubFolder_Results", "Results"])
    writer.writerow(["SubFolder_IntermediateData"," data"])
    writer.writerow(["fileName_Results", "results.csv"])
    for fileOwnName in fileOwnNames:
        fileOwnName_noExt=fileOwnName[:-4]
        writer.writerow(["File:", fileOwnName_noExt])
        #
        t, n_channels, data, fs=read_wav_and_calc_t_1(filePath1+"\\"+fileOwnName, max_seconds=None)
        writer.writerow(["Channels:", str(n_channels)])
        writer.writerow(["tmax:", str(t[-1])])
        #
        print("File:"+" "+fileOwnName+" -> "+fileOwnName_noExt)
        print("Файл:"+" "+fileOwnName+" Каналов: "+str(n_channels))
        print("Файл:"+" "+fileOwnName+" Каналов: "+str(n_channels)+" tmax=: "+str(t[-1]))
    #

print(filePath1+"\\"+"FolderAndFiles.csv successfully created")


print("Step0 finishes working")


    
