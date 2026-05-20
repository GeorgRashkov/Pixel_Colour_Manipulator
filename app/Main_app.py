from PyQt5 import QtWidgets
from PyQt5_Window_functions import open_or_minimize_window, open_or_minimize_windows
import sys
import numpy as np
import Window_capture, Window_settings, Window_form_convolutionalMask, Z_Swap_pixel_values_controller
from Draw_mask_controller import Draw_mask_controller
from Capture_mask_controller import Capture_mask_controller
from Z_RGB_formulas_mask import RGB_formulas_mask

from DXCamera_Singleton import DXCamera_Singleton

class MainApp: 
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        rgb_formulas_mask = RGB_formulas_mask()

        self.draw_mask_controller = Draw_mask_controller(rgb_formulas_mask=rgb_formulas_mask)
        self.draw_mask_controller.form_window_draw_mask.button_apply_mask.clicked.connect(self.apply_rgb_mask_from_draw_window)
        self.draw_mask_controller.form_window_draw_mask.button_remove_mask.clicked.connect(self.remove_rgb_mask)

        self.capture_mask_controller = Capture_mask_controller(rgb_formulas_mask=rgb_formulas_mask)
        self.capture_mask_controller.form_window_capture_mask.button_apply_mask.clicked.connect(self.apply_rgb_mask_from_capture_window)
        self.capture_mask_controller.form_window_capture_mask.button_remove_mask.clicked.connect(self.remove_rgb_mask)


        self.swap_pixel_values_controller = Z_Swap_pixel_values_controller.Swap_pixel_values_controller()       
        self.swap_pixel_values_controller.form_window_pixel_areas.button_apply_swap_areas.clicked.connect(self.apply_swap_pixel_areas)
        self.swap_pixel_values_controller.form_window_pixel_areas.button_remove_swap_areas.clicked.connect(self.remove_swap_pixel_areas)        
        

        #capture window
       
        self.camera = DXCamera_Singleton()
        self.capture_window = Window_capture.CaptureWindow()

        self.capture_window.button_open_settings.clicked.connect(self.open_window_settings)
        self.capture_window.button_open_drawMask.clicked.connect(self.open_windows_draw_mask)
        self.capture_window.button_open_captureMask.clicked.connect(self.open_window_capture_mask)
       
        self.capture_window.button_open_convolutionalFilter.clicked.connect(self.open_window_covolutional_filter)
        self.capture_window.button_open_swopAreas.clicked.connect(self.open_windows_swop_pixel_areas)
        
        #settings window
        self.settings_window = Window_settings.FormWindow_Settings()
        self.settings_window.button_apply_changes.clicked.connect(self.apply_settings)

        #convolutional filter window
        self.convolutional_filter_window = Window_form_convolutionalMask.FormWindow_ConvolutionalFilter()
        self.convolutional_filter_window.button_apply_filters.clicked.connect(self.apply_convolutional_filters)
        self.convolutional_filter_window.button_remove_filters.clicked.connect(self.remove_convolutional_filters)
        
        
    
        self.capture_window.show()
        sys.exit(self.app.exec_())
    
    def run(self):
        sys.exit(self.app.exec_())

    

    def apply_swap_pixel_areas(self):
        pixel_areas_manipulator = self.swap_pixel_values_controller.get_pixel_areas_manipulator()
        self.capture_window.set_pixel_areas_manipulator(pixel_areas_manipulator=pixel_areas_manipulator)

    def remove_swap_pixel_areas(self):
        self.capture_window.remove_pixel_areas_manipulator()
    
    
    def apply_rgb_mask_from_draw_window(self):
        rgb_formula_mask = self.draw_mask_controller.get_colour_mask()
        self.capture_window.set_rgb_mask(rgb_mask=rgb_formula_mask)

    def apply_rgb_mask_from_capture_window(self):
        img_mask = self.get_rgb_pixel_values_from_capture_window()
        rgb_formula_mask = self.capture_mask_controller.get_colour_mask(img_mask=img_mask)
        self.capture_window.set_rgb_mask(rgb_mask=rgb_formula_mask)
    
    def remove_rgb_mask(self):
        self.capture_window.remove_rgb_mask()


    
    def apply_convolutional_filters(self):
        
        rgb_kernels_values, rgb_kernels_strides, rgb_kernels_holes_count = self.convolutional_filter_window.get_filters_values()       
        
        print("rgb_kernels_values", rgb_kernels_values)
        print("rgb_kernels_strides", rgb_kernels_strides)
        print("rgb_kernels_holes_count", rgb_kernels_holes_count)

        if(rgb_kernels_values != None and rgb_kernels_strides != None and rgb_kernels_holes_count != None):
            self.capture_window.create_rgb_kernels(rgb_kernels_values = rgb_kernels_values, rgb_kernels_strides = rgb_kernels_strides, rgb_kernels_holes_count = rgb_kernels_holes_count)
        
    def remove_convolutional_filters(self):

        self.capture_window.remove_rgb_kernels()
    


    def open_window_settings(self):
        open_or_minimize_window(self.settings_window)


    
    def open_windows_draw_mask(self):
        windows = [self.draw_mask_controller.form_window_draw_mask, self.draw_mask_controller.canvas_window]
        open_or_minimize_windows(windows=windows)

    def open_window_capture_mask(self):
        open_or_minimize_window(self.capture_mask_controller.form_window_capture_mask)

    
    def open_window_covolutional_filter(self):
        open_or_minimize_window(self.convolutional_filter_window)
    
    def open_windows_swop_pixel_areas(self):
        windows = [self.swap_pixel_values_controller.form_window_pixel_areas, self.swap_pixel_values_controller.canvas_window]
        open_or_minimize_windows(windows=windows)
       
        

    def apply_settings(self):
        capture_time, slider_min_value, slider_max_value, RGB_use_doubles, color_functions_execution_order = self.settings_window.apply_settings()
        if(capture_time != None):#if any of the upper variables is "None" than all of them will always be "None"
            self.capture_window.apply_settings(capture_time=capture_time, slider_min_value=slider_min_value, slider_max_value=slider_max_value, RGB_use_doubles=RGB_use_doubles, color_functions_execution_order = color_functions_execution_order)

    
    #The returned numpy array has shape (Height, Width, 3[RGB])
    def get_rgb_pixel_values_from_capture_window(self) -> np.ndarray[np.uint8]:
        
        rgb_values_from_capture_window = self.capture_window.get_transformed_img()
        return rgb_values_from_capture_window
    







if __name__ == "__main__":
    MainApp().run()