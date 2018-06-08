


Useful information and links for doing the landing with dronekit.
# NOTE dronekit function.
```if args.fakerangefinder:
    # Following are for mavlink based rangefinder (not needed for 3.5-rc2+)
    craft.vehicle.parameters['RNGFND_TYPE'] = 10
    craft.vehicle.parameters['RNGFND_MIN_CM'] = 1
    craft.vehicle.parameters['RNGFND_MAX_CM'] = 10000
    craft.vehicle.parameters['RNGFND_GNDCLEAR'] = 5
    log.info("Faking RangeFinder data with distance_sensor messages")
if args.fakerangefinder:
        craft.send_distance_message(int(z*100))
### Control Commands.
craft.send_land_message(x,y,z, tracktime.estimate()/1000)

craft.vehicle.parameters['PLND_ENABLED'] = 1
craft.vehicle.parameters['PLND_TYPE'] = 1 # Mavlink landing mode
```

```
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
```
3. https://github.com/djnugent/cv_utils/blob/master/cv_utils/vehicle_control.py
```
# report_landing_target - send LANDING_TARGET command to vehicle to shift landing location
    def report_landing_target(self,usec,frame, angle_x, angle_y, distance,size_x,size_y):
        #only let commands through at 33hz
        if(time.time() - self.last_report_landing_target) > self.landing_update_rate:
            self.last_report_landing_target_ = time.time()
            # create the LANDING TARGET message
            msg = self.vehicle.message_factory.landing_target_encode(
							                             usec,      # time frame was captured
                                                         0,         # landing target number (not used)
                                                         frame,   # frame
                                                         angle_x,   # Angular offset x axis
                                                         angle_y,   # Angular offset y axis
                                                         distance,  # Distance to target
							                             size_x,    # unused
							                             size_y)    # unused
            # send command to vehicle
            self.vehicle.send_mavlink(msg)
            self.vehicle.flush()
```

Tiziano Fiorenzani @tizianofiorenzani
First I setup GPS_TYPE2 = 14 (mavlink), then I call this function. I also set GPS_AUTO_SWITCH = 2
```
def set_gps_input(vehicle, lat, lon, alt_amsl, hdop, vdop, vn, ve, vd, spd_acc, hor_acc, vert_acc, ignore_flags=0, fix_type=5, time_week_ms=0, time_week=0, time_us=0):
    # fix_type        = 5
    sat_visible     = 20
    epoch           = 315964782
    cur             = datetime.datetime.utcnow()
    ts              = cur - datetime.datetime(1970,1,1)
    epoch_sec       = ts.total_seconds() - epoch
    time_week       = epoch_sec / 604800.0
    time_week_ms    = (epoch_sec % 604800) * 1000.0 + ts.microseconds*0.001

    msg = vehicle.message_factory.gps_input_encode(
                         time_us,       # time_boot_ms (not used)
                         0,                 # gps_id
                         ignore_flags,      # gps_flag
                         int(time_week_ms),
                         int(time_week),
                         fix_type,
                         int(lat*1e7), int(lon*1e7), alt_amsl,  
                         hdop, vdop,
                         vn, ve, vd,
                         spd_acc, hor_acc, vert_acc,
                         sat_visible)                # Satellites visible



    # send command to vehicle
    vehicle.send_mavlink(msg)

```
## exerpt
>"
The variable which you should keep updating is ‘x’ and ‘y’ which are the co-ordinate information of your landing target in the image or video your python code is processing, in rcmackay9’s video, I’m guessing he is detecting circles, so he identifies the circle and he finds the center co-ordinate of the circle within the image and this is the ‘x’ and ‘y’ co-ordinate, so in the code the ‘x’ and ‘y’ variables keep updating so you have to run the above function again in a continuous loop so the copter knows where it has to go, horizontal_resolution and vertical_resolution are the resolution of your image, horizontal_fov and vertical_fov is how much your camera can see in terms of degrees, for a Pi camera v1.3 its 54 by 41 degrees. The rest of the parameters in the function I have yet to look into it. Try looking in this, you’ll get the idea of how the code should work. Hope this helps.
https://github.com/squilter/target-land/blob/master/target_land.py123
"
## links
https://github.com/squilter/target-land/blob/master/target_land.py
