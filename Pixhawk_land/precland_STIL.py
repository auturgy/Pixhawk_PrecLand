#Software In The Loop testing.
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import logging
import cv2
import numpy as np

vehicle = connect("127.0.0.1:14550",wait_ready=True)

def send_land_message(x,y):
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

def get_vehicle_state_simple():
    print(" 0.Mode: %s" % vehicle.mode.name)    # settable
    print " 1.Altitude: ", vehicle.location.global_relative_frame.alt
    print(" 2.Attitude: %s" % vehicle.attitude)
    print(" ***Velocity: %s" % vehicle.velocity)
    print(" Heading: %s" % vehicle.heading)
def arm_and_takeoff(tgt_altitude):
    print("Arming motors")

    while not vehicle.is_armable:
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed: time.sleep(1)

    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)

    #-- wait to reach the target altitude
    while True:
        altitude = vehicle.location.global_relative_frame.alt

        if altitude >= tgt_altitude -0.5:
            print("Altitude reached")
            break

        time.sleep(1)

vehicle.parameters['PLND_ENABLED'] = 1
vehicle.parameters['PLND_TYPE'] = 1 # Mavlink landing mode
#tgt_altitude=10
# Following are for SITL rangefinder
#enabling the range finder in SITL. -> to be able to send land message
#https://discuss.ardupilot.org/t/sitl-ubuntu-precision-landing-with-companion-computer/13959/3
vehicle.parameters['RNGFND_TYPE'] = 1
vehicle.parameters['RNGFND_MIN_CM'] = 0
vehicle.parameters['RNGFND_MAX_CM'] = 4000
vehicle.parameters['RNGFND_PIN'] = 0
vehicle.parameters['RNGFND_SCALING'] = 12.12

arm_and_takeoff(10)

time.sleep(5)

vehicle.mode = VehicleMode("LAND")
while 1:
    get_vehicle_state_simple()
    send_land_message(50,50)
    time.sleep(0.5)
