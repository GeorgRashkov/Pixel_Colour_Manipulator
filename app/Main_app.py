from PyQt5 import QtWidgets
import sys
import numpy as np

from PyQt5_Window_functions import open_or_minimize_window, open_or_minimize_windows

"""
import Window_capture, Window_settings, Z_Swap_pixel_values_controller
"""
from Window_capture import CaptureWindow
from Window_settings import FormWindow_Settings
from Z_Swap_pixel_values_controller import Swap_pixel_values_controller
from Window_dynamic_variables import Window_dynamic_variables
from Draw_mask_controller import Draw_mask_controller
from Capture_mask_controller import Capture_mask_controller
from Z_RGB_formulas_mask import RGB_formulas_mask

from Images_controller import Images_controller
from Images_manipulator import Images_manipulator

from Draw_formula_controller import Draw_formula_controller

from Convolutional_kernels_manipulator import Convolutional_kernels_manipulator
from Convolutional_kernels_controller import Convolutional_kernels_controller

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


        """
        self.swap_pixel_values_controller = Z_Swap_pixel_values_controller.Swap_pixel_values_controller()       
        self.swap_pixel_values_controller.form_window_pixel_areas.button_apply_elements_to_pixel_areas_manipulator.clicked.connect(self.apply_elements_to_pixel_areas_manipulator)
        self.swap_pixel_values_controller.form_window_pixel_areas.button_remove_elements_from_pixel_areas_manipulator.clicked.connect(self.remove_elements_from_pixel_areas_manipulator)
        
        self.swap_pixel_values_controller.pixel_areas_masks_controller.form_window_draw_mask.button_update_images.clicked.connect(self.update_images_for_masks_for_pixel_areas_manipulator)
        self.swap_pixel_values_controller.pixel_areas_masks_controller.form_window_draw_mask.button_apply_all_masks.clicked.connect(self.apply_all_masks_to_pixel_areas_manipulator)
        self.swap_pixel_values_controller.pixel_areas_masks_controller.form_window_draw_mask.button_apply_selected_masks.clicked.connect(self.apply_selected_masks_to_pixel_areas_manipulator)
        self.swap_pixel_values_controller.pixel_areas_masks_controller.form_window_draw_mask.button_remove_all_masks.clicked.connect(self.remove_all_masks_from_pixel_areas_manipulator)
        self.swap_pixel_values_controller.pixel_areas_masks_controller.form_window_draw_mask.button_remove_selected_masks.clicked.connect(self.remove_selected_masks_from_pixel_areas_manipulator)
        """
        

        self.draw_formula_controller = Draw_formula_controller()
        self.draw_formula_controller.form_window_draw_formula.button_show_drawing.clicked.connect(self.show_draw_formula_drawing)

        #capture window 
        self.camera = DXCamera_Singleton()
        """
        self.capture_window = Window_capture.CaptureWindow()
        """
        self.capture_window = CaptureWindow()

        self.capture_window.button_open_settings.clicked.connect(self.open_window_settings)
        self.capture_window.button_open_drawMask.clicked.connect(self.open_windows_draw_mask)
        self.capture_window.button_open_captureMask.clicked.connect(self.open_window_capture_mask)
        
        self.capture_window.button_open_convolutionalFilter.clicked.connect(self.open_window_convolutional_kernels)
        self.capture_window.button_open_swapAreas.clicked.connect(self.open_windows_swop_pixel_areas)
        self.capture_window.button_open_drawFormula.clicked.connect(self.open_window_draw_formula)
        self.capture_window.button_open_dynamic_variables.clicked.connect(self.open_window_dynamic_variables)
        self.capture_window.button_open_images.clicked.connect(self.open_window_images)
        
        #settings window
        """
        self.settings_window = Window_settings.FormWindow_Settings()
        """
        self.settings_window = FormWindow_Settings()
        self.settings_window.button_apply_changes.clicked.connect(self.apply_settings)

        #convolutional kernel window
        self.convolutional_kernels_controller = Convolutional_kernels_controller()
        self.convolutional_kernels_controller.window_form_convolutional_kernels.button_apply_cks.clicked.connect(self.apply_convolutional_kernels)
        self.convolutional_kernels_controller.window_form_convolutional_kernels.button_remove_cks.clicked.connect(self.remove_convolutional_kernels)

        #dynamic variables window
        self.window_dynamic_variables = Window_dynamic_variables()
        self.window_dynamic_variables.button_apply_dynamic_variables.clicked.connect(self.apply_dynamic_variables)
        self.window_dynamic_variables.button_remove_dynamic_variables.clicked.connect(self.remove_dynamic_variables)

        #images window
        """
        self.images_manipulator = Images_manipulator()
        self.images_controller = Images_controller(get_original_img=self.capture_window.get_original_img, get_transformed_img=self.capture_window.get_transformed_img)
        self.images_controller.window_form_images.button_apply_images_manipulator.clicked.connect(self.apply_images)
        """
        self.func_get_image_under_capture_window = self.capture_window.get_original_img
        self.func_get_transformed_image_from_capture_window = self.capture_window.get_transformed_img
        self.images_manipulator = Images_manipulator(func_get_image_under_capture_window=self.func_get_image_under_capture_window, func_get_transformed_image_from_capture_window=self.func_get_transformed_image_from_capture_window)
        self.images_controller = Images_controller(images_manipulator=self.images_manipulator)
        self.images_controller.window_form_images.button_apply_images_manipulator.clicked.connect(self.apply_images)

        #pixel areas
        self.swap_pixel_values_controller = Swap_pixel_values_controller(images_manipulator=self.images_manipulator)
        self.swap_pixel_values_controller.form_window_pixel_areas.button_apply_elements_to_pixel_areas_manipulator.clicked.connect(self.apply_elements_to_pixel_areas_manipulator)
        self.swap_pixel_values_controller.form_window_pixel_areas.button_remove_elements_from_pixel_areas_manipulator.clicked.connect(self.remove_elements_from_pixel_areas_manipulator)

    
        self.capture_window.show()
        sys.exit(self.app.exec_())
    
    def run(self):
        sys.exit(self.app.exec_())
        
        

    """
    def apply_elements_to_pixel_areas_manipulator(self):

        if(self.swap_pixel_values_controller.form_window_pixel_areas.check_box_masks.isChecked() == True and 
           self.swap_pixel_values_controller.pixel_areas_masks_controller.form_window_draw_mask.checkBox_auto_update_images_when_applying_masks.isChecked() == True):
            self.update_images_for_masks_for_pixel_areas_manipulator()

        self.swap_pixel_values_controller.apply_elements_to_pixel_areas_manipulator(images_manipulator=self.images_manipulator)
        pixel_areas_manipulator = self.swap_pixel_values_controller.get_pixel_areas_manipulator()
        self.capture_window.set_pixel_areas_manipulator(pixel_areas_manipulator=pixel_areas_manipulator)
    """
    
    def apply_elements_to_pixel_areas_manipulator(self):

        self.swap_pixel_values_controller.apply_elements_to_pixel_areas_manipulator()
        pixel_areas_manipulator = self.swap_pixel_values_controller.get_pixel_areas_manipulator()
        self.capture_window.set_pixel_areas_manipulator(pixel_areas_manipulator=pixel_areas_manipulator)


    def remove_elements_from_pixel_areas_manipulator(self):
        
        self.swap_pixel_values_controller.remove_elements_from_pixel_areas_manipulator()
        pixel_areas_manipulator = self.swap_pixel_values_controller.get_pixel_areas_manipulator()
        self.capture_window.set_pixel_areas_manipulator(pixel_areas_manipulator=pixel_areas_manipulator)
    

    """
    def update_images_for_masks_for_pixel_areas_manipulator(self):
        img_for_colour_range_masks = self.get_rgb_pixel_values_from_capture_window()
        self.swap_pixel_values_controller.pixel_areas_masks_controller.update_images_for_masks(img_for_colour_range_masks=img_for_colour_range_masks)

    def apply_selected_masks_to_pixel_areas_manipulator(self):
        img_for_colour_range_masks = self.get_rgb_pixel_values_from_capture_window()
        self.swap_pixel_values_controller.apply_selected_masks(img_for_colour_range_masks=img_for_colour_range_masks)

    def apply_all_masks_to_pixel_areas_manipulator(self):
        img_for_colour_range_masks = self.get_rgb_pixel_values_from_capture_window()
        self.swap_pixel_values_controller.apply_all_masks(img_for_colour_range_masks=img_for_colour_range_masks)

    def remove_selected_masks_from_pixel_areas_manipulator(self):
        self.swap_pixel_values_controller.remove_selected_masks()

    def remove_all_masks_from_pixel_areas_manipulator(self):
        self.swap_pixel_values_controller.remove_all_masks()
    """



    
    def apply_rgb_mask_from_draw_window(self):
        rgb_formula_mask = self.draw_mask_controller.get_colour_mask()
        self.capture_window.set_rgb_mask(rgb_mask=rgb_formula_mask)

    def apply_rgb_mask_from_capture_window(self):
        img_mask = self.get_rgb_pixel_values_from_capture_window()
        rgb_formula_mask = self.capture_mask_controller.get_colour_mask(img_mask=img_mask)
        self.capture_window.set_rgb_mask(rgb_mask=rgb_formula_mask)
    
    def remove_rgb_mask(self):
        self.capture_window.remove_rgb_mask()


    
    def apply_convolutional_kernels(self):
        cks_manipulator: Convolutional_kernels_manipulator = self.convolutional_kernels_controller.get_convolutional_kernels_manipulator()
        self.capture_window.set_convolutional_kernels(cks_manipulator=cks_manipulator)

    def remove_convolutional_kernels(self):
        self.convolutional_kernels_controller.remove_convolutional_kernels()
        self.capture_window.remove_convolutional_kernels()

    def apply_dynamic_variables(self):
        dynamic_variables = self.window_dynamic_variables.get_dynamic_variables()
        if(dynamic_variables is not None):
            self.capture_window.set_dynamic_variables(dynamic_variables=dynamic_variables)

    def remove_dynamic_variables(self):
        self.capture_window.set_dynamic_variables(dynamic_variables=[])

    def apply_images(self):
        """
        images_manipulator = self.images_controller.get_images_manipulator()
        """
        images_manipulator = self.images_controller.get_images_manipulator(func_get_image_under_capture_window=self.func_get_image_under_capture_window, func_get_transformed_image_from_capture_window=self.func_get_transformed_image_from_capture_window)
        if(images_manipulator is not None):
            self.images_manipulator = images_manipulator


    def show_draw_formula_drawing(self):
        
        img = self.get_rgb_pixel_values_from_capture_window()
        self.draw_formula_controller.show_drawing(img=img)


    def open_window_settings(self):
        open_or_minimize_window(self.settings_window)


    
    def open_windows_draw_mask(self):
        windows = [self.draw_mask_controller.form_window_draw_mask, self.draw_mask_controller.canvas_window]
        open_or_minimize_windows(windows=windows)

    def open_window_capture_mask(self):
        open_or_minimize_window(self.capture_mask_controller.form_window_capture_mask)

    
    def open_window_convolutional_kernels(self):
        self.convolutional_kernels_controller.open_window_form_convolutional_kernels()
    
    def open_windows_swop_pixel_areas(self):
        windows = [self.swap_pixel_values_controller.form_window_pixel_areas, self.swap_pixel_values_controller.canvas_window]
        open_or_minimize_windows(windows=windows)
    
    def open_window_draw_formula(self):
        open_or_minimize_window(window=self.draw_formula_controller.form_window_draw_formula)
       
    def open_window_dynamic_variables(self):
        open_or_minimize_window(self.window_dynamic_variables)

    def open_window_images(self):
        self.images_controller.open_window_images()


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