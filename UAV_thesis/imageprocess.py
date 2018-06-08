from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
 
kernel = np.ones((5,5),np.uint8)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.rotation = 180
camera.brightness = 55
camera.resolution = (320, 240)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(320, 240))

time.sleep(1)

 
# Take input from webcam
 
# Reduce the size of video to 320x240 so rpi can process faster
#cap.set(3,320)
#cap.set(4,240)
 
def nothing(x):
    pass
# Creating a windows for later use
cv2.namedWindow('HueComp')
##cv2.namedWindow('SatComp')
##cv2.namedWindow('ValComp')
##cv2.namedWindow('closing')
##cv2.namedWindow('tracking')
## 
 
# Creating track bar for min and max for hue, saturation and value
# You can adjust the defaults as you like
cv2.createTrackbar('hmin', 'HueComp',0,180,nothing)
cv2.createTrackbar('hmax', 'HueComp',0,180,nothing)
## 
##cv2.createTrackbar('smin', 'SatComp',0,255,nothing)
##cv2.createTrackbar('smax', 'SatComp',0,255,nothing)
## 
##cv2.createTrackbar('vmin', 'ValComp',0,255,nothing)
##cv2.createTrackbar('vmax', 'ValComp',0,255,nothing)
 

 
for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
     
    frame = image.array
  
    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hue,sat,val = cv2.split(hsv)
 
    # get info from track bar and appy to result
    hmn = cv2.getTrackbarPos('hmin','HueComp')
    hmx = cv2.getTrackbarPos('hmax','HueComp')
##   
## 
##    smn = cv2.getTrackbarPos('smin','SatComp')
##    smx = cv2.getTrackbarPos('smax','SatComp')
## 
## 
##    vmn = cv2.getTrackbarPos('vmin','ValComp')
##    vmx = cv2.getTrackbarPos('vmax','ValComp')
##    hmn=118
##    hmx=180
    smn=110
    smx=255
    vmn=0
    vmx=255
## 
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

    #if  max_area>15000 and max_area<200000:
    if max_area>0:
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        print(cx,cy)
        print(max_area)
        cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
    else:
        cx = 159
        cy = 119
    
    
 
   
    #Show the result in frames
    cv2.imshow('HueComp',hthresh)
##    cv2.imshow('SatComp',sthresh)
##    cv2.imshow('ValComp',vthresh)               
##    #cv2.imshow('closing',closing)
    cv2.imshow('tracking',frame)

    rawCapture.truncate(0)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
 
cap.release()
cv2.destroyAllWindows()
