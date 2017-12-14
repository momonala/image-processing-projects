import cv2
import numpy as np 
from scipy.misc import imresize

import matplotlib.pyplot as plt 

FONT = cv2.FONT_HERSHEY_DUPLEX
SIZE = 15 #size of sides of ascii .PNG (square)

class Processor: 
    def __init__(self, size=SIZE): 
        self.size = size
        self.img = None 
        self.out = None 
        
        #populate ascii lookup table percent fill to image array 
        self.ascii_lookup  = {}
        with open('files/ascii_lookup_table.txt', 'r') as f: 
            for line in f.readlines(): 
                l = line.split()
                ascii_pic = cv2.cvtColor(cv2.imread(l[1]), cv2.COLOR_BGR2GRAY)
                self.ascii_lookup[int(l[0])] = imresize(ascii_pic, (size, size))
                
        #vectorize mapping functions for SPEED 
        self.bin_pixels = np.vectorize(self.bin_pixels, cache=True)
        self.project2ascii= np.vectorize(self.project2ascii, otypes=[object])

             
    def bin_pixels(self, pix):
        '''binning pixels for mapping to ASCII chars '''
        return min(self.ascii_lookup, key=lambda x:abs(x-pix))
    
    def project2ascii(self, ascii_bin): 
        '''project/map binned ASCII chars to stored .PNGs'''
        return self.ascii_lookup[ascii_bin] 
    
    
    def process_image(self, input_image):
        '''process a single image or frame to ASCII format 
        
        args: 
            input_image : (str) or (np.array)
                if filename string is given, will open. Otherwise you 
                can supply a numpy array. 
                
        returns: 
            self.out : (np.array)
                output image processed. ASCII characters mapped to pixel value, and 
                size of image is self.size times bigger than the input image. 
        '''
        
        #input image 
        if type(input_image) is str: 
            input_image = cv2.imread(input_image)
            
        img = cv2.GaussianBlur(input_image, (7, 7), 0) #open and denoise image  
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #grayscale 
        
        #bin the pixels for mapping to ASCII chars
        ascii_bins =  self.bin_pixels(self.img) 
        
        #project to larger ASCII char image
        temp = np.array(list(map(self.project2ascii, ascii_bins))) 
        
        #temp is an array of arrays, so reformat to correct image dims 
        self.out = np.hstack([np.hstack(temp[i]).T for i in range(temp.shape[0])]).T #reformat 

        return self.out
        
        
    def write_output(self, output_name): 
        '''write image to file
        args: 
            output_name : (str)
                filename to write to 
                
        returns: None
        '''
        
        assert self.out is not None, 'process an image before saving'
        cv2.imwrite(output_name, self.out) 