fileOwnNames=["020-1", "020-2", "021-1", "021-2"]#, "052-1", "052-2"]
filePath="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav"
filePath1=filePath+"\\assets"
#fileOwnNames=["051_1_M.wav", "051-2.wav", "052-1.wav", "052-2.wav"]


from MyPyVibroLib import *

with open(filePath1+"\\"+"FolderAndFiles.csv", mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Name:", "Value"])
    writer.writerow(["Folder:", filePath])
    writer.writerow(["Files:", str(len(fileOwnNames))])
    for fileOwnName in fileOwnNames:
        writer.writerow(["File:", fileOwnName])

print(filePath1+"\\"+"FolderAndFiles.csv successfully created")
