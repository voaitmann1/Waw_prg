from MyPyVibroLib import *

print("Step0 starts working")

data=FilesData()

data.ReadWavFileData()

print("data read")

print(data)

print("trying to save toi file "+data.Folder+"\\"+data.SubFolder_IntermediateData+"\\"+"FolderAndFiles_1_Full.csv")

data.WriteToCsV(data.Folder+"\\"+data.SubFolder_IntermediateData+"\\"+"FolderAndFiles_1_Full.csv")

print("Step0 finishes working")
