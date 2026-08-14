import numpy as np
from typing import Callable
from PyQt5.QtGui import QColor


from PyQt5_Window_functions import open_or_minimize_window

from Window_form_images import Window_form_images
from Window_show_image import Window_show_image
from Window_Canvas_draw_mask import Window_Canvas_draw_mask

from Draw_formula_controller import Draw_formula_controller
from Images_manipulator import Images_manipulator

from Number_format_checker import check_for_int_format, check_for_positive_int_format
from Window_functions import get_rgb_pixel_values_from_window

class Images_controller:

    def __init__(self, images_manipulator:Images_manipulator):

        self.draw_formula_controller = Draw_formula_controller()
        self.draw_formula_controller.form_window_draw_formula.button_show_drawing.clicked.connect(self.open_window_show_draw_formula_drawing)

        self.window_form_images = Window_form_images()
        self.window_show_image = Window_show_image()
        self.window_canvas = Window_Canvas_draw_mask()

        self.window_form_images.form_elements__order_images.button_order_nums.clicked.connect(self.order_images)

        self.window_form_images.button_add_image.clicked.connect(self.add_image)
        self.window_form_images.button_remove_images.clicked.connect(self.remove_images)
        self.window_form_images.button_show_image.clicked.connect(self.show_image)
        self.window_form_images.button_resize_images.clicked.connect(self.resize_images)
        self.window_form_images.button_open_canvas_window.clicked.connect(self.open_window_canvas)
        self.window_form_images.button_open_image_window.clicked.connect(self.open_window_show_image)
        self.window_form_images.button_open_draw_formula_window.clicked.connect(self.open_window_draw_formula)

        self.window_form_images.draw_elements.slider_red.valueChanged.connect(lambda: self.slider_value_changed(self.window_form_images.draw_elements.slider_red.value(), 'r'))
        self.window_form_images.draw_elements.slider_green.valueChanged.connect(lambda: self.slider_value_changed(self.window_form_images.draw_elements.slider_green.value(), 'g'))
        self.window_form_images.draw_elements.slider_blue.valueChanged.connect(lambda: self.slider_value_changed(self.window_form_images.draw_elements.slider_blue.value(), 'b'))

        self.window_form_images.draw_elements.button_clear_canvas.clicked.connect(self.window_canvas.clear)
        self.window_form_images.draw_elements.button_apply_brush_size_changes.clicked.connect(self.change_brush_size_parameters)

        self.images_manipulator = images_manipulator

        self.images_count_front_text = "image count: "
        self.update_image_count_label()

    def open_window_images(self):
        open_or_minimize_window(window=self.window_form_images)

    def open_window_canvas(self):
        open_or_minimize_window(window=self.window_canvas)

    def open_window_show_image(self):
        open_or_minimize_window(window=self.window_show_image)

    def open_window_draw_formula(self):
        open_or_minimize_window(window=self.draw_formula_controller.form_window_draw_formula)

    def open_window_show_draw_formula_drawing(self):
        img = self.get_image()
        self.draw_formula_controller.show_drawing(img=img)


#<drawing functions
    def change_brush_size_parameters(self):

        #take the brush size parameters
        brush_size_min_value = self.window_form_images.draw_elements.textBox_brush_size_min_value.text()
        brush_size_max_value = self.window_form_images.draw_elements.textBox_brush_size_max_value.text()
        brush_size_delta = self.window_form_images.draw_elements.textBox_brush_size_delta.text()

        #check the the format of the brush size parameters
        if(check_for_positive_int_format(brush_size_min_value, is_zero_allowed=False) == False or brush_size_min_value == ""):
            print("Error: the brush min size field was either in wrong format or it was equal to 0")
            return        
        if(check_for_positive_int_format(brush_size_max_value, is_zero_allowed=False) == False or brush_size_min_value == ""):
            print("Error: the brush max size field was either in wrong format or it was equal to 0")
            return        
        if(check_for_positive_int_format(brush_size_delta, is_zero_allowed=False) == False or brush_size_min_value == ""):
            print("Error: the brush size icrement field was either in wrong format or it was equal to 0")
            return
        
        brush_min_size = int(brush_size_min_value)
        brush_max_size = int(brush_size_max_value)
        brush_delta = int(brush_size_delta)

        if(brush_min_size>brush_max_size):
            print("Error: brush min size value cannot be higher than brush max size value")
            return

        self.window_canvas.set_brush_size_arguments(brush_min_size = brush_min_size, brush_max_size=brush_max_size, brush_delta=brush_delta)
    
    def slider_value_changed(self, slider_value, slider_id):

        if(slider_id == "r"):
            self.window_form_images.draw_elements.colour.r = slider_value*self.window_form_images.draw_elements.slider_step
        if(slider_id == "g"):
            self.window_form_images.draw_elements.colour.g = slider_value*self.window_form_images.draw_elements.slider_step
        if(slider_id == "b"):
            self.window_form_images.draw_elements.colour.b = slider_value*self.window_form_images.draw_elements.slider_step
        
        self.window_form_images.draw_elements.set_colour_of_drawing_button()

        colour = QColor(self.window_form_images.draw_elements.colour.r, self.window_form_images.draw_elements.colour.g, self.window_form_images.draw_elements.colour.b)
        self.window_canvas.set_colour(colour)
    
#drawing functions>


    def get_image(self) -> np.ndarray[np.uint8]:

        image = None

        if(self.window_form_images.radioButton_add_window_capture_input.isChecked() == True):
            image = self.images_manipulator.get_image_under_capture_window()
        elif(self.window_form_images.radioButton_add_window_capture_output.isChecked() == True):
            image = self.images_manipulator.get_transformed_image_from_capture_window()
        elif(self.window_form_images.radioButton_add_draw_window_output.isChecked() == True):
            image = self.get_image_from_canvas()
        else:
            raise Exception("the image cannot be added when none of the image buttons is selected")

        return image


#<functions for altering the collection of images in the image manipulator

    def add_image(self):

        """
        image = None

        if(self.window_form_images.radioButton_add_window_capture_input.isChecked() == True):
            image = self.images_manipulator.get_image_under_capture_window()
        elif(self.window_form_images.radioButton_add_window_capture_output.isChecked() == True):
            image = self.images_manipulator.get_transformed_image_from_capture_window()
        elif(self.window_form_images.radioButton_add_draw_window_output.isChecked() == True):
            image = self.get_image_from_canvas()
        else:
            raise Exception("the image cannot be added when none of the image buttons is selected")
        """
        image = self.get_image()

        if(self.window_form_images.checkBox_remove_last_image_before_creating_new_image.isChecked() == True):
            self.images_manipulator.remove_image(index=-1)
        
        self.images_manipulator.add_image(img=image)
        self.update_image_count_label()
        self.window_show_image.show_image(img=image)

    def remove_images(self):

        images_index1_txt = self.window_form_images.textBox_remove_images_index1.text().replace(" ", "").replace("\n", "")
        images_index2_txt = self.window_form_images.textBox_remove_images_index2.text().replace(" ", "").replace("\n", "")

        are_image_indexes_correct = check_for_int_format(txt_value=images_index1_txt) and check_for_int_format(txt_value=images_index2_txt)

        if(are_image_indexes_correct == False):
            print("error: the range indexes must be integers")
            return

        if(images_index1_txt != "" and images_index2_txt != ""):
            self.images_manipulator.remove_images_in_range(index1=int(images_index1_txt), index2=int(images_index2_txt))
        elif(images_index1_txt != "" and images_index2_txt == ""):
            self.images_manipulator.remove_image(index=int(images_index1_txt))
        elif(images_index1_txt == "" and images_index2_txt != ""):
            self.images_manipulator.remove_image(index=int(images_index2_txt))

        self.update_image_count_label()


    def resize_images(self):

        images_index1_txt = self.window_form_images.textBox_resize_images_index1.text().replace(" ", "").replace("\n", "")
        images_index2_txt = self.window_form_images.textBox_resize_images_index2.text().replace(" ", "").replace("\n", "")
        are_image_indexes_correct = check_for_int_format(txt_value=images_index1_txt) and check_for_int_format(txt_value=images_index2_txt)

        if(are_image_indexes_correct == False):
            print("error: the range indexes must be integers")
            return

        images_new_height_txt = self.window_form_images.textBox_resize_images_height.text().replace(" ", "").replace("\n", "")
        images_new_width_txt = self.window_form_images.textBox_resize_images_width.text().replace(" ", "").replace("\n", "")
        are_image_width_and_height_correct = check_for_positive_int_format(txt_value=images_new_height_txt, is_zero_allowed=False) and check_for_positive_int_format(txt_value=images_new_width_txt, is_zero_allowed=False)

        if(are_image_width_and_height_correct == False):
            print("error: the width and height must be positive integers above 0")
            return

        
        images_height = 100
        if(images_new_height_txt  != ""):
            images_height = int(images_new_height_txt)

        images_width = 100
        if(images_new_width_txt != ""):
            images_width = int(images_new_width_txt)

        if(images_index1_txt != "" and images_index2_txt != ""):
            self.images_manipulator.resize_images_in_range(new_height=images_height, new_width=images_width, index1=int(images_index1_txt), index2=int(images_index2_txt))
        elif(images_index1_txt != "" and images_index2_txt == ""):
            self.images_manipulator.resize_image(images_new_percentage_height=images_height, images_new_percentage_width=images_width,  index=int(images_index1_txt))
        elif(images_index1_txt == "" and images_index2_txt != ""):
            self.images_manipulator.resize_image(images_new_percentage_height=images_height, images_new_percentage_width=images_width,  index=int(images_index2_txt))        

    def order_images(self):

        order_obj = self.window_form_images.form_elements__order_images.get__order_obj()
        if(order_obj is not None):
            self.images_manipulator.order_images(order_obj=order_obj)

#functions for altering the collection of images in the image manipulator>

    
    
    def get_image_from_canvas(self) -> np.ndarray[np.uint8]:
        img_from_canvas = get_rgb_pixel_values_from_window(window=self.window_canvas)
        return img_from_canvas

    def get_images_manipulator(self, func_get_image_under_capture_window:Callable[[],np.ndarray[np.uint8]], func_get_transformed_image_from_capture_window: Callable[[],np.ndarray[np.uint8]]) -> Images_manipulator | None:
        
        images_index1_txt = self.window_form_images.textBox_apply_images_index1.text().replace(" ", "").replace("\n", "")
        images_index2_txt = self.window_form_images.textBox_apply_images_index2.text().replace(" ", "").replace("\n", "")
        are_image_indexes_correct = check_for_int_format(txt_value=images_index1_txt) and check_for_int_format(txt_value=images_index2_txt)

        if(are_image_indexes_correct == False):
            print("error: the range indexes must be integers")
            return None

        if(images_index1_txt == "" or images_index2_txt == ""):
            print("in order to apply images you must fill the two range text boxes")
            return None

        images_manipulator = Images_manipulator(func_get_image_under_capture_window=func_get_image_under_capture_window, func_get_transformed_image_from_capture_window=func_get_transformed_image_from_capture_window)
        images = self.images_manipulator.get_images_in_range(index1=int(images_index1_txt), index2=int(images_index2_txt))
        for image in images:
            images_manipulator.add_image(img=image.copy())

        return images_manipulator
        

    def update_image_count_label(self):
        self.window_form_images.label_images_count.setText(f"{self.images_count_front_text} {self.images_manipulator.get_image_count()}")

    def show_image(self):

        image_index_txt =  self.window_form_images.textBox_show_image.text().replace(" ", "").replace("\n", "")
        if( check_for_int_format(txt_value=image_index_txt) == False or image_index_txt == "" ):
            print("the image index must be integer")
        else:
            image_index = int(image_index_txt)
            image = self.images_manipulator.get_image(index=image_index)
            if(image is not None):
                self.window_show_image.show_image(img=image)