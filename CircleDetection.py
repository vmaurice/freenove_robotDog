import socket
import threading
import time
from picamera import PiCamera
import cv2 as cv2
import numpy as np


lienImage='/home/pi/Pictures/image2.jpg'
class CircleDetection:
    
    def __init__(self):
        self.camera = PiCamera()
        self.camera.start_preview()
        time.sleep(2)
    
    def Looking_for_the_ball(self,image):
        THRESHOLD_LOW = (0, 80, 80)
        THRESHOLD_HIGH = (5,255,255)

        output=image.copy()
        #print(output)
        img_filter = cv2.GaussianBlur(image.copy(), (3, 3), 0)
        img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2HSV)
        img_binary = cv2.inRange(img_filter.copy(), THRESHOLD_LOW, THRESHOLD_HIGH)

        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_binary = cv2.bilateralFilter(img_binary, 11, 17, 17)
        edged = cv2.Canny(img_binary, 30, 200)
        edged = cv2.dilate(edged, None, iterations = 1)
        edged = cv2.erode(edged, None, iterations = 1)
        
        #cv2.imshow('edged', edged)
        #cv2.waitKey(0)
        '''
        circles = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1.3, 2000,param1=1,param2=40,minRadius=0,maxRadius=0)
        # ensure at least some circles were found
        print(circles)
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                print(output[x, y])
            # show the output image
            cv2.imshow("output", output)
            cv2.waitKey(0)
            return True
        return False
        '''
        _,contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contour_list = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
            area = cv2.contourArea(contour)
            #k=cv2.isContourConvex(approx)
            #print(k)
            if ((len(approx) >= 8) & (len(approx) < 23) & (area > 30)):
                contour_list.append(contour)
        blank_image = np.zeros(edged.shape, np.uint8)
        
        cv2.drawContours(blank_image, contour_list,  -1, (255,0,0), 2)
        #cv2.imshow('Objects Detected',blank_image)
        #cv2.waitKey(0)
        
        circles = cv2.HoughCircles(blank_image, cv2.HOUGH_GRADIENT, 1.4, 2000,param1=1,param2=50,minRadius=0,maxRadius=0)
        # ensure at least some circles were found
        print(circles)
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            # show the output image
            #cv2.imshow("output", output)
            #cv2.waitKey(0)
            cv2.imwrite("output.jpg", output)
            return True
        return False
        
    def takePict(self):
        my_file = open(lienImage, 'wb')
        self.camera.capture(my_file)
        my_file.close()
        #print("image")

    def findBall(self):
        self.takePict()
        img = cv2.imread(lienImage)
        return self.Looking_for_the_ball(img)

if __name__ == "__main__":
    a = CircleDetection()
    a.findBall()
    #while not a.findBall():
    #    print("no")
