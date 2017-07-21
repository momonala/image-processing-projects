import cv2
import numpy as np

def nothing(x):
	pass
desktop = (1920, 1080) #max resolution
orig = cv2.imread('blackmarble_8mb.jpg') #blackmarble_8mb.jpg
#resized = orig.copy()
resized = cv2.resize(orig, (desktop[0],
							desktop[1]))
cv2.namedWindow('slider') #Make the trackbar used for HSV masking 
cv2.createTrackbar('hue_up','slider',180,180,nothing)
cv2.createTrackbar('hue_low','slider',0,180,nothing)
cv2.createTrackbar('sat_up','slider',255,255,nothing)
cv2.createTrackbar('sat_low','slider',0,255,nothing)
cv2.createTrackbar('bright_up','slider',255,255,nothing)
cv2.createTrackbar('bright_low','slider',0,255,nothing)

while True: 
	hue_low = cv2.getTrackbarPos('hue_low', 'slider') 	
	hue_up = cv2.getTrackbarPos('hue_up', 'slider')
	sat_low = cv2.getTrackbarPos('sat_low', 'slider') 	
	sat_up = cv2.getTrackbarPos('sat_up', 'slider')
	bright_low = cv2.getTrackbarPos('bright_low', 'slider') 	
	bright_up = cv2.getTrackbarPos('bright_up', 'slider')
	lower = np.array([hue_low, sat_low, bright_low])
	upper = np.array([hue_up, sat_up, bright_up])

	mask = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV) #convert to hsv
	mask = cv2.inRange(mask, lower, upper) #threshold 
	overlay = cv2.bitwise_and(resized, resized, mask=mask) #replace dark pixels
	#hsv = cv2.bitwise_and(hsv, hsv, mask=mask) 
	
	cv2.imshow('black_marble', overlay)
	cv2.imshow('mask', mask)
	
	 
	if cv2.waitKey(1) & 0xFF == ord('q'): #quit	
		break 
		
mask = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV) #convert to hsv
mask = cv2.inRange(mask, lower, upper) #last recorded 
overlay = cv2.bitwise_and(orig, orig, mask=mask) 
cv2.imwrite('processed.jpg', overlay)
cv2.destroyAllWindows()