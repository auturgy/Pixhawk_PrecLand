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
vehicle.channels.overrides['3'] = 1100
vehicle.channels.overrides['4'] = 1900
time.sleep(5)
vehicle.channels.overrides['4'] = 1500
vehicle.channels.overrides['3'] = 1200
time.sleep(0.5)
vehicle.channels.overrides['3'] = 1300
time.sleep(0.5)
vehicle.channels.overrides['3'] = 1400
time.sleep(0.5)
vehicle.channels.overrides = {}
while True:
    get_vehicle_state_simple()
    get_channels()
    if 1450<=vehicle.channels['5']<=1550:
        #Channel override code.
        vehicle.channels.overrides['3'] = 1550
        time.sleep(0.5)
        vehicle.channels.overrides['3'] = 1480
    else:
        print("Clear all overrides")
        vehicle.channels.overrides = {}
    time.sleep(0.1)
    drone_logs=drone_logs+str(datetime.now())
text_file = open("Output.txt", "w")
text_file.write("Logs for %s" % startTime)
text_file.write("%s" % drone_logs)
text_file.close()
