from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor, QImage
import sys
import numpy as np
import dxcam
import Window_capture, Window_canvas, Window_form_drawMask, Window_form_captureMask, Window_settings, Window_form_convolutionalMask

import Number_format_checker

class MainApp: 
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        #screen
        self.screen = self.app.primaryScreen()
        self.screen_width = self.screen.geometry().width()
        self.screen_height = self.screen.geometry().height()

        #capture window
        self.camera = dxcam.create() #dxcam instance (fast screen capture)
        self.capture_window = Window_capture.CaptureWindow(self.screen_width, self.screen_height, self.camera)
        self.capture_window.button_open_settings.clicked.connect(self.open_window_settings)
        self.capture_window.button_open_drawMask.clicked.connect(self.open_windows_draw_mask)
        self.capture_window.button_open_captureMask.clicked.connect(self.open_window_capture_mask)
        self.capture_window.button_open_convolutionalFilter.clicked.connect(self.open_window_covolutional_filter)
        
        #settings window
        self.settings_window = Window_settings.FormWindow_Settings()
        self.settings_window.button_apply_changes.clicked.connect(self.apply_settings)

        #convolutional filter window
        self.convolutional_filter_window = Window_form_convolutionalMask.FormWindow_ConvolutionalFilter()
        self.convolutional_filter_window.button_apply_filters.clicked.connect(self.apply_convolutional_filters)
        self.convolutional_filter_window.button_remove_filters.clicked.connect(self.remove_convolutional_filters)

        #<form window with canvas window (draw mask)
        self.canvas_window = Window_canvas.CanvasWindow()
      
        self.mask_ids = [[255, 0, 0], [0, 255, 0],[0, 0, 255], [255, 255, 0],[0, 0, 0], [255, 255, 255]]
        draw_colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255), QColor(255, 255, 0), QColor(0, 0, 0), QColor(255, 255, 255),]
        self.form_window_draw_mask = Window_form_drawMask.FormWindow_DrawMask(columns_count=3, draw_colors = draw_colors)

        for i in range(0, len(self.form_window_draw_mask.forms)):
            self.form_window_draw_mask.forms[i].drawing_btn.clicked.connect(lambda _, color=draw_colors[i]: self.canvas_window.canvas.set_color(color))
            #self.form_window.forms[i].button_for_seting_color_variables.clicked.connect(self.form_window.forms[i].change_RGB_formula)
            self.form_window_draw_mask.forms[i].button_for_seting_color_variables.clicked.connect(lambda: self.apply_mask(True))
        
        self.form_window_draw_mask.clear_btn.clicked.connect(self.canvas_window.canvas.clear)
        self.form_window_draw_mask.apply_mask_btn.clicked.connect(lambda: self.apply_mask(False))
        self.form_window_draw_mask.remove_mask_btn.clicked.connect(self.remove_mask)
        self.form_window_draw_mask.button_apply_brush_size_changes.clicked.connect(self.change_brush_size_parameters)
        #form window with canvas window (draw mask)>

        #<form window (create mask from capture window)
        self.form_window_capture_mask = Window_form_captureMask.FormWindow_CaptureMask(columns_count=3, draw_colors = draw_colors)

        
        for i in range(0, len(self.form_window_capture_mask.forms)):
            self.form_window_capture_mask.forms[i].button_for_seting_color_variables.clicked.connect(self.apply_capture_mask)
        
        #form window (create mask from capture window)>
    
        self.capture_window.show()
        sys.exit(self.app.exec_())

    def run(self):
        sys.exit(self.app.exec_())
    
    def open_window_settings(self):
        self.settings_window.show()

    def open_windows_draw_mask(self):
        self.form_window_draw_mask.show()
        self.canvas_window.show()

    def open_window_capture_mask(self):
        self.form_window_capture_mask.show()
    
    def open_window_covolutional_filter(self):
        self.convolutional_filter_window.show()
        

    def apply_settings(self):
        capture_time, slider_min_value, slider_max_value, RGB_use_doubles, color_functions_execution_order = self.settings_window.apply_settings()
        if(capture_time != None):#if any of the upper variables is "None" than all of them will always be "None"
            self.capture_window.apply_settings(capture_time=capture_time, slider_min_value=slider_min_value, slider_max_value=slider_max_value, RGB_use_doubles=RGB_use_doubles, color_functions_execution_order = color_functions_execution_order)

    def apply_convolutional_filters(self):
        
        rgb_kernels_values, rgb_kernels_strides, rgb_kernels_holes_count = self.convolutional_filter_window.get_filters_values()       
        
        print("rgb_kernels_values", rgb_kernels_values)
        print("rgb_kernels_strides", rgb_kernels_strides)
        print("rgb_kernels_holes_count", rgb_kernels_holes_count)

        if(rgb_kernels_values != None and rgb_kernels_strides != None and rgb_kernels_holes_count != None):
            self.capture_window.create_rgb_kernels(rgb_kernels_values = rgb_kernels_values, rgb_kernels_strides = rgb_kernels_strides, rgb_kernels_holes_count = rgb_kernels_holes_count)
        
    def remove_convolutional_filters(self):

        self.capture_window.remove_rgb_kernels()

    def remove_mask(self):
        self.capture_window.remove_mask()


    def change_brush_size_parameters(self):

        #take the brush size parameters
        brush_size_min_value = self.form_window_draw_mask.textBox_brush_size_min_value.text()
        brush_size_max_value = self.form_window_draw_mask.textBox_brush_size_max_value.text()
        brush_size_delta = self.form_window_draw_mask.textBox_brush_size_delta.text()

        #check the the format of the brush size parameters
        if(Number_format_checker.check_for_positive_int_format(brush_size_min_value, is_zero_allowed=False) == False):
            print("Error: the brush min size field was either in wrong format or it was equal to 0")
            return        
        if(Number_format_checker.check_for_positive_int_format(brush_size_max_value, is_zero_allowed=False) == False):
            print("Error: the brush max size field was either in wrong format or it was equal to 0")
            return        
        if(Number_format_checker.check_for_positive_int_format(brush_size_delta, is_zero_allowed=False) == False):
            print("Error: the brush size icrement field was either in wrong format or it was equal to 0")
            return
        
        brush_min_size = int(brush_size_min_value)
        brush_max_size = int(brush_size_max_value)
        brush_delta = int(brush_size_delta)

        if(brush_min_size>brush_max_size):
            print("Error: brush min size value cannot be higher than brush max size value")
            return

        self.canvas_window.canvas.set_brush_size_arguments(brush_min_size = brush_min_size, brush_max_size=brush_max_size, brush_delta=brush_delta)      





 #< Functions for applying drawn/captured masks

        

    def apply_mask(self, change_RGB_formula):
        #Return the current canvas as a NumPy array (H x W x 4, RGBA).
        # Grab the widget’s current visual state as a QImage
        qimage = self.canvas_window.canvas.grab().toImage()

        # Ensure format is RGBA8888 for consistent bytes layout
        qimage = qimage.convertToFormat(QImage.Format_RGBA8888)

        width = qimage.width()
        height = qimage.height()
        
        # Get the raw pointer to the image data
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())

        
        mask = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))# Create a NumPy array (height, width, 4)
        mask = mask[:,:,:3]# a  NumPy array (height, width, 3); each value in the most inner arrays will contain 3 elements and 2 of them will be always 0
        
        
        color_functions = []
        color_functions_strings = []
        for form in self.form_window_draw_mask.forms:
            if(change_RGB_formula):
                form.rgb_elements.change_RGB_formula()
            color_functions.append(form.rgb_elements.rgb_function)
            color_functions_strings.append(form.rgb_elements.rgb_function_str)
       

        mask_filters = []
        for mask_id in self.mask_ids:
            mask_filter = np.all(mask == mask_id, axis=-1)
            mask_filters.append(mask_filter)

       
        color_functions, default_color_function, mask_filters = self.get_unique_colour_functions_and_masks(colour_functions = color_functions, colour_functions_strings = color_functions_strings, mask_filters = mask_filters, same_funcs_combine_masks=True)
        

        self.capture_window.apply_mask_settings(mask_filters, color_functions, default_color_function)


    #this function will get only the unique colour functions and their masks to increase performace when the user uses the same RGB formulas
    def get_unique_colour_functions_and_masks(self, colour_functions: list, colour_functions_strings: list, mask_filters: list, same_funcs_combine_masks: bool):#all parameter collections must have the same number of elements
        
        if(len(colour_functions)==0 or len(colour_functions_strings) == 0 or len(mask_filters) == 0):           
            return None, None, None

        colour_functions_output = []#this list will cotain the lambda functions
        mask_filters_output = {}#this dictionary will have the string representatation of the lambda functions as keys and it will have the filters as a value      
               
        for i in range(0, len(colour_functions_strings)):# cycle through all colour functions and masks

            is_colour_function_unique = True

            for j in range(0, i):#check whether the current (on index i) colour function is unique in comparison to the privous colour functions
                
                #if the current (on index i) colour function was not unique execute this code
                if(colour_functions_strings[i] == colour_functions_strings[j]):
                    is_colour_function_unique = False
                    if(same_funcs_combine_masks == True):
                        mask_filters_output[colour_functions_strings[j]] |= mask_filters[i]#since the current (on index i) colour function was not unique, combine it's mask filter with the mask filter of the first colour function that had the same content in it's body
                    break
            
            if(is_colour_function_unique == True):
                
                colour_functions_output.append(colour_functions[i])              
                mask_filters_output[colour_functions_strings[i]] = mask_filters[i]
                
                
        default_colour_function = colour_functions_output[-1]
        colour_functions_output = colour_functions_output[:len(colour_functions_output)-1]
        
        mask_filters_output = list(mask_filters_output.values())
        mask_filters_output = mask_filters_output[:len(mask_filters_output)-1]

        return colour_functions_output, default_colour_function, mask_filters_output



    def apply_capture_mask(self):#NOT FINISHED
        if(self.check_capture_mask_colour_range_format()==False):
            print("Error: one or more colour ranges were in wrong format")
            return
        
        
        #Return the current canvas as a NumPy array (H x W x 4, RGBA).
        # Grab the widget’s current visual state as a QImage
        qimage = self.capture_window.grab().toImage()

        # Ensure format is RGBA8888 for consistent bytes layout
        qimage = qimage.convertToFormat(QImage.Format_RGBA8888)

        width = qimage.width()
        height = qimage.height()
        
        # Get the raw pointer to the image data
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())

        
        mask = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))# Create a NumPy array (height, width, 4)
        mask = mask[:,:,:3]# a  NumPy array (height, width, 3); each value in the most inner arrays will contain 3 elements and 2 of them will be always 0
        
        
        color_functions = []
        color_functions_strings = []
        for form in self.form_window_capture_mask.forms:           
            
            form.rgb_elements.change_RGB_formula()
            color_functions.append(form.rgb_elements.rgb_function)
            color_functions_strings.append(form.rgb_elements.rgb_function_str)
        
        
        mask_ids_from = []
        mask_ids_to = []
        mask_filters = []
        print("values in the dict", self.form_window_capture_mask.forms[0].textBox_colorRange_list)
        for i in range(0, len(self.form_window_capture_mask.forms)):
            
            print("success index", i)
            
            red_channel_from = self.form_window_capture_mask.forms[i].textBox_colorRange_list["r0"].text()
            red_channel_from = -1 if(red_channel_from=='') else int(red_channel_from)
            red_channel_to = self.form_window_capture_mask.forms[i].textBox_colorRange_list["r1"].text()
            red_channel_to = -1 if(red_channel_to=='') else int(red_channel_to)

            if(red_channel_from==-1 or red_channel_to==-1):
                continue
            if(red_channel_from>red_channel_to):
                red_channel_from, red_channel_to = red_channel_to, red_channel_from
            mask_ids_from.append(red_channel_from)
            mask_ids_to.append(red_channel_to)
    


            green_channel_from = self.form_window_capture_mask.forms[i].textBox_colorRange_list["g0"].text()
            green_channel_from = -1 if(green_channel_from=='') else int(green_channel_from)
            green_channel_to = self.form_window_capture_mask.forms[i].textBox_colorRange_list["g1"].text()
            green_channel_to = -1 if(green_channel_to=='') else int(green_channel_to)
            
            if(green_channel_from==-1 or green_channel_to==-1):
                continue
            if(green_channel_from>green_channel_to):
                green_channel_from, green_channel_to = green_channel_to, green_channel_from
            mask_ids_from.append(green_channel_from)
            mask_ids_to.append(green_channel_to)



            blue_channel_from = self.form_window_capture_mask.forms[i].textBox_colorRange_list["b0"].text()
            blue_channel_from = -1 if(blue_channel_from=='') else int(blue_channel_from)
            blue_channel_to = self.form_window_capture_mask.forms[i].textBox_colorRange_list["b1"].text()
            blue_channel_to = -1 if(blue_channel_to=='') else int(blue_channel_to)

            if(blue_channel_from==-1 or blue_channel_to==-1):
                continue
            if(blue_channel_from>blue_channel_to):
                blue_channel_from, blue_channel_to = blue_channel_to, blue_channel_from
            mask_ids_from.append(blue_channel_from)
            mask_ids_to.append(blue_channel_to)

            print(f"mask_ids_from: {mask_ids_from}; mask_ids_to: {mask_ids_to}")
            mask_filter = np.all(((mask >= mask_ids_from).astype(np.uint8) + (mask <= mask_ids_to).astype(np.uint8))>1, axis=-1)
            mask_filters.append(mask_filter)

            mask_ids_from = []
            mask_ids_to = []
            print("filter shape", mask_filter.shape)
            
       
        if(len(mask_filters)==0):
            mask_filters = None
        
       
        color_functions, default_color_function, mask_filters = self.get_unique_colour_functions_and_masks(colour_functions = color_functions, colour_functions_strings = color_functions_strings, mask_filters=mask_filters, same_funcs_combine_masks=False)
        

        self.capture_window.apply_mask_settings(mask_filters, color_functions, default_color_function)



    def check_capture_mask_colour_range_format(self):

        is_format_correct = True

        for i in range(0, len(self.form_window_capture_mask.forms)):            
            is_format_correct = is_format_correct and Number_format_checker.check_for_positive_int_format(self.form_window_capture_mask.forms[i].textBox_colorRange_list["r0"].text())
            is_format_correct = is_format_correct and Number_format_checker.check_for_positive_int_format(self.form_window_capture_mask.forms[i].textBox_colorRange_list["r1"].text())
            is_format_correct = is_format_correct and Number_format_checker.check_for_positive_int_format(self.form_window_capture_mask.forms[i].textBox_colorRange_list["g0"].text())
            is_format_correct = is_format_correct and Number_format_checker.check_for_positive_int_format(self.form_window_capture_mask.forms[i].textBox_colorRange_list["g1"].text())
            is_format_correct = is_format_correct and Number_format_checker.check_for_positive_int_format(self.form_window_capture_mask.forms[i].textBox_colorRange_list["b0"].text())
            is_format_correct = is_format_correct and Number_format_checker.check_for_positive_int_format(self.form_window_capture_mask.forms[i].textBox_colorRange_list["b1"].text())

            if(is_format_correct==False):
                return False
        
        return True

# Functions for applying drawn/captured masks >







if __name__ == "__main__":
    MainApp().run()