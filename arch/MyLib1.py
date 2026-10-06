import copy

def isInArrayAtPosN(arr, val):
    L=len(arr)
    Ns=[]
    for i in range(L):
        if arr[i]==val:
            Ns.append(i+1)
        #
    #
    return Ns
#
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

def valIsAtPos(arr, val, vsh=0):
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
