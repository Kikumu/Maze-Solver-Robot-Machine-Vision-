import time 
import cv2
from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #easiest numbering 1,2,3,4...    
GPIO.setup(6,GPIO.OUT) #adjust left
GPIO.setup(13,GPIO.OUT) #adjust right
GPIO.setup(26,GPIO.OUT) #forward

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
    return image,mask
	
def shape_detector(image,mask):
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel)
    #contours
    A,contours,C = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
    
#-------------------------------------------------------------------------------------------------------------------##
#------------------------------------STEERING CONTROL SKELETON------------------------------------------------------##
#everything will be initially set to low at the start of the loop
def nothing(X):
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
scrn_y = int((480*0.5) + 200)                 #set y position of centre dot
left_adjust_dot = scrn_x + 30
print("y pos", scrn_y) #440
print("x pos", scrn_x) #320
cv2.namedWindow("Trackbar")
cv2.createTrackbar("L-H","Trackbar",0,180, nothing)
cv2.createTrackbar("L-S","Trackbar",145,255, nothing)
cv2.createTrackbar("L-V","Trackbar",74,180, nothing)
cv2.createTrackbar("U-H","Trackbar",180,180, nothing)
cv2.createTrackbar("U-S","Trackbar",255,255, nothing)
cv2.createTrackbar("U-V","Trackbar",255,255, nothing)
font = cv2.FONT_HERSHEY_COMPLEX
#low_yellow = np.array([0,68,154])
 #   up_yellow = np.array([180,255,243])

def sensor_calib(mask):
    pixelcnt= mask[420,320] #420
    pixel1=mask[420,438]#right
    pixel1f1=mask[420,468]#further right
    pixel1f2=mask[420,490]#furthest right
    pixel1f3=mask[420,520]#turn most right
    pixel1f4=mask[420,550]
    pixel2=mask[420,197]#287,420(left)
    pixel2f1=mask[420,167] #furtherleft
    pixel2f2=mask[420,137]#furthestleft
    pixel2f3=mask[420,107]#turn most left
    pixel2f4=mask[420,77]
    print("forward",pixelcnt)
    print("right",pixel1)
    print("right1",pixel1f1)
    print("right2",pixel1f2)
    print("left",pixel2)
    print("left1",pixel2f1)
    print("left2",pixel2f2)
    v = forward_signal(pixelcnt)
    left_signal(pixel2)
    right_signal(pixel1)
    print("pin state",v)
    if pixelcnt > 0:
       print("move forward")
    elif pixelcnt < 255:
       print("stop moving forward")
    if pixel1 > 0:
       print("tweak left")
    elif pixel1 < 255:
       print("stop tweaking left")
    #draw circles(after pixel detection)
    mask = cv2.circle(mask,(320,420),5,(255,255,255),0)#forward dot
    mask = cv2.circle(mask,(438,420),5,(100,50,255),0)#right dot
    mask = cv2.circle(mask,(468,420),5,(100,50,255),0)#further right dot
    mask = cv2.circle(mask,(490,420),5,(100,50,255),0)#farthest right dot
    mask = cv2.circle(mask,(520,420),5,(100,50,255),0)#furthest left dot
    mask = cv2.circle(mask,(550,420),5,(100,50,255),0)#turn left dot
    mask = cv2.circle(mask,(197,420),5,(100,50,255),0)#left dot
    mask = cv2.circle(mask,(167,420),5,(100,50,255),0)#further left  dot
    mask = cv2.circle(mask,(137,420),5,(100,50,255),0)#furthest left dot
    mask = cv2.circle(mask,(107,420),5,(100,50,255),0)#turn left dot
    mask = cv2.circle(mask,(77,420),5,(100,50,255),0)#turn left dot
    return mask	   

def forward_signal(pixel_value):
    if pixel_value > 0:#(pixel intensity high)
        v=1
        GPIO.output(26,1)#pin high
    elif pixel_value < 255:#(pixel intensity low)
        v=0
        GPIO.output(26,0)
    return v

def left_signal(pixel_value):
    if pixel_value > 0:#(pixel intensity high)
        GPIO.output(13,1)#pin high
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(13,0)
		
def further_left_signal(pixel_value):
    if pixel_value > 0:#(pixel intensity high)
        GPIO.output(26,1)#pin high
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(26,0)
		
def farthest_left_signal(pixel_value):
    if pixel_value > 0:#(pixel intensity high)
        GPIO.output(26,1)#pin high
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(26,0)

def right_signal(pixel_value):
    if pixel_value > 0:#(pixel intensity high)
        GPIO.output(6,1)#pin high
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(6,0)
		
def further_right_signal(pixel_value):
    if pixel_value > 0:#(pixel intensity high)
        GPIO.output(26,1)#pin high
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(26,0)
		
def furthest_right_signal(pixel_value):
    if pixel_value > 0:#(pixel intensity high)
        GPIO.output(26,1)#pin high
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(26,0)
		

#-------------------------------------------------------------------------------------------------------#
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    #---------------------------------LINES----------------------------------------------------------------------
    #---------------------------------SHAPE-----------------------------------------------------------------------
    image,mask = hsv_color_space(image) # shape
    #cv2.imshow("Frame", image)
    mask = sensor_calib(mask)
    cv2.imshow("Mask",mask)
    key = cv2.waitKey(1)&0xFF
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        GPIO.cleanup()
        break

