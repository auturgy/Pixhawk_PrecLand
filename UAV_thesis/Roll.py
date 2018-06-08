import time
#from dronekit import connect, VehicleMode, LocationGlobalRelative
#from pymavlink import mavutil
import simple_override

vehicle=simple_override.vehicle
#vehicle = connect('/dev/ttyACM0', baud=57600, wait_ready=True)
time.sleep(0.5)
vehicle.channels.overrides['1'] = 1600
time.sleep(0.5)
vehicle.channels.overrides['1'] = 1700


##global h
##
##start = time.time()
##for i in range(1,62):
##    if i <= 10: 
##        value=h*i/10
##            
##    elif 10< i <=50:
##        value=h
##            
##    elif 50< i <=60:
##        value=h*(60-i)/10
##            
##    else:
##        value=0
##        stop = time.time()
##        print stop-start
##
##
##    time.sleep(0.05)
##    value=round(value)
##    print value
##        #override here
##
### Toa do, nhan voi he so. Suy ra gia tri h, call ham Trapzoid_signal
##





