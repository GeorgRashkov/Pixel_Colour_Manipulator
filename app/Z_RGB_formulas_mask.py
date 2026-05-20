from PyQt5.QtWidgets import QWidget
from PyQt5_Window_functions import open_or_minimize_window, open_or_minimize_windows
import cv2
import numpy as np
from typing import Callable


from Colour import Colour, Colour_range


class RGB_formulas_mask:

    def __init__(self):
        
        self.mask:np.ndarray[np.uint8] = None #the mask is a numpy arrays which contains integers; each integer (except 0) in the array is also an id in `rgb_functions`
        self.mask_resized:np.ndarray[np.uint8] = None
        self.rgb_functions:dict[int,Callable] = None #this is a dictionary which has for keys the ids of rgb functions while the values must be a valid RGB formulas represented as lambda functions


    #`img_mask` must be a numpy array with shape (Height, Width, 3[RGB])
    #`rgb_functions` must be a dictionary which has for keys the ids of rgb functions while the values must be a valid RGB formulas represented as lambda functions 
    #`colours` must be a dictionary which has for keys the ids of the colours while the values must be objects of type `Colour`
    #a rgb formula (a lambda function inside `rgb_functions`) will be applied only to those regions whose colour id (in `colours`) matches the id of the rgb formula 
    def create_colour_mask(self, img_mask:np.ndarray[np.uint8], rgb_functions:dict[int,Callable], colours:dict[int,Colour]) -> np:
                   
        for rgb_function_id in rgb_functions.keys():
            if(rgb_function_id not in colours.keys()):
                raise Exception("rgb functions had id which had no maching colour id")
        
        if(len(rgb_functions) != len(colours)):
            raise Exception("colours had id which had no maching rgb function id")
            
        self.mask = np.zeros(img_mask.shape[:-1],np.uint8) #the mask will contain the ids of the rgb_funtions
        self.rgb_functions = {}
        

        """
        for x in img_mask:
            for y in x:

                for id in colours.keys():

                    if(y[0] == colours[id].r and y[1] == colours[id].g and y[2] == colours[id].b):
                        self.mask[y,x] = id
                        self.rgb_functions[id] = rgb_functions[id]
                        break
        """ 
        for i in range(0, img_mask.shape[0]):
            for j in range(0, img_mask.shape[1]):

                for id in colours.keys():

                    if(img_mask[i,j,0] == colours[id].r and img_mask[i,j,1] == colours[id].g and img_mask[i,j,2] == colours[id].b):
                        self.mask[i,j] = id
                        self.rgb_functions[id] = rgb_functions[id]
                        break
 
        self.mask_resized = self.mask.copy()
    

     #`img_mask` must be a numpy array with shape (Height, Width, 3[RGB])
    #`rgb_functions` must be a dictionary which has for keys the ids of rgb functions while the values must be a valid RGB formulas represented as lambda functions 
    #`colour_ranges` must be a dictionary which has for keys the ids of the colour ranges while the values must be objects of type `Colour_range`
    #a rgb formula (a lambda function inside `rgb_functions`) will be applied only to those regions whose colour range id (in `colour_ranges`) matches the id of the rgb formula 
    def create_colour_range_mask(self, img_mask:np.ndarray[np.uint8], rgb_functions:dict[int,Callable], colour_ranges:dict[int,Colour_range]) -> np.ndarray[np.uint8]:
                        
        for rgb_function_id in rgb_functions.keys():
            if(rgb_function_id not in colour_ranges.keys()):
                raise Exception("rgb functions had id which had no maching colour range id")
            
        if(len(rgb_functions) != len(colour_ranges)):
            raise Exception("colour ranges had id which had no maching rgb function id")
            
        self.mask = np.zeros(img_mask.shape[:-1],np.uint8) #the mask will contain the ids of the rgb_funtions
        self.rgb_functions = {}
        """
        for x in img_mask:
            for y in x:

                for id in colour_ranges.keys():

                    if(y[0] > colour_ranges[id].r_from and  y[0] < colour_ranges[id].r_to and
                        y[1] > colour_ranges[id].g_from and  y[1] < colour_ranges[id].g_from and 
                        y[2] > colour_ranges[id].b_from and  y[2] < colour_ranges[id].b_from):
                            
                        self.mask[x,y] = id
                        self.rgb_functions[id] = rgb_functions[id]
                        break
        """
        for i in range(0, img_mask.shape[0]):
            for j in range(0, img_mask.shape[1]):

                for id in colour_ranges.keys():

                    if(img_mask[i,j,0] >= colour_ranges[id].r_from and img_mask[i,j,0] <= colour_ranges[id].r_to and
                       img_mask[i,j,1] >= colour_ranges[id].g_from and img_mask[i,j,1] <= colour_ranges[id].g_to and
                       img_mask[i,j,2] >= colour_ranges[id].b_from and img_mask[i,j,2] <= colour_ranges[id].b_to):
                        self.mask[i,j] = id
                        self.rgb_functions[id] = rgb_functions[id]
                        break
            
        self.mask_resized = self.mask.copy()




    def apply_mask_to_image(self, img:np.ndarray[np.uint8]) -> np.ndarray[np.uint8]:#`img` must be a "numpy.ndarray" in the shape of (Height, Width, 3) Where 3 is for the RGB color channels
        
        if(self.mask is None or self.mask_resized is None or self.rgb_functions is None):
            return img

        img_r = img[:,:,0]
        img_g = img[:,:,1]
        img_b = img[:,:,2]

        for rgb_function_id in self.rgb_functions:
            
            #if the user changes the shape of the window than the code in the if statement whill be executed in order to make the size of the filters match the size of the resized image         
            if(img.shape[0] !=self.mask_resized.shape[0] or img.shape[1]!=self.mask_resized.shape[1]):
                self.resize_mask(img.shape[1],img.shape[0])
            
            boolean_mask = self.mask_resized == rgb_function_id
            #img[boolean_mask] = self.rgb_functions[rgb_function_id](r=img[:,:,0], g=img[:,:,1], b=img[:,:,2], m=boolean_mask)
            r = img_r[boolean_mask]
            g = img_g[boolean_mask]
            b = img_b[boolean_mask]
            
            img[boolean_mask] = self.rgb_functions[rgb_function_id](r=r, g=g, b=b)

        return img

    
    def resize_mask(self, new_width:int, new_hight:int):
        self.mask_resized = cv2.resize(self.mask, (new_width, new_hight), interpolation=cv2.INTER_NEAREST)