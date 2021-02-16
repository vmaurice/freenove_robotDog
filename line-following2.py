
from picamera.array import PiRGBArray
import time
import cv2
import picamera
import numpy as np
import math

# Initialize camera
camera = picamera.PiCamera()
camera.resolution = (500,300)
camera.framerate = 20
rawCapture = PiRGBArray(camera,size=(500,300))
time.sleep(0.1)

theta=0
minLineLength = 5
maxLineGap = 10

# Loop over all frames captured by camera indefinitely
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    # Display camera input
    image = frame.array

    # Create key to break for loop
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1)
        edged = cv2.Canny(blurred, 100, 140)

        #cv2.imshow("Frame",edged)

        lines = cv2.HoughLinesP(edged,1,np.pi/180,10,minLineLength,maxLineGap)
        
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
                theta=theta+math.atan2((y2-y1),(x2-x1))
                print(theta)
        
        threshold=6
        if(theta>threshold):
            print("right")
        if(theta<-threshold):
            print("left")
        if(abs(theta)<threshold):
            print("straight")

        theta=0
        

        cv2.imshow("Frame",image)

        
    except:
        pass

    rawCapture.truncate(0)
    

	
