from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QCheckBox
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
import Number_format_checker
from Number_operatios import get_integers_from_text

class FormWindow_Settings(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Settings")
        self.setMinimumSize(200, 30)

        #validators
        capture_time_validator = QDoubleValidator()
        capture_time_validator.setBottom(0.001)
        slider_validator = QIntValidator()
        colour_funcs_sequence_validator = QIntValidator()

        #elements - update capture time
        self.capture_time = 0.1
        self.label_update_capture_time = QLabel("Update capture Time")
        self.textBox_update_capture_time = QLineEdit(str(self.capture_time))
        self.textBox_update_capture_time.setMaxLength(6)
        self.textBox_update_capture_time.setValidator(capture_time_validator)
        


        #elements - use doubles or ints after pixel transformation (elements)
        self.label_RGB_use_doubles = QLabel("RGB use doubles")
        self.checkBox_RGB_use_doubles = QCheckBox()
                
        

        #<elements - set min and max values for the sliders on the window capture
        self.slider_min_value = 0
        self.label_slider_min_value = QLabel("Slider min value (in %)")
        self.textBox_slider_min_value = QLineEdit(str(self.slider_min_value))
        self.textBox_slider_min_value.setMaxLength(9)
        self.textBox_slider_min_value.setValidator(slider_validator)
        
        self.slider_max_value = 100
        self.label_slider_max_value = QLabel("Slider max value (in %)")
        self.textBox_slider_max_value = QLineEdit(str( self.slider_max_value))
        self.textBox_slider_max_value.setMaxLength(9)
        self.textBox_slider_max_value.setValidator(slider_validator)
        #elements - set min and max values for the sliders on the window capture>

        #<elements - rgb formulas ids
        self.rgb_formulas_ids:list[int] = [0]
        self.label_rgb_formulas_ids = QLabel("rgb formulas ids")
        self.textBox_rgb_formulas_ids = QLineEdit()
        #elements - rgb formulas ids>

        #<elements - execution sequence of the functions for setting the pixel values
        self.allowed_colour_functions_values = ["1", "2", "3", "4", "5"]
        
        self.label_colour_functions_sequence = QLabel("Colour functions sequence")
        
        self.label_rgbFunc_execution_index = QLabel("RGB Func")
        textBox_rgbFunc_execution_index_txt = "1"
        self.textBox_rgbFunc_execution_index = QLineEdit(textBox_rgbFunc_execution_index_txt)
        self.textBox_rgbFunc_execution_index.setMaxLength(1)
        self.textBox_rgbFunc_execution_index.setMaximumWidth(15)
        self.textBox_rgbFunc_execution_index.setValidator(colour_funcs_sequence_validator)

        self.label_mask_execution_index = QLabel("Mask")
        textBox_mask_execution_index_txt = "2"
        self.textBox_mask_execution_index = QLineEdit(textBox_mask_execution_index_txt)
        self.textBox_mask_execution_index.setMaxLength(1)
        self.textBox_mask_execution_index.setMaximumWidth(15)
        self.textBox_mask_execution_index.setValidator(colour_funcs_sequence_validator)
        
        self.label_convolution_execution_index = QLabel("Convolution")
        textBox_convolution_execution_index_txt = "3"
        self.textBox_convolution_execution_index = QLineEdit(textBox_convolution_execution_index_txt)
        self.textBox_convolution_execution_index.setMaxLength(1)
        self.textBox_convolution_execution_index.setMaximumWidth(15)
        self.textBox_convolution_execution_index.setValidator(colour_funcs_sequence_validator)

        self.label_swapPixelAreas_execution_index = QLabel("Swap areas")
        textBox_swapPixelAreas_execution_index_txt = "4"
        self.textBox_swapPixelAreas_execution_index = QLineEdit(textBox_swapPixelAreas_execution_index_txt)
        self.textBox_swapPixelAreas_execution_index.setMaxLength(1)
        self.textBox_swapPixelAreas_execution_index.setMaximumWidth(15)
        self.textBox_swapPixelAreas_execution_index.setValidator(colour_funcs_sequence_validator)

        self.label_sliders_execution_index = QLabel("Sliders")
        textBox_sliders_execution_index_txt = "5"
        self.textBox_sliders_execution_index = QLineEdit(textBox_sliders_execution_index_txt)
        self.textBox_sliders_execution_index.setMaxLength(1)
        self.textBox_sliders_execution_index.setMaximumWidth(15)
        self.textBox_sliders_execution_index.setValidator(colour_funcs_sequence_validator)

        self.colour_functions_execution_order = [
            int(textBox_rgbFunc_execution_index_txt), 
            int(textBox_mask_execution_index_txt),
            int(textBox_convolution_execution_index_txt), 
            int(textBox_swapPixelAreas_execution_index_txt),
            int(textBox_sliders_execution_index_txt)
        ]
        #elements - execution sequence of the functions for setting the pixel values>

        #elements - apply changes
        self.button_apply_changes = QPushButton("OK")


        #<widgets placement layout

        v_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_update_capture_time)
        h_layout.addWidget(self.textBox_update_capture_time)
        v_layout.addLayout(h_layout)




        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_RGB_use_doubles)
        h_layout.addWidget(self.checkBox_RGB_use_doubles)
        v_layout.addLayout(h_layout)

      


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_slider_min_value)
        h_layout.addWidget(self.textBox_slider_min_value)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_slider_max_value)
        h_layout.addWidget(self.textBox_slider_max_value)
        v_layout.addLayout(h_layout)
        


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_rgb_formulas_ids)
        h_layout.addWidget(self.textBox_rgb_formulas_ids)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_colour_functions_sequence)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()

        h_layout.addWidget(self.textBox_rgbFunc_execution_index)
        h_layout.addWidget(self.label_rgbFunc_execution_index)

        h_layout.addWidget(self.textBox_mask_execution_index)
        h_layout.addWidget(self.label_mask_execution_index)

        h_layout.addWidget(self.textBox_convolution_execution_index)
        h_layout.addWidget(self.label_convolution_execution_index)

        h_layout.addWidget(self.textBox_swapPixelAreas_execution_index)
        h_layout.addWidget(self.label_swapPixelAreas_execution_index)

        h_layout.addWidget(self.textBox_sliders_execution_index)
        h_layout.addWidget(self.label_sliders_execution_index)

        v_layout.addLayout(h_layout)




        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_changes)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

        #widgets placement layout>
    
    """
    def apply_settings(self):#applies the settings only if all fields are in valid format (empty fields are considered as a correct format which means there will be no error messages for emtpy fields but their correspoding settings values will not change)

        capture_time = self.textBox_update_capture_time.text()
        if(Number_format_checker.check_for_positive_float_format(capture_time, is_zero_allowed=False)==False):
            print("Error: the text box for updating the capture time was either in wrong format or it was equal to zero")
            return None, None, None, None, None

       
        slider_min_value = self.textBox_slider_min_value.text()
        if(Number_format_checker.check_for_int_format(slider_min_value)==False):
            print("Error: the text box for setting the min value of the slider was in wrong format")
            return None, None, None, None, None
        
        slider_max_value = self.textBox_slider_max_value.text()
        if(Number_format_checker.check_for_int_format(slider_max_value)==False):
            print("Error: the text box for setting the max value of the slider was in wrong format")
            return None, None, None, None, None
        
        if(self.check_colour_functions_sequence_values()==False):
            return None, None, None, None, None


        RGB_use_doubles = self.checkBox_RGB_use_doubles.isChecked()
       

        if(capture_time != ''):
            self.capture_time = float(capture_time)*1000 if(capture_time != "0") else 1
        if(slider_min_value != ''):
            self.slider_min_value = int(slider_min_value)
        if(slider_max_value != ''):
            self.slider_max_value = int(slider_max_value)

        if(self.slider_min_value > self.slider_max_value):
            print("Error: the minimun value of the sliders cannot be higher than the max value!")
            return None, None, None, None, None
        
        return self.capture_time, self.slider_min_value, self.slider_max_value, RGB_use_doubles, self.colour_functions_execution_order
    """

    #applies the settings only if all fields are in valid format;
    # empty fields are considered as a correct format which means there will be no error messages for emtpy fields but their correspoding settings values will not change
    def apply_settings(self) -> tuple[int, int, int, bool, list[int], list[int]]|None:

        capture_time_txt = self.textBox_update_capture_time.text()
        if(Number_format_checker.check_for_positive_float_format(capture_time_txt, is_zero_allowed=False)==False):
            print("Error: capture time must be a positive number above zero")
            return None

       
        slider_min_value_txt = self.textBox_slider_min_value.text()
        if(Number_format_checker.check_for_int_format(slider_min_value_txt)==False):
            print("Error: the slider min value must be an integer")
            return None
        
        slider_max_value_txt = self.textBox_slider_max_value.text()
        if(Number_format_checker.check_for_int_format(slider_max_value_txt)==False):
            print("Error: the slider max value must be an integer")
            return None

        rgb_formulas_ids_txt = self.textBox_rgb_formulas_ids.text().replace(" ", "").replace("\n", "")
        if(rgb_formulas_ids_txt != ""):

            rgb_formulas_ids:list[int] = get_integers_from_text(txt=rgb_formulas_ids_txt)
            if(rgb_formulas_ids is None):
                print("Error: rgb formulas ids must be positive integers separated by comma")
                return None
            else:
                self.rgb_formulas_ids = rgb_formulas_ids
        
        if(self.check_colour_functions_sequence_values()==False):
            return None


        RGB_use_doubles = self.checkBox_RGB_use_doubles.isChecked()
       

        if(capture_time_txt != ''):
            self.capture_time = float(capture_time_txt)*1000
        if(slider_min_value_txt != ''):
            self.slider_min_value = int(slider_min_value_txt)
        if(slider_max_value_txt != ''):
            self.slider_max_value = int(slider_max_value_txt)

        if(self.slider_min_value > self.slider_max_value):
            print("Error: the minimun value of the sliders cannot be higher than the max value!")
            return None
        
        return (self.capture_time, self.slider_min_value, self.slider_max_value, RGB_use_doubles, self.rgb_formulas_ids, self.colour_functions_execution_order)
    
    
    def check_colour_functions_sequence_values(self) -> bool:

        colour_functions_input = [self.textBox_rgbFunc_execution_index.text(), self.textBox_mask_execution_index.text(), 
                                  self.textBox_convolution_execution_index.text(), self.textBox_swapPixelAreas_execution_index.text(),
                                  self.textBox_sliders_execution_index.text()]
        
        for i in range(0, len(colour_functions_input)):
            
            if(colour_functions_input[i] not in self.allowed_colour_functions_values):
                print(f"Error: one or more of the entered colour functions indexes was not found! The allowed indexes are:\n{self.allowed_colour_functions_values}")
                return False
            
            for j in range(i+1, len(colour_functions_input)):
                if(colour_functions_input[i] == colour_functions_input[j]):
                    print("Error: an index of colour function cannot be the same as the index of any other colour function!")
                    return False
        
        for i in range(0, len(colour_functions_input)):
            self.colour_functions_execution_order[i] = int(colour_functions_input[i])

        return True
