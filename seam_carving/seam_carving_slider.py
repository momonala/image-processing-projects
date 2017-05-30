import cv2 
import numpy as np 
from skimage import transform
#from skimage import filters
#en_map = filters.sobel(gray.astype('float'))
#en_map = filters.scharr_h(gray.astype('float'))
#en_map = cv2.Laplacian(gray,cv2.CV_64F)

img = cv2.imread('castle_big.jpg')
direction = 'v' #vertical/horizontal

reso = img.shape #vert, horiz
#reso = [1920, 1080] #max resolution, fit image to screen 
reso = [int(x*.5) for x in reso] #reduce size by some fraction 
img = cv2.resize(img, (reso[1], reso[0]))
	
#compute energy map (Sobel gradient magnitude representation) on grayscale 
def create_energy_map(img):
	gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to gray scale 
	gray = cv2.GaussianBlur(gray,(3,3),0)
	sobel_x = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5) #sobel X
	sobel_x = cv2.convertScaleAbs(sobel_x) #get 8bit abs value 
	sobel_y = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5) #sobel Y
	sobel_y = cv2.convertScaleAbs(sobel_y)
	en_map = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
	return en_map
	
en_map = create_energy_map(img)	
cv2.imshow('energy map', en_map) 
cv2.waitKey(0)	

#set scale factor
if direction == 'v':	
	direction = 'vertical'
	max_dim = img.shape[1] #maximum size of image 	
elif direction == 'h':
	direction = 'horizontal'
	max_dim = img.shape[0]
	
def nothing(x):
	pass
cv2.namedWindow('slider') #Make the trackbar, # seams to remove 
cv2.createTrackbar('c','slider',0,100,nothing)

while True:
	scale = cv2.getTrackbarPos('c', 'slider')
	scale = float(scale/100.0) 
	pixels_to_rm = int(scale*max_dim) #number of seams to remove 
	
	carve = transform.seam_carve(img, en_map, direction, pixels_to_rm)
	
	cv2.imshow('carved', carve)
	if cv2.waitKey(1) & 0xFF == ord('q'): #quit	
		break 
