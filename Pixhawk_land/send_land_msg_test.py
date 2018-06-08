from picamera.array import PiRGBArray
from picamera import PiCamera
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import logging
import cv2
import numpy as np

def send_stop_land_message():
    msg = vehicle.message_factory.landing_target_encode(
    0,       # time_boot_ms (not used)
    0,       # target num
    1,       # gimbal frame
    0,
    0,
    0,       #altitude.  Not supported.
    0,0)     # size of target in radians
    vehicle.send_mavlink(msg)
    vehicle.flush()
def send_land_message(x, y):
    msg = vehicle.message_factory.landing_target_encode(
    0, # time_boot_ms (not used)
    0, # target num
    0, # frame
    x,
    y,
    0, # altitude. Not supported.
    0,0) # size of target in radians
    vehicle.send_mavlink(msg)
    vehicle.flush()

vehicle = connect("/dev/ttyACM0", baud=57600, wait_ready=True)
def get_vehicle_state():
    print " 0.Channel values from RC Tx:", vehicle.channels
    print " 1.Altitude: ", vehicle.location.global_relative_frame.alt
    print(" Global Location: %s" % vehicle.location.global_frame)
    print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    print(" Local Location: %s" % vehicle.location.local_frame)
    print(" Attitude: %s" % vehicle.attitude)
    print(" Velocity: %s" % vehicle.velocity)
    print(" GPS: %s" % vehicle.gps_0)
    #print(" Gimbal status: %s" % vehicle.gimbal)
    #print(" Battery: %s" % vehicle.battery)
    print(" EKF OK?: %s" % vehicle.ekf_ok)
    print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
    #print(" Rangefinder: %s" % vehicle.rangefinder)
    #print(" Rangefinder distance: %s" % vehicle.rangefinder.distance)
    #print(" Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
    print(" Heading: %s" % vehicle.heading)
    #print(" Is Armable?: %s" % vehicle.is_armable)
    print(" System status: %s" % vehicle.system_status.state)
    print(" Groundspeed: %s" % vehicle.groundspeed)    # settable
    print(" Airspeed: %s" % vehicle.airspeed)    # settable
    print(" Mode: %s" % vehicle.mode.name)    # settable
    #print(" Armed: %s" % vehicle.armed)    # settable

#vehicle.parameters['PLND_ENABLED'] = 2
#vehicle.parameters['PLND_TYPE'] = 1 # Mavlink landing mode
while(1):
    get_vehicle_state()
    if 1850<=vehicle.channels['5']<=1950:
        #Channel override code.

        #time.sleep(5)
        print "Loiter mode ..."
        #vehicle.mode = VehicleMode("LOITER")
        #Select which function is performed when CH7 is above 1800 pwm
        #http://ardupilot.org/copter/docs/parameters.html#ch7-opt-channel-7-option

        #then override channel 7 to go Precision Loiter
        #vehicle.channels.overrides['7']=1900
        send_land_message(0,0)

    else:
        print("Clear all overrides")
        vehicle.channels.overrides = {}
    time.sleep(0.1)
