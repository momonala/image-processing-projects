import cv2
import numpy as np  
import os 

font = cv2.FONT_HERSHEY_SIMPLEX

def show_img(im): 	
	im = cv2.resize(im, (im.shape[1]/2,im.shape[0]/2))
	cv2.imshow("Input", im)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def crop_sides_agar(im):
	#mask to cover the edges of the agar plate 
	mask = np.zeros(im.shape, dtype=np.uint8)
	roi_corners = np.array([[(165, 100),
							(1300, 100),
							(1395, 198),
							(1395, 1938),
							(1308, 2025),
							(165, 2025),]], dtype=np.int32)
	cv2.fillPoly(mask, roi_corners, 255) #cv2.fillConvexPoly
	im = cv2.bitwise_and(im, mask) #apply mask 
	return im 

def crop_sides_clean(im):
	#mask to cover hot pixels we get from adaptive thresholding 
	mask = np.zeros(im.shape, dtype=np.uint8)
	roi_corners = np.array([[(177, 120),
							(1300, 120),
							(1380, 210),
							(1380, 1923),
							(1281, 2010),
							(177, 2010),]], dtype=np.int32)
	cv2.fillPoly(mask, roi_corners, 255) #cv2.fillConvexPoly
	im = cv2.bitwise_and(im, mask) #apply mask 
	return im 
	
def boost_contrast(im):
	im*=3 #brighten 
	im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR) #convert it to bgr so that we can: 
	hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV) #convert it to hsv
	h, s, 	v = cv2.split(hsv)
	v+=250 #boost contrast w/ 'value' param	
	im = cv2.merge((h, s, v)) 
	im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR) #convert it to bgr
	im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #convert it to hsv
	return im 
	

def point_in_circle(x_point, y_point, x_circle, y_circle, radius_circle):
	#check to see if point is in circle 
	return (x_point-x_circle)**2 + (y_point-y_circle)**2 < radius_circle**2

def distance(x1, y1, x2, y2):
	#distance formula for cell separation 
	return np.sqrt((x2-x1)**2 + (y2-y1)**2)

############################## Pipeline ###############################################
#arg = name of image to process in same dir as .py file 

def pipeline(img_file):
	print img_file
	
	##### Read Values from File #####
	params = open('params.txt', 'r')
	for line in params:
		line = line.split('\n')[0]	
		line = line.split('=')
		param, value = line[0], line[1] 
		if 'MIN_RADIUS' in param:
			min_radius = int(value)
		elif 'MAX_RADIUS' in param: 
			max_radius = int(value)
		elif 'MIN_SEPARATION ' in param:
			min_sep = float(value)
		elif 'CELL_TYPE' in param: 
			cell_type = value
		elif 'RADIUS_WEIGHT' in param: 
			rad_weight = float(value)
		elif 'SEPARATION_WEIGHT' in param: 
			sep_weight = float(value)
		elif 'CELLS_TO_PICK' in param: 
			cells_to_pick = int(value)

	##### Setup #####
	raw_img = cv2.imread(img_file, 0) #grayscale img to count cells from 
	blank = cv2.imread('blank_tray_wdivets.TIF', 0) #control to subtract out
	
	color_img = raw_img.copy()
	color_img = crop_sides_clean(crop_sides_agar(color_img))
	color_img = cv2.cvtColor(color_img, cv2.COLOR_GRAY2BGR) #color for output 

	img = cv2.medianBlur(raw_img, 5) #denoise
	blank = cv2.medianBlur(blank, 5) #denoise
	img = cv2.absdiff(crop_sides_agar(blank), crop_sides_agar(img)) #subtract out blank 
	#show_img(img)

	### Image processing ###
	boost_contrast(img)
	img = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,-1)
	img = cv2.medianBlur(img, 9) #denoise
	img = 255-img	#invert
	img = crop_sides_clean(img)
	
	img = cv2.resize(img, (img.shape[1]*2,img.shape[0]*2)) #increase size helps counting 
	
	circles = cv2.HoughCircles(img, 
								cv2.HOUGH_GRADIENT, #detection method
								dp=1, #inverse ratio of resolution
								minDist=min_sep, #minimum distance between centers
								param1=50, #upper threshold for edge detector 
								param2=2, # threshold for center detection 
								minRadius=0, 
								maxRadius=max_radius)
	
	#revert size back to normal 
	img = cv2.resize(img, (img.shape[1]/2,img.shape[0]/2))
	thresh_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

	if circles is None: 
		print "no circles found"
	
	else:
		
		circles /= 2 #resize 
		circles = np.uint16(np.around(circles))  
		circles = circles[0, :, : ] #formatting 

		def get_pixel(a):
			y, x = a[0], a[1] #location of circle's center 
			return img[x, y] #corresponding pixel value 
		
		#remove found circles that are not on top of cells 
		pix_val = np.apply_along_axis(get_pixel, 1, circles) #apply to all 
		pix_val = pix_val.reshape(pix_val.shape[0], 1)
		circles = np.hstack((circles, pix_val)) #combine with centers array	
		circles = circles[circles[:,3]==255, :] #only keep circles with a cell under it ] 
		cell_counts = circles.shape[0]
		
		#for i in circles[0:]: #draw circles 
		#	cv2.circle(color_img,(i[0],i[1]),i[2],(0,255,0),20) #outer
		#	cv2.circle(color_img,(i[0],i[1]),2,(0,0,255),9) #center 
		#	cv2.circle(thresh_img,(i[0],i[1]),2,(0,0,255),9) #center 
		
		'''
		detect well plates 		
		spacing between plates is ~153 pixels in either direction 
		1st plate initialzied at (235, 242) in original raw image (manually determined)
		'''
		grid = np.indices((8,12)) #grid representing the 8x12 wells in plate
		grid[0] = ((grid[0]*153)+235) #calc corect well plate location, teach points  
		grid[1] = ((grid[1]*153)+242)

		well_radius = 69
		well_num = 1 #init 
		wells = np.array([0,0,0,0]) #init 
		well_labels = {}  #map 1-96 to a1-h12

		#iterate through grid to identify and number the 96 wells 
		for cols in range(grid.shape[1]):
			letter = (chr(ord('a')+cols)) #iterate a-h
			well_cols = grid[:, cols]
			for rows in range(well_cols.shape[1]):
				well_x, well_y = tuple(well_cols[:,rows])
				cv2.circle(thresh_img,(well_x, well_y),well_radius,(240,0,240),2) #center	
				cv2.circle(color_img,(well_x, well_y),well_radius,(240,0,240),2) #center	
				wells_temp  = np.array([well_x, well_y, well_radius, well_num]) #array of wells
				wells = np.vstack((wells, wells_temp))
				
				well_label = letter+str(12-rows) #for mapping 
				well_labels[str(well_num)] = well_label
				#cv2.putText(color_img,well_label, (well_x, well_y), font, 2, (0,255,0), 2)
				
				well_num += 1
				
		wells = wells[0:] #get rid of first row from init 
		circles = np.hstack((circles, np.zeros((cell_counts, 1)))).astype(int) #add plate# to cells array 

		#iterate through the identified cells to see which well they reside in
		for i, cell in enumerate(circles): 
			x_cell, y_cell, rad, pix, _ = tuple(cell)
			for well in wells:
				well_x, well_y, well_radius, well_num = tuple(well)
				
				#check if cell lies in circle 
				if point_in_circle(x_cell, y_cell, well_x, well_y, well_radius)== True: 
					circles[i, -1] = well_num
					break
		
		circles = circles[circles[:,-1]>0, :] #get rid of cells which werent in wells 
		circles = circles[np.argsort(circles[:,-1])] #sort by well plate 		
		
		def get_dist(a):
			#used with .apply_along_axis func to get distances of all cells within plate 
			other_x, other_y = a[0], a[1] 
			return distance(cell_x, celly, other_x, other_y)

		cell_distances = []
		for plate_count in range(96):	
			plate = circles[circles[:,-1]==(plate_count+1), :] #grab cells per active plate 
			for cell in plate:
				cell_x, celly = cell[0], cell[1] #active cell 
				#get distances of all nonactive cells on plate 
				dist = np.apply_along_axis(get_dist, 1, plate)
				if dist.shape[0] > 1: 
					cell_distances.append(sorted(dist)[1])
				else:
					cell_distances.append(dist)
					
		cell_distances = np.array(cell_distances)
		cell_distances = cell_distances.reshape(cell_distances.shape[0], 1) 
		circles = np.hstack((circles, cell_distances)).astype(int) #add to cells array
		
		def rank_cells(a):
			#apply weights for ranking 
			x, y, radius, _, well, sep = a 
			rad_weighted = float(radius)/10.*rad_weight # %weight for radius size 
			sep_weighted = float(sep)/50.*sep_weight # %weight for separation distance  
			return rad_weighted+sep_weighted*100 
		
		ranks = np.apply_along_axis(rank_cells, 1, circles) #apply ranks 
		ranks = ranks.reshape(ranks.shape[0], 1)
		circles = np.hstack((circles, ranks)).astype(int) #cast to int 	

		
		raw_img = cv2.cvtColor(raw_img, cv2.COLOR_GRAY2BGR)
		
		logs = np.zeros((1, 6), dtype='int') 
		for plate_count in range(96):	
			plate = circles[circles[:,4]==(plate_count+1), :] #grab cells per active plate 
			plate = plate[np.argsort(plate[:,-1])][::-1] #sort by separation/rank
			
			for j, i in enumerate(plate[0:]): #draw circles
				'''
				topped rank will be drawn first 
				increase cells_to_pick in params.txt 
				to choose how many cells will be picked 
				'''

				x, y, radius, _, well_plate, sep, rank = i
			
				if j <= cells_to_pick-1:
					if radius>min_radius: #radius threshold 
						if sep ==0 or sep>min_sep: #separation theshold
							cv2.circle(color_img,(x,y),2,(0, 255, 0),radius) #center 
							cv2.circle(thresh_img,(x,y),2,(0, 255, 0),radius) #center 
							cv2.circle(raw_img,(x,y),2,(0, 255, 0),radius) #center 
							log = np.array([x, y, radius, well_plate, sep, rank]).T
							log = log.reshape(1, len(log))
							logs = np.vstack((logs, log))	
							continue
				#'else' draw red circles and don't log 
				cv2.circle(color_img,(x,y),2,(0,0,255),radius) #center 
				cv2.circle(thresh_img,(x,y),2,(0,0,255),radius) #center 
					
		logs = logs.astype(str)[1:]
		
		def map_wells(a):
			well = a[3]
			mapped = well_labels[well]
			return mapped
			
		mapped_wells = np.apply_along_axis(map_wells, 1,logs)
		mapped_wells = mapped_wells.reshape(mapped_wells.shape[0], 1)
		logs = np.hstack((logs, mapped_wells))
		
		log_name = img_file.split('.')[0]+'_logs.dat'
		np.savetxt(log_name, logs, delimiter="     ", fmt='%s') #save
		
		print "total cells found: ", circles.shape[0]
		print 'pickable cells found: ', logs.shape[0]
		
	return thresh_img, color_img

### APPLY PIPELINE ### 
	
#img_file = 'ecoli.tif'
#thresh_img, color_img = pipeline(img_file)

dir = 'plates/' 
for filename in os.listdir(dir):	
	if '.tif' in filename or '.TIF' in filename:
		thresh_img, color_img = pipeline(dir+filename)

		outname = dir + 'image_out/' + filename.split('.')[0] + '_out.TIF'
		cv2.imwrite(outname, color_img)
		
		thresh_img = cv2.resize(thresh_img, (thresh_img.shape[1]/2,thresh_img.shape[0]/2))
		color_img = cv2.resize(color_img, (color_img.shape[1]/2,color_img.shape[0]/2))

		cv2.imshow('circles', thresh_img)
		cv2.waitKey(0)
		cv2.imshow('circles', color_img)
		cv2.waitKey(0)
		
		print #newline 