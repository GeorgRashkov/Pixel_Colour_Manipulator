import numpy as np
from PyQt5.QtGui import QColor

from Number_format_checker import check_for_positive_int_format
from Window_functions import get_rgb_pixel_values_from_window
from Colour import Colour, Colour_range

from Window_Canvas_draw_mask import Window_Canvas_draw_mask
from Z2_Window_Form_pixel_areas_masks import Window_Form_pixel_areas_masks
from Z_Mask import Mask

   
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

    #functions for getting user input>


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
            self.update_mask_img_from_canvas(mask=mask)
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

    

    def update_mask_img_from_canvas(self, mask:Mask):
        img_from_canvas = get_rgb_pixel_values_from_window(window=self.canvas_window)
        mask.update_img_from_canvas(new_img_from_canvas=img_from_canvas)

        
   
    def get_masks(self) -> list[Mask]:
        return list(self.masks.values())
    
    def display_masks_as_text(self):

        self.form_window_draw_mask.text_area.clear()
        self.form_window_draw_mask.text_area.setPlainText(self.to_string())


    def to_string(self):

        txt = ""
        for mask_id in self.masks.keys():
            txt += f"{"{"} mask id: {mask_id}; "
            txt += f"{self.masks[mask_id].to_string()}"
            txt += "\n}\n"
        
        return txt