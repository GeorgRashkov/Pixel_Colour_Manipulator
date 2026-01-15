from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QCheckBox
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator
import Number_format_checker

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
        self.capture_time = 999_999
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

        #<elements - execution sequence of the functions for setting the pixel values
        self.label_color_functions_sequence = QLabel("Color functions sequence")
        
        self.label_sliders_execution_index = QLabel("Sliders")
        textBox_sliders_execution_index_txt = "3"
        self.textBox_sliders_execution_index = QLineEdit(textBox_sliders_execution_index_txt)
        self.textBox_sliders_execution_index.setMaxLength(1)
        self.textBox_sliders_execution_index.setMaximumWidth(15)
        self.textBox_sliders_execution_index.setValidator(colour_funcs_sequence_validator)
        
        self.label_convolution_execution_index = QLabel("Convolution")
        textBox_convolution_execution_index_txt = "2"
        self.textBox_convolution_execution_index = QLineEdit(textBox_convolution_execution_index_txt)
        self.textBox_convolution_execution_index.setMaxLength(1)
        self.textBox_convolution_execution_index.setMaximumWidth(15)
        self.textBox_convolution_execution_index.setValidator(colour_funcs_sequence_validator)
        
        self.label_otherColorFunctions_execution_index = QLabel("Others")
        textBox_otherColorFunctions_execution_index_txt = "1"
        self.textBox_otherColorFunctions_execution_index = QLineEdit(textBox_otherColorFunctions_execution_index_txt)
        self.textBox_otherColorFunctions_execution_index.setMaxLength(1)
        self.textBox_otherColorFunctions_execution_index.setMaximumWidth(15)
        self.textBox_otherColorFunctions_execution_index.setValidator(colour_funcs_sequence_validator)

        self.color_functions_execution_order = [
            int(textBox_sliders_execution_index_txt), 
            int(textBox_convolution_execution_index_txt), 
            int(textBox_otherColorFunctions_execution_index_txt)
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
        h_layout.addWidget(self.label_color_functions_sequence)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_sliders_execution_index)
        h_layout.addWidget(self.textBox_sliders_execution_index)

        h_layout.addWidget(self.label_convolution_execution_index)
        h_layout.addWidget(self.textBox_convolution_execution_index)

        h_layout.addWidget(self.label_otherColorFunctions_execution_index)
        h_layout.addWidget(self.textBox_otherColorFunctions_execution_index)

        v_layout.addLayout(h_layout)




        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_changes)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

        #widgets placement layout>
    
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
        
        if(self.check_color_functions_sequence_values()==False):
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
        
        return self.capture_time, self.slider_min_value, self.slider_max_value, RGB_use_doubles, self.color_functions_execution_order
    

    def check_color_functions_sequence_values(self):
        allowed_values = ["1", "2", "3"]

        if(
            self.textBox_sliders_execution_index.text() not in allowed_values or
            self.textBox_convolution_execution_index.text() not in allowed_values or
            self.textBox_otherColorFunctions_execution_index.text() not in allowed_values
            ):
            print("Error: one or more of the entered color functions indexes was not found.")
            return False
        
        if(
            self.textBox_sliders_execution_index.text() == self.textBox_convolution_execution_index.text() or
            self.textBox_sliders_execution_index.text() == self.textBox_otherColorFunctions_execution_index.text() or
            self.textBox_convolution_execution_index.text() == self.textBox_otherColorFunctions_execution_index.text() 
        ):
            print("Error: an index of color function cannot be the same as the index of any other color function")
            return False

        if(
            self.textBox_sliders_execution_index.text() != "" or
            self.textBox_convolution_execution_index.text() != "" or
            self.textBox_otherColorFunctions_execution_index.text() != ""
        ):
            self.color_functions_execution_order[0] = int(self.textBox_sliders_execution_index.text())
            self.color_functions_execution_order[1] = int(self.textBox_convolution_execution_index.text())
            self.color_functions_execution_order[2] = int(self.textBox_otherColorFunctions_execution_index.text())
        
        return True
