import cv2 
import numpy as np 
from skimage import transform

direction = 'vertical' #vertical/horizontal
seams_per_iter = 1 #number of pixels to remove each iteration (lower is cleaner)


final_size = 0.5 #fraction of original image dimension to compress original into 

img = cv2.imread('castle_big.jpg')

#set scale factor 
if direction == 'vertical':
	scale = img.shape[1]
elif direction == 'horizontal':
	scale = img.shape[0]
scale = int(final_size*scale) #ratio to scale into 
print '%d pixels to remove at %d seams per iteration' % (scale, seams_per_iter) 

#compute energy map (Sobel gradient magnitude representation) on grayscale 
def create_energy_map(img):
	gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to gray scale 
	gray = cv2.GaussianBlur(gray,(3,3),0)
	sobel_x = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=5) #sobel X
	sobel_x = cv2.convertScaleAbs(sobel_x) #get 8bit abs value 
	sobel_y = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=5) #sobel Y
	sobel_y = cv2.convertScaleAbs(sobel_y)
	energy_map = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
	return energy_map
	
energy_map = create_energy_map(img)

cv2.imshow('original', energy_map)
cv2.waitKey(0)
cv2.DestroyAllWindows()

for num_seams in range(seams_per_iter, scale, seams_per_iter):
	carve = transform.seam_carve(img, energy_map, direction, seams_per_iter)
	img = (carve*255).astype(np.uint8) #recursively recalculate images, save time, cleaner cuts 
	energy_map = create_energy_map(img)
	
	print 'removing %d pixels' % (num_seams)
	num_seams_str = str(num_seams)
	
	title = 'carved'+num_seams_str + '.jpg'
	cv2.imwrite(title, (carve*255).astype(np.uint8)) #multiple to convert 0-1 to 0-255
	#cv2.imshow(title, carve) #for visualization 
	#cv2.waitKey(0)
print 'finished!'