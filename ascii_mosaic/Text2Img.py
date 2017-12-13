import cv2 
import numpy as np
from skimage.transform import resize
from itertools import cycle
import string 


FONT = cv2.FONT_HERSHEY_SIMPLEX

class Processor: 
    def __init__(self, size=size, text = 'files/transcript.txt', center_text=True): 
        '''Processor Constructor 
        args : 
            size : (int) size of sides of ascii .PNG (square)
            text : (str) text file to render ascii characters from 
            center_text : (bool) if True, center each ascii character in its grid position 
        
        returns: None 
        '''
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
                    char_img = np.zeros(shape=(40, 40))
                    cv2.putText(char_img, char, (9, 25), FONT, 1, 1, 1)
                    
                    if center_text:
                        if char != ' ' and char not in string.punctuation:
                            #get horz and vert center of mass 
                            horz = np.sum(char_img, axis=1)
                            horz_ind = np.where(horz>0)
                            horz_mean = np.mean(horz_ind).astype(int)

                            vert = np.sum(char_img, axis=0)
                            vert_ind = np.where(vert>0)
                            vert_mean = np.mean(vert_ind).astype(int)

                            #crop equidistant from center of mass 
                            char_img = char_img[(horz_mean-12):(horz_mean+12), 
                                        (vert_mean-12):(vert_mean+12)]

                    char_img = resize(char_img, (self.size, self.size))
                    char_img = 1- cv2.threshold(char_img,0,1,cv2.THRESH_BINARY)[1]
#                     plt.imshow(char_img); plt.show()
                    self.letter_lookup[char] = char_img
        self.transcipt = list(transcipt)
        self.cycle_transript = None
        
        self.project2ascii = np.vectorize(self.project2ascii, otypes=[object])
        
    def project2ascii(self, pixel): 
        '''project/map binned ASCII chars to stored .PNGs'''
        next_char = next(self.cycle_transript)
        char_img = self.letter_lookup[next_char]
        background = char_img*pixel
        out = cv2.addWeighted(char_img+255,0.5, background,0.5, 0)
        return out
        
    def process_image(self, input_image, shift = 0):
        '''Maps an image's grayscale pixel intensties to characters from self.transcript
        
        args: 
            input_image : (str) or (np.array)
                if filename string is given, will open. Otherwise you 
                can supply a numpy array. 
            shift : (int) indices to shift characters in transcipt array 
                
        returns: 
            self.out : (np.array)
                output grasycale image of mapped text(larger dims by factor of self.size)  
        '''
        
        #input image 
        if type(input_image) is str: 
            input_image = cv2.imread(input_image)
            
        self.img = cv2.GaussianBlur(input_image, (7, 7), 0) #open and denoise image  
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY) #grayscale 
        
        shift = shift % len(self.transcipt)
        self.transcipt = self.transcipt[shift:]+self.transcipt[:shift] #shift the transcipt array
        self.cycle_transript = cycle(self.transcipt) #reset for cyclcing through text chars 
        
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