import numpy as np
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel
from RGB_formula_initializer import RGB_formula_initializer

class RGB_formula_elements(QWidget):
    def __init__(self, use_areas: bool = False, text_boxes_max_lenght: int = 150):
        super().__init__()
        self.use_areas = use_areas

        self.channels = ["r","g","b"]
        self.text_boxes = {"r":QLineEdit(), "g":QLineEdit(), "b": QLineEdit()}
        self.labels = {"r":QLabel("Red channel formula"), "g":QLabel("Green channel formula"), "b":QLabel("Blue channel formula")}
                
        self.rgb_function_str = f"lambda r,g,b,v=0: np.stack([r,g,b], axis=-1)" if self.use_areas == False else f"lambda r,g,b,areas_count,v=np.array([0], dtype=np.uint8): np.stack([r,g,b], axis=-1)"
        self.rgb_function = eval(self.rgb_function_str)

        self.red_func = "r"
        self.green_func = "g"
        self.blue_func = "b"

        self.text_boxes["r"].setMaxLength(text_boxes_max_lenght)
        self.text_boxes["g"].setMaxLength(text_boxes_max_lenght)
        self.text_boxes["b"].setMaxLength(text_boxes_max_lenght)

        self.rgb_formula_initializer = RGB_formula_initializer()

    def test_method(self):
        message = f"the formula `{self.rgb_function_str}`\nfor the input (r=1,g=2,b=3) gives {self.rgb_function(r=1,g=2,b=3)}"
        print(message)

    def show_current_RGB_formulas(self):
        message = f"Red channel formula: {self.red_func} \nGreen channel formula: {self.green_func} \nBlue channel formula: {self.blue_func}"
        print(message)
   



    def change_RGB_formula(self) -> bool:  

        r_formula = self.text_boxes["r"].text()
        g_formula = self.text_boxes["g"].text()
        b_formula = self.text_boxes["b"].text()

        rgb_formula = self.rgb_formula_initializer.create_rgb_formulas_without_pixel_areas(r_formula=r_formula, g_formula=g_formula, b_formula=b_formula, use_pixel_areas=self.use_areas)
        
        if(rgb_formula is not None):
            self.rgb_function_str = rgb_formula.rgb_function_str
            self.rgb_function = rgb_formula.rgb_function

            self.red_func = rgb_formula.red_func
            self.green_func = rgb_formula.green_func
            self.blue_func = rgb_formula.blue_func

            return True
        else:
            return False