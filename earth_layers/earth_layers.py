import cv2
import numpy as np

#desktop = (1920, 1080) #resolution
desktop = (4320, 2160)
def nothing(x):
    pass 

earth = cv2.imread('raw_earth.jpg')
earth = cv2.resize(earth, desktop)

lights  = cv2.imread('lights_only_blue.jpg')
lights = cv2.resize(lights, desktop)
   
population_orig = cv2.imread('population.jpg') #prevent overwriting 
population_orig = cv2.resize(population_orig, desktop)

cv2.namedWindow('slider')
cv2.createTrackbar('gauss_kernel','slider',1,10,nothing)
cv2.createTrackbar('alpha','slider',1,10,nothing)

while True:
    alpha = cv2.getTrackbarPos('alpha', 'slider')
    alpha = float(alpha)/10
    beta = 1-alpha
    earth_lit = cv2.addWeighted(earth, alpha, lights , beta, 0)
    cv2.imshow('earth_lit', earth_lit)
    if cv2.waitKey(1) & 0xFF == ord('p'): #quit	
        print 'first alpha: ', alpha 
        break 
        
while True: 
    gauss = cv2.getTrackbarPos('gauss_kernel', 'slider')
    gauss = abs(gauss)
    if gauss % 2 != 1 or gauss==0: #make odd 
        gauss=gauss+1
    gauss = (gauss, gauss)
    population = cv2.GaussianBlur(population_orig, gauss, 1)

    alpha = cv2.getTrackbarPos('alpha', 'slider')
    alpha = float(alpha)/10
    beta = 1-alpha
    final = cv2.addWeighted(population, alpha, earth_lit , beta, 0)
    cv2.imshow('final', final)
    if cv2.waitKey(1) & 0xFF == ord('q'): #quit	
        print 'second alpha: ', alpha
        print 'gauss: ', gauss
        break       
cv2.imwrite('earth_layers.jpg', final)
cv2.destroyAllWindows()