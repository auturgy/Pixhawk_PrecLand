import time
import matplotlib.pyplot as plt
from datetime import datetime
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import os
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


def main():
    global vehicle
    vehicle = connect('/dev/ttyACM0', baud=57600, wait_ready=True)    
    print ("Channel override in 1 seconds")
    time.sleep(1)
    a=3.0
    b=2.0
    h=65
    rcList=[]
    timeList=[]
    i=0
    startTime=time.time()
    while True:
        currentTime=time.time()
        elapsedTime=currentTime-startTime
        print elapsedTime
        rc_offset=Trapezoid_signal(a,b,h,elapsedTime)
        #timeList.append(elapsedTime)
        #rcList.append(rc_offset)
        #print rc_offset
        #print time.time()
        vehicle.channels.overrides['3'] = 1500+rc_offset
        channel_override = 1500+rc_offset
        print vehicle.channels
        time.sleep(0.05)
        
        
        i=i+1
        if (i==40 | i==41 ):
            os.system("python /home/pi/UAV_Thesis/Roll.py")
        if (i>61):
            vehicle.channels.overrides['3']=None
            vehicle.channels.overrides['1']=None
            channel_override=0
            print channel_override
            break

if __name__ == "__main__":
    main()

