#from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
# Set up option parsing to get connection string
import argparse

parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None
# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

#main
print "Checks vehicle armable state"
# Don't let the user try to arm until autopilot is ready
#vehicle.mode    = VehicleMode("STABILIZE")
while not vehicle.is_armable:
  print " Waiting for vehicle to initialise..."
  time.sleep(1)

#if (mission_start=="yes")
print "Arming motors in 5 seconds from now"
time.sleep(5)
    # Copter should arm in GUIDED mode
vehicle.mode    = VehicleMode("GUIDED")
vehicle.armed   = True

#while not vehicle.armed: time.sleep(1)
while not vehicle.armed:
    print " Waiting for arming..."
    time.sleep(1)
print "armed successfully"
print "Taking off to 2 meters!"
altSetpoint=5
vehicle.simple_takeoff(altSetpoint)

def set_velocity_body(vehicle, vx, vy, vz):
    """ Remember: vz is positive downward!!!
    http://ardupilot.org/dev/docs/copter-commands-in-guided-mode.html

    Bitmask to indicate which dimensions should be ignored by the vehicle
    (a value of 0b0000000000000000 or 0b0000001000000000 indicates that
    none of the setpoint dimensions should be ignored). Mapping:
    bit 1: x,  bit 2: y,  bit 3: z,
    bit 4: vx, bit 5: vy, bit 6: vz,
    bit 7: ax, bit 8: ay, bit 9:


    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
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
    print(" Ch7: %s" % vehicle.channels['7'])
    print(" Ch8: %s" % vehicle.channels['8'])
while True:
    get_vehicle_state_simple()
    get_channels()
    if vehicle.location.global_relative_frame.alt>=0.93*altSetpoint:
      print "Reached target altitude"
      break
set_velocity_body(vehicle, 2.0, 2.0, 0.0)
time.sleep(5)
print("Now let's land")
vehicle.mode=VehicleMode("LAND")
while True:
    get_vehicle_state_simple()
    get_channels()
    if vehicle.location.global_relative_frame.alt<=0.1:
      print "Reached target altitude"
      break
    time.sleep(0.5)
# Close vehicle object
#vehicle.close()

# Shut down simulator if it was started.
#if sitl:
#    sitl.stop()
