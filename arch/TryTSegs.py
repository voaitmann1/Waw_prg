import numpy as np

dt=1.2

segs1=[[2.4, 3.9], [5.6, 6.8], [7.1, 8.4], [12.7, 13.3], [16.2, 17.8]]
segs2=[[2.4, 3.8], [5.5, 6.9], [9.5, 11.9],[12.1, 15.8], [16.3, 17.9]]
segsS=[segs1, segs2]
print("Given")
#print(segsS)
print(segs1)
print(segs2)

print("Solving")
QRowsToCompar=len(segsS)
NewSegs=[]
for i in range(1, len(segs1)+1):
    for j in range(1, len(segs2)+1):
        seg1=segs1[i-1]
        seg2=segs2[j-1]
        t11=seg1[1-1]
        t12=seg1[2-1]
        t21=seg2[1-1]
        t22=seg2[2-1]
        #print("Comparing: ["+str(t11)+","+str(t12)+"] with ["+str(t21)+","+str(t22)+"]")
        NewSeg=[]
        if np.abs(t11-t21)<dt and np.abs(t12-t22)<dt:
            #t1= t11>=t12 ? t11 : t12
            #t2= t21<=t22 ? t21 : t22
            if t11>=t21:
                t1=t11
            else:
                t1=t21
            if t12<=t22:
                t2=t12
            else:
                t2=t22
            #print("this: ["+str(t1)+","+str(t2)+"]")
            NewSeg.append(t1)
            NewSeg.append(t2)
            NewSegs.append(NewSeg)
        else:
            #print("no")
            pass
print("Found")
print(NewSegs)


def FindCommonSegnments(segs1, segs2):
    for i in range(1, len(segs1)+1):
        for j in range(1, len(segs2)+1):
            seg1=segs1[i-1]
            seg2=segs2[j-1]
            t11=seg1[1-1]
            t12=seg1[2-1]
            t21=seg2[1-1]
            t22=seg2[2-1]
            #print("Comparing: ["+str(t11)+","+str(t12)+"] with ["+str(t21)+","+str(t22)+"]")
            NewSeg=[]
            if np.abs(t11-t21)<dt and np.abs(t12-t22)<dt:
                #t1= t11>=t12 ? t11 : t12
                #t2= t21<=t22 ? t21 : t22
                if t11>=t21:
                    t1=t11
                else:
                    t1=t21
                if t12<=t22:
                    t2=t12
                else:
                    t2=t22
                #print("this: ["+str(t1)+","+str(t2)+"]")
                NewSeg.append(t1)
                NewSeg.append(t2)
                NewSegs.append(NewSeg)
            else:
                #print("no")
                pass
    return NewSegs
