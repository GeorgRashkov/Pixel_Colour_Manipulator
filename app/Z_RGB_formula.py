
import numpy as np

class RGB_formula():
    
    #the first 3 parameters must be rgb formulas for the 3 RGB channels; the provided rgb formulas must be valid
    def __init__(self, red_func = "r", green_func = "g", blue_func = "b"):
        
        self.red_func = red_func
        self.green_func = green_func
        self.blue_func = blue_func

        self.rgb_function_str = f"lambda r,g,b, areas_count=1, v=np.array([0], dtype=np.uint8) : np.stack([ {self.red_func}, {self.green_func}, {self.blue_func} ], axis=-1)"
        self.rgb_function = eval(self.rgb_function_str)