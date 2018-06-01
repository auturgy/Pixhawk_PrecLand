#from __future__ import print_function
import time
from datetime import datetime
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
# Set up option parsing to get connection string
import argparse
startTime=str(datetime.now())
#vehicle = connect('udp:192.168.42.1:14550', baud=57600, wait_ready=True)
vehicle = connect('/dev/ttyACM0', baud=57600, wait_ready=True)
#vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

def get_vehicle_state_simple():
    print(" 0.Mode: %s" % vehicle.mode.name)    # settable
    print " 1.Altitude: ", vehicle.location.global_relative_frame.alt
    print(" 2.Attitude: %s" % vehicle.attitude)
    print(" Velocity: %s" % vehicle.velocity)
    print(" Heading: %s" % vehicle.heading)
def get_channels():
    print(" Ch1: %s" % vehicle.channels['1'])
    print(" Ch2: %s" % vehicle.channels['2'])
    print(" Ch3: %s" % vehicle.channels['3'])
    print(" Ch4: %s" % vehicle.channels['4'])
    print(" Ch5: %s" % vehicle.channels['5'])
    print(" Ch6: %s" % vehicle.channels['6'])

drone_logs=""
pre_rc_roll=vehicle.channels['1']
def override_roll(dx):
    global pre_rc_roll
    #scale the dx ( delta distance ) to desired rc value -> setpoint angle
    rc_roll=1500+dx
    #saturate 2 consecutive values
    if rc_roll-pre_rc_roll>=3.2:
        rc_roll=pre_rc_roll+3.2
    if rc_roll-pre_rc_roll<=-3.2:
        rc_roll=pre_rc_roll-3.2
    #saturate the rc_roll output
    if rc_roll>=1550:
        rc_roll=1550
    if rc_roll<=1450:
        rc_roll=1450
    rc_roll=round(rc_roll)
    pre_rc_roll=rc_roll
    return rc_roll
while True:
    get_vehicle_state_simple()
    get_channels()
    #some function to get dx
    if 1450<=vehicle.channels['5']<=1550:
        #Channel override code.
        vehicle.channels.overrides['1'] = override_roll(dx)
    else:
        print("Clear all overrides")
        vehicle.channels.overrides = {}
    time.sleep(0.2)
