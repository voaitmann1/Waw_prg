print("Step0 starts working")
#fileOwnNames=["020-1", "020-2", "021-1", "021-2"]#, "052-1", "052-2"]
filePath="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav"
filePath1=filePath+"\\data"
#fileOwnNames=["051_1_M.wav", "051-2.wav", "052-1.wav", "052-2.wav"]


from MyPyVibroLib import *
import os

try:
    if not os.path.exists(filePath1):
        print("Incorrect patt!")
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
        print(fileOwnName+" -> "+fileOwnName_noExt)

print(filePath1+"\\"+"FolderAndFiles.csv successfully created")
print("Step0 finishes working")


    
