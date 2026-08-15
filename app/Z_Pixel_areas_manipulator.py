from __future__ import annotations
import cv2

from Z_Pixel_area import Pixel_area, Rectangle, Replica
from Z_RGB_formula import RGB_formula
import numpy as np
from Z_Image_version_controller import Image_version_controller
from Z_Areas_behiour_when_resizing_main_window import Areas_behaviour_when_resizing_main_window

from Z_Pixel_area_animation_manipulator import Pixel_area_animation_manipulator
from Convolutional_kernels_manipulator import Convolutional_kernels_manipulator
from Z_Pixel_areas_mask import Mask

from Images_manipulator import Images_manipulator

from Order_obj import Order_obj
from Number_operatios import order_numbers

from Traspose_dimensions_list import traspose_dimensions_list

class Pixel_areas_manipulator:


    def __init__(self):
        
        self.pixel_areas_ids: list[int] = []

        self.pixel_areas_dict: dict[int,Pixel_area] = {}
        self.rgb_formulas_dict: dict[int,RGB_formula] = {}
        
        self.img_height:int = 0
        self.img_width:int = 0
        
        self.image_versions_count:int = 1  #this is the number of image versions defined by the user (when the image is processed there will be 1 or 2 additional image versions)   
        
        self.areas_behiour_when_resizing_main_window:Areas_behaviour_when_resizing_main_window = Areas_behaviour_when_resizing_main_window.Keep_aspect_ratio

        
        self.rectangles_per_area: dict[int, list[Rectangle]]= None #the main dictionary has key-value pairs for pixel area; the key is the area id while the value is the rectangles which are used by the area  

        self.image_versions_controller:Image_version_controller = None
        self.initial_image_width:int = 100
        self.initial_image_height:int = 100

        self.use_copy_for_replicas:bool = True
        self.use_copy_for_images: bool = True

        self.use_special_image_version:bool = True

        self.animations_manipulator:Pixel_area_animation_manipulator = None
        self.convolutional_kernels_manipulator:Convolutional_kernels_manipulator = None
        self.images_manipulator:Images_manipulator = None

        self.masks:dict[int, Mask] = {}

        self.images:dict[int, np.ndarray[np.uint8]] = {} #the keys are the indexes of the images while the values are the pixel values of the images represented as a numpy array

    
    def order_pixel_areas_ids(self, order_obj: Order_obj):
        self.pixel_areas_ids = order_numbers(nums=self.pixel_areas_ids, order_type=order_obj.order_type, start=order_obj.start, end=order_obj.end, step=order_obj.step)

    def get_pixel_areas_ids(self) -> list[int]:
        return self.pixel_areas_ids.copy()

    
    #This function must be called from outside
    #The function returns a dictionary which has the ids of the main areas for keys and the rectangles corresponding to the main areas for values 
    def get_all_main_areas_as_rectangles(self) -> dict[int, Rectangle]:
        
        rectangles_with_ids = {}

        for pixel_area in self.pixel_areas_dict.values():
            
            rectangle = self.get_proper_rectangle(x = pixel_area.x, y = pixel_area.y, width = pixel_area.w, height = pixel_area.h)
            if(rectangle is None):
                continue
        
            
            rectangles_with_ids[pixel_area.id] = rectangle
            
        return rectangles_with_ids
    
    def get_main_areas_as_rectangles(self, pixel_areas_ids:list[int]) -> list["Rectangle"]:
        
        rectangles: list[Rectangle] = []

        #<those are the areas used by the main pixel area
        
        #cycle through the ids of the used areas
        for pixel_area_id in pixel_areas_ids:

            #check whether the id of the current used area exists
            if(pixel_area_id in self.pixel_areas_dict.keys()):
                pixel_area = self.pixel_areas_dict[pixel_area_id]

                rectangle = self.get_proper_rectangle(x = pixel_area.x, y = pixel_area.y, width = pixel_area.w, height = pixel_area.h)
                if(rectangle is not None):
                    rectangles.append(rectangle)
        #those are the areas used by the main pixel area>  

        return rectangles
    
    
    #<Those functions must be called from the outside

    def apply_pixel_areas(self, pixel_areas_dict: dict[int,Pixel_area]):
        self.pixel_areas_ids = list(pixel_areas_dict.keys())
        self.pixel_areas_dict = pixel_areas_dict

    def apply_rgb_formulas(self, rgb_formulas_dict: dict[int,RGB_formula]):
        self.rgb_formulas_dict = rgb_formulas_dict
    
    def apply_animations(self, animations_manipulator:Pixel_area_animation_manipulator):
        self.animations_manipulator = animations_manipulator

    
    #the input parameter must be a dictionary which has the masks' ids for keys and the masks for values
    def apply_masks(self, masks:dict[int, Mask]): 
        self.masks = masks

    def apply_convolutional_kernels(self, cks_manipulator:Convolutional_kernels_manipulator):
        self.convolutional_kernels_manipulator = cks_manipulator


    #this method must be called always when the desired output image version from the manipulator is different from the last version
    def apply_image_version_controller(self,  image_version_start_index:int = -1, image_version_end_index:int = -1, image_version_increment:int = 0, image_version_swap_frequency:int = 0, image_versions_count:int = 1,  use_special_image_version:bool = True):
        
        image_versions_count = max(1, image_versions_count)
        self.image_versions_count = image_versions_count

        #adding 1 or 2 additional image versions (the first image version will always have the pixel values of the original image; if a special image version is used then the last image version will be the special one which is always updated)
        image_versions_count = image_versions_count + 1 + use_special_image_version
        self.image_versions_controller = Image_version_controller(start = image_version_start_index, end = image_version_end_index,step = image_version_increment, swap_frequency = image_version_swap_frequency, image_versions_count = image_versions_count)

        self.use_special_image_version = use_special_image_version
    
    def apply_images_manipulator(self, images_manipulator:Images_manipulator):
        self.images_manipulator = images_manipulator

    
    
    def remove_pixel_areas(self):
        self.pixel_areas_ids = []
        self.pixel_areas_dict = {}
    
    def remove_rgb_formulas(self):
        self.rgb_formulas_dict = {}
    
    def remove_animations(self):
        self.animations_manipulator = None

    def remove_masks(self):
        self.masks = {}
    
    def remove_convolutional_kernels(self):
        self.convolutional_kernels_manipulator = None
    
    def remove_image_version_controller(self):
        self.image_versions_controller = None

    def remove_images_manipulator(self):
        self.images_manipulator = None



    def set__areas_behaviour_when_resizing_main_window(self, areas_behiour_when_resizing_main_window:Areas_behaviour_when_resizing_main_window, aspect_ratio_width:int, aspect_ratio_height:int):
        
        self.areas_behiour_when_resizing_main_window = areas_behiour_when_resizing_main_window
        self.initial_image_width = aspect_ratio_width
        self.initial_image_height = aspect_ratio_height
    
    def set__use_copy_for_replicas(self, use_copy_for_replicas:bool):
        self.use_copy_for_replicas = use_copy_for_replicas

    def set__use_copy_for_images(self, use_copy_for_images:bool):
        self.use_copy_for_images = use_copy_for_images
    
    def set_pixel_area__size_location(self, id:int, pixel_area_rec:Rectangle, window_h:int, window_w:int):
        
        if(id in self.pixel_areas_dict.keys()):

            aspect_ratio_vertical = self.img_height/window_h
            aspect_ratio_horizontal = self.img_width/window_w
            
            pixel_area = self.pixel_areas_dict[id]

            pixel_area.y = int(pixel_area_rec.y * aspect_ratio_vertical)
            pixel_area.x = int(pixel_area_rec.x * aspect_ratio_horizontal)
            pixel_area.h = int(pixel_area_rec.h * aspect_ratio_vertical)
            pixel_area.w = int(pixel_area_rec.w * aspect_ratio_horizontal)

    #Those functions must be called from the outside>




    #< functions for setting the image versions
    #functions for setting the image versions>

    def set_images(self):

        if(self.images_manipulator is None):
            self.images = {}
            return

        images_indexes:list[int] = []

        for pixel_area_id in  self.pixel_areas_ids:
        
            pixel_area = self.pixel_areas_dict[pixel_area_id] 
            if(pixel_area.img_index is not None):
                images_indexes.append(pixel_area.img_index)

        self.images = self.images_manipulator.get_resized_images(indexes=images_indexes, new_width=self.img_width, new_height=self.img_height, get_copies=self.use_copy_for_images)



    #this is the main function for applying the manipulator on an image
    #this function must be called from outside
    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def transform_image(self, img:np, v:np.ndarray[np.uint8]) -> np.ndarray:

        if(len(self.pixel_areas_dict) == 0 or len(self.rgb_formulas_dict) == 0):
            return img       
        
        #adding 1 or 2 additional image versions (the first image version will always have the pixel values of the original image; if a special image version is used then the last image version will be the special one which is always updated)
        image_versions_count = self.image_versions_count + 1 + self.use_special_image_version
        image_versions : list[np.ndarray] = []
        for i in range(image_versions_count):
            image_versions.append(img.copy())

        #for each area create the rectangles used by the areas only when the size of the input image is not the same as the size of the previous image which was passed to the method
        must_create_new_rectangles = True 
        #must_create_new_rectangles = False
        if(self.img_width != img.shape[1] or self.img_height != img.shape[0]):
            self.img_width = img.shape[1]
            self.img_height = img.shape[0]
            must_create_new_rectangles = True
            self.rectangles_per_area = {}
        
        self.set_images()
        

        for pixel_area_id in  self.pixel_areas_ids:

            pixel_area = self.pixel_areas_dict[pixel_area_id]

            if(self.animations_manipulator is not None):
                self.animations_manipulator.apply_animations(pixel_area=pixel_area, img=img)

            
            rgb_formula_id = pixel_area.f_id
            if(rgb_formula_id not in self.rgb_formulas_dict.keys()):#execute this code if the rgb formula id (of the current pixel area) does not exist
                continue
            
            image_input = None
            if(pixel_area.img_index is not None):
                if(pixel_area.img_index in self.images.keys()):
                    image_input = self.images[pixel_area.img_index]
            if(image_input is None):
                image_input = image_versions[pixel_area.img_in_v if pixel_area.img_in_v<len(image_versions) else 0]
            
            rgb_formula_dynamic_variables = np.array(np.concatenate([pixel_area.current_f_vars, v]), dtype=np.uint8)
            rgb_formulas_for_masks:list = [self.rgb_formulas_dict[f_id] for f_id in pixel_area.mask_f_ids if f_id in self.rgb_formulas_dict]
            
            #this is a numpy array of shape (AREA, Height, Width, 3[RGB])
            pixel_areas_as_parameters_for_rgb_formula = self.get_image_areas_as_parameters_for_rgb_formula(pixel_area_input = pixel_area, img=image_input, must_create_new_rectangles=must_create_new_rectangles, rgb_formula_dynamic_variables=rgb_formula_dynamic_variables, rgb_formulas_for_masks=rgb_formulas_for_masks)
            
            if(pixel_areas_as_parameters_for_rgb_formula.shape[0] == 0):#execute this code if no rectangles were extracted from the current pixel area (usually occurs when the top left corner of the current pixel area is outside the image)
                continue
            
            if(len(pixel_area.mask_p_ids) > 0):
                if(pixel_area.mask_id_p in self.masks.keys()):
                    mask = self.masks[pixel_area.mask_id_p]
                    rectangles = self.get_main_areas_as_rectangles(pixel_areas_ids=pixel_area.mask_p_ids)
                    if(len(rectangles) > 0):
                        region_images = []
                        for rectangle in rectangles:
                            region_images.append(image_input[rectangle.y:rectangle.y+rectangle.h, rectangle.x:rectangle.x+rectangle.w,:])
                        pixel_areas_as_parameters_for_rgb_formula = mask.transform_image_using_other_images(img = pixel_areas_as_parameters_for_rgb_formula, region_images=region_images)

            if(pixel_area.mask_use_areas == True):
                if(pixel_area.mask_id in self.masks.keys() and len(rgb_formulas_for_masks)>0):
                    mask = self.masks[pixel_area.mask_id]
                    pixel_areas_as_parameters_for_rgb_formula = mask.transform_image(img = pixel_areas_as_parameters_for_rgb_formula, rgb_formulas=rgb_formulas_for_masks, rgb_formulas_dynamic_variables=rgb_formula_dynamic_variables)
            
            #the rgb formula is this `eval(f"lambda r,g,b,areas_count,v=[0]: np.stack([ {self.red_func}, {self.green_func}, {self.blue_func} ], axis=-1)")`
            rgb_formula = self.rgb_formulas_dict[pixel_area.f_id].rgb_function
            rgb_formula_result = rgb_formula(r = pixel_areas_as_parameters_for_rgb_formula[:,:,:,0], g = pixel_areas_as_parameters_for_rgb_formula[:,:,:,1], b = pixel_areas_as_parameters_for_rgb_formula[:,:,:,2], areas_count = pixel_areas_as_parameters_for_rgb_formula.shape[0], v = rgb_formula_dynamic_variables)
            rgb_formula_result = self.transpose_image(img=rgb_formula_result, pixel_area=pixel_area)
            pixel_area.update_dynamic_variables_for_rgb_function()

            if(pixel_area.mask_use_areas == False):
                if(pixel_area.mask_id in self.masks.keys() and len(rgb_formulas_for_masks)>0):
                    mask = self.masks[pixel_area.mask_id]
                    rgb_formula_result = mask.transform_image(img = rgb_formula_result, rgb_formulas=rgb_formulas_for_masks, rgb_formulas_dynamic_variables=rgb_formula_dynamic_variables)

            if(self.convolutional_kernels_manipulator is not None):
                if(pixel_area.ck_count > 0):
                    rgb_formula_result = self.convolutional_kernels_manipulator.transform_image_1(img = rgb_formula_result, cks_count_to_process = pixel_area.ck_count)
                if(len(pixel_area.ck_ids) > 0):
                    rgb_formula_result = self.convolutional_kernels_manipulator.transform_image_2(img = rgb_formula_result, cks_ids=pixel_area.ck_ids)

            
            #<apply the values of the transformed pixel area to the image versions which the area is supposed to update

            rectangle = self.rectangles_per_area[pixel_area.id][0]#the first rectangle used by the area is the rectangle of the area itself
            starting_image_version = pixel_area.img_out_v
            ending_image_version = pixel_area.img_out_v + pixel_area.img_out_stack

            for i in range(starting_image_version, ending_image_version):
                if(i > self.image_versions_count):
                    break

                area_shape = image_versions[i][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ].shape
                image_versions[i][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ] = rgb_formula_result[0:area_shape[0], 0:area_shape[1], :]
                    
            #apply the values of the transformed pixel area to the image versions which the area is supposed to update>
            
            
            #make sure the last image version (the special one) is always updated when the special image version is used
            if(self.use_special_image_version == True):
                area_shape = image_versions[-1][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ].shape
                image_versions[-1][ rectangle.y : rectangle.y + pixel_areas_as_parameters_for_rgb_formula.shape[1], rectangle.x : rectangle.x + pixel_areas_as_parameters_for_rgb_formula.shape[2], : ] = rgb_formula_result[0:area_shape[0], 0:area_shape[1], :]
               

        #determine the image version to return
        output_image_version_index = -1 if self.image_versions_controller is None else self.image_versions_controller.get_next_image_version_index()
        return image_versions[output_image_version_index]




    #creates and returns the image pixel areas (as numpy array of shape (AREA, Height, Width, 3[RGB])) obtained from the the values of `id`, `p_ids`, `p_x`, `p_y` of the input pixel area
    def get_image_areas_as_parameters_for_rgb_formula(self, pixel_area_input:Pixel_area, img:np, must_create_new_rectangles:bool, rgb_formula_dynamic_variables:np, rgb_formulas_for_masks:list) -> np:
        
        rectangles = None
        if(must_create_new_rectangles == True):
            rectangles = self.get_rectangles_used_by_area(main_area=pixel_area_input)
            self.rectangles_per_area[pixel_area_input.id] = rectangles
        else:
            rectangles = self.rectangles_per_area[pixel_area_input.id]

        areas_from_img:list[np.array] = []

        #if the top left corner of the input pixel area is outside the image execute this code
        if(rectangles is None or len(rectangles) == 0):
            return np.array([])
        
        
        rec_index = 0

        for rec in rectangles:
            
            img_for_used_area = img
            img_index = self.pixel_areas_dict[rec.id].img_index
            if(img_index is not None):
                if(img_index in self.images.keys()):
                    img_for_used_area = self.images[img_index]
            
            area_from_img = self.get_result_after_applying_used_area_on_main_area(main_area = pixel_area_input, main_area_rec=rectangles[0], used_area_rec=rec, img = img_for_used_area, rec_index=rec_index, rgb_formula_dynamic_variables=rgb_formula_dynamic_variables, rgb_formulas_for_masks=rgb_formulas_for_masks)

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



   
    def get_replica_values(self, main_area:Pixel_area, main_area_rec:Rectangle, used_area_rec:Rectangle, rec_index:int, ):
        
        w_rep_p1 = main_area.w_rep_p1[min(rec_index,len(main_area.w_rep_p1)-1)]
        w_rep_p2 = main_area.w_rep_p2[min(rec_index,len(main_area.w_rep_p2)-1)]
        h_rep_p1 = main_area.h_rep_p1[min(rec_index,len(main_area.h_rep_p1)-1)]
        h_rep_p2 = main_area.h_rep_p2[min(rec_index,len(main_area.h_rep_p2)-1)]
        
        replica_width = 0
        if(w_rep_p1 > 0 or w_rep_p2 > 0):
            replica_width = min(100, w_rep_p1)/100*main_area_rec.w + min(100, w_rep_p2)/100*used_area_rec.w
            replica_width = min(int(replica_width), used_area_rec.w, main_area_rec.w)
        else:
            replica_width = min(used_area_rec.w, main_area_rec.w)

        replica_height = 0
        if(h_rep_p1 > 0 or h_rep_p2 > 0):
            replica_height = min(100, h_rep_p1)/100*main_area_rec.h + min(100, h_rep_p2)/100*used_area_rec.h
            replica_height = min(int(replica_height), used_area_rec.h, main_area_rec.h)
        else:
            replica_height = min(used_area_rec.h, main_area_rec.h)

        
        rep_x_ratio_p1 = main_area_rec.w/100
        rep_y_ratio_p1 = main_area_rec.h/100
        
        x_rep_start_p1 = int(main_area.x_rep_start_p1[min(rec_index,len(main_area.x_rep_start_p1)-1)]*rep_x_ratio_p1)
        y_rep_start_p1 = int(main_area.y_rep_start_p1[min(rec_index,len(main_area.y_rep_start_p1)-1)]*rep_y_ratio_p1)
        x_rep_end_p1 = int(main_area.x_rep_end_p1[min(rec_index,len(main_area.x_rep_end_p1)-1)]*rep_x_ratio_p1)
        y_rep_end_p1 = int(main_area.y_rep_end_p1[min(rec_index,len(main_area.y_rep_end_p1)-1)]*rep_y_ratio_p1)
        x_rep_step_p1 = int(main_area.x_rep_step_p1[min(rec_index,len(main_area.x_rep_step_p1)-1)]*rep_x_ratio_p1)
        y_rep_step_p1 = int(main_area.y_rep_step_p1[min(rec_index,len(main_area.y_rep_step_p1)-1)]*rep_y_ratio_p1)
        

        rep_x_ratio_p2 = used_area_rec.w/100
        rep_y_ratio_p2 = used_area_rec.h/100

        x_rep_start_p2 = int(main_area.x_rep_start_p2[min(rec_index,len(main_area.x_rep_start_p2)-1)]*rep_x_ratio_p2)
        y_rep_start_p2 = int(main_area.y_rep_start_p2[min(rec_index,len(main_area.y_rep_start_p2)-1)]*rep_y_ratio_p2)
        x_rep_end_p2 = int(main_area.x_rep_end_p2[min(rec_index,len(main_area.x_rep_end_p2)-1)]*rep_x_ratio_p2)
        y_rep_end_p2 = int(main_area.y_rep_end_p2[min(rec_index,len(main_area.y_rep_end_p2)-1)]*rep_y_ratio_p2)
        x_rep_step_p2 = int(main_area.x_rep_step_p2[min(rec_index,len(main_area.x_rep_step_p2)-1)]*rep_x_ratio_p2) + replica_width
        y_rep_step_p2 = int(main_area.y_rep_step_p2[min(rec_index,len(main_area.y_rep_step_p2)-1)]*rep_y_ratio_p2) + replica_height


        x_rep_count_p1 = main_area.x_rep_count_p1[min(rec_index,len(main_area.x_rep_count_p1)-1)]
        y_rep_count_p1 = main_area.y_rep_count_p1[min(rec_index,len(main_area.y_rep_count_p1)-1)]
        x_rep_count_p2 = main_area.x_rep_count_p2[min(rec_index,len(main_area.x_rep_count_p2)-1)]
        y_rep_count_p2 = main_area.y_rep_count_p2[min(rec_index,len(main_area.y_rep_count_p2)-1)]

        replica = Replica(x_rep_start_p1=x_rep_start_p1, y_rep_start_p1=y_rep_start_p1, x_rep_end_p1=x_rep_end_p1, y_rep_end_p1=y_rep_end_p1, x_rep_step_p1=x_rep_step_p1, y_rep_step_p1=y_rep_step_p1, x_rep_count_p1=x_rep_count_p1, y_rep_count_p1=y_rep_count_p1,
                          x_rep_start_p2=x_rep_start_p2, y_rep_start_p2=y_rep_start_p2, x_rep_end_p2=x_rep_end_p2, y_rep_end_p2=y_rep_end_p2, x_rep_step_p2=x_rep_step_p2, y_rep_step_p2=y_rep_step_p2, x_rep_count_p2=x_rep_count_p2, y_rep_count_p2=y_rep_count_p2,
                            replica_width=replica_width, replica_height=replica_height)

        return replica


    
    def get_result_after_applying_used_area_on_main_area(self, main_area:Pixel_area, main_area_rec:Rectangle, used_area_rec:Rectangle, img:np, rec_index:int, rgb_formula_dynamic_variables:np, rgb_formulas_for_masks:list) -> np:#a new version (in testing)

        main_area_from_img = np.copy(img[main_area_rec.y : main_area_rec.y + main_area_rec.h, main_area_rec.x : main_area_rec.x + main_area_rec.w, : ])
        used_area_from_img:np.ndarray = img[used_area_rec.y : used_area_rec.y + used_area_rec.h, used_area_rec.x : used_area_rec.x + used_area_rec.w, : ]

        #<determine the width and height of the main area and the used area

        main_area_height = main_area_from_img.shape[0]
        main_area_width = main_area_from_img.shape[1]
        used_area_height = used_area_from_img.shape[0]
        used_area_width = used_area_from_img.shape[1]

        if(main_area_height == 0 or main_area_width == 0 or used_area_height == 0 or used_area_width == 0):
            return main_area_from_img
        
        if(main_area.ua_h_resize != 0):
            used_area_height = main_area_height if main_area.ua_h_resize == 100 else int(main_area_height/100*main_area.ua_h_resize)
        
        if(main_area.ua_w_resize != 0):
            used_area_width = main_area_width if main_area.ua_w_resize == 100 else int(main_area_width/100*main_area.ua_w_resize)
        
        if(used_area_height == 0 or used_area_width == 0):
            return main_area_from_img
        
        if(main_area.ua_h_resize != 0 or main_area.ua_w_resize != 0):
            used_area_from_img = cv2.resize(used_area_from_img, (used_area_width, used_area_height), interpolation=cv2.INTER_NEAREST)

        main_area_rec = Rectangle(x=main_area_rec.x, y=main_area_rec.y, w=main_area_width, h=main_area_height)
        used_area_rec = Rectangle(x=used_area_rec.x, y=used_area_rec.y, w=used_area_width, h=used_area_height)

        #determine the width and height of the main area and the used area>
        
        rep:Replica = self.get_replica_values(main_area=main_area, main_area_rec=main_area_rec, used_area_rec=used_area_rec, rec_index=rec_index)

        if(rep.replica_height == 0 or rep.replica_width == 0):
            return main_area_from_img

        inner_area_y_p1 = rep.y_rep_start_p1
        inner_area_x_p1 = rep.x_rep_start_p1

        inner_area_y_p2 = rep.y_rep_start_p2
        inner_area_x_p2 = rep.x_rep_start_p2

        inner_area_height_helper = rep.replica_height
        inner_area_width_helper = rep.replica_width

        rows_count_p1 = 0
        columns_count_p1 = 0

        rows_count_p2 = 0
        columns_count_p2 = 0
        
        rep_index = 0 #this is the index of the replicas created by the current used area (rectangle)
        
        #cycle through the rows of the main area
        while(inner_area_y_p1 < main_area_height):
            
        #<make sure the replicas are inside the image, the used area and the main area (y)

            #make sure the replica is inside the main area (vertical)
            if(inner_area_y_p1 + rep.replica_height > rep.y_rep_end_p1):
                inner_area_height_helper = rep.y_rep_end_p1 - inner_area_y_p1
                if(inner_area_height_helper <= 0):
                    break
            else:
                inner_area_height_helper = rep.replica_height
            
            #make sure the replica is inside the used area (vertical)
            if(inner_area_y_p2 + inner_area_height_helper > rep.y_rep_end_p2):
                inner_area_height_helper = rep.y_rep_end_p2 - inner_area_y_p2
                if(inner_area_height_helper <= 0):
                    break
                    
            
            #make sure the main and used areas are inside the image (vertical)
            if(inner_area_y_p1 + inner_area_height_helper > main_area_height):
                inner_area_height_helper = main_area_height - inner_area_y_p1
                if(inner_area_height_helper <= 0):
                    break
            if(inner_area_y_p2 + inner_area_height_helper > used_area_height):
                inner_area_height_helper = used_area_height - inner_area_y_p2
                if(inner_area_height_helper <= 0):
                    break
            
        #make sure the replicas are inside the image, the used area and the main area (y)>

            #cycle through the columns of the main area
            while(inner_area_x_p1 < main_area_width):
                
            #<make sure the replicas are inside the image, the used area and the main area (x)

                #make sure the replica is inside the main area (horizontal)
                if(inner_area_x_p1 + rep.replica_width > rep.x_rep_end_p1):
                    inner_area_width_helper = rep.x_rep_end_p1 - inner_area_x_p1
                    if(inner_area_width_helper <= 0):
                        break
                else:
                    inner_area_width_helper = rep.replica_width

                #make sure the replica is inside the used area (horizontal)
                if(inner_area_x_p2 + inner_area_width_helper > rep.x_rep_end_p2):
                    inner_area_width_helper = rep.x_rep_end_p2 - inner_area_x_p2
                    if(inner_area_width_helper <= 0):
                        break
                
                #make sure the main and used areas are inside the image (horizontal)
                if(inner_area_x_p1 + inner_area_width_helper > main_area_width):
                    inner_area_width_helper = main_area_width - inner_area_x_p1
                    if(inner_area_width_helper <= 0):
                        break
                if(inner_area_x_p2 + inner_area_width_helper > used_area_width):
                    inner_area_width_helper = used_area_width - inner_area_x_p2
                    if(inner_area_width_helper <= 0):
                        break
                
            #make sure the replicas are inside the image, the used area and the main area (x)>

                
                #make sure the shape of the replica from the used area matches the shape of the replica from the main area
                replica_from_main_area = main_area_from_img[inner_area_y_p1: inner_area_y_p1 + inner_area_height_helper, inner_area_x_p1:inner_area_x_p1 + inner_area_width_helper, :]
                replica_from_used_area = used_area_from_img[inner_area_y_p2 : inner_area_y_p2 + inner_area_height_helper, inner_area_x_p2: inner_area_x_p2 + inner_area_width_helper, :]
                if(replica_from_main_area.shape != replica_from_used_area.shape):
                    break

                #apply the current replica to the main area
                main_area_from_img[inner_area_y_p1: inner_area_y_p1 + inner_area_height_helper, inner_area_x_p1:inner_area_x_p1 + inner_area_width_helper, :] = used_area_from_img[inner_area_y_p2 : inner_area_y_p2 + inner_area_height_helper, inner_area_x_p2: inner_area_x_p2 + inner_area_width_helper, :]
                
            
            #<apply rgb formulas, rotations, masks and convolutions to the replica
                                       
                rep_area:np = used_area_from_img[inner_area_y_p2 : inner_area_y_p2 + inner_area_height_helper, inner_area_x_p2: inner_area_x_p2 + inner_area_width_helper, :]
                if(self.use_copy_for_replicas == True):
                    rep_area = np.copy(rep_area)

                #<apply rotations
                if(len(main_area.rotations_rep) > rec_index):
                    if(len(main_area.rotations_rep[rec_index]) > 0):
                        rotation_index = rep_index % len(main_area.rotations_rep[rec_index])
                        rotation_number = main_area.rotations_rep[rec_index][rotation_index]
                        rep_area = self.rotate_replica_area(img = used_area_from_img,  used_area_width=inner_area_width_helper, used_area_height=inner_area_height_helper, used_area_x_left_corner=inner_area_x_p2, used_area_x_right_corner=inner_area_x_p2+inner_area_width_helper, used_area_y_top_corner=inner_area_y_p2,  used_area_y_bottom_corner=inner_area_y_p2+inner_area_height_helper, rotation_number=rotation_number)
                #apply rotations>
                
                #<apply mask
                if(len(main_area.mask_ids_rep) > rec_index): #make sure the current used area (rectangle) has a collection of ids of masks
                    if(len(main_area.mask_ids_rep[rec_index]) > 0): #make sure the collection of ids of masks for the current used area (rectangle) is not empty
                        mask_index = rep_index % len(main_area.mask_ids_rep[rec_index])
                        mask_id = main_area.mask_ids_rep[rec_index][mask_index]
                        if(mask_id in self.masks.keys()):
                            mask = self.masks[mask_id]
                            rep_area = mask.transform_image(img=rep_area,rgb_formulas=rgb_formulas_for_masks,rgb_formulas_dynamic_variables=rgb_formula_dynamic_variables)
                #apply mask>

                #<apply convolution
                if(self.convolutional_kernels_manipulator is not None):
                    if(len(main_area.ck_count_rep) > rec_index): #make sure the current used area (rectangle) has a collection of counts of convolutional kernels
                        if(len(main_area.ck_count_rep[rec_index]) > 0): #make sure the collection of counts of convolutional kernels for the current used area (rectangle) is not empty
                            ck_index = rep_index % len(main_area.ck_count_rep[rec_index])
                            ck_count = main_area.ck_count_rep[rec_index][ck_index]
                            rep_area = self.convolutional_kernels_manipulator.transform_image_1(img=rep_area, cks_count_to_process=ck_count)

                    if(len(main_area.ck_ids_rep) > rec_index): #make sure the current used area (rectangle) has a collection of ids of convolutional kernels
                        if(len(main_area.ck_ids_rep[rec_index]) > 0): #make sure the collection of ids of convolutional kernels for the current used area (rectangle) is not empty
                            ck_index = rep_index % len(main_area.ck_ids_rep[rec_index])
                            ck_id = main_area.ck_ids_rep[rec_index][ck_index]
                            rep_area = self.convolutional_kernels_manipulator.transform_image_2(img=rep_area, cks_ids=[ck_id])
                #apply convolution>

                #<apply rgb formula
                if(len(main_area.f_ids_rep) > rec_index): #make sure the current used area (rectangle) has a collection of ids of RGB formulas
                    if(len(main_area.f_ids_rep[rec_index]) > 0): #make sure the collection of ids of RGB formulas for the current used area (rectangle) is not empty
                        rgb_formula_index = rep_index % len(main_area.f_ids_rep[rec_index])
                        rgb_formula_id = main_area.f_ids_rep[rec_index][rgb_formula_index]
                        if(rgb_formula_id in self.rgb_formulas_dict.keys()):
                            rep_area = rep_area.reshape(1, rep_area.shape[-3], rep_area.shape[-2], rep_area.shape[-1])
                            rgb_formula = self.rgb_formulas_dict[rgb_formula_id].rgb_function
                            rep_area = rgb_formula(r = rep_area[:,:,:,0], g = rep_area[:,:,:,1], b = rep_area[:,:,:,2], areas_count = 1, v = rgb_formula_dynamic_variables)
                #apply rgb formula

                main_area_from_img[inner_area_y_p1: inner_area_y_p1 + inner_area_height_helper, inner_area_x_p1:inner_area_x_p1 + inner_area_width_helper, :] = rep_area
            
            #apply rgb formulas, rotations, masks and convolutions to the replica>           
                
                #increase the index of the replicas
                rep_index+=1
            
            #<move to the next column
                
                inner_area_x_p2 += rep.x_rep_step_p2
                columns_count_p2 += 1
                if(inner_area_x_p2 >= rep.x_rep_end_p2 or columns_count_p2 >= rep.x_rep_count_p2):
                    columns_count_p2 = 0
                    inner_area_x_p2 = rep.x_rep_start_p2
                
                inner_area_x_p1 += rep.x_rep_step_p1 + inner_area_width_helper
                columns_count_p1 += 1
                if(inner_area_x_p1 >= rep.x_rep_end_p1 or columns_count_p1 >= rep.x_rep_count_p1):
                    break

            #move to the next column>

        #<reset the columns when moving to the next row of the main area
            
            columns_count_p1 = 0
            inner_area_x_p1 = rep.x_rep_start_p1
            if(rep.x_rep_count_p1 == rep.x_rep_count_p2):
                        columns_count_p2 = 0
                        inner_area_x_p2 = rep.x_rep_start_p2

        #reset the columns when moving to the next row of the main area>

        #<move to the next row

            inner_area_y_p2 += rep.y_rep_step_p2
            rows_count_p2 += 1
            if(inner_area_y_p2 >= rep.y_rep_end_p2 or rows_count_p2 >= rep.y_rep_count_p2):
                rows_count_p2 = 0
                inner_area_y_p2 = rep.y_rep_start_p2

            inner_area_y_p1 += rep.y_rep_step_p1 + inner_area_height_helper
            rows_count_p1 += 1
            if(inner_area_y_p1 >= rep.y_rep_end_p1  or rows_count_p1 >= rep.y_rep_count_p1):
                break
        
        #move to the next row>
                           
        return main_area_from_img


    #<functions for creating rectangles used by pixel area 

    def get_rectangles_used_by_area(self, main_area:Pixel_area) -> list["Rectangle"]:
        
        rectangles: list[Rectangle] = []


        #<this is the main pixel area
        rectangle = self.get_proper_rectangle(x = main_area.x, y = main_area.y, width = main_area.w, height = main_area.h, id=main_area.id)
        if(rectangle is None):
            return None
        
        rectangles.append(rectangle)        
        #this is the main pixel area>


        #<those are the used areas defined by `p_ids` of the main pixel area
        
        #cycle through the areas used by the main pixel area whose id was found in `p_ids`
        for used_area_id in main_area.p_ids:

            #check only those pixel areas which have an existing id
            if(used_area_id in self.pixel_areas_dict.keys()):
                pixel_area = self.pixel_areas_dict[used_area_id]

                rectangle = self.get_proper_rectangle(x = pixel_area.x, y = pixel_area.y, width = pixel_area.w, height = pixel_area.h, id=used_area_id)
                if(rectangle is not None):
                    rectangles.append(rectangle)
        #those are the used areas defined by `p_ids` of the main pixel area>  

        
        #<those image areas are taken from the top left corners obtained from the values of `p_x` and `p_y` of the main pixel area
        anonymous_areas_count = min(len(main_area.p_x), len(main_area.p_y))        
        for i in range(0, anonymous_areas_count):                
                
            anonymous_area_x = main_area.p_x[i]
            anonymous_area_y = main_area.p_y[i]
                
            #if the top left corner of the anonymous area is outside the canvas don't create (nor add) rectangle
            if(anonymous_area_x >= self.initial_image_width or anonymous_area_y >= self.initial_image_height):
                continue

            anonymous_area_width = min(main_area.w, self.initial_image_width-anonymous_area_x)
            anonymous_area_height = min(main_area.h, self.initial_image_height-anonymous_area_y)
                
            rectangle = self.get_proper_rectangle(x = anonymous_area_x, y = anonymous_area_y, width = anonymous_area_width, height = anonymous_area_height, id=main_area.id)
            if(rectangle is not None):
                rectangles.append(rectangle)
        #those image areas are taken from the top left corners obtained from the values of `p_x` and `p_y` of the main pixel area>
        

        return rectangles



    def get_proper_rectangle(self, x:int, y:int, width: int, height: int, id:int = None) -> "Rectangle":
        
        rectangle = None

        if(self.areas_behiour_when_resizing_main_window == Areas_behaviour_when_resizing_main_window.Resize):
            rectangle = self.get_rectangle_which_can_resize(x=x, y=y, width=width, height=height, id=id)
        
        elif(self.areas_behiour_when_resizing_main_window == Areas_behaviour_when_resizing_main_window.Move):
            rectangle = self.get_rectangle_which_can_move(x=x, y=y, width=width, height=height, id=id)
        
        elif(self.areas_behiour_when_resizing_main_window == Areas_behaviour_when_resizing_main_window.Keep_aspect_ratio):
           rectangle = self.get_rectangle_which_keeps_aspect_ratio(x=x, y=y, width=width, height=height, id=id)
        
        return rectangle
        
    
    def get_rectangle_which_can_resize(self, x:int, y:int, width: int, height: int, id:int = None) -> "Rectangle":
        
        #execute this code if the top left corner is outside the image
        if(self.img_width <= x or self.img_height <= y):
            return None

        #make sure the width and height are not getting outside the image
        width = min(width, self.img_width-x)
        height = min(height, self.img_height-y)

        return Rectangle(x=x, y=y, w=width, h=height, id=id)

    
    def get_rectangle_which_can_move(self, x:int, y:int, width: int, height: int, id:int = None) -> "Rectangle":
        
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

        return Rectangle(x=x, y=y, w=width, h=height, id=id)

    
    def get_rectangle_which_keeps_aspect_ratio(self, x:int, y:int, width: int, height: int, id:int = None) -> "Rectangle":
        
        x_ratio = self.img_width/self.initial_image_width
        y_ratio = self.img_height/self.initial_image_height

        x = round(x*x_ratio)
        width = round(width*x_ratio)

        y = round(y*y_ratio)
        height = round(height*y_ratio)

        return Rectangle(x=x, y=y, w=width, h=height, id=id)

    #functions for creating rectangles used by pixel area>



    #<in testing state

    def transpose_image(self, img:np.ndarray[np.uint8], pixel_area:Pixel_area) -> np.ndarray:

        if(pixel_area.tr_h>0 and pixel_area.tr_w>0):
            traspose_dimensions_index = pixel_area.tr_dim if (pixel_area.tr_dim>0 and pixel_area.tr_dim<len(traspose_dimensions_list)) else 0
            traspose_dimensions = traspose_dimensions_list[traspose_dimensions_index]
            img = self.transpose_with_block_size(img=img, block_height=pixel_area.tr_h, block_width=pixel_area.tr_w, transpose_dimensions=traspose_dimensions)
        
        if(pixel_area.tr_count_row>0 and pixel_area.tr_count_col>0):
            traspose_dimensions_index = pixel_area.tr_count_dim if (pixel_area.tr_count_dim>0 and pixel_area.tr_count_dim<len(traspose_dimensions_list)) else 0
            traspose_dimensions = traspose_dimensions_list[traspose_dimensions_index]
            img = self.transpose_with_block_count(img=img, blocks_count_per_row=pixel_area.tr_count_row, blocks_count_per_column=pixel_area.tr_count_col, transpose_dimensions=traspose_dimensions)

        return img


    def transpose_with_block_size(self, img:np.ndarray, block_height:int, block_width:int, transpose_dimensions:list[int]) -> np.ndarray:
        
        image_height, image_width, rgb_values = img.shape
        if(image_height == 0 or image_width==0):
            return img

       
        if(block_height>image_height):
            block_height=image_height
        if(block_width>image_width):
            block_width=image_width

        height_crop = image_height % block_height
        width_crop = image_width % block_width

        height_transpose = image_height - height_crop
        width_transpose = image_width - width_crop
        
        blocks_count_per_column = height_transpose // block_height
        blocks_count_per_row = width_transpose // block_width

        t_d = transpose_dimensions
        img[:height_transpose, :width_transpose, :] = img[:height_transpose, :width_transpose, :].reshape(blocks_count_per_column, block_height, blocks_count_per_row, block_width, rgb_values).transpose(t_d[0], t_d[1], t_d[2], t_d[3], 4).reshape(height_transpose, width_transpose, rgb_values)
        return img

    def transpose_with_block_count(self, img:np.ndarray, blocks_count_per_row:int, blocks_count_per_column:int, transpose_dimensions:list[int]) -> np.ndarray:
        
        image_height, image_width, rgb_values = img.shape
        if(image_height == 0 or image_width==0):
            return img

        block_height = image_height//blocks_count_per_column
        block_width = image_width//blocks_count_per_row
       
        if(block_height>image_height):
            block_height=image_height
        if(block_width>image_width):
            block_width=image_width
        
        height_crop = image_height % blocks_count_per_column
        width_crop = image_width % blocks_count_per_row

        height_transpose = image_height - height_crop
        width_transpose = image_width - width_crop

        t_d = transpose_dimensions
        img[:height_transpose, :width_transpose, :] = img[:height_transpose, :width_transpose, :].reshape(blocks_count_per_column, block_height, blocks_count_per_row, block_width, rgb_values).transpose(t_d[0], t_d[1], t_d[2], t_d[3], 4).reshape(height_transpose, width_transpose, rgb_values)
        return img
    
    #in testing state>
