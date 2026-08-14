import numpy as np

from Window_Form_rgb_formulas_and_masks import Window_Form_rgb_formulas_and_masks

from RGB_formula_initializer import RGB_formula_initializer
from Enums import Functions_for__Enum__rgb_formulas_parameters, Enum__brackets
from Z_Pixel_areas_masks_controller import Pixel_areas_masks_controller

from Images_manipulator import Images_manipulator
from RGB_formulas_and_masks_manipulator import RGB_formulas_and_masks_manipulator

from Number_format_checker import check_for_positive_int_format
from Number_operatios import get_smallest_unique_positive_integer
from Bracket_expressions_getter import get_subjects_represented_as__parameters_and_values_from_bracket_expressions

from PyQt5_Window_functions import open_or_minimize_window

class RGB_formulas_and_masks_controller():

    def __init__(self, images_manipulator:Images_manipulator):

        self.form_window_rgb_formulas_and_masks = Window_Form_rgb_formulas_and_masks()
        self.form_window_rgb_formulas_and_masks.button_open_masks_window.clicked.connect(self.open_window_masks)
        self.form_window_rgb_formulas_and_masks.button_add_rgb_formula.clicked.connect(self.add_rgb_function)
        """
        self.form_window_rgb_formulas_and_masks.button_apply_elements_to__rgb_formulas_and_masks_manipulator.clicked.connect(self.apply_elements_to__rgb_formulas_and_masks_manipulator)
        self.form_window_rgb_formulas_and_masks.button_remove_elements_from__rgb_formulas_and_masks_manipulator.clicked.connect(self.apply_elements_to__rgb_formulas_and_masks_manipulator)
        """

        self.masks_controller = Pixel_areas_masks_controller()
        self.masks_controller.form_window_draw_mask.button_apply_all_masks.clicked.connect(lambda _: self.apply_masks(all_masks=True))
        self.masks_controller.form_window_draw_mask.button_apply_selected_masks.clicked.connect(lambda _: self.apply_masks(all_masks=False))
        self.masks_controller.form_window_draw_mask.button_remove_all_masks.clicked.connect(self.remove_all_masks)
        self.masks_controller.form_window_draw_mask.button_remove_selected_masks.clicked.connect(self.remove_selected_masks)

        self.rgb_formulas_and_masks_manipulator = RGB_formulas_and_masks_manipulator()
        self.images_manipulator = images_manipulator

    def open_window_rgb_formulas_and_masks(self):
        open_or_minimize_window(self.form_window_rgb_formulas_and_masks)

    def open_window_masks(self):
        open_or_minimize_window(self.masks_controller.form_window_draw_mask)
    
    #<functions for getting user input

    def get_text_area__rgb_formulas__formatted_text(self):
        rgb_formulas_str = self.form_window_rgb_formulas_and_masks.text_area_rgb_formulas.toPlainText()
        rgb_formulas_str = rgb_formulas_str.replace(" ", "").replace("\n", "")
        return rgb_formulas_str

    def get_text_area__masks_ids_and_rgb_formulas_ids__formatted_text(self):
        mask_ids_with_f_ids_str = self.form_window_rgb_formulas_and_masks.text_area_mask_ids_with_f_ids.toPlainText()
        mask_ids_with_f_ids_str = mask_ids_with_f_ids_str.replace(" ", "").replace("\n", "")
        return mask_ids_with_f_ids_str

    #functions for getting user input>



    def add_rgb_function(self):       
        
        rgb_function_from_text_area = self.get_text_area__rgb_formulas__formatted_text()
        rgb_function_id = get_smallest_unique_positive_integer(text=rgb_function_from_text_area, opening_separator="id->[", closing_separator="]")
        if(rgb_function_id is None):
            print("error: the maximum number of RGB formulas was reached")
            return
        
        is_formula_changed = self.form_window_rgb_formulas_and_masks.rgb_elements.change_RGB_formula()
        
        if(is_formula_changed == True):
            p_v_s = Functions_for__Enum__rgb_formulas_parameters().get_rgb_formulas_parameter_value_separator()
            ps_s = Functions_for__Enum__rgb_formulas_parameters().get_rgb_formulas_parameters_separator()

            rgb_formulas_str = f"id{p_v_s}[{rgb_function_id}]{ps_s} r{p_v_s}[ {self.form_window_rgb_formulas_and_masks.rgb_elements.text_boxes["r"].text()} ]{ps_s} g{p_v_s}[ {self.form_window_rgb_formulas_and_masks.rgb_elements.text_boxes["g"].text()} ]{ps_s} b{p_v_s}[ {self.form_window_rgb_formulas_and_masks.rgb_elements.text_boxes["b"].text()} ]"
            rgb_formulas_str = "{ " + rgb_formulas_str + " }\n"
            self.form_window_rgb_formulas_and_masks.text_area_rgb_formulas.append(rgb_formulas_str)



    #<functions for applying elements to the manipulator of rgb formulas and masks

    def apply_elements_to__rgb_formulas_and_masks_manipulator(self):

        if(self.form_window_rgb_formulas_and_masks.check_box_rgb_formulas.isChecked() == True):
            self.apply_rgb_formulas_to_manipulator()

        if(self.form_window_rgb_formulas_and_masks.check_box__masks_ids_and_rgb_formulas_ids.isChecked() == True):
            self.apply_masks_ids_and_rgb_formulas_ids_to_manipulator()

        if(self.form_window_rgb_formulas_and_masks.check_box_masks.isChecked() == True):
            self.apply_masks(all_masks=True)


    def apply_rgb_formulas_to_manipulator(self):

        rgb_formulas_str = self.get_text_area__rgb_formulas__formatted_text()
        rgb_formula_initializer = RGB_formula_initializer()
        rgb_formulas_dict = rgb_formula_initializer.create_many_rgb_formulas(rgb_formulas=rgb_formulas_str, use_pixel_areas=False)

        if(rgb_formulas_dict is None):
            rgb_formulas_dict = {}
        self.rgb_formulas_and_masks_manipulator.apply_rgb_formulas(rgb_formulas=rgb_formulas_dict)


    def apply_masks_ids_and_rgb_formulas_ids_to_manipulator(self):
        
        masks_ids_with_f_ids_str = self.get_text_area__masks_ids_and_rgb_formulas_ids__formatted_text()
        parameters=("mask_id", "f_ids")
        masks_ids_with_f_ids_as_strings = get_subjects_represented_as__parameters_and_values_from_bracket_expressions(txt=masks_ids_with_f_ids_str, subject_name="mask id with formula ids", outer_bracket_type=Enum__brackets.curly, inner_bracket_type=Enum__brackets.square, 
                                                                                    valid_parameters=parameters, required_parameters=parameters, parameter_value_separator=":", parameters_separator=";", parameter_for_error_messages="mask_id")
        if(masks_ids_with_f_ids_as_strings is None):
            return

        masks_ids_and_rgb_formulas_ids: dict[int, list[int]] = {}
        for mask_id_with_f_ids_as_strings in masks_ids_with_f_ids_as_strings:

            mask_id_str = mask_id_with_f_ids_as_strings["mask_id"]
            is_mask_id_valid = check_for_positive_int_format(txt_value=mask_id_str, is_zero_allowed=False)
            if(is_mask_id_valid == False):
                print("error: the mask id must be a positive integer above zero")
                return

            f_ids:list[int] = []
            f_ids_str = mask_id_with_f_ids_as_strings["f_ids"]
            f_ids_as_strings = f_ids_str.split(",")
            for f_id_str in f_ids_as_strings:

                is_f_id_valid = check_for_positive_int_format(txt_value=f_id_str, is_zero_allowed=False)
                if(is_f_id_valid == False):
                    print("error: the rgb formulas ids must be a positive integers")
                    print(f"the previous error ocurred on mask id {mask_id_str}")
                    return
                
                f_ids.append(int(f_id_str))

            mask_id = int(mask_id_str)
            masks_ids_and_rgb_formulas_ids[mask_id] = f_ids

        self.rgb_formulas_and_masks_manipulator.apply_masks_ids_and_rgb_formulas_ids(masks_ids_and_rgb_formulas_ids=masks_ids_and_rgb_formulas_ids)
                            

    def apply_masks(self, all_masks:bool):
        
        images_for_masks:list[np.ndarray[np.uint8]] = self.images_manipulator.get_images_in_range(index1=0, index2=-1)

        if(self.masks_controller.form_window_draw_mask.checkBox_update_last_image_when_applying_masks.isChecked() == True):
            additional_image = None
            if(self.masks_controller.form_window_draw_mask.radioButton_take_image_under_capture_window.isChecked() == True):
                additional_image = self.images_manipulator.get_image_under_capture_window() 
            else:
                additional_image = self.images_manipulator.get_transformed_image_from_capture_window()
            images_for_masks.append(additional_image)
        
        masks = self.masks_controller.apply_masks(rectangles_with_ids=None, images_for_masks=images_for_masks, all_masks=all_masks)

        if(masks is not None):
            self.rgb_formulas_and_masks_manipulator.apply_masks(masks=masks)

    #functions for applying elements to the manipulator of rgb formulas and masks>


    #<functions for removing elements from the manipulator of rgb formulas and masks

    def remove_elements_from__rgb_formulas_and_masks_manipulator(self):
        
        if(self.form_window_rgb_formulas_and_masks.check_box_rgb_formulas.isChecked() == True):
            self.remove_rgb_formulas_from_manipulator()

        if(self.form_window_rgb_formulas_and_masks.check_box__masks_ids_and_rgb_formulas_ids.isChecked() == True):
            self.remove_masks_ids_and_rgb_formulas_ids_from_manipulator()

        if(self.form_window_rgb_formulas_and_masks.check_box_masks.isChecked() == True):
            self.remove_all_masks()


    def remove_rgb_formulas_from_manipulator(self):
        self.rgb_formulas_and_masks_manipulator.apply_rgb_formulas(rgb_formulas={})


    def remove_masks_ids_and_rgb_formulas_ids_from_manipulator(self):
        self.rgb_formulas_and_masks_manipulator.apply_masks_ids_and_rgb_formulas_ids(masks_ids_and_rgb_formulas_ids={})


    def remove_selected_masks(self):
        
        remaining_masks = self.masks_controller.remove_applied_masks(all_masks=False)
        if(remaining_masks is not None):
            self.rgb_formulas_and_masks_manipulator.apply_masks(masks=remaining_masks)


    def remove_all_masks(self):
        empty_dict = self.masks_controller.remove_applied_masks(all_masks=True)
        self.rgb_formulas_and_masks_manipulator.apply_masks(masks={})

    #functions for removing elements from the manipulator of rgb formulas and masks>


    def get__rgb_formulas_and_masks_manipulator(self) -> RGB_formulas_and_masks_manipulator:
        return self.rgb_formulas_and_masks_manipulator

    
