import cv2
import numpy as np

from Colour import Colour, Colour_range
from Z_RGB_formula import RGB_formula


class RGB_formulas_mask:

    def __init__(self):
        
        self.region_id_max_value = 255
        self.regions_ids:list[np.uint8] = []

        self.mask_original:np.ndarray[np.uint8] = None #the mask is a numpy arrays which contains integers; each integer (except 0) in the array is also an id in `region_ids`
        self.mask_resized:np.ndarray[np.uint8] = None


    def update_original_mask(self, img_mask:np.ndarray[np.uint8], remove_previous_mask:bool):
        
        if(remove_previous_mask == True or self.mask_original is None):
            self.mask_original = np.zeros(img_mask.shape[:-1],np.uint8)#the mask will contain the ids of the regions

        elif(img_mask.shape[0] != self.mask_original.shape[0] or img_mask.shape[1]!= self.mask_original.shape[1]):
                self.resize_original_mask(img_mask.shape[1],img_mask.shape[0])

    #<those functions must be called from outside (all parameters must be correct and match exactly the specified type)
    def get_min_not_used_region_id(self) -> int:
        
        num = 1
        if(len(self.regions_ids) == 0):            
            return num

        while(num in self.regions_ids):
            
            num+=1
            if(num > self.region_id_max_value):
                return None

        return num
    

    def add_region(self, region_id:np.uint8) -> bool:

        if(region_id not in self.regions_ids):
            self.regions_ids.append(region_id)
            self.regions_ids.sort()
            return True
        else:
            return False


    def remove_region(self, region_id:np.uint8) -> bool:

        if(region_id in self.regions_ids):
            self.regions_ids.remove(region_id)
            self.regions_ids.sort()
            return True
        else:
            return False
    
    def does_region_exist(self, region_id:np.uint8) -> bool:
        
        if(region_id in self.regions_ids):
            return True
        else:
            return False
        

    #those functions must be called from outside (all parameters must be correct and match exactly the specified type)>

    
    #`img_for_creating_a_mask` must be a numpy array with shape (Height, Width, 3[RGB]) 
    #`colours` must be a dictionary which has for keys the ids of the colours while the values must be objects of type `Colour`
    def create_colour_regions(self, img_for_creating_a_mask:np.ndarray[np.uint8], colours:dict[np.uint8, Colour], remove_previous_mask:bool = True) -> np:
                        
        self.update_original_mask(img_mask=img_for_creating_a_mask, remove_previous_mask=remove_previous_mask)

       
        for i in range(0, img_for_creating_a_mask.shape[0]):
            for j in range(0, img_for_creating_a_mask.shape[1]):

                for id in colours.keys():

                    if(img_for_creating_a_mask[i,j,0] == colours[id].r and img_for_creating_a_mask[i,j,1] == colours[id].g and img_for_creating_a_mask[i,j,2] == colours[id].b):
                        self.mask_original[i,j] = id
                        break
 
        self.mask_resized = self.mask_original.copy()
    

    #`img_for_creating_a_mask` must be a numpy array with shape (Height, Width, 3[RGB])
    #`colour_ranges` must be a dictionary which has for keys the ids of the colour ranges while the values must be objects of type `Colour_range`
    def create_colour_range_regions(self, img_for_creating_a_mask:np.ndarray[np.uint8], colour_ranges:dict[np.uint8, Colour_range], remove_previous_mask:bool = True) -> np.ndarray[np.uint8]:
        
        self.update_original_mask(img_mask=img_for_creating_a_mask, remove_previous_mask=remove_previous_mask)
        
        for i in range(0, img_for_creating_a_mask.shape[0]):
            for j in range(0, img_for_creating_a_mask.shape[1]):

                for id in colour_ranges.keys():

                    if(img_for_creating_a_mask[i,j,0] >= colour_ranges[id].r_from and img_for_creating_a_mask[i,j,0] <= colour_ranges[id].r_to and
                       img_for_creating_a_mask[i,j,1] >= colour_ranges[id].g_from and img_for_creating_a_mask[i,j,1] <= colour_ranges[id].g_to and
                       img_for_creating_a_mask[i,j,2] >= colour_ranges[id].b_from and img_for_creating_a_mask[i,j,2] <= colour_ranges[id].b_to):
                        self.mask_original[i,j] = id
                        break
            
        self.mask_resized = self.mask_original.copy()
    
   
    #`img` must be a "numpy.ndarray" in the shape of (Areas, Height, Width, 3) or (Height, Width, 3) Where 3 is for the RGB color channels
    #`rgb_formulas` must be a list which contains objects of type `RGB_formula`
    #the first rgb formula will be applied to the first region, the second rgb formula will be applied to the second region and so on
    def transform_image(self, img:np.ndarray[np.uint8], rgb_formulas:list[RGB_formula], rgb_formulas_dynamic_variables:np.ndarray[np.uint8], keep_ratio:bool) -> np.ndarray[np.uint8]:
        
        if(len(img.shape) == 3):
            areas_count = 1

            h = img.shape[0]
            w = img.shape[1]

            img_r = img[:,:,0]
            img_g = img[:,:,1]
            img_b = img[:,:,2]

        elif(len(img.shape) == 4):
            areas_count = img.shape[0]

            h = img.shape[1]
            w = img.shape[2]

            img_r = img[:,:,:,0]
            img_g = img[:,:,:,1]
            img_b = img[:,:,:,2]
            
        else:
            raise Exception("the shape of the image must have either 3 or 4 dimentions")

        if(self.mask_original is None or self.mask_resized is None or
           h == 0 or w == 0 or len(rgb_formulas) == 0):
            return img
        
        if(rgb_formulas_dynamic_variables.shape[0] == 0):
            rgb_formulas_dynamic_variables = np.array([0], dtype=np.uint8)
        
        #if the user changes the shape of the window then the code in the if statement will be executed in order to make the size of the filters match the size of the resized image         
        if(h !=self.mask_resized.shape[0] or w!=self.mask_resized.shape[1]):
            self.resize_resizable_mask(new_width=w,new_hight=h, keep_ratio=keep_ratio)

        rgb_formula_index = 0
        rgb_formulas_count = len(rgb_formulas)
        regions_count = len(self.regions_ids)

        for region_index in range(0, regions_count):
            
            boolean_mask = self.mask_resized == self.regions_ids[region_index]

            #the image is processed faster when the boolean mask is used without slicing
            if(len(img.shape) == 3):
                r = np.expand_dims(img_r[boolean_mask], axis=0)
                g = np.expand_dims(img_g[boolean_mask], axis=0)
                b = np.expand_dims(img_b[boolean_mask], axis=0)
                
                img[boolean_mask] = rgb_formulas[rgb_formula_index].rgb_function(r=r, g=g, b=b, areas_count=areas_count, v=rgb_formulas_dynamic_variables)

            #the image can use the pixel values of other images in the rgb formulas when the boolean mask is used with slicing 
            else:
                r = img_r[:,boolean_mask]
                g = img_g[:,boolean_mask]
                b = img_b[:,boolean_mask]
                
                img[:,boolean_mask] = rgb_formulas[rgb_formula_index].rgb_function(r=r, g=g, b=b, areas_count=areas_count, v=rgb_formulas_dynamic_variables)

            rgb_formula_index+=1
            if(rgb_formula_index >= rgb_formulas_count):
                rgb_formula_index = 0
        
        return img
    
    #`img` must be a "numpy.ndarray" in the shape of (Areas, Height, Width, 3) Where 3 is for the RGB color channels
    #`region_images` must be a list which contains elements of type "numpy.ndarray" in the shape of (Height, Width, 3) Where 3 is for the RGB color channels
    #`rgb_formulas` must be a list which contains objects of type `RGB_formula`
    #the first region image will be applied to the first region, the second region image will be applied to the second region and so on
    def transform_image_using_other_images(self, img:np.ndarray[np.uint8], region_images:list[np.ndarray[np.uint8]], keep_ratio:bool) -> np.ndarray[np.uint8]:
        
        if(self.mask_original is None or self.mask_resized is None or
           img.shape[2] == 0 or img.shape[1] == 0 or len(region_images) == 0):
            return img
        
        #if the user changes the shape of the window then the code in the if statement will be executed in order to make the size of the filters match the size of the resized image         
        if(img.shape[2] !=self.mask_resized.shape[1] or img.shape[1]!=self.mask_resized.shape[0]):
            self.resize_resizable_mask(new_width=img.shape[2],new_hight=img.shape[1], keep_ratio=keep_ratio)


        region_images_index = 0
        region_images_count = len(region_images)
        regions_count = len(self.regions_ids)

        for region_index in range(0, regions_count):

            region_image = region_images[region_images_index]
            region_height = min(region_image.shape[0], img.shape[1])
            region_width = min(region_image.shape[1], img.shape[2])
            
            boolean_mask = self.mask_resized[:region_height, :region_width] == self.regions_ids[region_index]
            
            img[:, :region_height, :region_width, :][:,boolean_mask] = region_image[:region_height, :region_width, :][boolean_mask]

            region_images_index+=1
            if(region_images_index >= region_images_count):
                region_images_index = 0

        return img


    
    def resize_resizable_mask(self, new_width:int, new_hight:int, keep_ratio:bool):

        if(keep_ratio == True):
            self.mask_resized = cv2.resize(self.mask_original, (new_width, new_hight), interpolation=cv2.INTER_NEAREST)
        else:
            self.mask_resized = self.mask_original[:new_hight,:new_width].copy()

            if(self.mask_resized.shape[0] != new_hight or self.mask_resized.shape[1] != new_width):
                self.mask_resized = cv2.resize(self.mask_resized, (new_width, new_hight), interpolation=cv2.INTER_NEAREST)
    
    def resize_original_mask(self, new_width:int, new_hight:int):
        self.mask_original = cv2.resize(self.mask_original, (new_width, new_hight), interpolation=cv2.INTER_NEAREST)
    
    def get_regions_ids(self) -> list[np.uint8]:
        return self.regions_ids

    def copy(self):

        self_copy = RGB_formulas_mask()
        self_copy.regions_ids = self.regions_ids.copy()
        if(self.mask_original is not None and self.mask_resized is not None):
            self_copy.mask_original = self.mask_original.copy()
            self_copy.mask_resized = self.mask_resized.copy()

        return self_copy