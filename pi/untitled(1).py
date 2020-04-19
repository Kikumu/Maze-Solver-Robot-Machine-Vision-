import time 
import cv2
from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM) #easiest numbering 1,2,3,4...    
GPIO.setup(16,GPIO.OUT) #adjust left
GPIO.setup(20,GPIO.OUT) #adjust right
GPIO.setup(26,GPIO.OUT) #forward


#line midpoint
def acquire_midpoint(var1,var2,var3,var4):
	x = ((var1 + var3)/2)
	y = ((var2 + var4)/2)
	return x,y

#line gradient
def acquire_slope(var1,var2,var3,var4):
	grad = (var2-var4)/(var1 - var3)
	return grad
	
def hsv_color_space(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L-H","Trackbar")
    l_s = cv2.getTrackbarPos("L-S","Trackbar")
    l_v = cv2.getTrackbarPos("L-V","Trackbar")
    u_h = cv2.getTrackbarPos("U-H","Trackbar")
    u_s = cv2.getTrackbarPos("U-S","Trackbar")
    u_v = cv2.getTrackbarPos("U-V","Trackbar")
    lower_red = np.array([l_h,l_s,l_v])
    upper_red = np.array([u_h,u_s,u_v])
    mask = cv2.inRange(hsv,lower_red,upper_red)
    kernel = np.ones((10,10),np.uint8)
    mask = cv2.erode(mask,kernel)
    #contours
    A,contours,C = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #image = draw_lines(image,scrn_x,scrn_y)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt,True),True)
        if area > 400:
          cv2.drawContours(image,[approx],0,(0,0,0),5)
            #scene/"shape" detector
          if(len(approx)==4):
            cv2.putText(image, "rectangle",(10,10),font,1,(0,0,0))
          elif(len(approx)==3):
            cv2.putText(image, "triangle",(10,10),font,1,(0,0,0))
          elif(len(approx)==10):
            cv2.putText(image, "10sides",(10,10),font,1,(0,0,0))
          elif(len(approx)==5):
            cv2.putText(image, "5sides",(10,10),font,1,(0,0,0))
          elif(len(approx)==7):
            cv2.putText(image, "7sven",(10,10),font,1,(0,0,0))
          elif(len(approx)==8):
            cv2.putText(image, "ate",(10,10),font,1,(0,0,0))
    return image,mask
	

def region_of_interest(width,height):
    vertices = [(0,height),(0,300),(width/2,300),(width,300),(width,height)]
    return vertices
    
def ROI_mask(image,vertices):
    mask = np.zeros_like(image)
    channel_count = image.shape[2]
    match_mask = (255,)*channel_count
    cv2.fillPoly(mask,vertices,match_mask)
    masked_img = cv2.bitwise_and(image,mask)
    return masked_img
    
def draw_lines(img,mid_x,mid_y):
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    hsv =cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #cv2.imshow("hsv",hsv)
    #cv2.waitKey()
    low_yellow = np.array([148,88,0])
    up_yellow = np.array([163,119,225])
    mask = cv2.inRange(hsv,low_yellow,up_yellow)
    kernel = np.ones((10,10),np.uint8)
    mask = cv2.erode(mask,kernel)
    cv2.imshow("mask1",mask)
    #cv2.waitKey()
    edges = cv2.Canny(mask,threshold1=200,threshold2=300)
    #cv2.imshow("edges",edges)
    #cv2.waitKey()
    lines = cv2.HoughLinesP(edges,1,np.pi/180,20,maxLineGap=50)
    #cv2.imshow("lines",lines)
    #cv2.waitKey()
    img = cv2.circle(img,(mid_x,mid_y),10,(0,0,0),-1) #draws circle in the middle(used to steer)
    if lines is None:
      GPIO.output(26,0)
    if lines  is not None:
      forward()
      steer_switch = 0 #controls adjustment
      print("forward")
      for line in lines:
        coord = line[0]   #grab line
        cv2.line(img,(coord[0],coord[1]),(coord[2],coord[3]),(255,0,255),2)
        p1,p2 = acquire_midpoint(coord[0],coord[1],coord[2],coord[3]) #obtain midpoint
        gradient = acquire_slope(coord[0],coord[1],coord[2],coord[3]) #obtain gradient
        #print("Gradient", gradient)
        if(gradient > 0):
            if(p2 < 350 and p1 > 320):
               img = cv2.circle(img,(int(p1),int(p2)),10,(0,255,0),-1)
               mid_dist = p1-mid_x
               print("Green dist: ",mid_dist)
               if(mid_dist < 250):
                   print("adjust right")
                   adjust_right()
                   #forward()
        elif(gradient < 0):
            if(p2 < 350 and p1 < 320):
               img = cv2.circle(img,(int(p1),int(p2)),10,(255,255,255),-1)
               mid_dist1 = mid_x-p1
               print("White dist",mid_dist1)# positive values
#------------------------------------STEERING SYSTEM--------------------------------------------------------------##
               if(mid_dist1<220):
                   print("adjust left",mid_dist1)
                   adjust_left()
                   #forward()
    return img
#-------------------------------------------------------------------------------------------------------------------##
#------------------------------------STEERING CONTROL SKELETON------------------------------------------------------##
#everything will be initially set to low at the start of the loop
def nothing(X):
    pass

def adjust_left():
    GPIO.output(16,1) #set pin to high

def stop_adjusting_left():
    GPIO.output(16,0)
def stop_adjusting_right():
    GPIO.output(20,0) 
    
def adjust_right():
    GPIO.output(20,1) #set pin to high
    
def steer_left_by_45():
    pass
    
def forward():
    GPIO.output(26,1)
    
def turn_round_360():
    pass
    
#--------------------------------------------------------------------------------------------------------------------##
#--------------------------------------------template setup and trackbar---------------------------------------------##
camera = PiCamera()
camera.resolution = (640,480)
camera.vflip = True
camera.framerate = 20
rawCapture = PiRGBArray(camera, size = (640,480))
time.sleep(0.1)
scrn_x = int(640*0.5)                         #set x position of centre dot
scrn_y = int((480*0.5) + 100)                 #set y position of centre dot
cv2.namedWindow("Trackbar")
cv2.createTrackbar("L-H","Trackbar",0,180, nothing)
cv2.createTrackbar("L-S","Trackbar",80,255, nothing)
cv2.createTrackbar("L-V","Trackbar",129,180, nothing)
cv2.createTrackbar("U-H","Trackbar",180,180, nothing)
cv2.createTrackbar("U-S","Trackbar",255,255, nothing)
cv2.createTrackbar("U-V","Trackbar",240,255, nothing)
font = cv2.FONT_HERSHEY_COMPLEX
#-------------------------------------------------------------------------------------------------------#
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    GPIO.output(16,0)
    GPIO.output(20,0)
    GPIO.output(26,0)
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    #---------------------------------LINES----------------------------------------------------------------------
    vertices = region_of_interest(640,480) # create roi skeleton
    cropped = ROI_mask(image,np.array([vertices],np.int32),) #create cropped image usiing roi
    cropped = draw_lines(cropped,scrn_x,scrn_y) #draw lines on cropped image and pass as new image to display
    #---------------------------------SHAPE-----------------------------------------------------------------------
    image,mask = hsv_color_space(image) # shape
    cv2.imshow("Frame", cropped)
    cv2.imshow("Mask",mask)
    key = cv2.waitKey(1)&0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        GPIO.output(16,0)
        GPIO.output(20,0)
        #GPIO.output(21,0)
        GPIO.cleanup()
        break

