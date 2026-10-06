import copy

import numpy as np
import matplotlib.pyplot as plt

#def isInArrayAtPosN(arr, val):
#    L=len(arr)
#    Ns=[]
#    for i in range(L):
#        if arr[i]==val:
#            Ns.append(i+1)
#        #
#    #
#    return Ns
##

    


def Sort3ArraysByOne_v1(arr1, arr2, arr3, by123=3, DescNotAsc=True):
    Q=len(arr1)
   
    for i in range(1, Q-1+1):
        for j in range(i+1, Q+1):
            arr1_i=arr1[-1]
            arr2_i=arr2[i-1]
            arr3_i=arr3[i-1]
            arr1_j=arr1[j-1]
            arr2_j=arr2[j-1]
            arr3_j=arr3[j-1]
            #
            if (
                  DescNotAsc
                  and
                  (
                   (by123==1 and arr1_j>arr1_i)
                    or
                   (by123==1 and arr2_j>arr2_i)
                    or
                    (by123==1 and arr3_j>arr3_i)
                   )
               ) \
               or \
               (
                  DescNotAsc==False
                  and
                  (
                   (by123==1 and arr1_j<arr1_i)
                    or
                   (by123==1 and arr2_j<arr2_i)
                    or
                    (by123==1 and arr3_j<arr3_i)
                   )
               ):
                arr1[i-1]=arr1_j
                arr2[i-1]=arr2_j
                arr3[i-1]=arr3_j
                arr1[j-1]=arr1_i
                arr2[j-1]=arr2_i
                arr3[j-1]=arr3_i
            #
        #
    #
#
def Sort3ArraysByOne_v2(arr1, arr2, arr3, by123=3, DescNotAsc=True, vsh=0):
    if vsh==1:
        print("Sort3ArraysByOne_v2 starts working")
        if DescNotAsc:
            print("sort by arr"+str(by123)+" descending")
        else:
            print("sort by arr"+str(by123)+" ascending")
        #
    #
    Q=len(arr1)
    if vsh==1:
        print("given:")
        if Q%2==0:
            print("Q ="+str(Q)+"- is even")
            N=1
            if isinstance(N, int):
                print("N - int")
            else:
                print("N - ne int")
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q/2
            print("N=Q/2="+str(N))
            if isinstance(N, int):
                print("N - int")
            else:
                print("N - ne int")
            N=Q//2
            print("N=Q//2="+str(N))
            if isinstance(N, int):
                print("N - int")
            else:
                print("N - ne int")
            N=(Q+2.2+2.4-1.3-3.1)//2
            print("N=(Q+2.2+2.4-1.3-3.1)//2="+str(N))
            print("N="+str(N))
            if isinstance(Q, int):
                print("Q - int")
            else:
                print("Q - ne int")
            if isinstance(N, int):
                print("N - int")
            else:
                print("N - ne int")
            N=Q//2
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
        else:
            print("Q ="+str(Q)+" - is odd")
            N=1
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=(Q-1)/2+1
            N=(Q-1)//2+1
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q
            print("N="+str(N)+": x1["+str(N)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
        #
    #
    for i in range(1, Q-1+1):
        for j in range(i+1, Q+1):
            arr1_i=arr1[i-1]
            arr2_i=arr2[i-1]
            arr3_i=arr3[i-1]
            arr1_j=arr1[j-1]
            arr2_j=arr2[j-1]
            arr3_j=arr3[j-1]
            if vsh==1:
                print("i="+str(i)+" j="+str(j)) 
                print("i: x1["+str(i)+"]="+str(arr1_i)+" x2["+str(i)+"]="+str(arr2_i)+" x3["+str(i)+"]="+str(arr3_i))
                print("j: x1["+str(j)+"]="+str(arr1_j)+" x2["+str(j)+"]="+str(arr2_j)+" x3["+str(j)+"]="+str(arr3_j))
            #
            if DescNotAsc:
                if \
                   (by123==1 and arr1_j>arr1_i) \
                    or \
                   (by123==2 and arr2_j>arr2_i) \
                    or \
                   (by123==3 and arr3_j>arr3_i):
                    arr1[i-1]=arr1_j
                    arr2[i-1]=arr2_j
                    arr3[i-1]=arr3_j
                    arr1[j-1]=arr1_i
                    arr2[j-1]=arr2_i
                    arr3[j-1]=arr3_i
                    if vsh==1:
                        print("exchange")
                    #
                else:
                    if vsh==1:
                        print("stay")
                    #
                #
            else:
                if \
                   (by123==1 and arr1_j<arr1_i) \
                    or \
                   (by123==2 and arr2_j<arr2_i) \
                    or \
                   (by123==3 and arr3_j<arr3_i):
                    arr1[i-1]=arr1_j
                    arr2[i-1]=arr2_j
                    arr3[i-1]=arr3_j
                    arr1[j-1]=arr1_i
                    arr2[j-1]=arr2_i
                    arr3[j-1]=arr3_i
                    if vsh==1:
                        print("exchange")
                    #
                else:
                    if vsh==1:
                        print("stay")
                    #
                #
            #
        #
    #
    if vsh==1:
        print("answer:")
        for N in range(Q):
            print("N="+str(N+1)+": x1["+str(N+1)+"]="+str(arr1[N])+" x2["+str(N+1)+"]="+str(arr2[N])+" x3["+str(N+1)+"]="+str(arr3[N]))
        #
        print("Sort3ArraysByOne_v2 finishes working")    
    #
#
def Sort3ArraysByOne_v3(arr1, arr2, arr3, by123=3, AscNotDesc=False, vsh=0):
    if vsh==1:
        print("Sort3ArraysByOne_v3 starts working")
        if AscNotDesc:
            print("sort by arr"+str(by123)+" ascending")
        else:
            print("sort by arr"+str(by123)+" descending")
        #
    #
    Q=len(arr1)
    if vsh==1:
        print("given:")
        if Q%2==0:
            print("Q ="+str(Q)+" - is even")
            N=1
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q/2
            N=Q//2
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
        else:
            print("Q ="+str(Q)+" - is odd")
            N=1
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=(Q-1)/2+1
            N=(Q-1)//2+1
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
            N=Q
            print("N="+str(N)+": x1["+str(N-1)+"]="+str(arr1[N-1])+" x2["+str(N)+"]="+str(arr2[N-1])+" x3["+str(N)+"]="+str(arr3[N-1]))
        #
    #
    for i in range(1, Q-1+1):
        for j in range(i+1, Q+1):
            arr1_i=arr1[i-1]
            arr2_i=arr2[i-1]
            arr3_i=arr3[i-1]
            arr1_j=arr1[j-1]
            arr2_j=arr2[j-1]
            arr3_j=arr3[j-1]
            if vsh==1:
                print("i="+str(i)+" j="+str(j)) 
                print("i: x1["+str(i)+"]="+str(arr1_i)+" x2["+str(i)+"]="+str(arr2_i)+" x3["+str(i)+"]="+str(arr3_i))
                print("j: x1["+str(j)+"]="+str(arr1_j)+" x2["+str(j)+"]="+str(arr2_j)+" x3["+str(j)+"]="+str(arr3_j))
            #
            if AscNotDesc:
                if \
                   (by123==1 and arr1_j<arr1_i) \
                    or \
                   (by123==2 and arr2_j<arr2_i) \
                    or \
                   (by123==3 and arr3_j<arr3_i):
                    arr1[i-1]=arr1_j
                    arr2[i-1]=arr2_j
                    arr3[i-1]=arr3_j
                    arr1[j-1]=arr1_i
                    arr2[j-1]=arr2_i
                    arr3[j-1]=arr3_i
                    if vsh==1:
                        print("exchange")
                    #
                else:
                    if vsh==1:
                        print("stay")
                    #
                #
            else:
                if \
                   (by123==1 and arr1_j>arr1_i) \
                    or \
                   (by123==2 and arr2_j>arr2_i) \
                    or \
                   (by123==3 and arr3_j>arr3_i):
                    arr1[i-1]=arr1_j
                    arr2[i-1]=arr2_j
                    arr3[i-1]=arr3_j
                    arr1[j-1]=arr1_i
                    arr2[j-1]=arr2_i
                    arr3[j-1]=arr3_i
                    if vsh==1:
                        print("exchange")
                    #
                else:
                    if vsh==1:
                        print("stay")
                    # 
                #
            #
        #
    #
    if vsh==1:
        print("answer:")
        for N in range(Q):
            print("N="+str(N+1)+": x1["+str(N+1)+"]="+str(arr1[N])+" x2["+str(N+1)+"]="+str(arr2[N])+" x3["+str(N+1)+"]="+str(arr3[N]))
        #
        print("Sort3ArraysByOne_v3 finishes working")    
    #
    return arr1, arr2, arr3
#

def arr1DSwapVals(arr, NN1, NN2):
     if(isinstance(arr, list)):
        Q=len(arr)
        if(NN1<0):
            NN1-=(Q+1)
        #
        if(NN2<0):
            NN2-=(Q+1)
        #
        if(NN1>=1 and NN1<=Q and NN2>=1 and NN2<=Q):
            buf=copy.deepcopy(arr[NN1-1])
            arr[NN1-1]=copy.deepcopy(arr[NN2-1])
            arr[NN2-1]=copy.deepcopy(buf)
        #
    #
#
            

def arr1DIns(arr, val, NN, vsh=0):
    if vsh!=0:
        print("arr1DIns staerts working")
        print("given: "+str(arr))
        print("task is ins val "+str(val)+" to pos "+str(NN))
    #
    if(isinstance(arr, list)):
        Q=len(arr)
        if(NN<0):
            NN-=(Q+1)
            if vsh!=0:
                print("NN="+str(NN))
            #
        #
        if(NN>=1 and NN<=Q):
            arr.append(val)
            Q=len(arr)
            if vsh!=0:
                print("first action - now arr is: ", arr)
                print("now:")
            for i in range (NN+1, Q+1):
                #j=Q+1-i
                j=Q+NN+1-i
                arr1DSwapVals(arr, j-1, j)
                if(vsh!=0):
                    print("i="+str(i)+" j="+str(j))
                    print("currently arr is: ", arr) 
            #
            
        else:
            if vsh!=0:
                print("N out of range")
            #
        #
    #
    if vsh!=0:
        print("Answer: "+str(arr))
#

def Array1DReverse(arr):
    L=len(arr)
    if(L%2==0):
        N=L/2
    else:
        N=(L-1)/2
    #
    for N1 in range (1, N+1):
        N2=(L-N1+1)
        buf=arr[N1-1]
        arr[N1-1]=arr[N2-1]
        arr[N2-1]=buf
    #    

def arr1DOfNums_InsOrAddSmart(arr, val, NN=0, vsh=0):
    L=len(arr)
    if NN<0:
        NN+=(L+1)
    #
    if NN>=0:
        arr1DIns(arr, val, NN, vsh)
    else:
        if isSortedDescending(arr):
            Array1DReverse(arr)
        #
        if isSortedAscending(arr):
            poss=valIsAtPos(arr, val, vsh)
            if poss.isLess:
                arr1DIns(arr, val, 1, vsh)
            elif poss.isGreater:
                arr.append(val)
            elif poss.lessNN>0:
                arr1DIns(arr, val, poss.lessNN, vsh)
            #
        #
        if isSortedDescending(arr):
            Array1DReverse(arr)
        #
    #
#
            

def BoolToInt(val):
    intVal=0
    if val==True:
        intVal=1
    #
    return intVal
#
def IntOfBool(val):
    return BoolToInt(val)
#

def ValPosNInArray(arr, val):
    L=len(arr)
    Ns=[]
    for i in range(L):
        if arr[i]==val:
            Ns.append(i+1)
        #
    #
    return Ns
#

def isInArray(arr, val):
    Ns=ValPosNInArray(arr, val)
    return(len(Ns)>0)
#

class Poss:
    def __init__(self, isLess=False, isGreater=False, isWithin=False, lessNN=0, equalNN=0):
        self.isLess=isLess
        self.isGreater=isGreater
        self.isWithin=isWithin
        self.lessNN=lessNN
        self.equalNN=equalNN
    #
    def __str__(self):
        s=""
        s+="isLess="
        s+=str(IntOfBool(self.isLess))
        s+="; "
        s+="isGreater="
        s+=str(IntOfBool(self.isGreater))
        s+="; "
        s+="isWithin="
        s+=str(IntOfBool(self.isWithin))
        s+="; "
        s+="lessNN="
        s+=str(self.lessNN)
        s+="; "
        s+="equalNN="
        s+=str(self.equalNN)
        #
        return s
    #
#

def isSortedAscending(arr):
    verdict=True
    if isinstance(arr, list):
        Q=len(arr)
        for i in range(Q-1):
            if arr[i]>=arr[i+1]:
                verdict=False
            #
        #
    #
    return verdict
#
def isSortedDescending(arr):
    verdict=True
    if isinstance(arr, list):
        Q=len(arr)
        for i in range(Q-1):
            if arr[i]<=arr[i+1]:
                verdict=False
            #
        #
    #
    return verdict
#

def valIsAtPos(arr, val, vsh=0):# old vrn ac eps
    poss=Poss()
    if vsh!=0:
        print("valIsAtPos starts working")
        print("given:")
        print(arr)
        print(val)
    #
    if isinstance(arr, list) and isSortedAscending(arr):
        Q=len(arr)
        if val<arr[0]:
            poss.isLess=True
            if vsh!=0:
                print("isLess")
        elif val>arr[Q-1]:
            poss.isGreater=True
            if vsh!=0:
                print("isGreater")
        else:
            poss.isWithin=True
            if vsh!=0:
                print("isWithin")
            for i in range(Q):
                if arr[i]==val:
                   poss.equalNN=i+1
                #
            #
            if poss.equalNN==0:
                for i in range(Q-1):
                    if arr[i]<val and arr[i+1]>val:
                       poss.lessNN=i+1
                    #
                #
            #
        #
    else:
        if vsh!=0:
            print("arr is not a list or list but not sorted")
        #
    #
    if vsh!=0:
        print("Answer: "+str(poss)+" valIsAtPos finishes working")
    #
    return poss
#

def valIsAtPos(arr, val, eps=0, vsh=0): # new vrn co eps
    poss=Poss()
    if vsh!=0:
        print("valIsAtPos starts working")
        print("given:")
        print(arr)
        print("val="+str(val))
        print("eps="+str(eps))
    #
    if isinstance(arr, list) and isSortedAscending(arr):
        Q=len(arr)
        if val<arr[0] and abs(val-arr[0])>eps:
            poss.isLess=True
            if vsh!=0:
                print("isLess")
        elif val>arr[Q-1] and abs(val-arr[Q-1])>eps:
            poss.isGreater=True
            if vsh!=0:
                print("isGreater")
        else:
            poss.isWithin=True
            if vsh!=0:
                print("isWithin")
            for i in range(Q):
                if abs(val-arr[i])<=eps:#arr[i]==val
                   poss.equalNN=i+1
                #
            #
            if poss.equalNN==0:
                for i in range(Q-1):
                    if arr[i]<val and arr[i+1]>val and abs(val-arr[i])>eps and abs(val-arr[i+1])>eps:
                       poss.lessNN=i+1
                    #
                #
            #
        #
    else:
        if vsh!=0:
            print("arr is not a list or list but not sorted")
        #
    #
    if vsh!=0:
        print("Answer: "+str(poss)+" valIsAtPos finishes working")
    #
    return poss
#

def LInterp(X, Y, x):
    poss=valIsAtPos(X, x)
    y=0
    Q=len(X)
    if len(Y)==Q and isSortedAscending(X):
        if poss.equalNN>0:
            y=Y[poss.isEqualNN-1]
        else:
            if poss.isLess:
                x1=X[1-1]
                x2=X[2-1]
                y1=Y[1-1]
                y2=Y[2-1]
            elif poss.isGreater:
                x1=X[Q-2]
                x2=X[Q-1]
                y1=Y[Q-2]
                y2=Y[Q-1]
            else:
                #x1=X[poss.lesslNN-1]
                #x2=X[poss.lesslNN-0]
                #y1=Y[poss.lesslNN-1]
                #y2=Y[poss.lesslNN-0]
                x1=X[poss.lessNN-1]
                x2=X[poss.lessNN-0]
                y1=Y[poss.lessNN-1]
                y2=Y[poss.lessNN-0]
            #
            k=(y2-y1)/(x2-x1)
            y=k*(x-x1)+y1
        #
    #
    return y
#

def arr1DComparableInsByOrder(arr, val, vsh=0):
    poss=valIsAtPos(arr, val)
    if isinstance(arr, list) and isSortedAscending(arr):
        Q=len(arr)
        if poss.isLess:
            arr1DIns(arr, val, 1, vsh)
        elif poss.isGreater:
            arr.append(val)
        elif poss.lessNN>0:
            arr1DIns(arr, val, poss.lessNN+1, vsh)
        else:
            print("already present at pos "+str( poss.equalNN))
        #
    #
#
def Arr1DAdd(arr, val):
    arr.append(val)
#

def Arr1DDelN(arr, N):
    Q=len(arr)
    if Q>0:
        if N<0:
            N+=(Q+1)
        if N>0 and N<=Q:
            del arr[N-1]
        #
    #
#

def Arr1DShiftForward(arr):
    L=len(buf)
    buf=arr[1-1]
    for i in range(2, L+1):
        arr[i-1-1]=copy.deepcopy(arr[i-1])
    arr[L-1]=buf

def Arr1DShiftBackward(arr):
    L=len(buf)
    buf=arr[L-1]
    for N1 in range(2, L+1):
        N2=L-N1+1
        arr[N2-1]=copy.deepcopy(arr[N2-1-1])
    arr[1-1]=buf

def Arr1D_SubArrIsAtPos(whereArr, whatArr, N, subArrIsNotReversed=True, vsh=0):
    verdict=True
    whereL=len(whereArr)
    whatL=len(whatArr)
    if vsh==1:
        print("Arr1D_SubArrIsAtPos starts working")
        print("whereArr, L="+str(whereL))
        print(whereArr)
        print("whatArr, L="+str(whatL))
        print(whatArr)
    #
    if subArrIsNotReversed:
        if vsh==1:
            print("comparing: N+whatL-1="+str(N+whatL-1)+" wherteL="+str(whereL))
        if N+whatL-1>whereL:
            verdict=False
            if vsh==1:
                print("verdict=False")
        else:
            for whatN in range(1, whatL+1):
                whereN=N+whatN-1
                whereVal=whereArr[whereN-1]
                whatVal=whatArr[whatN-1]
                if vsh==1:
                    print(" what["+str(whatN)+"]="+str(whatVal)+"- comparing to: where["+str(whereN)+"]="+str(whereVal))
                if not whatVal==whereVal:
                    verdict=False
                    if vsh==1:
                        print("verdict=False")
                else:
                    if vsh==1:
                        print("verdict=True")        
            #
        #
    else:
        if vsh==1:
            print("comparing: N-whatL+1="+str(N-whatL+1)+" and 1")
        if N-whatL+1<1:
            verdict=False
            if vsh==1:
                print("verdict=False")
        else:
            for whatN in range(1, whatL+1):
                whereN=N-whatN+1
                whereVal=whereArr[whereN-1]
                whatVal=whatArr[whatN-1]
                if vsh==1:
                    print(" what["+str(whatN)+"]="+str(whatVal)+"- comparing to: where["+str(whereN)+"]="+str(whereVal))
                if not whatVal==whereVal:
                    verdict=False
                    if vsh==1:
                        print("verdict=False")
                else:
                    if vsh==1:
                        print("verdict=True") 
                #
            #
        #
    #
    if vsh==1:
        print("verdict ="+str(verdict))
        print("Arr1D_SubArrIsAtPos finishes working")
    #
    return verdict
#

def Arr1D_SeekSubArr(whereArr, whatArr, subArrIsNotReversed=True, vsh=0):
    Ns=[]
    L=len(whereArr)
    for N in range(1, L+1):
        if Arr1D_SubArrIsAtPos(whereArr, whatArr, N, subArrIsNotReversed, vsh):
            Ns.append(N)
        #
    #
    return Ns
#

def Arr1D_SubArrIsIn(whereArr, whatArr, subArrIsNotReversed=True, vsh=0):
    Ns=Arr1D_SeekSubArr(whereArr, whatArr, N, subArrIsNotReversed, vsj)
    return(len(Ns)>0)
#

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    #
#

def ReturnListsOfArrayNs_NearestToNN(L, NN):#gut but not tested
    NsBefore=[]
    NsAround=[]
    NsAfter=[]
    if NN>7:
        for j in range(1, 3+1):
            NsBefore.append(j)
        #
        for j in range(NN-4, NN+1):
            NsAround.append(j)
        #
        if L>NN+7:
            for j in range(NN+1, NN+4+1):
                NsAround.append(j)
            #
            for j in range(L-3, L+1):
                NsAfter.append(j)
            #
        else:
            for j in range(NN+1, L+1):
                NsAround.append(j)
            #
        #
    else:#NN<7
        for j in range(1, NN+1):
            NsAround.append(j)
        #
        if L>NN+7:
            for j in range(NN+1, NN+4+1):
                NsAround.append(j)
            #
            for j in range(L-3, L+1):
                NsAfter.append(j)
            #
        else:
            for j in range(NN+1, L+1):
                NsAround.append(j)
            #
        #
    #
    return NsBefore, NsAround, NsAfter
#

def ReturnSomeArrayValsFirstLastAndNearestToNN_asStr1(NN, X=[]):# better than ac 1 but not tersted
    NsBefore, NsAround, NsAfter=ReturnListsOfArrayNs_NearestToNN(len(X), NN)
    s="["
    if NsBefore==[]:
        pass
    else:
        LBefore=len(NsBefore)
        for i in range(LBefore):
            if X==[]:
                s+=str(NsBefore[i])
            else:
                s+=str(X[NsBefore[i]-1])
            #
            if i<LBefore:
                s+=", "
            #
        #
    #
    if not (NsBefore==[] and  (not NsAround==[] or not NsAfter==[])):
        s+="..."
    #
    if NsAround==[]:
        pass
    else:
        LAround=len(NsAround)
        for i in range(LAround):
            if X==[]:
                s+=str(NsAround[i])
            else:
                s+=str(X[NsAround[i]-1])
            #
            if i<LAround:
                s+=", "
            #
        #
    #
    if not NsAround==[] and not NsAfter==[]:
        s+="..."
    #
    if NsAfter==[]:
        pass
    else:
        LAfter=len(NsAfter)
        for i in range(LAfter):
            if X==[]:
                s+=str(NsAfter[i])
            else:
                s+=str(X[NsAfter[i]-1])
            #
            if i<LAfter:
                s+=", "
            #
        #
    #
    s="]"
    return s
#

def ReturnSomeArrayValsFirstLastAndNearestToNN_asStr(X, NN):
    L=len(X)
    s="["
    if NN>7:
        for j in range(1, 3+1):
            s+=str(X[j-1])
            #print("x["+str(j)+"]="+str(X[j-1]))
            s+=", "
        #
        s+=" ... "
        for j in range(NN-4, NN+1):
            s+=str(X[j-1])
            #print("x["+str(j)+"]="+str(X[j-1]))
            s+=", "
        #
        if L>NN+7:
            for j in range(NN+1, NN+4+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                s+=", "
            #
            s+=" ... "
            for j in range(L-3, L+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                if j<L:
                    s+=", "
                #
            #
        else:
            for j in range(NN+1, L+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                if j<L:
                    s+=", "
                #
            #
        #
    else:#NN<7
        for j in range(1, NN+1):
            s+=str(X[j-1])
            s+=", "
        #
        if L>NN+7:
            for j in range(NN+1, NN+4+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(XZ[j-1]))
                s+=", "
            #
            s+=" ... "
            for j in range(L-3, L+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                if j<L:
                    s+=", "
                #
            #
        else:
            for j in range(NN+1, L+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                if j<L:
                    s+=", "
                #
            #
        #
    #
    s+="]"
    return s
#

def ReturnSomeArrayValsFirstLastAndNearestToNN_asLists(X, NN):#not done, os nur effa
    L=len(X)
    if NN>7:
        for j in range(1, 3+1):
            s+=str(X[j-1])
            #print("x["+str(j)+"]="+str(X[j-1]))
            s+=", "
        #
        s+=" ... "
        for j in range(NN-4, NN+1):
            s+=str(X[j-1])
            #print("x["+str(j)+"]="+str(X[j-1]))
            s+=", "
        #
        if L>NN+7:
            for j in range(NN+1, NN+4+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                s+=", "
            #
            s+=" ... "
            for j in range(L-3, L+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                if j<L:
                    s+=", "
                #
            #
        else:
            for j in range(NN+1, L+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                if j<L:
                    s+=", "
                #
            #
        #
    else:#NN<7
        for j in range(1, NN+1):
            s+=str(X[j-1])
            s+=", "
        #
        if L>NN+7:
            for j in range(NN+1, NN+4+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(XZ[j-1]))
                s+=", "
            #
            s+=" ... "
            for j in range(L-3, L+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                if j<L:
                    s+=", "
                #
            #
        else:
            for j in range(NN+1, L+1):
                s+=str(X[j-1])
                #print("x["+str(j)+"]="+str(X[j-1]))
                if j<L:
                    s+=", "
                #
            #
        #
    #
    s+="]"
    return s
#

def SortByExtrsXY(Y, X=[], AllExtrs0NurMaxs1NurMins2=0, vsh=0):
    data=[]
    L=len(Y)
    if X==[]:
        for i in range(L):
            X.append(i+1)
        #
    #
    if vsh==1:
        print("SortByExtrs starts working")
    #
    for i in range(L):
        if i>0 and i<L-1:
            if vsh==1:
                print(" X["+str(i+1)+"]="+str(X[i])+" X["+str(i-1+1)+"]="+str(Y[i-1])+" X["+str(i+1+1)+"]="+str(X[i+1]))
                print(" Y["+str(i+1)+"]="+str(Y[i])+" Y["+str(i-1+1)+"]="+str(Y[i-1])+" X["+str(i+1+1)+"]="+str(Y[i+1]))
            #
            if Y[i]>Y[i-1] and Y[i]>X[i+1] and (AllExtrs0NurMaxs1NurMins2==0 or AllExtrs0NurMaxs1NurMins2==1):#maximum
                element=[]
                element.append(+1)#0
                element.append(i+1)#1
                element.append(X[i])#2
                element.append(Y[i])#3
                j=i
                cond=True
                while cond:
                    j-=1
                    if j==1:
                        cond=False
                    #
                    if Y[j]>=Y[i]:
                        cond=False
                    #
                #
                element.append(i-j)#4
                j=i
                cond=True
                while cond:
                    j+=1
                    if j==L-1:
                        cond=False
                    #
                    if Y[j]>=Y[i]:
                        cond=False
                    #
                #
                element.append(j-i)#5
                if vsh==1:
                    print("X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i])+"- maximum: before: "+str(element[4])+", after: "+str(element[5])+" vals")
                #
                data.append(element)
            #
            elif Y[i]<Y[i-1] and Y[i]<Y[i+1] and (AllExtrs0NurMaxs1NurMins2==0 or AllExtrs0NurMaxs1NurMins2==2):#minimum
                element=[]
                element.append(-1)#0
                element.append(i+1)#1
                element.append(X[i])#2
                element.append(Y[i])#3
                j=i
                cond=True
                while cond:
                    j-=1
                    if j==1:
                        cond=False
                    #
                    if Y[j]<=Y[i]:
                        cond=False
                    #
                #
                element.append(i-j)#4
                j=i
                cond=True
                while cond:
                    j+=1
                    if j==L-1:
                        cond=False
                    #
                    if Y[j]<=Y[i]:
                        cond=False
                    #
                #
                element.append(j-i)#5
                if vsh==1:
                    print("X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i])+"- minimum: before: "+str(element[4])+", after: "+str(element[5])+" vals")
                #
                data.append(element)
            else:
                if vsh==1:
                    print("X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i])+"- not extremum")
                #
            #
        else:
            if vsh==1:
                print("X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i])+"-edge val")
            #
        #
    #
    if vsh==1:
        print("SortByExtrs finishes working")
    #
    return data
#


def MyFindPeaksAndSmoothRestXY1(Y, X=[], AllExtrs0NurMaxs1NurMins2=1, MinValsToIgnore=10, prominence=0, CallN1=1, CallN=1, vsh=0):
    data=[]
    data=[]
    X1=[]
    Y1=[]
    L=len(Y)
    if X==[]:
        for i in range(L):
            X.append(i+1)
        #
    #
    if vsh>0:
        print("SortByExtrs starts working CallN "+str(CallN))
    #
    if vsh>2:
        print("Parameters: AllExtrs0NurMaxs1NurMins2="+str(AllExtrs0NurMaxs1NurMins2)+" MinValsToIgnore="+str(MinValsToIgnore)+" prominence="+str(prominence))
        print("Array given L="+str(L)+":")
        #
        for i in range(L):
            print(str(i+1)+") "+" X="+str(X[i])+" Y="+str(Y[i]))
        #
    #
    if vsh>2:
        if CallN==CallN1:
            graphTitle="Smoothing signal: initial"
        else:
            graphTitle="Smoothing signal: before"
        #
        plot_signal(X, Y, title=graphTitle)
        #
    #
    smoothedNs=[]
    i=-1
    while i<L:
        i+=1
        if vsh>2:
            print("i="+str(i)+" (cycle start)")
        #
        if i>0 and i<L-1:
            if vsh>2:
                print(" X["+str(i+1)+"]="+str(X[i])+" X["+str(i-1+1)+"]="+str(Y[i-1])+" X["+str(i+1+1)+"]="+str(X[i+1]))
                print(" Y["+str(i+1)+"]="+str(Y[i])+" Y["+str(i-1+1)+"]="+str(Y[i-1])+" X["+str(i+1+1)+"]="+str(Y[i+1]))
            #
            if Y[i]>Y[i-1] and Y[i]>Y[i+1] and (AllExtrs0NurMaxs1NurMins2==0 or AllExtrs0NurMaxs1NurMins2==1):
                element=[]
                NN=i+1
                element.append(+1)#0
                element.append(NN)#1
                element.append(X[i])#2
                element.append(Y[i])#3
                #
                # e - extremums
                #
                j=i
                cond=True
                while cond:
                    j-=1
                    if j==1:
                        cond=False
                    #
                    if Y[j]>=Y[j+1]:
                        j-=1
                        cond=False
                    #
                #
                leftQPe=i-j
                leftNNe=j+1
                element.append(leftQPe)#4
                j=i
                cond=True
                while cond:
                    j+=1
                    if j==L-1:
                        cond=False
                    #
                    if Y[j]>=Y[j-1]:
                        j-=1
                        cond=False
                    #
                #
                rightQPe=j-i
                rightNNe=j+1
                element.append(rightQPe)#5
                if leftQPe>=rightQPe:
                    greaterQPe=leftQPe
                else:
                    greaterQPe=rightQPe
                #
                element.append(greaterQPe)#6
                if vsh>1:
                    print("X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i])+"- maximum: before: "+str(element[4])+", after: "+str(element[5])+"(max: "+str(element[6])+") vals")
                #
                #elenent.append(curMinQP)#7
                element.append(leftNNe)#7
                element.append(rightNNe)#8
                #
                # c - comparison
                #
                k=i
                cond=True
                while cond:
                    k-=1
                    if k==1:
                        cond=False
                    #
                    if Y[k]>=Y[i] or (prominence>0 and Y[i]/Y[k]<prominence):
                        #if Y[k]>=Y[i]:
                        k-=1
                        cond=False
                    #
                #
                leftQPc=i-k
                leftNNc=k+1
                element.append(leftQPc)#9
                k=i
                cond=True
                while cond:
                    k+=1
                    if k==L-1:
                        cond=False
                    #
                    if Y[k]>=Y[i]:
                        k-=1
                        cond=False
                    #
                #
                rightQPc=k-i
                rightNNc=k+1
                element.append(rightQPc)#10
                if leftQPc>=rightQPc:
                    greaterQPc=leftQPc
                else:
                    greaterQPc=rightQPc
                #
                element.append(greaterQPc)#11
                #
                element.append(leftNNc)#12
                element.append(rightNNc)#13
                #
                data.append(element)
                dataL=len(data)
                #
                # e - extremums
                #
                if dataL==1 or (dataL>1 and greaterQPe<curMinQPe):
                    curMinQPe=greaterQPe
                #
                data[dataL-1].append(curMinQPe)#14
                #
                # c - comparison
                #
                if dataL==1 or (dataL>1 and greaterQPc<curMinQPc):
                    curMinQPc=greaterQPc
                #
                data[dataL-1].append(curMinQPc)#15
                #
                i=j
            elif Y[i]<Y[i-1] and Y[i]<Y[i+1] and (AllExtrs0NurMaxs1NurMins2==0 or AllExtrs0NurMaxs1NurMins2==2):
                element=[]
                element.append(-1)#0
                element.append(i+1)#1
                element.append(X[i])#2
                element.append(Y[i])#3
                j=i
                cond=True
                while cond:
                    j-=1
                    if j==1:
                        cond=False
                    #
                    if Y[j]<=Y[j+1]:
                        j-=1
                        cond=False
                    #
                #
                leftQPe=i-j
                leftNNe=j+1
                element.append(leftQPe)#4
                #
                # e - extremums
                #
                j=i
                cond=True
                while cond:
                    j+=1
                    if j==L-1:
                        cond=False
                    #
                    if Y[j]<=Y[j-1]:
                        j-=1
                        cond=False
                    #
                #
                rightQPe=j-i
                rightNNe=j+1
                element.append(rightQPe)#5
                if leftQPe>=rightQPe:
                    greaterQPe=leftQPe
                else:
                    greaterQPe=rightQPe
                #
                element.append(greaterQPe)#6
                if vsh>1:
                    print("X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i])+"- maximum: before: "+str(element[4])+", after: "+str(element[5])+"(max: "+str(element[6])+") vals")
                #
                #elenent.append(curMinQP)#7
                element.append(leftNNe)#7
                element.append(rightNNe)#8
                #
                # c - comparison
                #
                k=i
                cond=True
                while cond:
                    k-=1
                    if k==1:
                        cond=False
                    #
                    if Y[j]<=Y[k+1]:
                        k-=1
                        cond=False
                    #
                #
                leftQPc=i-k
                leftNNc=k+1
                element.append(leftQPc)#9
                k=i
                cond=True
                while cond:
                    k+=1
                    if k==L-1:
                        cond=False
                    #
                    if Y[K]<=Y[i]:
                        k-=1
                        cond=False
                    #
                #
                rightQPc=k-i
                rightNNc=k+1
                element.append(rightQPc)#10
                if leftQPc>=rightQPc:
                    greaterQPc=leftQPc
                else:
                    greaterQPc=rightQPce
                #
                element.append(greaterQPc)#11
                if vsh>1:
                    print("X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i])+"- maximum: before: "+str(element[4])+", after: "+str(element[5])+"(max: "+str(element[6])+") vals")
                #
                element.append(leftNNc)#12
                element.append(rightNNc)#13
                #
                data.append(element)
                dataL=len(data)
                #
                # e - extremums
                #
                if dataL==1 or (dataL>1 and greaterQPe<curMinQPe):
                    curMinQPe=greaterQPe
                #
                data[dataL-1].append(curMinQPe)#14
                #
                # c - comparison
                #
                if dataL==1 or (dataL>1 and greaterQPc<curMinQPc):
                    curMinQPc=greaterQPc
                #
                data[dataL-1].append(curMinQPc)#15
                #
            elif X[i-1]==X[i]:
                element=[]
                element.append(0)#0
                element.append(i+1)#1
                element.append(X[i])#2
                element.append(Y[i])#3
                cond=True
                j=i
                while cond:
                    j+=1
                    if not (X[j]==X[i]):
                        j-=1
                    #
                #
                element.append(1)#4
                element.append(j-i)#5
                element.append(j-i+1)#6
                data.append(element)
                dataL=len(data)
            else:
                j=i
                if vsh>1:
                    if X[i]>X[i-1]:
                        print("- not an extremum - part of maximum")
                    elif X[i]<X[i-1]:
                        print("- not an extremum - part of minimum")
                    #
                #
                j+=1
            #
            i=j
            i-=1 # ob at start i+=1
            if vsh>2:
                print("i="+str(i)+" (cycle end)")
            #
        else:#ends of array
            if vsh>2:
                print("edge val: N="+str(i)+" L="+str(L))
                print("X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i])+" -edge val")
                i+=1
            #
        #if N
    #for
    if vsh>0:
        print("Among given "+str(len(Y))+" vals "+str(len(data))+" maximums are detected. Checking them")
    #
    #if QPMim<MinValsToIgnore:
    #isNothingToChange=True
    for c in range(1, 2+1):
        for i in range(1, dataL+1):
            if CallN%2==0:
                N=i
            else:
                N=dataL-i+1
            #
            greaterQPe=data[N-1][6]
            greaterQPc=data[N-1][11]
            extrTypeN=data[N-1][0]
            if greaterQPe<=MinValsToIgnore and greaterQPc<=MinValsToIgnore and not (extrTypeN==0):
                if vsh>0:#2:
                    print("Peak N"+str(N)+" has no more than "+str(greaterQPe)+" points and is greater than no more than "+str(greaterQPc)+" nearest values => to smooth")
                #isNothingToChange=False
                smoothedNs.append(N)
                N0=data[N-1][1]
                N1=N0-data[N-1][5]
                N2=N0+data[N-1][6]
                leftNNe=data[N-1][7]
                rightNNe=data[N-1][8]
                N1=leftNNe
                N2=rightNNe
                if vsh>0:#2:
                    print("Smoothing points NN "+str(N1)+" ... "+str(N2)+" (in all "+str(L)+" vals)")
                #
                k=(Y[N2-1]-Y[N1-1])/(X[N2-1]-X[N1-1])
                b=Y[N1-1]-k*X[N1-1]
                #if data[N-1][0]==1: #    b=b+((Y[N2-1]+Y[N1-1])/2+Y[N0-1])/2
                #elif data[N-1][0]==-1: # b=b-((Y[N2-1]+Y[N1-1])/2+Y[N0-1])/2
                ##
                for j in range(N1, N2+1):
                    Y[j-1]=k*X[j-1]+b
                #
                if vsh>2:
                    print("Peak along points NN "+str(N1)+".."+str(N2)+" is smoothed as not significant")
                #
            else:
                if vsh>2:
                    print("Peak at point N "+str(N)+": from point N "+str(data[N-1][1]-data[N-1][5])+" to point N "+str(data[N-1][1]+data[N-1][6])+" has more than "+str(greaterQPe)+" points, is greater than more than "+str(greaterQPc)+" nearest values")
                #
                #pass
            #
        #for dataL
        smoothedQ=len(smoothedNs)
        #print(" smoothedQ="+str(smoothedQ)+" CallN-CallN1="+str(CallN)+"-"+str(CallN1)+"="+str(CallN-CallN1)+"<MinValsToIgnore="+str(MinValsToIgnore)+" Contin="+str(Contin))
        if smoothedQ>0 and vsh>2:
            graphTitle="Smoothing signal: after ("+str(c)+")"
            plot_signal(X, Y, title=graphTitle)
        else:
            if vsh>1:
                print("Nothing to smooth, all peaks are actual ("+str(c)+")")
            #
        #
    #
    Contin=(smoothedQ>0 and CallN-CallN1<MinValsToIgnore)
    if Contin:
        if vsh>2:
            print("continuing - recursion from call N "+str(CallN))
        #
        data, Contin, CallN2 = MyFindPeaksAndSmoothRestXY1(Y, X, AllExtrs0NurMaxs1NurMins2, MinValsToIgnore, prominence, CallN1, CallN+1, vsh)
        if vsh>2:
            print("returned after recursion call N "+str(CallN2)+" to function call N "+str(CallN))
        #
    #
    #if Contin==false:# not else ob V abl adha False after recursion # if V returned so V abl exgo
    if (vsh>1 and CallN>1) or (vsh>0 and CallN==1):
        #print("Values (corrected) list:")
        #for i in range(L):
        #    print(" X["+str(i+1)+"]="+str(X[i])+" Y["+str(i+1)+"]="+str(Y[i]))
        ##
        dataL=len(data)
        print("Peaks list:")
        for i in range(dataL):
            print("extrN"+str(i+1)+" X="+str(data[i][2])+" Y="+str(data[i][3])+" Consists of points: left: "+str(data[i][7])+" right: "+str(data[i][8])+" Greater thsan vals: left: "+str(data[i][12])+" right: "+str(data[i][13]))
        #
    #
    if (vsh>1 and CallN>1) or (vsh>0 and CallN==1):
        plot_signal(X, Y, title="Finally")
    #
    if vsh>0:
        print("SortByExtrs finishes working CallN "+str(CallN))
    #
    return data, Contin, CallN
    #
# end def    

def plot_signal(t, signal, title="Сигнал", t_start=None, t_end=None):
    t = np.array(t)
    signal = np.array(signal)
    if t_start is None:
        t_start = t[0]
    if t_end is None:
        t_end = t[-1]

    mask = (t >= t_start) & (t <= t_end)
    plt.figure(figsize=(12,6))
    plt.plot(t[mask], signal[mask])
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.title(title)
    plt.grid()
    plt.show()

#def medium of list

    
#arr=[10, 20, 40, 50, 60, 70, 80, 90]
#arr1DIns(arr, 30, 3, vsh=1)
#print("arr after insert:", arr)
#arr=[10, 20, 40, 50, 60, 70, 80, 90]
#arr1DIns(arr, 30, 1, vsh=1)
#print("arr after insert:", arr)
#print(str(LInterp([1, 2, 3, 4], [10, 20, 30, 40], 2.5)))
#print(str(LInterp([1, 2, 3, 4], [10, 20, 30, 40], 0.5)))
#print(str(LInterp([1, 2, 3, 4], [10, 20, 30, 40], 6.5)))
#print(str(LInterp([1, 2, 3, 4], [10, 20, 30, 40], 3.7)))
