from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import os

import matplotlib.pyplot as plt
from datetime import datetime
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil


vehicle = connect('/dev/ttyACM0', baud=57600, wait_ready=True)
print ("Channel override in 1 seconds")
time.sleep(1)

while vehicle.channels['5'] > 1000 and vehicle.channels['5'] <1200:
    print vehicle.channels['5']
    pass
os.system("sudo /home/pi/RPi_Cam_Web_Interface/stop.sh")  
##def signal(h1,h2):
##    for i in range(1,18):
##        if i <= 3: 
##            Roll=h1*i/3
##            Pitch=h2*i/3
##        elif 4< i <=15:
##            Roll=h1
##            Pitch=h2
##                
##        elif 15< i <=18:
##            Roll=h1*(18-i)/3
##            Pitch=h2*(18-i)/3
##                
##        else:
##            Roll=0
##            Pitch=0


##def signal(h1,h2):
##    for i in range(1,18):
##        if i <= 14: 
##            Roll=h1
##            Pitch=h2
##        elif 14< i <=18:
##            Roll=0
##            Pitch=0
##        
##        time.sleep(0.01)
##        Roll=round(Roll)
##        Pitch=round(Pitch)
##        vehicle.channels.overrides['1'] = 1500 + Roll
##        vehicle.channels.overrides['2'] = 1500 + Pitch
##        #print vehicle.channels['1'], vehicle.channels['2']
##        #print Roll, Pitch

def signal(h1,h2):  
    Roll=round(h1)
    Pitch=round(h2)
    vehicle.channels.overrides['1'] = 1400 + Roll
    vehicle.channels.overrides['2'] = 1500 + Pitch
    time.sleep(0.3)
    vehicle.channels.overrides['1'] = 1400
    vehicle.channels.overrides['2'] = 1500
    time.sleep(0.02)
    #print vehicle.channels['1'], vehicle.channels['2']
    #print Roll, Pitch


              
        
kernel = np.ones((5,5),np.uint8)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.rotation = 180
camera.brightness = 55
camera.resolution = (320, 240)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(320, 240))

time.sleep(0.25)
# Take input from webcam
 
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
 
    
    frame = image.array
  
    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)
 
    # get experience value
    hmn = 0
    hmx = 24
   
 
    smn = 110
    smx = 255
 
 
    vmn = 0
    vmx = 255
 
    # Apply thresholding
    hthresh = cv2.inRange(np.array(hue),np.array(hmn),np.array(hmx))
    sthresh = cv2.inRange(np.array(sat),np.array(smn),np.array(smx))
    vthresh = cv2.inRange(np.array(val),np.array(vmn),np.array(vmx))
 
    # AND h s and v
    tracking = cv2.bitwise_and(hthresh,cv2.bitwise_and(sthresh,vthresh))
 
    # Some morpholigical filtering
    erosion = cv2.erode(tracking,kernel,iterations = 1)
    opening = cv2.morphologyEx(erosion,cv2.MORPH_OPEN,kernel)
    
    dilation = cv2.dilate(opening,kernel,iterations = 1)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    closing = cv2.GaussianBlur(closing,(3,3),0)
 
    #find contour in the threshold image

    im2, contours, hierarchy = cv2.findContours(closing,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    best_contour = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    

    #finding centroids of best_cnt

    if  max_area>0:  # get value 15000 from experience
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
##        cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
    else:
        cx=159
        cy=119
    print(cx,cy)
    print(max_area)

##    cv2.imshow('tracking',frame)


    if (159-cx)>0 and (119-cy)<0:     #Qua  phai,  di len
        signal((159-cx)*65/158,(119-cy)*80/118)
    elif (159-cx)<0 and (119-cy)>0:      #Qua trai,  di xuong
        signal((159-cx)*75/158,(119-cy)*70/118)
    elif (159-cx)>0 and (119-cy)>0:     #Qua phai,,di xuong
        signal((159-cx)*65/159,(119-cy)*70/118)
    else:                               #qua trai,,  di llenn
        signal((159-cx)*75/159,(119-cy)*80/118)
        
    
    
    rawCapture.truncate(0)
    
    

    if vehicle.channels['5'] > 1000 and vehicle.channels['5'] <1200:  #regain tx controller
        vehicle.channels.overrides['1'] = None
        vehicle.channels.overrides['2'] = None
        vehicle.channels.overrides['2'] = {}
        vehicle.channels.overrides['2'] = 0
        
        break
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
 
 
cv2.destroyAllWindows()
