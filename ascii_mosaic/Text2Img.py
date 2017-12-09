import cv2 
import numpy as np
from scipy.misc import imresize 
from itertools import cycle 


FONT = cv2.FONT_HERSHEY_SIMPLEX
SIZE = 15 #size of sides of ascii .PNG (square)

class Processor: 
    def __init__(self, size=SIZE, text = 'transcript.txt'): 
        self.size = size
        self.img = None 
        self.out = None
        
        #preprocess the text 
        self.letter_lookup = {}
        transcipt = ''
        with open(text) as f: 
            for word in f: 
                transcipt = '{}{}'.format(transcipt, word)
                for char in word: 
                    char_img = np.zeros(shape=(28, 28))
                    cv2.putText(char_img, char, (3, 25), FONT, 1, 1, 1)
                    char_img = imresize(char_img, (self.size, self.size))
                    char_img = 1- cv2.threshold(char_img,0,1,cv2.THRESH_BINARY)[1]
#                     plt.imshow(char_img); plt.show()
                    self.letter_lookup[char] = char_img
        self.transcipt = cycle(list(transcipt))
        
        self.project2ascii = np.vectorize(self.project2ascii, otypes=[object])
        
    def project2ascii(self, pixel): 
        '''project/map binned ASCII chars to stored .PNGs'''
        next_char = next(self.transcipt)
        char_img = self.letter_lookup[next_char]
        background = char_img*pixel
        o = cv2.addWeighted(char_img+255,0.8, background,0.8, 0)
        return o
        
    def process_image(self, input_image):
        '''Maps an image's grayscale pixel intensties to characters from self.transcript
        
        args: 
            input_image : (str) or (np.array)
                if filename string is given, will open. Otherwise you 
                can supply a numpy array. 
                
        returns: 
            self.out : (np.array)
                output grasycale image of mapped text(larger dims by factor of self.size)  
        '''
        
        #input image 
        if type(input_image) is str: 
            input_image = cv2.imread(input_image)
            
        self.img = cv2.GaussianBlur(input_image, (7, 7), 0) #open and denoise image  
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) #grayscale 
        
        temp = self.project2ascii(self.img) #map the characters to the pixels 
        
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