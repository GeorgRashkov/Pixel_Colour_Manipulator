
import numpy as np
from PyQt5.QtGui import QColor

from Window_Form_draw_mask import Window_Form_draw_mask
from Number_format_checker import check_for_positive_int_format
from Window_Canvas_draw_mask import Window_Canvas_draw_mask
from Z_RGB_formulas_mask import RGB_formulas_mask
from Window_functions import get_rgb_pixel_values_from_window
from Z_RGB_formula import RGB_formula
from Colour import Colour
from RGB_formula_initializer import RGB_formula_initializer
from typing import Callable


class Draw_mask_controller():

    def __init__(self, rgb_formulas_mask:RGB_formulas_mask):
        
        self.form_window_draw_mask = Window_Form_draw_mask()
        self.canvas_window = Window_Canvas_draw_mask()
        self.rgb_formulas_mask = rgb_formulas_mask


        self.form_window_draw_mask.colour_variables_group_box.button_add_rgb_formula.clicked.connect(self.create_rgb_formula)
        self.form_window_draw_mask.colour_variables_group_box.button_show_rgb_formula.clicked.connect(self.show_rgb_formulas)
        self.form_window_draw_mask.colour_variables_group_box.button_remove_rgb_formula.clicked.connect(self.remove_rgb_formula)

        
        self.form_window_draw_mask.slider_red.valueChanged.connect(lambda: self.slider_value_changed(self.form_window_draw_mask.slider_red.value(), 'r'))
        self.form_window_draw_mask.slider_green.valueChanged.connect(lambda: self.slider_value_changed(self.form_window_draw_mask.slider_green.value(), 'g'))
        self.form_window_draw_mask.slider_blue.valueChanged.connect(lambda: self.slider_value_changed(self.form_window_draw_mask.slider_blue.value(), 'b'))
        
        
        self.form_window_draw_mask.button_clear_canvas.clicked.connect(self.canvas_window.clear)
        self.form_window_draw_mask.button_apply_brush_size_changes.clicked.connect(self.change_brush_size_parameters)

        self.rgb_formulas:dict[int,RGB_formula] = {}
        self.mask_colours:dict[int,Colour] = {}

        self.rgb_formula_initializer = RGB_formula_initializer(use_many_areas=False)


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

    
    #<get functions (helpers)
    
    def get_id_of_colour(self, colour:Colour):

        for colour_id in self.mask_colours.keys():
            if(colour.r == self.mask_colours[colour_id].r and colour.g == self.mask_colours[colour_id].g and colour.b == self.mask_colours[colour_id].b):
                return colour_id
        
        return None
    


    def get_text_in_rgb_function_fields(self) -> dict[str, str]:

        user_input = {}
        rgb_channels = ["r", "g", "b"]

        for rgb_channel in rgb_channels:
            user_input[rgb_channel] = self.form_window_draw_mask.colour_variables_group_box.rgb_elements.text_boxes[rgb_channel].text().replace(" ","").replace("\n","")

        return user_input

    def get_rgb_formulas_as_lambdas(self) -> dict[int,Callable]:

        rgb_functions = {}

        for id in self.rgb_formulas.keys():
            rgb_functions[id] = self.rgb_formulas[id].rgb_function
        
        return rgb_functions

    #get functions (helpers)>

    #<functions for altering the values of rgb formulas and colours of mask
    def create_rgb_formula(self):
        
        rgb_formulas_str = self.get_text_in_rgb_function_fields()
        rgb_formula = self.rgb_formula_initializer.create_rgb_formulas_without_pixel_areas(r_formula=rgb_formulas_str["r"], g_formula=rgb_formulas_str["g"], b_formula=rgb_formulas_str["b"])
        if(rgb_formula is None):
            return
        
        colour = Colour(r=self.form_window_draw_mask.colour.r, g=self.form_window_draw_mask.colour.g, b=self.form_window_draw_mask.colour.b)
        colour_id = self.get_id_of_colour(colour = colour)
      
        if(colour_id is None):
            colour_id = self.rgb_formulas_mask.get_min_not_used_id_for_rgb_formula()
            if(colour_id is None):
                print("warning: the rgb formula and the paint region will not be applied because the maximum number of paint regions was reached")
                return
            
        self.rgb_formulas[colour_id] = rgb_formula
        self.mask_colours[colour_id] = colour

    
    
    def show_rgb_formulas(self):

        for rgb_formulas_id in self.rgb_formulas.keys():
            print(f"id {rgb_formulas_id} -> rgb formula {self.rgb_formulas[rgb_formulas_id].rgb_function_str} -> colour: r:{self.mask_colours[rgb_formulas_id].r}, g:{self.mask_colours[rgb_formulas_id].g}, b:{self.mask_colours[rgb_formulas_id].b}")

    def remove_rgb_formula(self):

        rgb_formula_id_str = self.form_window_draw_mask.colour_variables_group_box.text_box_rgb_formula_id.text().replace(" ","").replace("\n","")
        
        if(check_for_positive_int_format(rgb_formula_id_str) == True and rgb_formula_id_str != ""):
            rgb_formula_id = int(rgb_formula_id_str)
            if(rgb_formula_id in self.rgb_formulas.keys()):
                del self.mask_colours[rgb_formula_id]
                del self.rgb_formulas[rgb_formula_id]
                self.rgb_formulas_mask.remove_used_id(id=rgb_formula_id)

    #functions for altering the values of rgb formulas and colours of mask>
    

    

    def get_colour_mask(self):

        img_mask = get_rgb_pixel_values_from_window(window=self.canvas_window)
        rgb_functions = self.get_rgb_formulas_as_lambdas()
        remove_presious_mask = self.form_window_draw_mask.checkBox_auto_remove_previous_mask_when_applying_new_mask.isChecked()
        self.rgb_formulas_mask.create_colour_mask(img_mask=img_mask, rgb_functions=rgb_functions, colours=self.mask_colours, remove_presious_mask=remove_presious_mask)
        return self.rgb_formulas_mask
