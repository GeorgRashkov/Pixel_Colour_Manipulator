import numpy as np
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel
import RGB_formula_checker

class RGB_formula_elements(QWidget):
    def __init__(self):
        super().__init__()

        self.channels = ["r","g","b"]
        self.text_boxes = {"r":QLineEdit(), "g":QLineEdit(), "b": QLineEdit()}
        self.labels = {"r":QLabel("Red channel formula"), "g":QLabel("Green channel formula"), "b":QLabel("Blue channel formula")}
                
        self.rgb_function_str = f"lambda r,g,b: np.stack([r,g,b], axis=-1)"
        self.rgb_function = eval(self.rgb_function_str)

        self.red_func = "r"
        self.green_func = "g"
        self.blue_func = "b"

        self.text_boxes["r"].setMaxLength(150)
        self.text_boxes["g"].setMaxLength(150)
        self.text_boxes["b"].setMaxLength(150)

    def test_method(self):
        message = f"the formula `{self.rgb_function_str}`\nfor the input (r=1,g=2,b=3) gives {self.rgb_function(r=1,g=2,b=3)}"
        print(message)

    def show_current_RGB_formulas(self):
        message = f"Red channel formula: {self.red_func} \nGreen channel formula: {self.green_func} \nBlue channel formula: {self.blue_func}"
        print(message)
   
   
    def change_RGB_formula(self):       

        r_formula = self.text_boxes["r"].text().replace(' ', '')# removes spaces 
        r_formula = None if (RGB_formula_checker.check_RGB_formula_format(r_formula, "red")==False) else r_formula.replace('^','**').replace('=','==')#replaces '^' with '**' and '=' with '=='
        r_formula = None if (RGB_formula_checker.is_RGB_formula_compatible_with_dxcam(r_formula, "red")==False) else r_formula

        g_formula = self.text_boxes["g"].text().replace(' ', '')# removes spaces
        g_formula = None if (RGB_formula_checker.check_RGB_formula_format(g_formula, "green")==False) else g_formula.replace('^','**').replace('=','==')#replaces '^' with '**' and '=' with '=='
        g_formula = None if (RGB_formula_checker.is_RGB_formula_compatible_with_dxcam(g_formula, "green")==False) else g_formula
        
        b_formula = self.text_boxes["b"].text().replace(' ', '')# removes spaces
        b_formula = None if (RGB_formula_checker.check_RGB_formula_format(b_formula, "blue")==False) else b_formula.replace('^','**').replace('=','==')#replaces '^' with '**' and '=' with '=='
        b_formula = None if (RGB_formula_checker.is_RGB_formula_compatible_with_dxcam(b_formula, "blue")==False) else b_formula

        self.set_color_variables(r_formula, g_formula, b_formula)
        
    
    def set_color_variables(self, r_formula, g_formula, b_formula):
        
        if(r_formula!=None):
            self.red_func = r_formula
        if (g_formula!=None):
            self.green_func = g_formula
        if(b_formula!=None):
            self.blue_func = b_formula
        
        self.rgb_function_str = f"lambda r,g,b: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)"
        self.rgb_function = eval(self.rgb_function_str)