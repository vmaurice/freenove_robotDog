
from picamera.array import PiRGBArray
import time
import cv2
import picamera
import numpy as np

# Initialize camera
camera = picamera.PiCamera()
camera.resolution = (160,120)
camera.framerate = 20
rawCapture = PiRGBArray(camera,size=(160,120))
time.sleep(0.1)

# Loop over all frames captured by camera indefinitely
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

	# Display camera input
	image = frame.array
	

	# Create key to break for loop
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break

	try:

		# convert to grayscale, gaussian blur, and threshold
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		#cv2.imshow('img',gray)

		blur = cv2.GaussianBlur(gray,(15,15),0)

		#cv2.imshow('img',blur)

		ret,thresh1 = cv2.threshold(blur,100,150,cv2.THRESH_BINARY)

		# Erode to eliminate noise, Dilate to restore eroded parts of image
		mask = cv2.erode(thresh1, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		# Find all contours in frame
		something, contours, hierarchy = cv2.findContours(mask.copy(),1,cv2.CHAIN_APPROX_NONE)

		# Find x-axis centroid of largest contour and cut power to appropriate motor
		# to recenter camera on centroid.
		# This control algorithm was written referencing guide:
			# Author: Einsteinium Studios
			# Availability: http://einsteiniumstudios.com/beaglebone-opencv-line-following-robot.html
		if len(contours) > 0:
			# Find largest contour area and image moments
			c = max(contours, key = cv2.contourArea)
			M = cv2.moments(c)

			# Find x-axis centroid using image moments
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])

			if cx >= 120:
				print ("Turn Right")

			if cx < 120 and cx > 50:
				print ("ForWard")

			elif cx <= 50:
				print ("Turn Left")

			cv2.line(image,(cx,0),(cx,120),(255,0,0),1)
			cv2.line(image,(0,cy),(160,cy),(255,0,0),1)


			cv2.drawContours(image, contours, -1, (0,255,0), 1)

		cv2.imshow('img',image)
	
		rawCapture.truncate(0)
	except :
		pass

	
