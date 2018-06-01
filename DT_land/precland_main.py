from picamera.array import PiRGBArray
from picamera import PiCamera
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import logging
import cv2
import numpy as np
# horizontal_fov and vertical_fov is how much your camera can see in terms of degrees, for a Pi camera v1.3 its 54 by 41 degrees
#color settings
hue_lower = 55
hue_upper = 185
saturation_lower = 110
saturation_upper = 170
value_lower = 190
value_upper = 250
min_contour_area = 500 # the smallest number of pixels in a contour before it will register this as a target

#camera
horizontal_fov = 54*math.pi/180
vertical_fov = 41*math.pi/180
horizontal_resolution = 1280
vertical_resolution = 720

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
    (x-horizontal_resolution/2)*horizontal_fov/horizontal_resolution,
    (y-vertical_resolution/2)*vertical_fov/vertical_resolution,
    0, # altitude. Not supported.
    0,0) # size of target in radians
    vehicle.send_mavlink(msg)
    vehicle.flush()

vehicle = connect("/dev/ttyACM2", baud=57600, wait_ready=True)
craft.vehicle.parameters['PLND_ENABLED'] = 1
craft.vehicle.parameters['PLND_TYPE'] = 1 # Mavlink landing mode
while(1):
    if 1450<=vehicle.channels['5']<=1550:
        vehicle.channels.overrides['7']=1850
        #Channel override code.


        #Select which function is performed when CH7 is above 1800 pwm
        #http://ardupilot.org/copter/docs/parameters.html#ch7-opt-channel-7-option

        #then override channel 7 to go Precision Loiter

    else:
        print("Clear all overrides")
        vehicle.channels.overrides = {}
