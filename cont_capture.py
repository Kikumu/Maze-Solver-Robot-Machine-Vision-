import picamera
from picamera.array import PiRGBArray
import time
import cv2
import numpy as np

#camera =picamera.PiCamera()
#camera.resolution = (640,480)
#camera.framerate = 20
#raw_capture = PiRGBArray(camera,size=(640,480))
#time.sleep(1)

#line midpoint
def acquire_midpoint(var1,var2,var3,var4):
	x = ((var1 + var3)/2)
	y = ((var2 + var4)/2)
	return x,y

#line gradient
def acquire_slope(var1,var2,var3,var4):
	grad = (var2-var4)/(var1 - var3)
	return grad
	
#remember has to be in the form of a numpy array
def vct_sub(a,b):
	val=b-a
	return val
	
#remember has to be in the form of a numpy array
def cross_vct(a,b):
	res = np.cross(a, b)
	magnitude = res[0]**2 + res[1]**2 + res[2]**2
	return res,magnitude
	

#bulk of math done here
#might not be using this anymore
def  distance_between_skew_lines(var1,var2,var3,var4,var5,var6,var7,var8):
	v1 = np.array([var1,var2,0])
	v2 = np.array([var3,var4,0])
	v3 = np.array([var5,var6,0])
	v4 = np.array([var7,var8,0])
	sub_res1 = vct_sub(v1,v2)
	sub_res2 = vct_sub(v3,v4)
	crs_product,magnitude = cross_vct(sub_res1,sub_res2)
	a = sub_res1[0]
	b = sub_res2[0]
	c = crs_product[0]
	d = sub_res1[1]
	e = sub_res2[1]
	f = crs_product[1]
	g = sub_res1[2]
	h = sub_res2[2]
	i = crs_product[2]
	a = np.array([[a,-b,-c],[d,-e,-f],[g,-h,-i]])
	b = np.array([(var5-var1),(var6-var2),(-0 + 0)])
	coeff_array = np.linalg.solve(a,b)
	constant = coeff_array[2]
	resultant = constant*magnitude
	#d_1  = k(magnitude)
	return resultant
	
def subtract_x_axis(var2,var4,var):
	result = var4-var2
	return result,var
	

def longest_line(var1,var2,var3,var4):
	line_length =  ((var1 - var3)**2 + (var2 - var4)**2)**1/2
	return line_length
	
def draw_lines(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,threshold1=175,threshold2=315)
	lines = cv2.HoughLinesP(edges,1,np.pi/180,180,np.array([]),100,15)
	count = 1
	#last = lines[-1]
	#first = lines[0]
	for line in lines:
		coord = line[0] 
		#print(coord)  
		cv2.line(img,(coord[0],coord[1]),(coord[2],coord[3]),(255,0,255),2)
		p1,p2 = acquire_midpoint(coord[0],coord[1],coord[2],coord[3])
		gradient = acquire_slope(coord[0],coord[1],coord[2],coord[3])
		dist = longest_line(coord[0],coord[1],coord[2],coord[3])
		init_midpoint = 0
		save_x_axes = []
		if(count < len(lines)):
			line2 = lines[count]
			coord2 = line2[0]
			gradient2 = acquire_slope(coord2[0],coord2[1],coord2[2],coord2[3])
			
			if(gradient==1 and gradient2 ==-2):
				x_axis,y_axis = subtract_x_axis(coord2[0],coord[0],coord[1])
				save_x_axes.append([x_axis])
				max_x = np.amax(save_x_axes)
				#img = cv2.circle(img,(x_axis,y_axis),10,(255,0,0),-3)
				init_midpoint+1
			#res =distance_between_skew_lines(coord[0],coord[1],coord[2],coord[3],coord2[0],coord[1],coord2[2],coord2[3])
			#print(coord2,"nxt")
		
		#print out midpoint
		if(count == len(lines)):
			img = cv2.circle(img,(max_x,y_axis),10,(255,0,0),-3)
			
		#print out midpoints depending on gradient
		if(gradient == 1):
			img = cv2.circle(img,(p1,p2),10,(0,255,0),-1)
			#print(coord,"right")
		elif(gradient == -2):
			img = cv2.circle(img,(p1,p2),10,(255,255,255),-1)
			#print(coord,"lft")
			#print(coord[0],coord[1],coord[2],coord[3])
		#elif(gradient == -1):
			#img = cv2.circle(img,(p1,p2),10,(0,255,255),-1)
		#elif(gradient == 0):
			#img = cv2.circle(img,(p1,p2),10,(255,255,255),-1)
		else:
			print(gradient)
		count=count+1	
	return img

	
img = cv2.imread('/home/pi/Downloads/tiles.jpg')
img1 = draw_lines(img)
scale_percent = 50 # percent of original size
width = int(img1.shape[1] * scale_percent / 100)
height = int(img1.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
 
print('Resized Dimensions : ',resized.shape)
 
cv2.imshow("Resized image", resized)
#cv2.imshow("Frame", img1)
cv2.waitKey()
#print(cnt)


#for frame in camera.capture_continuous(raw_capture,format="bgr",use_video_port=True):
#	image = frame.array
#	#image = draw_lines(image)
#	cv2.imshow("Frame", image)
#	key = cv2.waitKey(1)&0xFF
#	raw_capture.truncate(0)
#	if key == ord("q"):
#		break

