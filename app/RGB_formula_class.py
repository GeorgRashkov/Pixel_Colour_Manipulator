import numpy as np

class RGB_formula_class():
    
    def __init__(self, red_func = "r", green_func = "g", blue_func = "b"):
        self.index = 0
        
        self.red_func = red_func
        self.green_func = green_func
        self.blue_func = blue_func

        self.rgb_function_str = f"lambda r,g,b: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)"
        self.rgb_function = eval( self.rgb_function_str)
        
