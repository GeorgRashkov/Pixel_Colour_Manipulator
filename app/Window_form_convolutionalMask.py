from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
)
from PyQt5.QtGui import QIntValidator, QDoubleValidator

import numpy as np

import Number_format_checker

class FormWindow_ConvolutionalFilter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Convolutional mask")
        self.setMinimumSize(200, 30)
        
        #int validators
        int_validator_0to9 = QIntValidator(0, 9, self)
        int_validator_0to999 = QIntValidator(0, 999, self)
        self.filter_value_validator = QDoubleValidator()
        

        #RGB channel bales
        self.label_RGB_channels = QLabel("channels")
        self.label_red_channel = QLabel("red")
        self.label_green_channel = QLabel("green")
        self.label_blue_channel = QLabel("blue")
        

        #filter width 
        self.label_width = QLabel("width")

        self.textBox_width_r = QLineEdit("2")
        self.textBox_width_r.setMaxLength(1)
        self.textBox_width_r.setValidator(int_validator_0to9)
        self.width_r = 2

        self.textBox_width_g = QLineEdit("2")
        self.textBox_width_g.setMaxLength(1)
        self.textBox_width_g.setValidator(int_validator_0to9)
        self.width_g = 2

        self.textBox_width_b = QLineEdit("2")
        self.textBox_width_b.setMaxLength(1)
        self.textBox_width_b.setValidator(int_validator_0to9)
        self.width_b = 2


        #filter height 
        self.label_height = QLabel("height")

        self.textBox_height_r = QLineEdit("2")
        self.textBox_height_r.setMaxLength(1)
        self.textBox_height_r.setValidator(int_validator_0to9)
        self.height_r = 2

        self.textBox_height_g = QLineEdit("2")
        self.textBox_height_g.setMaxLength(1)
        self.textBox_height_g.setValidator(int_validator_0to9)
        self.height_g = 2

        self.textBox_height_b = QLineEdit("2")
        self.textBox_height_b.setMaxLength(1)
        self.textBox_height_b.setValidator(int_validator_0to9)
        self.height_b = 2


        #filter stride (step)
        self.label_stride = QLabel("stride")

        self.textBox_stride_r = QLineEdit("1")
        self.textBox_stride_r.setMaxLength(1)
        self.textBox_stride_r.setValidator(int_validator_0to9)

        self.textBox_stride_g = QLineEdit("1")
        self.textBox_stride_g.setMaxLength(1)
        self.textBox_stride_g.setValidator(int_validator_0to9)

        self.textBox_stride_b = QLineEdit("1")
        self.textBox_stride_b.setMaxLength(1)
        self.textBox_stride_b.setValidator(int_validator_0to9)

        
        #filter dilation (number of holes between the values of the filter)
        self.label_dilation = QLabel("dilation")

        self.textBox_dilation_r = QLineEdit("0")
        self.textBox_dilation_r.setMaxLength(3)
        self.textBox_dilation_r.setValidator(int_validator_0to999)

        self.textBox_dilation_g = QLineEdit("0")
        self.textBox_dilation_g.setMaxLength(3)
        self.textBox_dilation_g.setValidator(int_validator_0to999)

        self.textBox_dilation_b = QLineEdit("0")
        self.textBox_dilation_b.setMaxLength(3)
        self.textBox_dilation_b.setValidator(int_validator_0to999)


        #buttons for creating and appying the filters
        self.button_create_filters = QPushButton("Create filters")
        self.button_create_filters.clicked.connect(self.create_filters)

        self.button_apply_filters = QPushButton("Apply filters")
        self.button_remove_filters = QPushButton("Remove filters")


        #<widgets placement layout

        self.v_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_RGB_channels)
        h_layout.addWidget(self.label_red_channel)
        h_layout.addWidget(self.label_green_channel)
        h_layout.addWidget(self.label_blue_channel)
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_width)
        h_layout.addWidget(self.textBox_width_r)
        h_layout.addWidget(self.textBox_width_g)
        h_layout.addWidget(self.textBox_width_b)
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_height)
        h_layout.addWidget(self.textBox_height_r)
        h_layout.addWidget(self.textBox_height_g)
        h_layout.addWidget(self.textBox_height_b)
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_stride)
        h_layout.addWidget(self.textBox_stride_r)
        h_layout.addWidget(self.textBox_stride_g)
        h_layout.addWidget(self.textBox_stride_b)
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_dilation)
        h_layout.addWidget(self.textBox_dilation_r)
        h_layout.addWidget(self.textBox_dilation_g)
        h_layout.addWidget(self.textBox_dilation_b)
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_create_filters)
        h_layout.addWidget(self.button_apply_filters)
        h_layout.addWidget(self.button_remove_filters)
        self.v_layout.addLayout(h_layout)

        #widgets placement layout>


        #<widgets for placement layout of the values of the convolutional filters 
                
        self.label_red_filter = QLabel("red channel filter")
        self.r_filter_values_layout = QHBoxLayout()
        self.r_filter_values = []#must contain only float numbers

        self.label_green_filter = QLabel("green channel filter")
        self.g_filter_values_layout = QHBoxLayout()
        self.g_filter_values = []#must contain only float numbers

        self.label_blue_filter = QLabel("blue channel filter")
        self.b_filter_values_layout = QHBoxLayout()  
        self.b_filter_values = []#must contain only float numbers     

        self.RGB_filters_values_layout = QVBoxLayout()
        self.RGB_filters_values_layout.addWidget(self.label_red_filter)
        self.RGB_filters_values_layout.addLayout(self.r_filter_values_layout)
        self.RGB_filters_values_layout.addWidget(self.label_green_filter)
        self.RGB_filters_values_layout.addLayout(self.g_filter_values_layout)
        self.RGB_filters_values_layout.addWidget(self.label_blue_filter)
        self.RGB_filters_values_layout.addLayout(self.b_filter_values_layout)

        self.v_layout.addLayout(self.RGB_filters_values_layout)
       
        #widgets for placement layout of the values of the convolutional filters>

        self.setLayout(self.v_layout)
        self.create_filters()

#<functions for creating the RGB filters

    def create_filters(self):
        
        self.fill_empty_filter_characteristics()
        width_height_format_message = self.check_filter_widht_and_height()
        if(width_height_format_message != ""):
            print(width_height_format_message)
            return
       
    
        self.height_r = int(self.textBox_height_r.text())
        self.width_r = int(self.textBox_width_r.text())           
        self.create_filter(int(self.textBox_width_r.text()), self.height_r, "red")
        

        self.height_g = int(self.textBox_height_g.text())
        self.width_g = int(self.textBox_width_g.text())
        self.create_filter(int(self.textBox_width_g.text()), self.height_g, "green")
        

        self.height_b = int(self.textBox_height_b.text())
        self.width_b = int(self.textBox_width_b.text())
        self.create_filter(int(self.textBox_width_b.text()), self.height_b, "blue")

    
    def create_filter(self, width: int, height: int, RBG_channel: str):
        
        v_layout = QVBoxLayout()
       
        for i in range(0, height):
            h_layout = QHBoxLayout()
            
            for j in range(0, width):
                textBox_filterValue = QLineEdit()
                textBox_filterValue.setMaxLength(10)
                textBox_filterValue.setValidator(self.filter_value_validator)
                h_layout.addWidget(textBox_filterValue)

            v_layout.addLayout(h_layout)

        if(RBG_channel == "red"):
            self.clear_layout(self.r_filter_values_layout)
            self.r_filter_values_layout.addLayout(v_layout)
        
        elif(RBG_channel == "green"):
            self.clear_layout(self.g_filter_values_layout)
            self.g_filter_values_layout.addLayout(v_layout)
        
        elif(RBG_channel == "blue"):
            self.clear_layout(self.b_filter_values_layout)
            self.b_filter_values_layout.addLayout(v_layout)

    
    def clear_layout(self, layout: QHBoxLayout):#Recursively delete all widgets and sub-layouts in a layout.
        
        if (layout is not None):
            while (layout.count()):
                item = layout.takeAt(0)

                # Case 1: item is a widget
                widget = item.widget()
                if (widget is not None):
                    widget.deleteLater()

                # Case 2: item is a layout (sub-layout)
                sub_layout = item.layout()
                if (sub_layout is not None):
                    self.clear_layout(sub_layout)  # recurse into sub-layout
                    sub_layout.deleteLater()

#functions for creating the RGB filters>



#<functions for applying the RGB filters to the capture window

    def get_filters_values(self):
                
        self.fill_empty_filter_characteristics()
        stride_dilation_format_message = self.check_filter_stride_and_dilation()
        if(stride_dilation_format_message != ""):
            print(stride_dilation_format_message)
            return None, None, None

        
        self.r_filter_values.clear()
        self.g_filter_values.clear()
        self.b_filter_values.clear()
        
        error_message = ""
        error_message += self.get_filter_values(self.r_filter_values_layout, "red")
        error_message += self.get_filter_values(self.g_filter_values_layout, "green")
        error_message += self.get_filter_values(self.b_filter_values_layout, "blue")
        
        print('{"r": self.r_filter_values, "g":  self.g_filter_values, "b":  self.b_filter_values}\n', {"r": self.r_filter_values, "g":  self.g_filter_values, "b":  self.b_filter_values})
        print('{"r": int(self.textBox_stride_r.text()), "g": int(self.textBox_stride_g.text()), "b": int(self.textBox_stride_b.text())}\n', {"r": int(self.textBox_stride_r.text()), "g": int(self.textBox_stride_g.text()), "b": int(self.textBox_stride_b.text())})
        print('{"r": int(self.textBox_dilation_r.text()), "g": int(self.textBox_dilation_g.text()), "b": int(self.textBox_dilation_b.text())}\n', {"r": int(self.textBox_dilation_r.text()), "g": int(self.textBox_dilation_g.text()), "b": int(self.textBox_dilation_b.text())})
        
        if(error_message == ""):

            r_filter_values = np.array(self.r_filter_values).reshape(self.height_r, self.width_r)
            g_filter_values = np.array(self.g_filter_values).reshape(self.height_g, self.width_g)
            b_filter_values = np.array(self.b_filter_values).reshape(self.height_b, self.width_b)

            self.textBox_width_r.setText(str(self.width_r))
            self.textBox_height_r.setText(str(self.height_r))

            self.textBox_width_g.setText(str(self.width_g))
            self.textBox_height_g.setText(str(self.height_g))

            self.textBox_width_b.setText(str(self.width_b))
            self.textBox_height_b.setText(str(self.height_b))

            #returns 3 dictionaries: the first contains the filters values; the second contains the filters strides; the third contains the filters dilations (number of holes between the elements of the filters)
            return {"r": r_filter_values, "g":  g_filter_values, "b":  b_filter_values}, {"r": int(self.textBox_stride_r.text()), "g": int(self.textBox_stride_g.text()), "b": int(self.textBox_stride_b.text())}, {"r": int(self.textBox_dilation_r.text()), "g": int(self.textBox_dilation_g.text()), "b": int(self.textBox_dilation_b.text())}
            
        else:
            print(error_message)
            return None, None, None
            
        
    
    def get_filter_values(self, filter_layout: QHBoxLayout, RBG_channel: str):
               
        #cycle through all elements inside `filter_layout`       
        for i in range(0, filter_layout.count()):
            
            item = filter_layout.itemAt(i)

            # Case 1: item is a widget
            widget = item.widget()
            if(widget is not None and isinstance(widget, QLineEdit)):#if the current element in `filter_layout` is text box execute this code (each text box must contain a separate filter value) 
                filter_value = widget.text()
                    
                if(Number_format_checker.check_for_float_format(filter_value)==False):#if the filter value is not a valid float number execute this code
                        
                    if(RBG_channel=="red"):
                        self.r_filter_values.clear()
                    elif(RBG_channel=="green"):
                        self.g_filter_values.clear()
                    elif(RBG_channel=="blue"):
                        self.b_filter_values.clear()
                    return f"Error: one or more of the values of the filter for the {RBG_channel} channel were in wrong format!\n"
                
                else:#if the filter value is a valid float number execute this code (empty string is also considered a valid format)
                    if(filter_value==""):
                        filter_value = 0

                    filter_value = float(filter_value)
                    if(RBG_channel=="red"):
                        self.r_filter_values.append(filter_value)
                    elif(RBG_channel=="green"):
                        self.g_filter_values.append(filter_value)
                    elif(RBG_channel=="blue"):
                        self.b_filter_values.append(filter_value)
                
            # Case 2: item is a layout (sub-layout)
            sub_layout = item.layout()
            if(sub_layout is not None):
                error_message = self.get_filter_values(sub_layout, RBG_channel)
                if(error_message != ""):
                    return error_message
            
        return ""
        
#functions for applying the RGB filters to the capture window>



#<functions for checking the format of the filter characteristics

    #this check is needed before creating the filters
    def check_filter_widht_and_height(self):
        is_valid = True

        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_width_r.text()) 
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_width_g.text()) 
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_width_b.text()) 
        if(is_valid==False):
            return "Error: one or more of the width fields were in wrong format."

        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_height_r.text()) 
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_height_g.text()) 
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_height_b.text()) 
        if(is_valid==False):
            return "Error: one or more of the height fields were in wrong format."

        return ""
    
    #this check is needed before applying the filters
    def check_filter_stride_and_dilation(self):      
        is_valid = True

        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_stride_r.text(), is_zero_allowed=False) 
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_stride_g.text(), is_zero_allowed=False) 
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_stride_b.text(), is_zero_allowed=False)  
        if(is_valid==False):
            return "Error: one or more of the stride fields were either in wrong format or were equal to zero."
      
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_dilation_r.text()) 
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_dilation_g.text()) 
        is_valid = is_valid and Number_format_checker.check_for_positive_int_format(self.textBox_dilation_b.text()) 
        if(is_valid==False):
            return "Error: one or more of the dilation fields were in wrong format."
               
        return ""
    
#functions for checking the format of the filter characteristics>



    #fills every emtpy filter characteristic field with default value    
    def fill_empty_filter_characteristics(self):
        
        self.textBox_width_r.setText("0" if(self.textBox_width_r.text()=="") else self.textBox_width_r.text())
        self.textBox_width_g.setText("0" if(self.textBox_width_g.text()=="") else self.textBox_width_g.text())
        self.textBox_width_b.setText("0" if(self.textBox_width_b.text()=="") else self.textBox_width_b.text())

        self.textBox_height_r.setText("0" if(self.textBox_height_r.text()=="") else self.textBox_height_r.text())
        self.textBox_height_g.setText("0" if(self.textBox_height_g.text()=="") else self.textBox_height_g.text())
        self.textBox_height_b.setText("0" if(self.textBox_height_b.text()=="") else self.textBox_height_b.text())

        self.textBox_stride_r.setText("1" if(self.textBox_stride_r.text()=="") else self.textBox_stride_r.text())
        self.textBox_stride_g.setText("1" if(self.textBox_stride_g.text()=="") else self.textBox_stride_g.text())
        self.textBox_stride_b.setText("1" if(self.textBox_stride_b.text()=="") else self.textBox_stride_b.text())

        self.textBox_dilation_r.setText("0" if(self.textBox_dilation_r.text()=="") else self.textBox_dilation_r.text())
        self.textBox_dilation_g.setText("0" if(self.textBox_dilation_g.text()=="") else self.textBox_dilation_g.text())
        self.textBox_dilation_b.setText("0" if(self.textBox_dilation_b.text()=="") else self.textBox_dilation_b.text())
       
      