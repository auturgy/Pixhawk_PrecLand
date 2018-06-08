from picamera import PiCamera
import time
camera = PiCamera()

camera.brightness = 55
camera.resolution = (1920, 1280)

camera.start_preview()
time.sleep(5)
camera.stop_preview()

