from Z_Pixel_area import Pixel_area
from Z_RGB_formula import RGB_formula
import numpy as np

class Pixel_areas_manipulator:

    def __init__(self, pixel_areas_dict: dict[int,Pixel_area], rgb_formulas_dict: dict[int,RGB_formula] ):
        
        self.pixel_areas_dict = pixel_areas_dict
        self.rgb_formulas_dict = rgb_formulas_dict
        
        self.img_height = 0
        self.img_width = 0
        
        self.image_versions_count = 0  #this is the number of image versions defined by the user (when the image is processed there will be 2 additional image versions)   
        self.max_image_versions = 99

        self.set_image_versions()

    

    #set's proper value for `self.image_versions_count` and for each pixel area set's proper values for `img_in_v`, `img_out_v` and `img_out_stack`
    def set_image_versions(self):

        self.set_image_versions_count()

        for pixel_area in self.pixel_areas_dict.values():
                        
            if(pixel_area.img_in_v > self.image_versions_count+1):#the values inside `img_in_v` start from `0`
                pixel_area.img_in_v = self.image_versions_count+1 #set's `img_in_v` to be the last image version (the special one)
                        
            if(pixel_area.img_out_v > self.image_versions_count+1):#the values inside `img_out_v` start from `1`
                pixel_area.img_out_v = self.image_versions_count+1 #set's `img_out_v` to be the last image version (the special one)
                           
            #the value of `img_out_stack` will be combined with `img_out_v` in order to determine 
            #the number of image versions which will be affected after applying the rgb formula           
            if(pixel_area.img_out_stack == 0): #if `img_out_stack` is `0` then every image version (starting from `img_out_v`) will be affected by the rgb formula result
                pixel_area.img_out_stack = self.image_versions_count                

        
    def set_image_versions_count(self):
        image_versions_count = 0
        
        for pixel_area in self.pixel_areas_dict.values():            
            image_versions_count = max(image_versions_count, pixel_area.img_in_v, pixel_area.img_out_v)
        
        if(image_versions_count > self.max_image_versions):
            image_versions_count = self.max_image_versions
            print(f"warning: the maximum number of image versions is {self.max_image_versions};\n if the value of `img_in_v` is equal or above the max value than the special last image version will be used;\n if the value of `img_out_v` is equal or above the max value than the special last image version will be used")

        self.image_versions_count = image_versions_count


    """
    #set's proper value for `self.image_versions_count` and for each pixel area set's proper values for `img_in_v`, `img_out_v` and `img_out_stack`
    def set_image_versions(self):

        are_image_version_values_changed = False

        for pixel_area in self.pixel_areas_dict.values():
            
            if(pixel_area.img_in_v >= self.max_image_versions):#the values inside `img_in_v` start from `0`
                pixel_area.img_in_v = 0
                are_image_version_values_changed = True
            
            if(pixel_area.img_out_v >= self.max_image_versions):#the values inside `img_out_v` start from `0`
                pixel_area.img_out_v = self.max_image_versions-1
                are_image_version_values_changed = True
            
            #the value of `img_out_stack` will be combined with `img_out_v` in order to determine 
            #the number of image versions which will be afected after applying the rgb formula           
            if(pixel_area.img_out_stack == 0):
                pixel_area.img_out_stack = self.max_image_versions                


        for pixel_area in self.pixel_areas_dict.values():                  
            
            self.image_versions_count = max(pixel_area.img_in_v+1, pixel_area.img_out_v+1, self.image_versions_count)
            if(self.image_versions_count == self.max_image_versions):
                break
        

        if(are_image_version_values_changed == True):       
            print(f"warning: the maximum number of image versions is {self.max_image_versions};\n if the value of `img_in_v` is equal or above the max value than 0 will be used;\n if the value of `img_out_v` is equal or above the max value than max-1 will be used")

        """
       
    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def transform_image(self, img:np) -> np.array:       

        image_versions : list[np.array] = []
        for i in range(self.image_versions_count + 2):#adding 2 additional image versions (the first image version will always have pixel values of the original image; the last image version will be the output from the transform image function)
            image_versions.append(img.copy())


        self.img_width = img.shape[1]
        self.img_height = img.shape[0]
        

        for pixel_area in  self.pixel_areas_dict.values():
            
            rgb_formula_id = pixel_area.f_id
            if(rgb_formula_id not in self.rgb_formulas_dict.keys()):#execute this code if the rgb formula id (of the current pixel area) does not exist
                continue
            
            image_version_input = image_versions[pixel_area.img_in_v]
            pixel_areas_as_parameters_for_rgb_formula = self.get_pixel_areas_as_parameters_for_rgb_formula(pixel_area_input = pixel_area, img=image_version_input)#this is a numpy array of shape (AREA, Height, Width, 3[RGB])
            if(pixel_areas_as_parameters_for_rgb_formula.shape[0] == 0):#execute this code if no image pixel areas were extracted from the current pixel area (usually occurs when the top left corner of the current pixel area is outside the image)
                continue
            
            #the rgb formula is this `eval(f"lambda r,g,b,areas_count: np.stack([ {self.red_func}, {self.green_func}, {self.blue_func} ], axis=-1)")`
            rgb_formula = self.rgb_formulas_dict[pixel_area.f_id].rgb_function
            rgb_formula_result = rgb_formula(r = pixel_areas_as_parameters_for_rgb_formula[:,:,:,0], g = pixel_areas_as_parameters_for_rgb_formula[:,:,:,1], b = pixel_areas_as_parameters_for_rgb_formula[:,:,:,2], areas_count = pixel_areas_as_parameters_for_rgb_formula.shape[0])

            starting_image_version = pixel_area.img_out_v
            ending_image_version = pixel_area.img_out_v + pixel_area.img_out_stack
            for i in range(starting_image_version, ending_image_version):
                if(i > self.image_versions_count):
                    break

                image_versions[i][ pixel_area.y : pixel_area.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], pixel_area.x : pixel_area.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ] = rgb_formula_result

            #make sure the last image version (the special one) is always updated
            image_versions[-1][ pixel_area.y : pixel_area.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], pixel_area.x : pixel_area.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ] = rgb_formula_result
       
        
        return image_versions[-1]#always returns the last image version (the special one)


     #creates and returns the image pixel areas (as numpy array of shape (AREA, Height, Width, 3[RGB])) obtinaed from the the values of `id`, `p_ids`, `p_x`, `p_y` of the input pixel area
    def get_pixel_areas_as_parameters_for_rgb_formula(self, pixel_area_input:Pixel_area, img:np) -> np:
        
        areas_from_img:list[np.array] = []

        (area_width, area_height) = self.get_proper_width_and_height_for_areas_used_by_area(pixel_area_input=pixel_area_input)

        #if the top left corner of the input pixel area is outside the image execute this code
        if(area_width == -1 or area_height == -1):
            return np.array([])
        
        #this image area is created from the input pixel area
        area_from_img = img[pixel_area_input.y : pixel_area_input.y + area_height, pixel_area_input.x : pixel_area_input.x + area_width, : ]
        areas_from_img.append(area_from_img)
        
        if(pixel_area_input.p_ids is not None):
            #those image areas are created from the pixel areas whose id was found in `p_ids` of the input pixel area
            for pixel_area_id in pixel_area_input.p_ids:

                #get only those pixel areas which have an existing id
                if(pixel_area_id in self.pixel_areas_dict.keys()):
                    pixel_area = self.pixel_areas_dict[pixel_area_id]

                    #get only those pixel areas whose top left corner is inside the image
                    if(pixel_area.x < self.img_width and pixel_area.y < self.img_height):                
                        area_from_img = img[ pixel_area.y : pixel_area.y + area_height, pixel_area.x : pixel_area.x + area_width : ]
                        areas_from_img.append(area_from_img)
        

        #those image areas are created from the top left corners obtined from the values of `p_x` and `p_y` of the input pixel area
        if(pixel_area_input.p_x is not None and pixel_area_input.p_y is not None):
            anonymous_areas_count = min(len(pixel_area_input.p_x), len(pixel_area_input.p_y))        
            for i in range(0, anonymous_areas_count):

                #skip the anonymous pixel areas whose top left corner is outside the image
                if(pixel_area_input.p_x[i] < self.img_width and pixel_area_input.p_y[i] < self.img_height):
                    area_from_img = img[pixel_area_input.p_y[i] : pixel_area_input.p_y[i] + area_height, pixel_area_input.p_x[i] : pixel_area_input.p_x[i] + area_width, : ]
                    areas_from_img.append(area_from_img)
        
        return np.array(areas_from_img)
    

    def get_proper_width_and_height_for_areas_used_by_area(self, pixel_area_input:Pixel_area):
        
        widths = []
        heights = []

        (area_width, area_height) = self.get_proper_width_and_height(x = pixel_area_input.x, y = pixel_area_input.y, width = pixel_area_input.w, height = pixel_area_input.h)
        if(area_width==-1 or area_height ==-1):
            return -1, -1
        
        widths.append(area_width)
        heights.append(area_height)

        if(pixel_area_input.p_ids is not None):
            #cycle through the areas from the input pixel area whose id was found in `p_ids`
            for pixel_area_id in pixel_area_input.p_ids:

                #check only those pixel areas which have an existing id
                if(pixel_area_id in self.pixel_areas_dict.keys()):
                    pixel_area = self.pixel_areas_dict[pixel_area_id]

                    (area_width, area_height) = self.get_proper_width_and_height(x = pixel_area.x, y = pixel_area.y, width = pixel_area.w, height = pixel_area.h)
                    if(area_width!=-1 and area_height !=-1):
                        widths.append(area_width)
                        heights.append(area_height)
        
        #those image areas are taken from the top left corners obtined from the values of `p_x` and `p_y` of the input pixel area
        if(pixel_area_input.p_x is not None and pixel_area_input.p_y is not None):
            anonymous_areas_count = min(len(pixel_area_input.p_x), len(pixel_area_input.p_y))        
            for i in range(0, anonymous_areas_count):                

                (area_width, area_height) = self.get_proper_width_and_height(x = pixel_area_input.p_x[i], y = pixel_area_input.p_y[i], width = pixel_area_input.w, height = pixel_area_input.h)
                if(area_width!=-1 and area_height !=-1):
                    widths.append(area_width)
                    heights.append(area_height)
        
        min_width = min(widths)
        min_height = min(heights)

        return (min_width, min_height)


    def get_proper_width_and_height(self, x:int, y:int, width: int, height: int):
        
        #execute this code if the top left corner is outside the canvas 
        if(self.img_width <= x or self.img_height <= y):
            return -1, -1

        area_width = min(width, self.img_width-x)
        area_height = min(height, self.img_height-y)

        return (area_width, area_height)