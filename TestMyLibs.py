#TestMyLibs
import MyLib1
from MyLib1 import *
from TestVibro_Step1_MulCha_ReadSignal_ReadFileNamesFromCsv2_3 import *

arr=[10, 20, 30, 40]
val1=9
val2=12
val3=22
val4=42

print("Initial arr")
print(arr)
val=val1
print("Inserting val ="+str(val))
#def arr1DComparableInsByOrder(arr, val, vsh=0)
arr1DComparableInsByOrder(arr, val, vsh=0)
print("Now arr")
print(arr)
val=val2
print("Inserting val ="+str(val))
arr1DComparableInsByOrder(arr, val, vsh=0)
print("Now arr")
print(arr)
val=val3
print("Inserting val ="+str(val))
arr1DComparableInsByOrder(arr, val, vsh=0)
print("Now arr")
print(arr)
val=val4
print("Inserting val ="+str(val))
arr1DComparableInsByOrder(arr, val, vsh=0)
print("Now arr")
print(arr)
val=45
print("adding val ="+str(val))
Arr1DAdd(arr, val)
print("Now arr")
print(arr)
N=len(arr)-1
print("deleting val from N="+str(N))
Arr1DDelN(arr, N)
print("Now arr")
print(arr)
N=1
print("deleting val from N="+str(N))
Arr1DDelN(arr, N)
print("Now arr")
print(arr)
N=2
print("deleting val from N="+str(N))
Arr1DDelN(arr, N)
print("Now arr")
print(arr)
print("\nTrestuing seek subArr:")
sArr=[20, 22, 30]
print("in arr:")
print(arr)
print("sub.arr (not reversed):")
print(sArr)
Ns=Arr1D_SeekSubArr(whereArr=arr, whatArr=sArr, subArrIsNotReversed=True, vsh=1)
print("is present "+str(len(Ns))+" times")
if(len(Ns)>0):
    print("at Ns: ", Ns)
#
print("\nTrestuing seek subArr:")
sArr=[30, 22, 20]
print("In arr:")
print(arr)
print("sub.arr (Reversed):")
print(sArr)
Ns=Arr1D_SeekSubArr(whereArr=arr, whatArr=sArr, subArrIsNotReversed=False, vsh=1)
print("is present "+str(len(Ns))+" times")
if(len(Ns)>0):
    print("at Ns: ", Ns)
#



print("\n\n Testing tme segments:")
peaksTimes1=[4.464305555555556, 15.821944444444444, 25.02638888888889, 35.255, 44.939305555555556, 55.07486111111111, 65.14194444444445, 75.14861111111111, 85.3951388888889]
segments1=[]
for i in range(1, len(peaksTimes1)):
    t1=peaksTimes1[i-1]
    t2=peaksTimes1[i+1-1]
    segment=[]
    segment.append(t1)
    segment.append(t2)
    segments1.append(segment)
#
print("segments 1:")
print(segments1)
peaksTimes2=[4.455416666666666, 15.808194444444444, 24.923194444444444, 35.25333333333333, 44.923611111111114, 55.085, 75.14319444444445, 85.40583333333333]
segments2=[]
for i in range(1, len(peaksTimes2)):
    t1=peaksTimes2[i-1]
    t2=peaksTimes2[i+1-1]
    segment=[]
    segment.append(t1)
    segment.append(t2)
    segments2.append(segment)
print("segments 2:")
print(segments1)
sg=FindCommonSegnmentLists(segments1, segments2, dt_s=1.0, vsh=1)
print("Answer:")
print(sg)
