import numpy as np
from PyQt5.QtGui import QColor

from Number_format_checker import check_for_positive_int_format, check_numbers_from_string
from Window_functions import get_rgb_pixel_values_from_window
from Colour import Colour, Colour_range

from Window_Canvas_draw_mask import Window_Canvas_draw_mask
from Z2_Window_Form_pixel_areas_masks import Window_Form_pixel_areas_masks
from Z_Mask import Mask

from Z_Pixel_area import Rectangle
   
class Pixel_areas_masks_controller:

    def __init__(self):

        self.region_id_max_value = 255

        self.form_window_draw_mask = Window_Form_pixel_areas_masks()
        self.canvas_window = Window_Canvas_draw_mask()

        self.form_window_draw_mask.button_create_mask.clicked.connect(self.create_mask)
        self.form_window_draw_mask.button_delete_mask.clicked.connect(self.delete_mask)

        self.form_window_draw_mask.button_create_colour_region.clicked.connect(self.create_colour_region)
        self.form_window_draw_mask.button_create_colour_range_region.clicked.connect(self.create_colour_range_region)
        self.form_window_draw_mask.button_delete_region.clicked.connect(self.delete_region)

        self.form_window_draw_mask.button_alter_pixel_area_id.clicked.connect(self.alter_pixel_area_id)

        self.form_window_draw_mask.slider_red.valueChanged.connect(lambda: self.slider_value_changed(self.form_window_draw_mask.slider_red.value(), 'r'))
        self.form_window_draw_mask.slider_green.valueChanged.connect(lambda: self.slider_value_changed(self.form_window_draw_mask.slider_green.value(), 'g'))
        self.form_window_draw_mask.slider_blue.valueChanged.connect(lambda: self.slider_value_changed(self.form_window_draw_mask.slider_blue.value(), 'b'))

        self.form_window_draw_mask.button_clear_canvas.clicked.connect(self.canvas_window.clear)
        self.form_window_draw_mask.button_apply_brush_size_changes.clicked.connect(self.change_brush_size_parameters)

        self.form_window_draw_mask.checkBox_auto_remove_previous_masks_when_applying_new_masks.clicked.connect(self.change_value_of__auto_remove_previous_masks_when_applying_new_masks)
        self.form_window_draw_mask.checkBox_keep_ratio.clicked.connect(self.change_value_of__keep_ratio)

        self.masks:dict[int,Mask] = {}
        self.applied_masks:dict[int,Mask] = {}

        self.img_for_colour_masks:np.ndarray = None
        self.img_for_colour_range_masks:np.ndarray = None


#<drawing functions
    def change_brush_size_parameters(self):

        #take the brush size parameters
        brush_size_min_value = self.form_window_draw_mask.textBox_brush_size_min_value.text()
        brush_size_max_value = self.form_window_draw_mask.textBox_brush_size_max_value.text()
        brush_size_delta = self.form_window_draw_mask.textBox_brush_size_delta.text()

        #check the the format of the brush size parameters
        if(check_for_positive_int_format(brush_size_min_value, is_zero_allowed=False) == False or brush_size_min_value == ""):
            print("Error: the brush min size field was either in wrong format or it was equal to 0")
            return        
        if(check_for_positive_int_format(brush_size_max_value, is_zero_allowed=False) == False or brush_size_min_value == ""):
            print("Error: the brush max size field was either in wrong format or it was equal to 0")
            return        
        if(check_for_positive_int_format(brush_size_delta, is_zero_allowed=False) == False or brush_size_min_value == ""):
            print("Error: the brush size icrement field was either in wrong format or it was equal to 0")
            return
        
        brush_min_size = int(brush_size_min_value)
        brush_max_size = int(brush_size_max_value)
        brush_delta = int(brush_size_delta)

        if(brush_min_size>brush_max_size):
            print("Error: brush min size value cannot be higher than brush max size value")
            return

        self.canvas_window.set_brush_size_arguments(brush_min_size = brush_min_size, brush_max_size=brush_max_size, brush_delta=brush_delta)
    
    def slider_value_changed(self, slider_value, slider_id):

        if(slider_id == "r"):
            self.form_window_draw_mask.colour.r = slider_value*self.form_window_draw_mask.slider_step
        if(slider_id == "g"):
            self.form_window_draw_mask.colour.g = slider_value*self.form_window_draw_mask.slider_step
        if(slider_id == "b"):
            self.form_window_draw_mask.colour.b = slider_value*self.form_window_draw_mask.slider_step
        
        self.form_window_draw_mask.set_colour_of_drawing_button()

        colour = QColor(self.form_window_draw_mask.colour.r, self.form_window_draw_mask.colour.g, self.form_window_draw_mask.colour.b)
        self.canvas_window.set_colour(colour)
    
#drawing functions>


#<functions for getting user input

    def get_mask_id_from_user_input (self) -> int:
        mask_id_txt = self.form_window_draw_mask.textBox_mask_id.text()

        if(check_for_positive_int_format(mask_id_txt, is_zero_allowed=False) == False or mask_id_txt == ""):
            return None
        
        mask_id = int(mask_id_txt)
        return mask_id

    def get_pixel_area_id_from_user_input (self) -> int:
        pixel_area_id_txt = self.form_window_draw_mask.textBox_pixel_area_id.text()

        if(check_for_positive_int_format(pixel_area_id_txt, is_zero_allowed=True) == False or pixel_area_id_txt == ""):
            return None
        
        pixel_area_id = int(pixel_area_id_txt)
        return pixel_area_id

    def get_region_id_from_user_input (self) -> np.uint8:
        
        region_id_txt = self.form_window_draw_mask.textBox_region_id.text()

        if(check_for_positive_int_format(region_id_txt, is_zero_allowed=True) == False or region_id_txt == ""):
            return None
        
        region_id = int(region_id_txt)
        if(region_id > self.region_id_max_value):
            return None
    
        return np.uint8(region_id)
    
    
    def get_colour_from_user_input(self) -> Colour:
        colour = Colour(r=self.form_window_draw_mask.colour.r, g=self.form_window_draw_mask.colour.g, b=self.form_window_draw_mask.colour.b)
        return colour

    def get_colour_ranges_from_user_input(self) -> Colour_range:

        user_input_rgb_ranges:list[int] = []

        textBoxes_colorRange_list = self.form_window_draw_mask.textBox_colorRange_list

        for i in range(0, len(textBoxes_colorRange_list)):
            
            user_input_rgb_range:list[int] = []

            for j in range(0, len(textBoxes_colorRange_list[i])):
                
                user_input_str = self.form_window_draw_mask.textBox_colorRange_list[i][j].text().replace(" ","").replace("\n","")

                if(check_for_positive_int_format(user_input_str) == False):
                    return None
                
                rbg_channel_value = int(user_input_str)

                if(rbg_channel_value > self.region_id_max_value):
                    return None

                user_input_rgb_range.append(rbg_channel_value)
            
            user_input_rgb_ranges.append(min(user_input_rgb_range[0], user_input_rgb_range[1]))
            user_input_rgb_ranges.append(max(user_input_rgb_range[0], user_input_rgb_range[1]))



        colour_range = Colour_range(r_from=user_input_rgb_ranges[0], r_to=user_input_rgb_ranges[1], g_from=user_input_rgb_ranges[2], g_to=user_input_rgb_ranges[3], b_from=user_input_rgb_ranges[4], b_to=user_input_rgb_ranges[5])
        
        return colour_range

    def get_selected_masks_ids(self, matching_masks_ids:list[int] = None) -> list[int]:
    
        masks_ids_str = self.form_window_draw_mask.textBox_apply_masks.text().replace(" ", "").replace("\n", "")
        is_masks_ids_str_valid = check_numbers_from_string(txt_value=masks_ids_str, separator=",", search_for_floats=False, search_for_positives_only=True)
        if(is_masks_ids_str_valid == False):
            print("error: the selected mask ids were in wrong format - make sure you use only positive integers separated by comma")
            return None
    
        masks_ids:list[int] = list(map(int, masks_ids_str.split(",")))
        if(matching_masks_ids is None):
            return masks_ids

        found_masks_ids:list[int] = []
    
        for mask_id in masks_ids:
            if(mask_id in matching_masks_ids):
                found_masks_ids.append(mask_id)
    
        return found_masks_ids

    #The image is returned as a numpy array with shape (Height, Width, 3[RGB])
    def get_image_from_canvas(self) -> np.ndarray[np.uint8]:
        img_from_canvas = get_rgb_pixel_values_from_window(window=self.canvas_window)
        return img_from_canvas

#functions for getting user input>



#<functions which are called when the user presses a button

    #<mask functions
    def create_mask(self):

        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            print("Error: the mask id must be a positive integer")
            return  

        pixel_area_id = self.get_pixel_area_id_from_user_input()

        if(pixel_area_id is None):
            print("Error: the pixel area id must be a positive integer")
            return        

        if(mask_id not in self.masks.keys()):
            self.masks[mask_id] = Mask(mask_id=mask_id, pixel_area_id=pixel_area_id)
            self.display_masks_as_text()
        else:
            print("Warning: the mask was not created because the mask id is used by another mask")
            return
    

    def delete_mask(self):

        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            print("Error: the mask id must be a positive integer")
            return

        if(mask_id in self.masks.keys()):
            del self.masks[mask_id]
            self.display_masks_as_text()
        else:
            print("Error: the mask could not be deleted because the id was not found")
            return
        
    #mask functions>

    #<region functions

    def create_colour_region(self):
        
        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            print("Error: the mask id must be a positive integer")
            return
        
        if(mask_id not in self.masks.keys()):
            print("Warning: the region cannot be created because the mask id was not found")
            return

        region_id = self.get_region_id_from_user_input()

        if(region_id is None):
            print(f"Error: the region id must be a positive integer which is equal to or below {self.region_id_max_value}")
            return
        
        colour = self.get_colour_from_user_input()

        mask = self.masks[mask_id]
        was_region_added =  mask.rgb_formulas_mask.add_region(region_id=region_id)

        if(was_region_added == False):
            print(f"Warning: the region was not created because the mask with id {mask_id} already had an existing region with id {region_id}")
        else:
            mask.add_or_alter_colour(region_id=region_id, colour=colour)
            """
            self.update_mask_img_from_canvas(mask=mask)
            """
            self.display_masks_as_text()
        

    def create_colour_range_region(self):
        
        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            print("Error: the mask id must be a positive integer")
            return
        
        if(mask_id not in self.masks.keys()):
            print("Warning: the region cannot be created because the mask id was not found")
            return

        region_id = self.get_region_id_from_user_input()

        if(region_id is None):
            print(f"Error: the region id must be a positive integer which is equal to or below {self.region_id_max_value}")
            return

        
        colour_range = self.get_colour_ranges_from_user_input()
        if(colour_range is None):
            print("Error: the colour ranges must be integers in the range [0-255]")
            return
        
        mask = self.masks[mask_id]
        was_region_added =  mask.rgb_formulas_mask.add_region(region_id=region_id)

        if(was_region_added == False):
            print(f"Warning: the region was not created because the mask with id {mask_id} already had an existing region with id {region_id}")
        else:
            mask.add_or_alter_colour_range(region_id=region_id, colour_range=colour_range)
            self.display_masks_as_text()

    

    def delete_region(self):
        
        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            print("Error: the mask id must be a positive integer")
            return
        
        if(mask_id not in self.masks.keys()):
            print("Warning: the region cannot be deleted because the mask id was not found")
            return

        region_id = self.get_region_id_from_user_input()

        if(region_id is None):
            print(f"Error: the region id must be a positive integer which is equal to or below {self.region_id_max_value}")
            return

        mask = self.masks[mask_id]
        was_region_removed = mask.rgb_formulas_mask.remove_region(region_id=region_id)

        if(was_region_removed == True):
            mask.remove_colour_or_colour_range(region_id=region_id)
            self.display_masks_as_text()
        else:
            print(f"Warning: the region was not deleted because the mask with id {mask_id} does not have a region with id {region_id}")
            return

    #region functions>

    #<pixel area functions

    def alter_pixel_area_id(self):

        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            print("Error: the mask id must be a positive integer")
            return
        
        if(mask_id not in self.masks.keys()):
            print("Warning: the pixel area id cannot be altered because the mask id was not found")
            return

        pixel_area_id = self.get_pixel_area_id_from_user_input()
        if(pixel_area_id is None):
            print("Error: the pixel area id must be a positive integer")
            return
        
        mask = self.masks[mask_id]
        mask.alter_pixel_area_id(new_pixel_area_id=pixel_area_id)
        self.display_masks_as_text()

    #pixel area functions>



    #<functions for applying masks
    
    #the function: updates the selected masks; adds the selected masks to the applied masks; returns the applied masks
    def apply_selected_masks(self, rectangles_with_ids:dict[int, Rectangle], img_for_colour_range_masks:np.ndarray[np.uint8] = None) -> dict[int,Mask]:

        masks_ids = self.get_selected_masks_ids(matching_masks_ids=list(self.masks.keys()))
        if(masks_ids is None):
            return None

        masks = self.apply_masks(masks_ids = masks_ids, rectangles_with_ids=rectangles_with_ids, img_for_colour_range_masks=img_for_colour_range_masks)
        return masks

    #the function: updates all masks; adds all masks to the applied masks; returns the applied masks
    def apply_all_masks(self, rectangles_with_ids:dict[int, Rectangle], img_for_colour_range_masks:np.ndarray[np.uint8] = None) -> dict[int,Mask]:

        masks_ids = list(self.masks.keys())
        masks = self.apply_masks(masks_ids = masks_ids, rectangles_with_ids=rectangles_with_ids, img_for_colour_range_masks=img_for_colour_range_masks)
        return masks

    def apply_masks(self, masks_ids:list[int], rectangles_with_ids:dict[int, Rectangle], img_for_colour_range_masks:np.ndarray[np.uint8] = None):

        if(self.form_window_draw_mask.checkBox_auto_update_images_when_applying_masks.isChecked() == True):
            self.update_images_for_masks(img_for_colour_range_masks=img_for_colour_range_masks)

        are_masks_updated = self.update_applied_masks(masks_ids=masks_ids, rectangles_with_ids=rectangles_with_ids)
        if(are_masks_updated == False):
            print("warning: the masks could not be applied")
            return None
        else:
            self.display_masks_as_text()
            return self.applied_masks

    #functions for applying masks>


    #<functions for removing applied masks

    #the function: removes the selected masks from the applied masks; returns the remaining elements from the applied masks
    def remove_selected_applied_masks(self) -> dict[int,Mask]:

        masks_ids = self.get_selected_masks_ids(matching_masks_ids=list(self.applied_masks.keys()))
        if(masks_ids is None):
            return None

        #remove selected masks from applied masks
        for mask_id in masks_ids:
            self.applied_masks.pop(mask_id)

        self.display_masks_as_text()
        return self.applied_masks

    #the function: removes all masks from the applied masks
    def remove_all_applied_masks(self):
        self.applied_masks = {}
        self.display_masks_as_text()
        
    
    #functions for removing applied masks>

#functions which are called when the user presses a button>




#<functions which are called when the user presses a check box

    def change_value_of__auto_remove_previous_masks_when_applying_new_masks(self):

        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            print("Error: the mask id must be a positive integer")
            return
        
        if(mask_id not in self.masks.keys()):
            print("Warning: the auto remove previous mask behaviour when applying new masks cannot be altered because the mask id was not found")
            return
        
        mask = self.masks[mask_id]
            
        if(self.form_window_draw_mask.checkBox_auto_remove_previous_masks_when_applying_new_masks.isChecked() == True):
            mask.set_value_for__auto_remove_previous_masks_when_applying_new_masks(new_value=True)
        else:
            mask.set_value_for__auto_remove_previous_masks_when_applying_new_masks(new_value=False)
        
        self.display_masks_as_text()
    
    def change_value_of__keep_ratio(self):

        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            print("Error: the mask id must be a positive integer")
            return
        
        if(mask_id not in self.masks.keys()):
            print("Warning: the resize behaviour of the mask cannot be altered because the mask id was not found")
            return
        
        mask = self.masks[mask_id]
            
        if(self.form_window_draw_mask.checkBox_keep_ratio.isChecked() == True):
            mask.set_value_for__keep_ratio(new_value=True)
        else:
            mask.set_value_for__keep_ratio(new_value=False)
        
        self.display_masks_as_text()

    
#functions which are called when the user presses a check box>

    """
    def update_mask_img_from_canvas(self, mask:Mask):
        img_from_canvas = get_rgb_pixel_values_from_window(window=self.canvas_window)
        mask.update_img_from_canvas(new_img_from_canvas=img_from_canvas)

        
   
    def get_masks(self) -> list[Mask]:
        return list(self.masks.values())
    
    """

#<functions for showing info about the masks

    def display_masks_as_text(self):

        self.form_window_draw_mask.text_area.clear()
        self.form_window_draw_mask.text_area.setPlainText(self.to_string())


    def to_string(self):

        txt = ""
        txt += "applied masks ids: {" + str.join(", ", list(map(str, self.applied_masks.keys()))) + "}\n\n"
        for mask_id in self.masks.keys():
            txt += f"{"{"} mask id: {mask_id}; "
            txt += f"{self.masks[mask_id].to_string()}"
            txt += "\n}\n"
        
        return txt

#functions for showing info about the masks>




#<functions for updating: applied masks; images which are used to apply masks

    def update_images_for_masks(self, img_for_colour_range_masks:np.ndarray[np.uint8] = None):

        img_for_colour_masks = self.get_image_from_canvas()
        
        if(self.form_window_draw_mask.checkBox_update_image_for_colour_masks.isChecked() == True):
            if(img_for_colour_masks.shape[0] > 0 and img_for_colour_masks.shape[1] > 0):
                self.img_for_colour_masks = img_for_colour_masks.copy()

        if(self.form_window_draw_mask.checkBox_update_image_for_colour_range_masks.isChecked() == True and img_for_colour_range_masks is not None):
            if(img_for_colour_range_masks.shape[0] > 0 and img_for_colour_range_masks.shape[1] > 0):
                self.img_for_colour_range_masks = img_for_colour_range_masks.copy()


    def update_applied_masks(self, masks_ids:list[int], rectangles_with_ids:dict[int, Rectangle]) -> bool:
    
        does_images_for_masks_exist = True
    
        if(self.img_for_colour_masks is None):
            does_images_for_masks_exist = False
            print("error: the masks could not be updated because the image for colour masks was not found")
    
        if(self.img_for_colour_range_masks is None):
            does_images_for_masks_exist = False
            print("error: the masks could not be updated because the image for colour range masks was not found")
    
        if(does_images_for_masks_exist == False):
            return False
    
        #apply colour regions and colour range regions to each mask
        for mask_id in masks_ids:
    
            if(mask_id in self.applied_masks and self.form_window_draw_mask.checkBox_apply_already_applied_masks.isChecked() == False):
                print(f"warning: the mask with id {mask_id} could not be applied because it is already applied")
                continue
    
            mask = self.masks[mask_id]
            img_for_colour_range_masks = self.img_for_colour_range_masks
    
            if(mask.pixel_area_id in rectangles_with_ids.keys()):
                rec = rectangles_with_ids[mask.pixel_area_id]
                img_for_colour_range_masks =  self.img_for_colour_range_masks[rec.x : rec.x+rec.w , rec.y : rec.y+rec.h , :]
    
            mask.apply_regions(img_for_colour_regions=self.img_for_colour_masks.copy(), img_for_colour_range_regions=img_for_colour_range_masks.copy())
            self.applied_masks[mask_id] = mask.copy()
    
        return True
    
#functions for updating: applied masks; images which are used to apply masks>

