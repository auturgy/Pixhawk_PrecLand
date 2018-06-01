# Require to manually takeoff to any Altitude. switch to 1500
# Enable Precision LAND with Companion Computer. switch to LAND mode.


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
(x-horizontal_resolution/2)*horizontal_fov/horizontal_resolution,
(y-vertical_resolution/2)*vertical_fov/vertical_resolution,
0, # altitude. Not supported.
0,0) # size of target in radians
vehicle.send_mavlink(msg)
vehicle.flush()

vehicle = connect("/dev/ttyACM2", baud=57600, wait_ready=True)
def get_vehicle_state_simple():
    print(" 0.Mode: %s" % vehicle.mode.name)    # settable
    print " 1.Altitude: ", vehicle.location.global_relative_frame.alt
    print(" 2.Attitude: %s" % vehicle.attitude)
    print(" Velocity: %s" % vehicle.velocity)
    print(" Heading: %s" % vehicle.heading)
while(1):
    get_vehicle_state_simple()
    if 1450<=vehicle.channels['5']<=1550:
        #Channel override code.
        #http://ardupilot.org/copter/docs/parameters.html#plnd-parameters
        craft.vehicle.parameters['PLND_ENABLED'] = 1
        #http://ardupilot.org/copter/docs/parameters.html#plnd-type-precision-land-type
        # PLND_TYPE=1 -> Companion Computer
        craft.vehicle.parameters['PLND_TYPE'] = 1 # Mavlink landing mode

        # we have to change to LAND mode.
        vehicle.mode=VehicleMode("LAND")

        time.sleep(0.1)
        send_land_message(0, 0)
    else:
        print("Clear all overrides")
        vehicle.channels.overrides = {}
