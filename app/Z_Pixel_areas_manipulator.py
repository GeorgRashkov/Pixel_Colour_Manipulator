from Z_Pixel_area import Pixel_area
from Z_RGB_formula import RGB_formula
import numpy as np
from Z_Image_version_controller import Image_version_controller
from Z_Areas_behiour_when_resizing_main_window import Areas_behaviour_when_resizing_main_window

class Pixel_areas_manipulator:

    def __init__(self, pixel_areas_dict: dict[int,Pixel_area], rgb_formulas_dict: dict[int,RGB_formula], areas_behiour_when_resizing_main_window:Areas_behaviour_when_resizing_main_window, get_inner_areas_fast:bool):
        
        self.pixel_areas_dict = pixel_areas_dict
        self.rgb_formulas_dict = rgb_formulas_dict
        
        self.img_height = 0
        self.img_width = 0
        
        self.image_versions_count = 0  #this is the number of image versions defined by the user (when the image is processed there will be 2 additional image versions)   
        self.max_image_versions = 99

        self.set_image_versions()

        # in testing state!!!!!!!!!!!!
        self.areas_behiour_when_resizing_main_window:Areas_behaviour_when_resizing_main_window = areas_behiour_when_resizing_main_window

        #self.movable_rectangles = movable_rectangles 
        self.rectangles_per_area: dict[int, list[Rectangle]]= None #the main dictionary has key-value pairs for pixel area; the key is the area id while the value is the rectangles which are used by the area  

        self.image_versions_controller = None
        self.initial_image_width = 100
        self.initial_image_height = 100

        self.get_inner_areas_fast = get_inner_areas_fast

    #this function must be called from outside
    #this method must be called always when the desired output image version from the manipulator is different from the last version
    def create_image_version_controller(self, image_version_start_index:int = 0, image_version_increment:int = 1, image_version_swap_frequency:int = 1):
        self.image_versions_controller = Image_version_controller(image_version_start_index = image_version_start_index, image_version_increment = image_version_increment, image_version_swap_frequency = image_version_swap_frequency, image_versions_count = self.image_versions_count+2)

    #this function must be called from outside
    #this method must be called always when resize behaviour of the areas is set to `Keep_aspect_ratio`
    #the values the input parameters must be width and height of the canvas
    def set_aspect_ratio(self, initial_image_width, initial_image_height):

        self.initial_image_width = initial_image_width
        self.initial_image_height = initial_image_height



    #< functions for setting the image versions
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
    #functions for setting the image versions>



    #this is the main function for applying the manipulator on an image
    #this function must be called from outside
    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def transform_image(self, img:np) -> np.array:       

        image_versions : list[np.array] = []
        for i in range(self.image_versions_count + 2):#adding 2 additional image versions (the first image version will always have pixel values of the original image; the last image version will be the output from the transform image function)
            image_versions.append(img.copy())

        #for each area create the rectangles used by the areas only when the size of the input image is not the same as the previous image which was passed to the method
        must_create_new_rectangles = False
        if(self.img_width != img.shape[1] or self.img_height != img.shape[0]):
            self.img_width = img.shape[1]
            self.img_height = img.shape[0]
            must_create_new_rectangles = True
            self.rectangles_per_area = {}
        
        
        

        for pixel_area in  self.pixel_areas_dict.values():
            
            rgb_formula_id = pixel_area.f_id
            if(rgb_formula_id not in self.rgb_formulas_dict.keys()):#execute this code if the rgb formula id (of the current pixel area) does not exist
                continue
            
            image_version_input = image_versions[pixel_area.img_in_v]

            #this is a numpy array of shape (AREA, Height, Width, 3[RGB])
            pixel_areas_as_parameters_for_rgb_formula = None
            if(self.get_inner_areas_fast == True):
                pixel_areas_as_parameters_for_rgb_formula = self.get_image_areas_as_parameters_for_rgb_formula__fast(pixel_area_input = pixel_area, img=image_version_input, must_create_new_rectangles=must_create_new_rectangles) 
            else:
                pixel_areas_as_parameters_for_rgb_formula = self.get_image_areas_as_parameters_for_rgb_formula(pixel_area_input = pixel_area, img=image_version_input, must_create_new_rectangles=must_create_new_rectangles)
            
            if(pixel_areas_as_parameters_for_rgb_formula.shape[0] == 0):#execute this code if no rectangles were extracted from the current pixel area (usually occurs when the top left corner of the current pixel area is outside the image)
                continue
            
            #the rgb formula is this `eval(f"lambda r,g,b,areas_count: np.stack([ {self.red_func}, {self.green_func}, {self.blue_func} ], axis=-1)")`
            rgb_formula = self.rgb_formulas_dict[pixel_area.f_id].rgb_function
            rgb_formula_result = rgb_formula(r = pixel_areas_as_parameters_for_rgb_formula[:,:,:,0], g = pixel_areas_as_parameters_for_rgb_formula[:,:,:,1], b = pixel_areas_as_parameters_for_rgb_formula[:,:,:,2], areas_count = pixel_areas_as_parameters_for_rgb_formula.shape[0])

            starting_image_version = pixel_area.img_out_v
            ending_image_version = pixel_area.img_out_v + pixel_area.img_out_stack
            for i in range(starting_image_version, ending_image_version):
                if(i > self.image_versions_count):
                    break
                
                rectangle = self.rectangles_per_area[pixel_area.id][0]#the first rectangle used by the area is the rectangle of the area itself

                if(self.get_inner_areas_fast == True):
                    image_versions[i][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ] = rgb_formula_result
                else:
                    area_shape = image_versions[i][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ].shape
                    image_versions[i][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ] = rgb_formula_result[0:area_shape[0], 0:area_shape[1], :]
                    

            #make sure the last image version (the special one) is always updated
            if(self.get_inner_areas_fast == True):
                image_versions[-1][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ] = rgb_formula_result
            else:
                area_shape = image_versions[-1][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ].shape
                image_versions[-1][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ] = rgb_formula_result[0:area_shape[0], 0:area_shape[1], :]
            

        #determine the image version to return (the first and the last image versions are special ones)
        output_image_version_index = -1 if self.image_versions_controller is None else self.image_versions_controller.get_next_image_version_index()
        return image_versions[output_image_version_index]


    #creates and returns the image pixel areas (as numpy array of shape (AREA, Height, Width, 3[RGB])) obtinaed from the the values of `id`, `p_ids`, `p_x`, `p_y` of the input pixel area
    def get_image_areas_as_parameters_for_rgb_formula__fast(self, pixel_area_input:Pixel_area, img:np, must_create_new_rectangles:bool) -> np:
        
        rectangles = None
        if(must_create_new_rectangles == True):
            rectangles = self.get_rectangles_used_by_area__fast(pixel_area_input=pixel_area_input)
            self.rectangles_per_area[pixel_area_input.id] = rectangles
        else:
            rectangles = self.rectangles_per_area[pixel_area_input.id]

        areas_from_img:list[np.array] = []

        #if the top left corner of the input pixel area is outside the image execute this code
        if(rectangles is None or len(rectangles) == 0):
            return np.array([])
       
        for rec in rectangles:
            area_from_img = img[rec.y : rec.y + rec.h, rec.x : rec.x + rec.w, : ]

            areas_from_img.append(area_from_img)

        return np.array(areas_from_img)


    #creates and returns the image pixel areas (as numpy array of shape (AREA, Height, Width, 3[RGB])) obtinaed from the the values of `id`, `p_ids`, `p_x`, `p_y` of the input pixel area
    def get_image_areas_as_parameters_for_rgb_formula(self, pixel_area_input:Pixel_area, img:np, must_create_new_rectangles:bool) -> np:
        
        rectangles = None
        if(must_create_new_rectangles == True):
            rectangles = self.get_rectangles_used_by_area(pixel_area_input=pixel_area_input)
            self.rectangles_per_area[pixel_area_input.id] = rectangles
        else:
            rectangles = self.rectangles_per_area[pixel_area_input.id]

        areas_from_img:list[np.array] = []

        #if the top left corner of the input pixel area is outside the image execute this code
        if(rectangles is None or len(rectangles) == 0):
            return np.array([])
        elif(must_create_new_rectangles == True):
            pixel_area_input.set_area_zeros(height=rectangles[0].h, width=rectangles[0].w) #area_zeros = np.zeros(shape=(rectangles[0].h, rectangles[0].w, 3))
        

        for rec in rectangles:

            area_width = min(rectangles[0].w, rec.w)#the first rectangle corresponds to the input pixel area
            area_height = min(rectangles[0].h, rec.h)#the first rectangle corresponds to the input pixel area
            
            area_from_img = pixel_area_input.get_area_zeros()#pixel_area_input.area_zeros.copy()
            area_from_img[0:area_height, 0:area_width, :] = img[rec.y : rec.y + area_height, rec.x : rec.x + area_width, :]

            areas_from_img.append(area_from_img)


        return np.array(areas_from_img)





    #<functions for creating rectangles used by pixel area 

    def get_rectangles_used_by_area__fast(self, pixel_area_input:Pixel_area) -> list["Rectangle"]:
        
        rectangles: list[Rectangle] = []


        #<this is the input pixel area
        rectangle = self.get_proper_rectangle(x = pixel_area_input.x, y = pixel_area_input.y, width = pixel_area_input.w, height = pixel_area_input.h)
        if(rectangle is None):
            return None
        
        rectangles.append(rectangle)        
        #this is the input pixel area>


        #<those are the areas defined by `p_ids` of the input pixel area
        if(pixel_area_input.p_ids is not None):
            #cycle through the areas from the input pixel area whose id was found in `p_ids`
            for pixel_area_id in pixel_area_input.p_ids:

                #check only those pixel areas which have an existing id
                if(pixel_area_id in self.pixel_areas_dict.keys()):
                    pixel_area = self.pixel_areas_dict[pixel_area_id]

                    rectangle = self.get_proper_rectangle(x = pixel_area.x, y = pixel_area.y, width = pixel_area.w, height = pixel_area.h)
                    if(rectangle is not None):
                        rectangles.append(rectangle)
        #those are the areas defined by `p_ids` of the input pixel area>  

        
        #<those image areas are taken from the top left corners obtained from the values of `p_x` and `p_y` of the input pixel area
        if(pixel_area_input.p_x is not None and pixel_area_input.p_y is not None):
            anonymous_areas_count = min(len(pixel_area_input.p_x), len(pixel_area_input.p_y))        
            for i in range(0, anonymous_areas_count):                
                
                rectangle = self.get_proper_rectangle(x = pixel_area_input.p_x[i], y = pixel_area_input.p_y[i], width = pixel_area_input.w, height = pixel_area_input.h)
                if(rectangle is not None):
                    rectangles.append(rectangle)
        #those image areas are taken from the top left corners obtained from the values of `p_x` and `p_y` of the input pixel area>

        
        
        #make sure all rectangles have the same width and height
        min_width = min(retangle.w for retangle in rectangles)
        min_height = min(retangle.h for retangle in rectangles)
        for rec in rectangles:
            rec.w = min_width
            rec.h = min_height
       
        return rectangles


    def get_rectangles_used_by_area(self, pixel_area_input:Pixel_area) -> list["Rectangle"]:
        
        rectangles: list[Rectangle] = []


        #<this is the input pixel area
        rectangle = self.get_proper_rectangle(x = pixel_area_input.x, y = pixel_area_input.y, width = pixel_area_input.w, height = pixel_area_input.h)
        if(rectangle is None):
            return None
        
        rectangles.append(rectangle)        
        #this is the input pixel area>


        #<those are the areas defined by `p_ids` of the input pixel area
        if(pixel_area_input.p_ids is not None):
            #cycle through the areas from the input pixel area whose id was found in `p_ids`
            for pixel_area_id in pixel_area_input.p_ids:

                #check only those pixel areas which have an existing id
                if(pixel_area_id in self.pixel_areas_dict.keys()):
                    pixel_area = self.pixel_areas_dict[pixel_area_id]

                    rectangle = self.get_proper_rectangle(x = pixel_area.x, y = pixel_area.y, width = pixel_area.w, height = pixel_area.h)
                    if(rectangle is not None):
                        rectangles.append(rectangle)
        #those are the areas defined by `p_ids` of the input pixel area>  

        
        #<those image areas are taken from the top left corners obtained from the values of `p_x` and `p_y` of the input pixel area
        if(pixel_area_input.p_x is not None and pixel_area_input.p_y is not None):
            anonymous_areas_count = min(len(pixel_area_input.p_x), len(pixel_area_input.p_y))        
            for i in range(0, anonymous_areas_count):                
                
                anonymous_area_x = pixel_area_input.p_x[i]
                anonymous_area_y = pixel_area_input.p_y[i]
                
                #if the top left corner of the anonymous area is outside the canvas don't create (nor add) rectangle
                if(anonymous_area_x >= self.initial_image_width or anonymous_area_y >= self.initial_image_height):
                    continue

                anonymous_area_width = min(pixel_area_input.w, self.initial_image_width-anonymous_area_x)
                anonymous_area_height = min(pixel_area_input.h, self.initial_image_height-anonymous_area_y)
                
                rectangle = self.get_proper_rectangle(x = anonymous_area_x, y = anonymous_area_y, width = anonymous_area_width, height = anonymous_area_height)
                if(rectangle is not None):
                    rectangles.append(rectangle)
        #those image areas are taken from the top left corners obtained from the values of `p_x` and `p_y` of the input pixel area>

        return rectangles



    def get_proper_rectangle(self, x:int, y:int, width: int, height: int) -> "Rectangle":
        
        rectangle = None

        if(self.areas_behiour_when_resizing_main_window == Areas_behaviour_when_resizing_main_window.Resize):
            rectangle = self.get_rectangle_which_can_resize(x=x, y=y, width=width, height=height)
        
        elif(self.areas_behiour_when_resizing_main_window == Areas_behaviour_when_resizing_main_window.Move):
            rectangle = self.get_rectangle_which_can_move(x=x, y=y, width=width, height=height)
        
        elif(self.areas_behiour_when_resizing_main_window == Areas_behaviour_when_resizing_main_window.Keep_aspect_ratio):
           rectangle = self.get_rectangle_which_keeps_aspect_ratio(x=x, y=y, width=width, height=height)
        
        return rectangle
        
    
    def get_rectangle_which_can_resize(self, x:int, y:int, width: int, height: int) -> "Rectangle":
        
        #execute this code if the top left corner is outside the image
        if(self.img_width <= x or self.img_height <= y):
            return None

        #make sure the width and height are not getting outside the image
        width = min(width, self.img_width-x)
        height = min(height, self.img_height-y)

        return Rectangle(x=x, y=y, w=width, h=height)

    
    def get_rectangle_which_can_move(self, x:int, y:int, width: int, height: int) -> "Rectangle":
        
        #set the values of `x` and `y` before setting the width and height (executed only if the rectangles are able to move)
        right_corner_x = x + width
        if(right_corner_x > self.img_width):
            x = max(0, x - (right_corner_x - self.img_width))
            
        right_corner_y = y + height
        if(right_corner_y > self.img_height):
            y = max(0, y - (right_corner_y - self.img_height))
            
        #make sure the width and height are not getting outside the image
        width = min(width, self.img_width-x)
        height = min(height, self.img_height-y)

        return Rectangle(x=x, y=y, w=width, h=height)

    
    def get_rectangle_which_keeps_aspect_ratio(self, x:int, y:int, width: int, height: int) -> "Rectangle":
        
        x_ratio = self.img_width/self.initial_image_width
        y_ratio = self.img_height/self.initial_image_height

        x = round(x*x_ratio)
        width = round(width*x_ratio)

        y = round(y*y_ratio)
        height = round(height*y_ratio)

        return Rectangle(x=x, y=y, w=width, h=height)

    #functions for creating rectangles used by pixel area>






class Rectangle():
    def __init__(self, x, y, w, h):
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h