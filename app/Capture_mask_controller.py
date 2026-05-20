
import numpy as np


from Window_Form_capture_mask import Window_Form_capture_mask
from Number_format_checker import check_for_positive_int_format
from Z_RGB_formulas_mask import RGB_formulas_mask
from Z_RGB_formula import RGB_formula
from Colour import Colour_range
from Z_RGB_formula_checker import check_RGB_formula_format
from typing import Callable


class Capture_mask_controller():

    def __init__(self, rgb_formulas_mask:RGB_formulas_mask):
        
        
        self.form_window_capture_mask = Window_Form_capture_mask()
        self.rgb_formulas_mask = rgb_formulas_mask

        #self.rbg_formula_id_max_value = 255
        
        self.form_window_capture_mask.colour_variables_group_box.button_add_rgb_formula.clicked.connect(self.create_rgb_formula)
        self.form_window_capture_mask.colour_variables_group_box.button_show_rgb_formula.clicked.connect(self.show_rgb_formulas)
        self.form_window_capture_mask.colour_variables_group_box.button_remove_rgb_formula.clicked.connect(self.remove_rgb_formula)
        
        self.rgb_formulas:dict[int,RGB_formula] = {}
        self.mask_colour_ranges:dict[int,Colour_range] = {}


    #<get functions (helpers)
    """
    def get_min_not_used_id_for_rgb_formula(self) -> int:

        num = 1
        while(num in self.rgb_formulas.keys()):
            
            num+=1
        
        return num
    """
    def get_id_of_colour_range(self, colour_range:Colour_range):

        for colour_id in self.mask_colour_ranges.keys():
            if(
                colour_range.r_from == self.mask_colour_ranges[colour_id].r_from and colour_range.r_to == self.mask_colour_ranges[colour_id].r_to and
               colour_range.g_from == self.mask_colour_ranges[colour_id].g_from and colour_range.g_to == self.mask_colour_ranges[colour_id].g_to and
               colour_range.b_from == self.mask_colour_ranges[colour_id].b_from and colour_range.b_to == self.mask_colour_ranges[colour_id].b_to
               ):
                return colour_id
        
        return None



    def get_text_in_rgb_function_fields(self) -> dict[str, str]:

        user_input = {}
        rgb_channels = ["r", "g", "b"]

        for rgb_channel in rgb_channels:
            user_input[rgb_channel] = self.form_window_capture_mask.colour_variables_group_box.rgb_elements.text_boxes[rgb_channel].text().replace(" ","").replace("\n","")

        return user_input
    
    def get_colour_ranges_from_user_input(self) -> Colour_range:

        user_input_rgb_ranges:list[int] = []

        textBoxes_colorRange_list = self.form_window_capture_mask.textBox_colorRange_list

        for i in range(0, len(textBoxes_colorRange_list)):
            
            user_input_rgb_range:list[int] = []

            for j in range(0, len(textBoxes_colorRange_list[i])):
                
                user_input_str = self.form_window_capture_mask.textBox_colorRange_list[i][j].text().replace(" ","").replace("\n","")

                if(check_for_positive_int_format(user_input_str) == False):
                    return None
                
                rbg_channel_value = int(user_input_str)

                if(rbg_channel_value > 255):
                    return None

                user_input_rgb_range.append(rbg_channel_value)
            
            user_input_rgb_ranges.append(min(user_input_rgb_range[0], user_input_rgb_range[1]))
            user_input_rgb_ranges.append(max(user_input_rgb_range[0], user_input_rgb_range[1]))



        colour_range = Colour_range(r_from=user_input_rgb_ranges[0], r_to=user_input_rgb_ranges[1], g_from=user_input_rgb_ranges[2], g_to=user_input_rgb_ranges[3], b_from=user_input_rgb_ranges[4], b_to=user_input_rgb_ranges[5])
        
        return colour_range

    def get_rgb_formulas_as_lambdas(self) -> dict[int,Callable]:

        rgb_functions = {}

        for id in self.rgb_formulas.keys():
            rgb_functions[id] = self.rgb_formulas[id].rgb_function
        
        return rgb_functions

    #get functions (helpers)>




    #<functions for altering the values of rgb formulas and mask

    def create_rgb_formula(self):
        
        rgb_formulas_str = self.get_text_in_rgb_function_fields()
        are_rgb_formulas_correct = False

        for rgb_channel in rgb_formulas_str.keys():
            are_rgb_formulas_correct = check_RGB_formula_format(rgb_formula=rgb_formulas_str[rgb_channel], channel=rgb_channel, use_areas=False)
            if(are_rgb_formulas_correct == False):
                return
        
        rgb_formula = RGB_formula(red_func=rgb_formulas_str["r"], green_func=rgb_formulas_str["g"], blue_func=rgb_formulas_str["b"], use_pixel_areas=False)
        colour_range = self.get_colour_ranges_from_user_input()
        if(colour_range == None):
            print("error: the colour ranges must be integers in the range [0-255]")
            return
        
        colour_range_id = self.get_id_of_colour_range(colour_range = colour_range)

        """
        if(colour_range_id is None):
            colour_range_id = self.get_min_not_used_id_for_rgb_formula()
            if(colour_range_id > self.rbg_formula_id_max_value):
                print("warning: the rgb formula and the colour range will not be applied because the maximum number of colour ranges was reached")
                return
        """
        if(colour_range_id is None):
            colour_range_id = self.rgb_formulas_mask.get_min_not_used_id_for_rgb_formula()
            if(colour_range_id is None):
                print("warning: the rgb formula and the colour range will not be applied because the maximum number of colour ranges was reached")
                return
                
        self.rgb_formulas[colour_range_id] = rgb_formula
        self.mask_colour_ranges[colour_range_id] = colour_range
    
    def show_rgb_formulas(self):

        for rgb_formulas_id in self.rgb_formulas.keys():
            print(f"id {rgb_formulas_id} -> rgb formula {self.rgb_formulas[rgb_formulas_id].rgb_function_str} -> colour range: r:{self.mask_colour_ranges[rgb_formulas_id].r_from}-{self.mask_colour_ranges[rgb_formulas_id].r_to}, g:{self.mask_colour_ranges[rgb_formulas_id].g_from}-{self.mask_colour_ranges[rgb_formulas_id].g_to}, b:{self.mask_colour_ranges[rgb_formulas_id].b_from}-{self.mask_colour_ranges[rgb_formulas_id].b_to}")

    def remove_rgb_formula(self):

        rgb_formula_id_str = self.form_window_capture_mask.colour_variables_group_box.text_box_rgb_formula_id.text().replace(" ","").replace("\n","")
        
        if(check_for_positive_int_format(rgb_formula_id_str) == True and rgb_formula_id_str != ""):
            rgb_formula_id = int(rgb_formula_id_str)
            if(rgb_formula_id in self.rgb_formulas.keys()):
                del self.mask_colour_ranges[rgb_formula_id]
                del self.rgb_formulas[rgb_formula_id]
                self.rgb_formulas_mask.remove_used_id(id=rgb_formula_id)

    #functions for altering the values of rgb formulas and mask>
    

    

    def get_colour_mask(self, img_mask:np.ndarray[np.uint8]):

        rgb_functions = self.get_rgb_formulas_as_lambdas()
        remove_presious_mask = self.form_window_capture_mask.checkBox_auto_remove_previous_mask_when_applying_new_mask.isChecked()
        self.rgb_formulas_mask.create_colour_range_mask(img_mask=img_mask, rgb_functions=rgb_functions, colour_ranges=self.mask_colour_ranges, remove_presious_mask=remove_presious_mask)
        return self.rgb_formulas_mask
