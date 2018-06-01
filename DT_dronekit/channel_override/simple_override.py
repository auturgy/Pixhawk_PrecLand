import time
import matplotlib.pyplot as plt
from datetime import datetime
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
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

#vehicle = connect('/dev/ttyACM0', baud=57600, wait_ready=True)
print "Channel override in 5 seconds"
time.sleep(5)
a=3.0
b=2.0
h=65.0
rcList=[]
timeList=[]
i=0
startTime=time.time()
while True:
    currentTime=time.time()
    elapsedTime=currentTime-startTime
    rc_offset=Trapezoid_signal(a,b,h,elapsedTime)
    #timeList.append(elapsedTime)
    #rcList.append(rc_offset)
    #print rc_offset
    #print time.time()
    #vehicle.channels.overrides['1'] = 1500+rc_offset
    channel_override = 1500+rc_offset
    print channel_override
    time.sleep(0.05)
    i=i+1
    if (i>61):
        #vehicle.channels.overrides['1']=0
        channel_override=0
        print channel_override
        break
