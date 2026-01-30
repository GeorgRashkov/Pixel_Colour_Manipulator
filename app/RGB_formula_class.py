import numpy as np
from Z_RGB_formula_checker import make_areas_indexes_in_RGB_formula_fit_areas_count, add_default_indexes_to_rgb_channel_function

class RGB_formula_class():
    
    #the first 3 parameters must be rgb formulas for the 3 RGB channels; the provided rgb formulas must be valid
    def __init__(self, red_func = "r", green_func = "g", blue_func = "b", use_pixel_areas = False):
        
        if(use_pixel_areas == False):
            self.red_func = red_func
            self.green_func = green_func
            self.blue_func = blue_func
            
            self.rgb_function_str = f"lambda r,g,b: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)"
            self.rgb_function = eval( self.rgb_function_str)
        else:
            
            self.red_func = add_default_indexes_to_rgb_channel_function(rgb_function=red_func)
            self.green_func = add_default_indexes_to_rgb_channel_function(rgb_function=green_func)
            self.blue_func = add_default_indexes_to_rgb_channel_function(rgb_function=blue_func)

            self.red_func = make_areas_indexes_in_RGB_formula_fit_areas_count(self.red_func)
            self.green_func = make_areas_indexes_in_RGB_formula_fit_areas_count(self.green_func)
            self.blue_func = make_areas_indexes_in_RGB_formula_fit_areas_count(self.blue_func)

            
            
            self.rgb_function_str = f"lambda r,g,b,areas_count: np.stack([ {self.red_func}, {self.green_func}, {self.blue_func} ], axis=-1)"
            self.rgb_function = eval( self.rgb_function_str)
        
