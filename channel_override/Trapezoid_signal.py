#generate trapezoi signal to simulate RC input.
#Used for RC override mode Pixhawk.
import time
import matplotlib.pyplot as plt
#a,b lll day lon, day be cua hinh thang
#output value >=0
def Trapezoid_signal(a,b,h,elapsedTime):
    t1=(a-b)/2
    t2=a-(a-b)/2
    #0->(a-b)/2
    if elapsedTime<t1: #t1=0??
        value=elapsedTime*h/t1
    elif t1<elapsedTime<=t2:
        #next->a-(a-b)/2
        value=h
    elif t2<elapsedTime<a:
        value=h*(elapsedTime-a)/(t2-a)
    else:
        value=0
    #next->a
    value=round(value)
    return value
a=2.5
b=1.5
h=30
startTime=time.time()
rcList=[]
timeList=[]
i=0
while True:
    currentTime=time.time()
    elapsedTime=currentTime-startTime
    rc_offset=Trapezoid_signal(a,b,h,elapsedTime)
    timeList.append(elapsedTime)
    rcList.append(rc_offset)
    print rc_offset
    print time.time()
    time.sleep(0.05)
    #i=i+1
    #if (i>300):
        #break
plt.plot(timeList,rcList)
plt.xlabel('Time')
plt.ylabel('rc_offset')
plt.show()
