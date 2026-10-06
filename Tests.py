import copy
from MyPyVibroLib import *


arr=[1, 2, 3, 4, 5]

print(arr)

SwapVals(arr, 2,4)
SwapVals(arr, 1,3)
SwapVals(arr, 5,2)

print(arr)

SortArray(arr, True)

print(arr)

QPoints=125#100590#1250#100590#125
QSects=10#200#100#200#10
#
##QPoints=len(signal)
#QPairs=QPoints-1
##dt=1/fs
#SectLenMed=QPairs/QSects
#SectLenInt=int(QPairs/QSects)
#rest=QPairs%QSects
#print("QPoints="+str(QPoints)+" QSects="+str(QSects)+" QPairs="+str(QPairs)+" SectLenInt="+str(SectLenInt)+" SectLenMed="+str(SectLenMed)+" rest="+str(rest)+" In all: "+str(SectLenInt*QSects+rest))
#print("Forming rows")
#rows=[]
#row=[]
#rowN=0
#for N in range (1, QPoints+1):
#    print("N="+str(N))
#    row.append(N)
#    if N%QSects==0:
#        if N<SectLenInt*QSects:
#            print("row bound reached")
#            print("row:")
#            print(row)
#            #rowToAdd=copy.deepcopy(row)
#            #rows.append(rowToAdd)
#            rows.append(row)
#            rowN+=1
#            print("last subRow")
#            print(rows[rowN-1])
#            if rowN>2:
#                print("pre-last subRow")
#                print(rows[rowN-2])
#            row=[]
#            #rowToAdd=[]
#            row.append(N)
#            #print("row bound reached")
#        else:
#            print("N="+str(N)+"=SectLenInt*QSects="+str(SectLenInt)+"*"+str(QSects)+"="+str(SectLenInt*QSects)+" - ignoring this point")
#    elif N==QPoints:
#        print("end reached")
#        print("row:")
#        print(row)
#        #rowToAdd=copy.deepcopy(row)
#        #rows.append(rowToAdd)
#        rows.append(row)
#        rowN+=1
#        print("last subRow")
#        print(rows[rowN-1])
#        if rowN>2:
#            print("pre-last subRow")
#            print(rows[rowN-2])
#        #rowToAdd=[]
#        row=[]
#        break
#
##
#QRows=len(rows)
#print("Result - "+str(QRows)+" rows:")
#for rowN in range(1, QRows+1):
#    rowL=len(rows[rowN-1])
#    print("row"+str(rowN)+" L="+str(rowL))
#    for cmpnN in range(1, rowL-1+1):
#        print(str(rows[rowN-1][cmpnN-1])+" ... "+str(rows[rowN-1][cmpnN-1+1]))
#
#print("rows:")
#print(rows)
#print("====================================================================")
#from MyPyVibroLib import MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr
#vv
#RowNs=MyEnvelopeBuilding_part1of3_SortPointsNumbersToSects_to2DArr(QPoints, QSects, vsh=2)
#^^
#
#      1   2 3  4  5  6  7  8  9 10 11 12 13 14 
arr1=[10, 8, 3, 2, 1, 4, 6, 5, 4, 5, 3, 2, 4, 3]

Qelts=len(arr1)

ts=[]

print("Initial:")

for i in range(1, Qelts+1):
    ts.append(i*10)
    print("N="+str(i)+" t="+str(ts[i-1])+" h="+str(arr1[i-1]))

print("Selected:")

Ns, t2s, Hs1 = ExcludeLowerPeaks(arr1, ts)

QSel=len(t2s)

for i in range(1, QSel+1):
    print("N="+str(i)+"="+str(Ns[i-1])+" t="+str(t2s[i-1])+" h="+str(Hs1[i-1]) )

