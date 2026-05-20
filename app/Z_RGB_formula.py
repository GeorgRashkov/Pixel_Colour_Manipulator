import numpy as np
#from Z_RGB_formula_checker import make_areas_indexes_in_RGB_formula_fit_areas_count, add_default_indexes_to_rgb_channel_function

class RGB_formula():
    
    #the first 3 parameters must be rgb formulas for the 3 RGB channels; the provided rgb formulas must be valid
    def __init__(self, red_func = "r", green_func = "g", blue_func = "b", use_pixel_areas = False):
        
        if(use_pixel_areas == False):
            self.red_func = red_func
            self.green_func = green_func
            self.blue_func = blue_func
            
            self.rgb_function_str = f"lambda r,g,b,v=0: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)"
            self.rgb_function = eval( self.rgb_function_str)
        else:
            
            self.red_func = self.add_default_indexes_to_rgb_channel_function(rgb_function=red_func)
            self.green_func = self.add_default_indexes_to_rgb_channel_function(rgb_function=green_func)
            self.blue_func = self.add_default_indexes_to_rgb_channel_function(rgb_function=blue_func)

            self.red_func = self.make_areas_indexes_in_RGB_formula_fit_areas_count(self.red_func)
            self.green_func = self.make_areas_indexes_in_RGB_formula_fit_areas_count(self.green_func)
            self.blue_func = self.make_areas_indexes_in_RGB_formula_fit_areas_count(self.blue_func)

            
            self.rgb_function_str = f"lambda r,g,b,areas_count,v=np.array([0], dtype=np.uint8): np.stack([ {self.red_func}, {self.green_func}, {self.blue_func} ], axis=-1)"
            self.rgb_function = eval( self.rgb_function_str)
    


    
    
    #this function can be used by any rgb function that uses image areas; the function replaces ["r","g","b"] with ["r[0]","g[0]","b[0]"] only when the rgb channels have no area index
    #this function must be used only for valid rgb functions
    def add_default_indexes_to_rgb_channel_function(self, rgb_function:str):#`rgb_function` must be a rgb formula for one of the rgb channels
        
        rgb_channels = ["r", "g", "b", "v"]#`v` is not a rgb channel; it is a numpy array containing int values

        for i in range (0, len(rgb_channels)):
            rgb_channel = rgb_channels[i]
            rgb_function = self.add_default_indexes_to_rgb_channel(rgb_function, rgb_channel)
        
        return rgb_function

    def add_default_indexes_to_rgb_channel(self, rgb_function:str, rgb_channel:str):
        
        index = 0
        while (index < len(rgb_function)):
            
            channel_index = rgb_function.find(rgb_channel,index)
            if(channel_index == -1):
                break

            if(channel_index < len(rgb_function) - 1):
                if(rgb_function[channel_index+1] != "["):
                    rgb_function = rgb_function[:channel_index+1] + "[0]" + rgb_function[channel_index+1:]

            elif(channel_index == len(rgb_function) - 1):
                rgb_function = rgb_function + "[0]"
            
            index = channel_index+1
        
        return rgb_function
    

    #this functions can be used by any RGB channel formula which is supposed to work with image areas; it will replace things like `r[5]` with `r[5 if 5<areas_count else 0]}`
    def make_areas_indexes_in_RGB_formula_fit_areas_count(self, rgb_formula: str):

        start_index = 0
        while(True):

            openining_bracket_index = rgb_formula.find("[",start_index)
            if(openining_bracket_index == -1):
                break

            closing_bracket_index = rgb_formula.find("]",openining_bracket_index+1)
            if(closing_bracket_index == -1):
                break

            current_index_in_brackets = rgb_formula[openining_bracket_index+1:closing_bracket_index]
            
            values_count_variable = "len(v)" if(rgb_formula[openining_bracket_index-1]=="v") else "areas_count"

            rgb_formula = rgb_formula[:closing_bracket_index] + f" if {current_index_in_brackets}<{values_count_variable} else 0" + rgb_formula[closing_bracket_index:]

            start_index = rgb_formula.find("]",closing_bracket_index+1)
        
        return rgb_formula



"""
#< in testing state !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   
    
    #the first 3 parameters must be rgb formulas for the 3 RGB channels; the provided rgb formulas must be valid
    def __init__(self, red_func = "r", green_func = "g", blue_func = "b", use_pixel_areas = False):
        
        if(use_pixel_areas == False):
            self.red_func = red_func
            self.green_func = green_func
            self.blue_func = blue_func

            self.red_func = self.add_masks_to_rgb_channel_formula(self.red_func)
            self.green_func = self.add_masks_to_rgb_channel_formula(self.green_func)
            self.blue_func = self.add_masks_to_rgb_channel_formula(self.blue_func)
            
            self.rgb_function_str = f"lambda r,g,b,v=0, m=slice(None): np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)"
            self.rgb_function = eval( self.rgb_function_str)
        else:
            
            self.red_func = self.add_default_indexes_to_rgb_channel_function(rgb_function=red_func)
            self.green_func = self.add_default_indexes_to_rgb_channel_function(rgb_function=green_func)
            self.blue_func = self.add_default_indexes_to_rgb_channel_function(rgb_function=blue_func)

            self.red_func = self.make_areas_indexes_in_RGB_formula_fit_areas_count(self.red_func)
            self.green_func = self.make_areas_indexes_in_RGB_formula_fit_areas_count(self.green_func)
            self.blue_func = self.make_areas_indexes_in_RGB_formula_fit_areas_count(self.blue_func)

            self.red_func = self.add_masks_to_rgb_channel_formula(self.red_func)
            self.green_func = self.add_masks_to_rgb_channel_formula(self.green_func)
            self.blue_func = self.add_masks_to_rgb_channel_formula(self.blue_func)
            
            self.rgb_function_str = f"lambda r,g,b,areas_count,v=np.array([0], dtype=np.uint8), m=slice(None): np.stack([ {self.red_func}, {self.green_func}, {self.blue_func} ], axis=-1)"
            self.rgb_function = eval( self.rgb_function_str)

    def add_masks_to_rgb_channel_formula(self, rgb_formula: str):

        rgb_channels = ["r", "g", "b"]

        for rgb_channel in rgb_channels:
            rgb_formula = self.add_masks_to_rgb_channel(rgb_formula=rgb_formula, rgb_channel=rgb_channel)
        
        return rgb_formula
        


    def add_masks_to_rgb_channel(self, rgb_formula: str, rgb_channel:str):

        rgb_channel_index = 0
        mask_index = 0
        mask_str = "[m]"

        while (rgb_channel_index < len(rgb_formula)):
            
            rgb_channel_index = rgb_formula.find(rgb_channel,rgb_channel_index)
            if(rgb_channel_index == -1):
                break
            
            openining_bracket_index = rgb_formula.find("[",rgb_channel_index)
            if(openining_bracket_index != rgb_channel_index+1):
                mask_index = rgb_channel_index+1
            else:
                closing_bracket_index = rgb_formula.find("]",rgb_channel_index+1)
                mask_index = closing_bracket_index+1

            rgb_formula = rgb_formula[:mask_index] + mask_str + rgb_formula[mask_index:]

            rgb_channel_index = mask_index + len(mask_str)
        
        return rgb_formula



    #in testing state>!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
            
