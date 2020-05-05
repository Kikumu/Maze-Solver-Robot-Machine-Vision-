import time 
import cv2
from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
from picamera.array import PiRGBArray
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)  #easiest numbering 1,2,3,4...    
GPIO.setup(6,GPIO.OUT)  #adjust left
GPIO.setup(13,GPIO.OUT) #adjust right
GPIO.setup(26,GPIO.OUT) #forward
GPIO.setup(16,GPIO.OUT) #turn left completely
GPIO.setup(20,GPIO.OUT) #turn round signal
GPIO.setup(23,GPIO.OUT) #turn left
GPIO.setup(12,GPIO.IN)  #check if board has another "turning" task

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
    pixel1f5=mask[420,587]
    pixel1f6=mask[420,605]
    pixel2=mask[420,197]#287,420(left)
    pixel2f1=mask[420,167] #furtherleft
    pixel2f2=mask[420,137]#furthestleft
    pixel2f3=mask[420,107]#turn most left
    pixel2f4=mask[420,77]
    pixel2f5=mask[420,25]
    print("forward",pixelcnt)
    print("right",pixel1)
    print("right1",pixel1f1)
    print("right2",pixel1f2)
    print("most right",pixel1f4)
    print("left",pixel2)
    print("left1",pixel2f1)
    print("left2",pixel2f2)
    print("most left", pixel2f5)
    v = forward_signal(pixelcnt)#v1
    left_signal(pixel2,pixel2f1,pixel2f2,pixel2f3,pixel2f4)
    right_signal(pixel1,pixel1f5,pixel1f2,pixel1f4,pixel1f3)
    turn_signal = furthest_right_signal(pixel1f6) # 1 for i need to turn and zero for i dont need to turn
    turn_left_signal = furthest_left_signal(pixel2f5,turn_signal)
    print("turn left 90?", turn_left_signal)
    job_flag = GPIO.input(12) # 1 theres a job 0 theres no job
    print("job_flag",job_flag)
    trn = turn_around(pixelcnt,pixel1,pixel1f1,pixel1f2,pixel1f3,pixel1f4,pixel2,pixel2f1,pixel2f2,pixel2f3,pixel2f4,pixel2f5,turn_signal,job_flag)#only turn for when i dont need to turn and all sensors are dulled
    print("turn around?",trn)
    print("Right hand rule?",turn_signal)
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
    mask = cv2.circle(mask,(587,420),5,(100,50,255),0)#turn left dot
    mask = cv2.circle(mask,(605,420),5,(100,50,255),0)#turn left dot
    mask = cv2.circle(mask,(197,420),5,(100,50,255),0)#left dot
    mask = cv2.circle(mask,(167,420),5,(100,50,255),0)#further left  dot
    mask = cv2.circle(mask,(137,420),5,(100,50,255),0)#furthest left dot
    mask = cv2.circle(mask,(107,420),5,(100,50,255),0)#turn left dot
    mask = cv2.circle(mask,(77,420),5,(100,50,255),0)#turn left dot
    mask = cv2.circle(mask,(25,420),5,(100,50,255),0)#turn left dot
    return mask	   

def forward_signal(pixel_value):
    if pixel_value > 0:#(pixel intensity high)
        GPIO.output(20,0) #disable turn around
        v=1
        GPIO.output(26,1)#pin high
    elif pixel_value < 255:#(pixel intensity low)
        v=0
        GPIO.output(26,0)
    return v

def left_signal(pixel_value,pixel_value1,pixel_value2,pixel_value3,pixel_value4):
    if ((pixel_value > 0) or (pixel_value1 > 0) or (pixel_value2 > 0) or (pixel_value3 > 0) or (pixel_value4 > 0)):#(pixel intensity high)
        GPIO.output(20,0)#disable turn around
        GPIO.output(13,1)#pin high
        v=1
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(13,0)
        v=0
    return v

def right_signal(pixel_value,pixel_value1,pixel_value2,pixel_value3,pixel_value4):
    if ((pixel_value > 0) or (pixel_value1 > 0)or(pixel_value2 > 0)or(pixel_value3 > 0)or(pixel_value4 > 0)):#(pixel intensity high)
        GPIO.output(6,1)#pin high
        GPIO.output(20,0)#disable turn around
        v = 1
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(6,0)
        v = 0
    return v
		
def furthest_right_signal(pixel_value):
    if ((pixel_value > 0)):#(pixel intensity high)
        GPIO.output(16,1)#pin high
        print("furthest right high",1)
        v=1
        #time.sleep(0.5)
    elif pixel_value < 255:#(pixel intensity low)
        GPIO.output(16,0)
        print("furthest right low",0)
        v=0
    return v

def furthest_left_signal(pixel_data,right_status):
    if((pixel_data > 0) and (right_status==0)):
       GPIO.output(23,1)
       v = 1
    elif((pixel_data < 255) or (right_status==1)):
       GPIO.output(23,0)
       v = 0
    return v
        
def turn_around(one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,turn,job_flag):
    GPIO.output(20,0)
    v=0
    if (one==0 and two==0 and three==0 and four==0 and five==0 and six==0 and seven==0 and eight==0 and nine==0 and ten==0 and eleven == 0 and turn==0 and twelve == 0 and job_flag==0): #is okay...but...should give "space" for other function
        v=1
        GPIO.output(20,1)
    return v

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

