import cv2
import numpy as np

from Colour import Colour, Colour_range
from Z_RGB_formula import RGB_formula


class RGB_formulas_mask:

    def __init__(self):
        
        self.region_id_max_value = 255
        self.rgb_formulas_and_regions_ids:dict[int, np.uint8] = {}

        self.mask_original:np.ndarray[np.uint8] = None #the mask is a numpy arrays which contains integers; each integer (except 0) in the array is also an id in `region_ids`
        self.mask_resized:np.ndarray[np.uint8] = None


    def update_original_mask(self, img_mask:np.ndarray[np.uint8], remove_presious_mask:bool):
        
        if(remove_presious_mask == True or self.mask_original is None):
            self.mask_original = np.zeros(img_mask.shape[:-1],np.uint8)#the mask will contain the ids of the rgb_funtions

        elif(img_mask.shape[0] != self.mask_original.shape[0] or img_mask.shape[1]!= self.mask_original.shape[1]):
                self.resize_original_mask(img_mask.shape[1],img_mask.shape[0])

    #<those functions must be called from outside (all parameters must be correct and match exactly the specified type)
    def get_min_not_used_region_id(self) -> int:
        
        num = 1
        if(len(self.rgb_formulas_and_regions_ids) == 0):            
            return num

        while(num in self.rgb_formulas_and_regions_ids.values()):
            
            num+=1
            if(num > self.region_id_max_value):
                return None

        return num
    

    def add_region(self, rgb_formula_id:int, region_id:np.uint8) -> bool:

        if(region_id not in self.rgb_formulas_and_regions_ids.values()):
            self.rgb_formulas_and_regions_ids[rgb_formula_id] = region_id
            return True
        else:
            return False


    def remove_region(self, region_id:np.uint8) -> bool:

        if(region_id in self.rgb_formulas_and_regions_ids.values()):
            del self.rgb_formulas_and_regions_ids[region_id]
            return True
        else:
            return False
    
    def does_region_exist(self, region_id:np.uint8) -> bool:
        
        if(region_id in self.rgb_formulas_and_regions_ids.values()):
            return True
        else:
            return False
        
    
    def update_rgb_formula_id_region(self, rgb_formula_id:int, region_id:np.uint8):
        
        self.rgb_formulas_and_regions_ids[rgb_formula_id] = region_id

    #those functions must be called from outside (all parameters must be correct and match exactly the specified type)>

    #`img_for_creating_a_mask` must be a numpy array with shape (Height, Width, 3[RGB]) 
    #`colours` must be a dictionary which has for keys the ids of the colours while the values must be objects of type `Colour`
    def create_colour_mask(self, img_for_creating_a_mask:np.ndarray[np.uint8], colours:dict[int,Colour], remove_presious_mask:bool = True) -> np:
                        
        self.update_original_mask(img_mask=img_for_creating_a_mask, remove_presious_mask=remove_presious_mask)

       
        for i in range(0, img_for_creating_a_mask.shape[0]):
            for j in range(0, img_for_creating_a_mask.shape[1]):

                for id in colours.keys():

                    if(img_for_creating_a_mask[i,j,0] == colours[id].r and img_for_creating_a_mask[i,j,1] == colours[id].g and img_for_creating_a_mask[i,j,2] == colours[id].b):
                        self.mask_original[i,j] = id
                        break
 
        self.mask_resized = self.mask_original.copy()
    

    #`img_for_creating_a_mask` must be a numpy array with shape (Height, Width, 3[RGB])
    #`colour_ranges` must be a dictionary which has for keys the ids of the colour ranges while the values must be objects of type `Colour_range`
    def create_colour_range_mask(self, img_for_creating_a_mask:np.ndarray[np.uint8], colour_ranges:dict[int,Colour_range], remove_presious_mask:bool = True) -> np.ndarray[np.uint8]:
        
        self.update_original_mask(img_mask=img_for_creating_a_mask, remove_presious_mask=remove_presious_mask)
        
        for i in range(0, img_for_creating_a_mask.shape[0]):
            for j in range(0, img_for_creating_a_mask.shape[1]):

                for id in colour_ranges.keys():

                    if(img_for_creating_a_mask[i,j,0] >= colour_ranges[id].r_from and img_for_creating_a_mask[i,j,0] <= colour_ranges[id].r_to and
                       img_for_creating_a_mask[i,j,1] >= colour_ranges[id].g_from and img_for_creating_a_mask[i,j,1] <= colour_ranges[id].g_to and
                       img_for_creating_a_mask[i,j,2] >= colour_ranges[id].b_from and img_for_creating_a_mask[i,j,2] <= colour_ranges[id].b_to):
                        self.mask_original[i,j] = id
                        break
            
        self.mask_resized = self.mask_original.copy()



    #`rgb_formulas` must be a dictionary which has for keys the ids of rgb formulas while the values must be a valid objects of type `RGB_formula`
    #each rgb formula will be applied only to those regions of the mask whose value matches the id of the rgb formula 
    def apply_mask_to_image(self, img:np.ndarray[np.uint8], rgb_formulas:dict[int, RGB_formula], rgb_formulas_dynamic_variables:np.ndarray[np.uint8]) -> np.ndarray[np.uint8]:#`img` must be a "numpy.ndarray" in the shape of (Height, Width, 3) Where 3 is for the RGB color channels
        
        if(self.mask_original is None or self.mask_resized is None):
            return img

        img_r = img[:,:,0]
        img_g = img[:,:,1]
        img_b = img[:,:,2]

        for rgb_formula_id in rgb_formulas.keys():

            if(rgb_formula_id not in self.rgb_formulas_and_regions_ids.keys()):
                continue
            
            #if the user changes the shape of the window then the code in the if statement whill be executed in order to make the size of the filters match the size of the resized image         
            if(img.shape[0] !=self.mask_resized.shape[0] or img.shape[1]!=self.mask_resized.shape[1]):
                self.resize_resizable_mask(img.shape[1],img.shape[0])
            
            boolean_mask = self.mask_resized == self.rgb_formulas_and_regions_ids[rgb_formula_id]

            r = img_r[boolean_mask]
            g = img_g[boolean_mask]
            b = img_b[boolean_mask]
            
            img[boolean_mask] = rgb_formulas[rgb_formula_id].rgb_function(r=r, g=g, b=b, v=rgb_formulas_dynamic_variables)

        return img

    
    def resize_resizable_mask(self, new_width:int, new_hight:int):
        self.mask_resized = cv2.resize(self.mask_original, (new_width, new_hight), interpolation=cv2.INTER_NEAREST)
    
    def resize_original_mask(self, new_width:int, new_hight:int):
        self.mask_original = cv2.resize(self.mask_original, (new_width, new_hight), interpolation=cv2.INTER_NEAREST)