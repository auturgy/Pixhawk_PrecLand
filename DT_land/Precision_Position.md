https://discuss.ardupilot.org/t/feed-optical-flow-from-custom-sensor-algorithm-to-ardupilot/13070
http://ardupilot.org/copter/docs/indoor-flying.html
http://ardupilot.org/copter/docs/precision-landing-with-irlock.htmlc

### Gyro compensation.
Gimbal, camera stabilization
https://www.youtube.com/watch?v=wQypj7ti7Vw
![arUco marker](../media_files/arUco_marker.png)
# Precision Position Hold

## Approaches
+ disable GPS.
+ diable throttle high failsafe -> ( armed by dronekit in other MODE
  )
+ set some limits on parameters ( setpoint roll pitch angles )

### Buying Sensors
+ The Ardupilot has precision landing feature, based on Optical Flow Sensor ( used in Loiter mode for position hold )
PX4Flow hardware has a gyro and does its own compensation before data arrives at the ArduPilot side

http://ardupilot.org/copter/docs/parameters.html#plnd-enabled
+ IR sensor. For environment-independent environments ( light, ...)
https://raspberrypi.vn/shop/phu-kien-raspberry-pi/camera-hong-ngoai-raspberry-pi-noir

DFRobot IR positioning camera
>"Thomas' system uses an IR transmitter on the ground and with the camera on the drone, presumably having an IR filter to reduce background clutter. From what I've seen this system seems to have a very good signal-to-noise ratio with little background clutter. I've got one of his transmitters and it really pumps out IR making it very clear on my IR cameras.
From a design point of view there's a lot to be said for "active" systems that have clearly defined targets. Passive systems that rely on image recognition seem to be a lot more problematic when conditions are less than ideal - especially if you are planning to use the Pi camera ;).
https://diydrones.com/forum/topics/image-processing-for-precision-landing
"

Copter 3.4 (and higher) supports Precision Landing using the IR-LOCK sensor and a sonar or lidar. Using this system, when the vehicle enters LAND mode (and has GPS lock) it is possible to reliably land within 30cm of an IR beacon that is moving at less than 1m/s.

### RC override

Try different ways to do the North-East hold first ( position hold without altitude hold ). My dirty-way script ( using RC override ).

### Using Precision Loiter mode.
Possible approach.
Combine firmware's feature.
and Raspberry will feed the target's coordinate via dronekit.
https://discuss.ardupilot.org/t/precision-loiter-help/22583
+ Enable PrecLoiter mode ( override CHANNEL 7 > 1800 )
http://ardupilot.org/copter/docs/parameters.html#ch7-opt-channel-7-option
+ Change PLND_Type = 1 ( companion computer )
http://ardupilot.org/copter/docs/parameters.html#plnd-type
+ Set the drone in LOITER mode.
+ feed the Fight Controller using the Mavlink LANDING_TARGET. in dronekit
https://discuss.ardupilot.org/t/how-to-use-precision-landing-feature-with-companion-computer/9619/12

### Precision Landing



## Projects:
https://github.com/squilter/target-land
https://github.com/djnugent/cv_utils
## References:
https://diydrones.com/forum/topics/image-processing-for-precision-landing   
https://github.com/openmv   
https://diydrones.com/forum/topics/apm-drifts-in-loiter-position-hold-alt-hold-is-acceptable
https://gitter.im/dronekit/dronekit-python/archives/2017/01/04
