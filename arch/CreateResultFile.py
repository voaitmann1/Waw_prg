#filePath1="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\assets"
filePath2="C:\\Users\\V\\Documents\\MyPrgs\\Python\\Wav\\results"

from MyPyVibroLib import *

with open(filePath2+"\\"+"Results.csv", mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["F or ch 1", "F or ch 2", "decr1", "decr2", "decrS"])

print("created empty: "+filePath2+"\\"+"Results.csv")
