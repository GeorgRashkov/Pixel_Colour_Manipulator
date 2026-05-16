from __future__ import annotations

from Z_Pixel_area import Pixel_area
from Z_RGB_formula import RGB_formula
import numpy as np
from Z_Image_version_controller import Image_version_controller
from Z_Areas_behiour_when_resizing_main_window import Areas_behaviour_when_resizing_main_window

from Z_Pixel_area_animation_manipulator import Pixel_area_animation_manipulator



class Pixel_areas_manipulator:

    def __init__(self, pixel_areas_dict: dict[int,Pixel_area], rgb_formulas_dict: dict[int,RGB_formula], animations_manipulator:Pixel_area_animation_manipulator, areas_behiour_when_resizing_main_window:Areas_behaviour_when_resizing_main_window, get_inner_areas_fast:bool):
        
        self.pixel_areas_dict = pixel_areas_dict
        self.rgb_formulas_dict = rgb_formulas_dict
        
        self.img_height = 0
        self.img_width = 0
        
        self.image_versions_count = 0  #this is the number of image versions defined by the user (when the image is processed there will be 2 additional image versions)   
        self.max_image_versions = 99

        self.set_image_versions()

        
        self.areas_behiour_when_resizing_main_window:Areas_behaviour_when_resizing_main_window = areas_behiour_when_resizing_main_window

        
        self.rectangles_per_area: dict[int, list[Rectangle]]= None #the main dictionary has key-value pairs for pixel area; the key is the area id while the value is the rectangles which are used by the area  

        self.image_versions_controller = None
        self.initial_image_width = 100
        self.initial_image_height = 100

        self.get_inner_areas_fast = get_inner_areas_fast

        self.animations_manipulator = animations_manipulator

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

        #for each area create the rectangles used by the areas only when the size of the input image is not the same as the size of the previous image which was passed to the method
        must_create_new_rectangles = True 
        #must_create_new_rectangles = False
        if(self.img_width != img.shape[1] or self.img_height != img.shape[0]):
            self.img_width = img.shape[1]
            self.img_height = img.shape[0]
            must_create_new_rectangles = True
            self.rectangles_per_area = {}
        
        
        

        for pixel_area in  self.pixel_areas_dict.values():

            if(self.animations_manipulator is not None):
                self.animations_manipulator.apply_animations(pixel_area=pixel_area, img=img)

            
            rgb_formula_id = pixel_area.f_id
            if(rgb_formula_id not in self.rgb_formulas_dict.keys()):#execute this code if the rgb formula id (of the current pixel area) does not exist
                continue
            
            image_version_input = image_versions[pixel_area.img_in_v]
            rgb_formula_dynamic_variables = np.array(pixel_area.current_f_vars, dtype=np.uint8) if( len(pixel_area.current_f_vars) > 0 ) else np.array([0], dtype=np.uint8)
            
            #this is a numpy array of shape (AREA, Height, Width, 3[RGB])
            pixel_areas_as_parameters_for_rgb_formula = None
            if(self.get_inner_areas_fast == True):
                pixel_areas_as_parameters_for_rgb_formula = self.get_image_areas_as_parameters_for_rgb_formula__fast(pixel_area_input = pixel_area, img=image_version_input, must_create_new_rectangles=must_create_new_rectangles) 
            else:
                pixel_areas_as_parameters_for_rgb_formula = self.get_image_areas_as_parameters_for_rgb_formula(pixel_area_input = pixel_area, img=image_version_input, must_create_new_rectangles=must_create_new_rectangles, rgb_formula_dynamic_variables=rgb_formula_dynamic_variables)
            
            if(pixel_areas_as_parameters_for_rgb_formula.shape[0] == 0):#execute this code if no rectangles were extracted from the current pixel area (usually occurs when the top left corner of the current pixel area is outside the image)
                continue
            
            #the rgb formula is this `eval(f"lambda r,g,b,areas_count,v=[0]: np.stack([ {self.red_func}, {self.green_func}, {self.blue_func} ], axis=-1)")`
            rgb_formula = self.rgb_formulas_dict[pixel_area.f_id].rgb_function
            rgb_formula_result = rgb_formula(r = pixel_areas_as_parameters_for_rgb_formula[:,:,:,0], g = pixel_areas_as_parameters_for_rgb_formula[:,:,:,1], b = pixel_areas_as_parameters_for_rgb_formula[:,:,:,2], areas_count = pixel_areas_as_parameters_for_rgb_formula.shape[0], v = rgb_formula_dynamic_variables)
            pixel_area.update_dynamic_variables_for_rgb_function()

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
            rectangles = self.get_rectangles_used_by_area(pixel_area_input=pixel_area_input)
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
    def get_image_areas_as_parameters_for_rgb_formula(self, pixel_area_input:Pixel_area, img:np, must_create_new_rectangles:bool, rgb_formula_dynamic_variables:np) -> np:
        
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
        
        
        rec_index = 0

       
        for rec in rectangles:
           
            area_from_img = self.get_result_after_applying_used_area_on_main_area(main_area = pixel_area_input, main_area_rec=rectangles[0], used_area_rec=rec, img = img, rec_index=rec_index, rgb_formula_dynamic_variables=rgb_formula_dynamic_variables)

            rec_index+=1

            areas_from_img.append(area_from_img)
        
        return np.array(areas_from_img)

      
    

    #the image must be a numpy array of shape [height, width, RGB channels]
    def rotate_replica_area(self, img:np, used_area_width:int, used_area_height:int, used_area_x_left_corner:int, used_area_x_right_corner:int, used_area_y_top_corner:int, used_area_y_bottom_corner:int, rotation_number:int):
       
        #simple rotations
        if(rotation_number == 1):
                        
            used_area_size = min(used_area_width, used_area_height)  

            arr_helper:np = img[used_area_y_bottom_corner - used_area_size : used_area_y_bottom_corner, used_area_x_left_corner : used_area_x_left_corner + used_area_size, :]
            arr_helper = arr_helper[::-1,:,:]
            arr_helper = arr_helper.transpose([1,0,2])
            
            img = np.copy(img[used_area_y_top_corner:used_area_y_bottom_corner, used_area_x_left_corner:used_area_x_right_corner, :])
            img[0:used_area_size, 0:used_area_size] = arr_helper  
            

        elif(rotation_number == 2):
            img = img[used_area_y_top_corner:used_area_y_bottom_corner, used_area_x_left_corner:used_area_x_right_corner, :]
            img = img[::-1,::-1,:]

        elif(rotation_number == 3):

            used_area_size = min(used_area_width, used_area_height) 

            arr_helper:np = img[used_area_y_top_corner:used_area_y_top_corner+used_area_size, used_area_x_left_corner : used_area_x_left_corner + used_area_size, :]
            arr_helper = arr_helper[:,::-1,:]
            arr_helper = arr_helper.transpose([1,0,2])
            
            img = np.copy(img[used_area_y_top_corner:used_area_y_bottom_corner, used_area_x_left_corner:used_area_x_right_corner, :])
            img[0:used_area_size, 0:used_area_size] = arr_helper 
            
        

        #mirror
        elif(rotation_number == 4):
            img = img[used_area_y_top_corner:used_area_y_bottom_corner, used_area_x_left_corner:used_area_x_right_corner, :]
            img = img[:,::-1,:]
       
        

        #rotations with mirror
        elif(rotation_number == 5):

            used_area_size = min(used_area_width, used_area_height) 

            arr_helper:np = img[used_area_y_top_corner:used_area_y_top_corner+used_area_size, used_area_x_left_corner : used_area_x_left_corner + used_area_size, :]
            arr_helper = arr_helper.transpose([1,0,2])
            
            img = np.copy(img[used_area_y_top_corner:used_area_y_bottom_corner, used_area_x_left_corner:used_area_x_right_corner, :])
            img[0:used_area_size, 0:used_area_size] = arr_helper 

        elif(rotation_number == 6):
            img = img[used_area_y_top_corner:used_area_y_bottom_corner, used_area_x_left_corner:used_area_x_right_corner, :]
            img = img[::-1,:,:]

        elif(rotation_number == 7):

            used_area_size = min(used_area_width, used_area_height) 

            arr_helper:np = img[used_area_y_top_corner:used_area_y_top_corner+used_area_size, used_area_x_left_corner : used_area_x_left_corner + used_area_size, :]
            arr_helper = arr_helper[::-1,::-1,:]
            arr_helper = arr_helper.transpose([1,0,2])
            
            img = np.copy(img[used_area_y_top_corner:used_area_y_bottom_corner, used_area_x_left_corner:used_area_x_right_corner, :])
            img[0:used_area_size, 0:used_area_size] = arr_helper
        

        
        #original image
        else:
            img = img[used_area_y_top_corner:used_area_y_bottom_corner, used_area_x_left_corner:used_area_x_right_corner, :]
        
        return img



   


    def get_result_after_applying_used_area_on_main_area(self, main_area:Pixel_area, main_area_rec:Rectangle, used_area_rec:Rectangle, img:np, rec_index:int, rgb_formula_dynamic_variables:np) -> np:
        
        replica_width = 0
        if(main_area.w_rep_p1[rec_index] > 0 or main_area.w_rep_p2[rec_index] > 0):
            replica_width = min(100, main_area.w_rep_p1[rec_index])/100*main_area_rec.w + min(100, main_area.w_rep_p2[rec_index])/100*used_area_rec.w
            replica_width = min(int(replica_width), used_area_rec.w, main_area_rec.w)
        else:
            replica_width = min(used_area_rec.w, main_area_rec.w)

        replica_height = 0
        if(main_area.h_rep_p1[rec_index] > 0 or main_area.h_rep_p2[rec_index] > 0):
            replica_height = min(100, main_area.h_rep_p1[rec_index])/100*main_area_rec.h + min(100, main_area.h_rep_p2[rec_index])/100*used_area_rec.h
            replica_height = min(int(replica_height), used_area_rec.h, main_area_rec.h)
        else:
            replica_height = min(used_area_rec.h, main_area_rec.h)

        
        main_area_from_img = np.copy(img[main_area_rec.y : main_area_rec.y + main_area_rec.h, main_area_rec.x : main_area_rec.x + main_area_rec.w, : ])
        used_area_from_img = img[used_area_rec.y : used_area_rec.y + used_area_rec.h, used_area_rec.x : used_area_rec.x + used_area_rec.w, : ]
         
        
        rep_x_ratio_p1 = main_area_rec.w/100
        rep_y_ratio_p1 = main_area_rec.h/100
        
        x_rep_start_p1 = int(main_area.x_rep_start_p1[rec_index]*rep_x_ratio_p1)
        y_rep_start_p1 = int(main_area.y_rep_start_p1[rec_index]*rep_y_ratio_p1)
        x_rep_end_p1 = int(main_area.x_rep_end_p1[rec_index]*rep_x_ratio_p1)
        y_rep_end_p1 = int(main_area.y_rep_end_p1[rec_index]*rep_y_ratio_p1)
        x_rep_step_p1 = int(main_area.x_rep_step_p1[rec_index]*rep_x_ratio_p1)
        y_rep_step_p1 = int(main_area.y_rep_step_p1[rec_index]*rep_y_ratio_p1)
        inner_area_y_p1 = y_rep_start_p1
        inner_area_x_p1 = x_rep_start_p1


        rep_x_ratio_p2 = used_area_rec.w/100
        rep_y_ratio_p2 = used_area_rec.h/100

        x_rep_start_p2 = int(main_area.x_rep_start_p2[rec_index]*rep_x_ratio_p2)
        y_rep_start_p2 = int(main_area.y_rep_start_p2[rec_index]*rep_y_ratio_p2)
        x_rep_end_p2 = int(main_area.x_rep_end_p2[rec_index]*rep_x_ratio_p2)
        y_rep_end_p2 = int(main_area.y_rep_end_p2[rec_index]*rep_y_ratio_p2)
        x_rep_step_p2 = int(main_area.x_rep_step_p2[rec_index]*rep_x_ratio_p2) + replica_width
        y_rep_step_p2 = int(main_area.y_rep_step_p2[rec_index]*rep_y_ratio_p2) + replica_height
        inner_area_y_p2 = y_rep_start_p2
        inner_area_x_p2 = x_rep_start_p2


        x_rep_count_p1 = main_area.x_rep_count_p1[rec_index]
        y_rep_count_p1 = main_area.y_rep_count_p1[rec_index]
        x_rep_count_p2 = main_area.x_rep_count_p2[rec_index]
        y_rep_count_p2 = main_area.y_rep_count_p2[rec_index]

        inner_area_height_helper = replica_height
        inner_area_width_helper = replica_width

        rows_count_p1 = 0
        columns_count_p1 = 0

        rows_count_p2 = 0
        columns_count_p2 = 0


        rep_index = 0 #this is the index of the replicas created by the current used area (rectangle)
        
        #cycle through the rows of the main area
        while(inner_area_y_p1 < main_area_rec.h):
            
        #<make sure the replicas are inside the image, the used area and the main area (y)

            #make sure the replica is inside the main area (vertical)
            if(inner_area_y_p1 + replica_height > y_rep_end_p1):
                inner_area_height_helper = y_rep_end_p1 - inner_area_y_p1
                if(inner_area_height_helper <= 0):
                    break
            else:
                inner_area_height_helper = replica_height
            
            #make sure the replica is inside the used area (vertical)
            if(inner_area_y_p2 + inner_area_height_helper > y_rep_end_p2):
                inner_area_height_helper = y_rep_end_p2 - inner_area_y_p2
                if(inner_area_height_helper <= 0):
                    break
                    
            
            #make sure the main and used areas are inside the image (vertical)
            if(inner_area_y_p1 + inner_area_height_helper > main_area_from_img.shape[0]):
                inner_area_height_helper = main_area_from_img.shape[0] - inner_area_y_p1
                if(inner_area_height_helper <= 0):
                    break
            if(inner_area_y_p2 + inner_area_height_helper > img.shape[0]):
                inner_area_height_helper = img.shape[0] - inner_area_y_p2
                if(inner_area_height_helper <= 0):
                    break
            
        #make sure the replicas are inside the image, the used area and the main area (y)>

            #cycle through the columns of the main area
            while(inner_area_x_p1 < main_area_rec.w):
                
            #<make sure the replicas are inside the image, the used area and the main area (x)

                #make sure the replica is inside the main area (horizontal)
                if(inner_area_x_p1 + replica_width > x_rep_end_p1):
                    inner_area_width_helper = x_rep_end_p1 - inner_area_x_p1
                    if(inner_area_width_helper <= 0):
                        break
                else:
                    inner_area_width_helper = replica_width

                #make sure the replica is inside the used area (horizontal)
                if(inner_area_x_p2 + inner_area_width_helper > x_rep_end_p2):
                    inner_area_width_helper = x_rep_end_p2 - inner_area_x_p2
                    if(inner_area_width_helper <= 0):
                        break
                
                #make sure the main and used areas are inside the image (horizontal)
                if(inner_area_x_p1 + inner_area_width_helper > main_area_from_img.shape[1]):
                    inner_area_width_helper = main_area_from_img.shape[1] - inner_area_x_p1
                    if(inner_area_width_helper <= 0):
                        break
                if(inner_area_x_p2 + inner_area_width_helper > img.shape[1]):
                    inner_area_width_helper = img.shape[1] - inner_area_x_p2
                    if(inner_area_width_helper <= 0):
                        break
                
            #make sure the replicas are inside the image, the used area and the main area (x)>

                
                #apply the current replica to the main area
                main_area_from_img[inner_area_y_p1: inner_area_y_p1 + inner_area_height_helper, inner_area_x_p1:inner_area_x_p1 + inner_area_width_helper, :] = used_area_from_img[inner_area_y_p2 : inner_area_y_p2 + inner_area_height_helper, inner_area_x_p2: inner_area_x_p2 + inner_area_width_helper, :]               
                
            
            #<apply rgb formulas and rotations to the replica
                
                #make sure the current used area (rectangle) has a collection of ids of RGB formulas
                if(len(main_area.f_ids_rep) > rec_index):
                    #make sure the collection of ids of RGB formulas for the current used area (rectangle) is not empty
                    if(len(main_area.f_ids_rep[rec_index]) > 0):
                        rgb_formula_index = rep_index % len(main_area.f_ids_rep[rec_index])
                        rgb_formula_id = main_area.f_ids_rep[rec_index][rgb_formula_index]
                        
                        if(rgb_formula_id in self.rgb_formulas_dict.keys()):
                                                        
                            rep_area:np = used_area_from_img[inner_area_y_p2 : inner_area_y_p2 + inner_area_height_helper, inner_area_x_p2: inner_area_x_p2 + inner_area_width_helper, :]
                            if(len(main_area.rotations_rep) > rec_index):
                                if(len(main_area.rotations_rep[rec_index]) > 0):
                                    rotation_index = rep_index % len(main_area.rotations_rep[rec_index])
                                    rotation_number = main_area.rotations_rep[rec_index][rotation_index]
                                    rep_area = self.rotate_replica_area(img = used_area_from_img,  used_area_width=inner_area_width_helper, used_area_height=inner_area_height_helper, used_area_x_left_corner=inner_area_x_p2, used_area_x_right_corner=inner_area_x_p2+inner_area_width_helper, used_area_y_top_corner=inner_area_y_p2,  used_area_y_bottom_corner=inner_area_y_p2+inner_area_height_helper, rotation_number=rotation_number)

                            rep_area = rep_area.reshape(1, rep_area.shape[0], rep_area.shape[1], rep_area.shape[2])
                            rgb_formula = self.rgb_formulas_dict[rgb_formula_id].rgb_function
                            rgb_formula_result = rgb_formula(r = rep_area[:,:,:,0], g = rep_area[:,:,:,1], b = rep_area[:,:,:,2], areas_count = 1, v = rgb_formula_dynamic_variables)
                            main_area_from_img[inner_area_y_p1: inner_area_y_p1 + inner_area_height_helper, inner_area_x_p1:inner_area_x_p1 + inner_area_width_helper, :] = rgb_formula_result
            
            #apply rgb formulas and rotations to the replica>           
                
                #increase the index of the replicas
                rep_index+=1
            
            #<move to the next column
                
                inner_area_x_p2 += x_rep_step_p2
                columns_count_p2 += 1
                if(inner_area_x_p2 >= x_rep_end_p2 or columns_count_p2 >= x_rep_count_p2):
                    columns_count_p2 = 0
                    inner_area_x_p2 = x_rep_start_p2
                
                inner_area_x_p1 += x_rep_step_p1 + inner_area_width_helper
                columns_count_p1 += 1
                if(inner_area_x_p1 >= x_rep_end_p1 or columns_count_p1 >= x_rep_count_p1):
                    break

            #move to the next column>

        #<reset the columns when moving to the next row of the main area
            
            columns_count_p1 = 0
            inner_area_x_p1 = x_rep_start_p1
            if(main_area.x_rep_count_p1[rec_index] == main_area.x_rep_count_p2[rec_index]):
                        columns_count_p2 = 0
                        inner_area_x_p2 = x_rep_start_p2

        #reset the columns when moving to the next row of the main area>

        #<move to the next row

            inner_area_y_p2 += y_rep_step_p2
            rows_count_p2 += 1
            if(inner_area_y_p2 >= y_rep_end_p2 or rows_count_p2 >= y_rep_count_p2):
                rows_count_p2 = 0
                inner_area_y_p2 = y_rep_start_p2

            inner_area_y_p1 += y_rep_step_p1 + inner_area_height_helper
            rows_count_p1 += 1
            if(inner_area_y_p1 >= y_rep_end_p1  or rows_count_p1 >= y_rep_count_p1):
                break
        
        #move to the next row>
                           
        return main_area_from_img




    #<functions for creating rectangles used by pixel area 

    def get_rectangles_used_by_area(self, pixel_area_input:Pixel_area) -> list["Rectangle"]:
        
        rectangles: list[Rectangle] = []


        #<this is the input pixel area
        rectangle = self.get_proper_rectangle(x = pixel_area_input.x, y = pixel_area_input.y, width = pixel_area_input.w, height = pixel_area_input.h)
        if(rectangle is None):
            return None
        
        rectangles.append(rectangle)        
        #this is the input pixel area>


        #<those are the areas defined by `p_ids` of the input pixel area
        
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
        
        if(self.get_inner_areas_fast == True):
            #make sure all rectangles have the width and height of the smallest one/s
            min_width = min(retangle.w for retangle in rectangles)
            min_height = min(retangle.h for retangle in rectangles)
            for rec in rectangles:
                rec.w = min_width
                rec.h = min_height

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