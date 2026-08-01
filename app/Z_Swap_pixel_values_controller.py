import numpy as np
from PyQt5.QtCore import Qt

"""
import Window_canvas, Z_Window_Canvas_swap_pixel_values, Z_Window_Form_swap_pixel_values
"""
from Window_canvas import CanvasWindow
from Z_Window_Canvas_swap_pixel_values import DrawingWidget
from Z_Window_Form_swap_pixel_values import FormWindow_SwapPixelValues

from Number_format_checker import check_for_positive_int_format, check_for_int_format

from Z_Pixel_area import Pixel_area, Rectangle
from Z_Pixel_area_initializer import Pixel_area_initializer
from Z_Pixel_areas_manipulator import Pixel_areas_manipulator
from Convolutional_kernels_manipulator import Convolutional_kernels_manipulator
from Z_Areas_behiour_when_resizing_main_window import Areas_behaviour_when_resizing_main_window
from Z_Window_Form_pixel_areas_animations import FormWindow_PixelAreasAnimations

from Z_Pixel_area_animations_initializer import Pixel_area_animations_initializer
from Z_Pixel_area_animations_group_initializer import Pixel_area_animation_groups_initializer
from Z_Pixel_area_animation_manipulator import Pixel_area_animation_manipulator
"""
from Z2_Pixel_areas_masks_controller import Pixel_areas_masks_controller
"""
from Z_Pixel_areas_masks_controller import Pixel_areas_masks_controller

from Convolutional_kernels_controller import Convolutional_kernels_controller

from Images_manipulator import Images_manipulator

from RGB_formula_initializer import RGB_formula_initializer

from Order_obj import Order_obj

"""
from PyQt5_Window_functions import open_or_minimize_window, open_or_minimize_windows
"""
from PyQt5_Window_functions import open_or_minimize_window

class Swap_pixel_values_controller: 
    
    """
    def __init__(self):
    """
    def __init__(self, images_manipulator:Images_manipulator):

        self.pixel_areas_masks_controller = Pixel_areas_masks_controller()
        self.convolutional_kernels_controller = Convolutional_kernels_controller()
        
        """
        canvas_swap_pixel_values = Z_Window_Canvas_swap_pixel_values.DrawingWidget()
        self.canvas_window = Window_canvas.CanvasWindow(canvas = canvas_swap_pixel_values)
        self.form_window_pixel_areas = Z_Window_Form_swap_pixel_values.FormWindow_SwapPixelValues()
        """
        canvas_swap_pixel_values = DrawingWidget()
        self.canvas_window = CanvasWindow(canvas = canvas_swap_pixel_values)
        self.form_window_pixel_areas = FormWindow_SwapPixelValues()
        self.form_window_pixel_areas_animations = FormWindow_PixelAreasAnimations()

        self.pixel_areas_masks_controller.form_window_draw_mask.button_apply_all_masks.clicked.connect(lambda _: self.apply_masks(all_masks=True))
        self.pixel_areas_masks_controller.form_window_draw_mask.button_apply_selected_masks.clicked.connect(lambda _: self.apply_masks(all_masks=False))
        self.pixel_areas_masks_controller.form_window_draw_mask.button_remove_all_masks.clicked.connect(self.remove_all_masks)
        self.pixel_areas_masks_controller.form_window_draw_mask.button_remove_selected_masks.clicked.connect(self.remove_selected_masks)

        self.convolutional_kernels_controller.window_form_convolutional_kernels.button_apply_cks.clicked.connect(self.apply_convolutions_to__pixel_areas_manipulator)
        self.convolutional_kernels_controller.window_form_convolutional_kernels.button_remove_cks.clicked.connect(self.remove_convolutional_kernels)
        
        self.form_window_pixel_areas.form_elements__order_ids.button_order_nums.clicked.connect(self.order_pixel_areas_ids)

        self.form_window_pixel_areas.button_clear_canvas.clicked.connect(self.clear_canvas)

        self.form_window_pixel_areas.button_add_rgb_formula.clicked.connect(self.add_rgb_function)
        self.form_window_pixel_areas.button_apply_brush_width_changes.clicked.connect(lambda _, change_width=True: self.change_brush_size_parameters(change_width))
        self.form_window_pixel_areas.button_apply_brush_height_changes.clicked.connect(lambda _, change_width=False: self.change_brush_size_parameters(change_width))
        self.form_window_pixel_areas.button_set_brush_size.clicked.connect(self.set_brush_size)

        self.form_window_pixel_areas.button_open_window__swap_areas_animations.clicked.connect(self.show_animations_form_window)
        self.form_window_pixel_areas.button_open_window__swap_areas_masks.clicked.connect(self.show_window_pixel_areas_mask)
        self.form_window_pixel_areas.button_open_window__swap_areas_convolutional_kernels.clicked.connect(self.show_window_convolutional_kernels)

        self.canvas_window.canvas.mousePressed.connect(self.canvas_clicked)  
        self.canvas_window.canvas.mouseMoved.connect(self.update_dynamic_pixel_area)

        self.form_window_pixel_areas.radioButtonGroup_resize_behaviour.buttonToggled.connect(self.set__areas_resize_behaviour_to__pixel_areas_manipulator)
        self.form_window_pixel_areas.checkBox_use_copy_for_replicas.clicked.connect(self.set__use_copy_for_replicas_to__pixel_areas_manipulator)
        self.form_window_pixel_areas.checkBox_use_copy_for_images.clicked.connect(self.set__use_copy_for_images_to__pixel_areas_manipulator)
        
        self.pixel_areas_manipulator:Pixel_areas_manipulator = Pixel_areas_manipulator()

        self.dynamic_pixel_area_id:int = -1

        self.images_manipulator = images_manipulator



    #<code for showing windows
   
    def show_animations_form_window(self):
        open_or_minimize_window(self.form_window_pixel_areas_animations)
    
    def show_window_pixel_areas_mask(self):
        """
        windows = [self.pixel_areas_masks_controller.form_window_draw_mask, self.pixel_areas_masks_controller.canvas_window]
        open_or_minimize_windows(windows=windows)
        """
        open_or_minimize_window(self.pixel_areas_masks_controller.form_window_draw_mask)

    def show_window_convolutional_kernels(self):
        self.convolutional_kernels_controller.open_window_form_convolutional_kernels()
    #code for showing windows>





    #<code for manipulating the canvas which draws rectangles
    def clear_canvas(self):
        self.canvas_window.canvas.clear()

    def delete_insert_rectangles_to_canvas(self, rectangles: list[Pixel_area]):

        self.clear_canvas()

        for rectangle in rectangles:
            self.canvas_window.canvas.insert_rectangle(x = rectangle.x, y = rectangle.y, width=rectangle.w, height=rectangle.h)

    def set_brush_size(self):
        width = self.form_window_pixel_areas.textBox_brush_width_set.text()
        height = self.form_window_pixel_areas.textBox_brush_height_set.text()

        if(check_for_positive_int_format(width, is_zero_allowed=False) == False or check_for_positive_int_format(height, is_zero_allowed=False)==False):
            print("Error: the brush width or height was either in wrong format or it was equal to 0")
            return
        
        self.canvas_window.canvas.set_brush_size(brush_width=int(width), brush_height=int(height))


    def change_brush_size_parameters(self, change_width: bool):

        #take the brush size parameters
        brush_size_min_value, brush_size_max_value, brush_size_delta = None, None, None
        if(change_width == True):
            brush_size_min_value = self.form_window_pixel_areas.textBox_brush_width_min_value.text()
            brush_size_max_value = self.form_window_pixel_areas.textBox_brush_width_max_value.text()
            brush_size_delta = self.form_window_pixel_areas.textBox_brush_width_delta.text()
        else:
            brush_size_min_value = self.form_window_pixel_areas.textBox_brush_height_min_value.text()
            brush_size_max_value = self.form_window_pixel_areas.textBox_brush_height_max_value.text()
            brush_size_delta = self.form_window_pixel_areas.textBox_brush_height_delta.text()

        #check the the format of the brush size parameters
        if(check_for_positive_int_format(brush_size_min_value, is_zero_allowed=False) == False):
            print("Error: the brush min size field was either in wrong format or it was equal to 0")
            return        
        if(check_for_positive_int_format(brush_size_max_value, is_zero_allowed=False) == False):
            print("Error: the brush max size field was either in wrong format or it was equal to 0")
            return        
        if(check_for_positive_int_format(brush_size_delta, is_zero_allowed=False) == False):
            print("Error: the brush size icrement field was either in wrong format or it was equal to 0")
            return
        
        brush_min_size = int(brush_size_min_value)
        brush_max_size = int(brush_size_max_value)
        brush_delta = int(brush_size_delta)

        if(brush_min_size>brush_max_size):
            print("Error: brush min size value cannot be higher than brush max size value")
            return
        
        if(change_width == True):
            self.canvas_window.canvas.set_brush_width_arguments(brush_min_width = brush_min_size, brush_max_width=brush_max_size, brush_delta_width=brush_delta) 
        else:
            self.canvas_window.canvas.set_brush_height_arguments(brush_min_height = brush_min_size, brush_max_height=brush_max_size, brush_delta_height=brush_delta) 

    #code for manipulating the canvas which draws rectangles>




    
    #<code for getting text (without spaces and new lines) from user input

    def get_text_area_swap_pixel_areas_formatted_text(self):
        swap_pixel_areas_str = self.form_window_pixel_areas.text_area_swap_pixel_areas.toPlainText()
        swap_pixel_areas_str = swap_pixel_areas_str.replace(" ", "").replace("\n", "")
        return swap_pixel_areas_str
    
    def get_text_area_pixel_areas_animations_formatted_text(self):
        pixel_areas_animations_str = self.form_window_pixel_areas_animations.text_area_pixel_areas_animations.toPlainText()
        pixel_areas_animations_str = pixel_areas_animations_str.replace(" ", "").replace("\n", "")
        return pixel_areas_animations_str

    def get_text_area_pixel_areas_animations_groups_formatted_text(self):
        pixel_areas_animations_groups_str = self.form_window_pixel_areas_animations.text_area_pixel_areas_animations_groups.toPlainText()
        pixel_areas_animations_groups_str = pixel_areas_animations_groups_str.replace(" ", "").replace("\n", "")
        return pixel_areas_animations_groups_str
    
    #code for getting text (without spaces and new lines) from user input>




    #<code for working with the text inside the text area containing the information for the pixel swap areas


    #draws the rectangle and gets its coordinates
    def canvas_clicked(self, pos, button):
        
        if button == Qt.LeftButton:
            
            x = pos.x()
            y = pos.y()
               
            
            #draws the rectangle and get's its coordinates
            x, y, w, h = self.canvas_window.canvas.left_mouse_button_pressed(x = x, y = y)

            #get a proper value for the id of the drawn area
            
            swap_pixel_area_id = self.get_first_unused_pixel_area_id()
            if(swap_pixel_area_id == -1):
                print("error: the maximum number of areas was reached")
                return

            #get data which will be inserted in the text area for pixel swap values and the text area for rgb functions
            area_id = str(swap_pixel_area_id)

           
            #append the pixel are properties of the drawn rectangle to the text area
            self.insertTextIn_formWindow_textArea_swapPixelAreas( id=area_id, x=x, y=y, w=w, h=h,)
        
        elif(button == Qt.RightButton):

            pixel_area_id = self.canvas_window.canvas.get_pixel_area_id()
            self.dynamic_pixel_area_id = pixel_area_id

    def update_dynamic_pixel_area(self, dynamic_pixel_area:Rectangle):

        if(self.dynamic_pixel_area_id > -1):
            canvas_window_h = self.canvas_window.size().height()
            canvas_window_w = self.canvas_window.size().width()
            self.pixel_areas_manipulator.set_pixel_area__size_location(id = self.dynamic_pixel_area_id, pixel_area_rec=dynamic_pixel_area, window_h=canvas_window_h, window_w=canvas_window_w)

    def get_first_unused_pixel_area_id(self):

        text = self.get_text_area_swap_pixel_areas_formatted_text()

        pixel_area_end_index = -1
        used_numbers = []
        pixel_area_start_symbol = "{"
        pixel_area_end_symbol = "}"

        pixel_area_id_txt_initial = "{id:"
        pixel_area_id_txt_not_initial = ";id:"

        pixel_area_id_end_separator_1 = ";"
        pixel_area_id_end_separator_2 = "}"

        while (True):

            pixel_area_start_index = text.find(pixel_area_start_symbol, pixel_area_end_index+1)#get's the index of the first symbol of the current pixel area
            pixel_area_end_index = text.find(pixel_area_end_symbol, pixel_area_start_index+1)#get's the index of the last symbol of the current pixel area
            if(pixel_area_start_index == -1 or pixel_area_end_index==-1):
                break
            
            #check whether the current area has an id
            pixel_area_id_txt__start_index = text.find(pixel_area_id_txt_initial, pixel_area_start_index, pixel_area_end_index+1)#the `end` parameter in `find` is not inclusive
            if(pixel_area_id_txt__start_index == -1):
                pixel_area_id_txt__start_index = text.find(pixel_area_id_txt_not_initial, pixel_area_start_index, pixel_area_end_index+1)
                if(pixel_area_id_txt__start_index == -1):
                    continue
            
            #check whether the id of the current area has a proper separator
            pixel_area_id_txt__end_index = text.find(pixel_area_id_end_separator_1, pixel_area_id_txt__start_index, pixel_area_end_index+1)
            if(pixel_area_id_txt__end_index == -1):
                pixel_area_id_txt__end_index = text.find(pixel_area_id_end_separator_2, pixel_area_id_txt__start_index, pixel_area_end_index+1)
                if(pixel_area_id_txt__end_index == -1):
                    continue
            
            id_num = text[pixel_area_id_txt__start_index+len(pixel_area_id_txt_initial):pixel_area_id_txt__end_index]
            is_number_correct = check_for_positive_int_format(txt_value = id_num, is_zero_allowed=False)
            if(is_number_correct == True):
                used_numbers.append(int(id_num))

        #finds the first unused number
        for i in range (1, 1_000_000):
            if(i not in used_numbers):
                return i
        
        return -1 #this code should never be reached unless the user defines over 999_999 valid numbers
    

    def insertTextIn_formWindow_textArea_swapPixelAreas(self, id:str, x:str, y:str, w:str, h:str): 
        text = f"{{ id:{id}; x:{x}; y:{y}; w:{w}; h:{h}; f_id:0 }}"
        self.form_window_pixel_areas.text_area_swap_pixel_areas.append(text)

    #code for working with the text inside the text area containing the information for the pixel swap areas>

    
    

    

    #<code for working with the text inside the text area containing the information for the rgb formulas


    #explores the text inside the provided text; selects all valid ids; determines the first number which is not used as an id in the text (allowed ids should be in this range 1-999_999)
    def get_first_unused_rgb_func_id(self, text: str, id_separator: str, id_max_digits:int):#each element which is inside 2 `id_separator` values will be considered as an id; only ids which are positive integer will be considered as valid (not valid ids are ignored)
        
        start_index = 0
        used_ids = []

        #this code get's the valid ids written in the text area
        while True:
            
            stard_index_current_id = text.find(id_separator, start_index)
            start_index = stard_index_current_id + 1

            if (stard_index_current_id == -1):
                break
            
            end_index_current_id = text.find(id_separator, stard_index_current_id+1)
            if(end_index_current_id == -1):
                break
            
            if(end_index_current_id - stard_index_current_id < 2):
                continue

            end_index_current_id = end_index_current_id if end_index_current_id - stard_index_current_id <= id_max_digits + 1 else  stard_index_current_id + id_max_digits + 1
            current_id = text[stard_index_current_id+1:end_index_current_id]

            is_id_correct = check_for_positive_int_format(txt_value = current_id, is_zero_allowed=False)
            if(is_id_correct == True):
                used_ids.append(int(current_id))

        #this code get's the valid ids written in the text area

        #finds the first unused index
        for i in range (1, 1_000_000):
            if(i not in used_ids):
                return i
        
        return -1 #this code should never be reached unless the user defines over 999_999 valid ids

    def get_text_area_rgb_functions_formatted_text(self):
        rgb_funcs_str = self.form_window_pixel_areas.text_area_rgb_formulas.toPlainText()
        rgb_funcs_str = rgb_funcs_str.replace(" ", "").replace("\n", "")
        return rgb_funcs_str
    
    def add_rgb_function(self):       
        
        rgb_function_from_text_area = self.get_text_area_rgb_functions_formatted_text()
        rgb_function_id = self.get_first_unused_rgb_func_id(text = rgb_function_from_text_area, id_separator="|", id_max_digits=6)
        if(rgb_function_id == -1):
            print("error: the maximum number of RGB formulas was reached")
            return
        
        self.form_window_pixel_areas.rgb_elements.change_RGB_formula()

        rgb_formulas_str = f"|{rgb_function_id}|  r->[ {self.form_window_pixel_areas.rgb_elements.red_func} ]  g->[ {self.form_window_pixel_areas.rgb_elements.green_func} ]  b->[ {self.form_window_pixel_areas.rgb_elements.blue_func} ]"
        rgb_formulas_str = "{ " + rgb_formulas_str + " }\n"

        self.form_window_pixel_areas.text_area_rgb_formulas.append(rgb_formulas_str)


    

    #code for working with the text inside the text area containing the information for the rgb formulas>
    




    #<those functions must be called from the outside
    def get_pixel_areas_manipulator(self) -> Pixel_areas_manipulator:
        return self.pixel_areas_manipulator

    """
    def apply_elements_to_pixel_areas_manipulator(self, images_manipulator:Images_manipulator = None):
    """
    def apply_elements_to_pixel_areas_manipulator(self):

        if(self.form_window_pixel_areas.check_box_pixel_areas.isChecked() == True):
            self.apply_pixel_areas_to__pixel_areas_manipulator()

        if(self.form_window_pixel_areas.check_box_rgb_formulas.isChecked() == True):
            self.apply_rgb_formulas_to__pixel_areas_manipulator()
        
        if(self.form_window_pixel_areas.check_box_animations.isChecked() == True):
            self.apply_animations_to__pixel_areas_manipulator()
        
        if(self.form_window_pixel_areas.check_box_masks.isChecked() == True):
            """
            self.apply_all_masks()
            """
            self.apply_masks(all_masks=True)
        
        if(self.form_window_pixel_areas.check_box_convolutional_kernels.isChecked() == True):
            self.apply_convolutions_to__pixel_areas_manipulator()
        
        if(self.form_window_pixel_areas.check_box_image_versions.isChecked() == True):
            self.apply_image_version_controller()

        """
        if(self.form_window_pixel_areas.check_box_images.isChecked() == True and images_manipulator is not None):
            self.apply_images_manipulator(images_manipulator=images_manipulator)
        """
        if(self.form_window_pixel_areas.check_box_images.isChecked() == True):
            self.apply_images_manipulator()
        

    def remove_elements_from_pixel_areas_manipulator(self):

        if(self.form_window_pixel_areas.check_box_pixel_areas.isChecked() == True):
            self.remove_pixel_areas_from__pixel_areas_manipulator()

        if(self.form_window_pixel_areas.check_box_rgb_formulas.isChecked() == True):
            self.remove_rgb_formulas_from__pixel_areas_manipulator()
        
        if(self.form_window_pixel_areas.check_box_animations.isChecked() == True):
            self.remove_animations_from__pixel_areas_manipulator()
        
        if(self.form_window_pixel_areas.check_box_masks.isChecked() == True):
            self.remove_all_masks()
        
        if(self.form_window_pixel_areas.check_box_convolutional_kernels.isChecked() == True):
            self.remove_convolutional_kernels()
        
        if(self.form_window_pixel_areas.check_box_image_versions.isChecked() == True):
            self.remove_image_version_controller()

        if(self.form_window_pixel_areas.check_box_images.isChecked() == True):
            self.remove_images_manipulator()

    #those functions must be called from the outside>


## <functions for applying/setting/removing elements for the pixel area manipulator


#<functions for applying elements to the pixel area manipulator

    def apply_pixel_areas_to__pixel_areas_manipulator(self):
        
        pixel_area_initializer = Pixel_area_initializer()

        #returns a list  of objects of type `Pixel_area`
        pixel_areas = pixel_area_initializer.create_pixel_areas(text=self.get_text_area_swap_pixel_areas_formatted_text())

        #execute this code if the format of the pixel areas is wrong 
        if(pixel_areas is None or len(pixel_areas)==0):            
            return          

        pixel_areas = self.update_canvas(pixel_areas=pixel_areas)# get's those areas whose top left corner and bottom right corner are inside the canvas
        
        #execute this code if all pixel areas with valid format were outside the canvas
        if(pixel_areas is None or len(pixel_areas)==0):            
            return               

        pixel_areas_dict = {}
        for pixel_area in pixel_areas:
            pixel_areas_dict[pixel_area.id] = pixel_area
        
        self.pixel_areas_manipulator.apply_pixel_areas(pixel_areas_dict=pixel_areas_dict)
    

    def apply_rgb_formulas_to__pixel_areas_manipulator(self):

        rgb_formulas_str = self.get_text_area_rgb_functions_formatted_text()
        rgb_formula_initializer = RGB_formula_initializer()
        rgb_formulas_dict = rgb_formula_initializer.create_rgb_formulas_with_pixel_areas(rgb_formulas=rgb_formulas_str)

        if(rgb_formulas_dict is None):
            rgb_formulas_dict = {}
        self.pixel_areas_manipulator.apply_rgb_formulas(rgb_formulas_dict=rgb_formulas_dict)

    def apply_animations_to__pixel_areas_manipulator(self):
        
        #<pixel areas animations

        pixel_area_animations_initializer = Pixel_area_animations_initializer()
        pixel_areas_animations_formatted_text = self.get_text_area_pixel_areas_animations_formatted_text()
        pixel_areas_animations = None
        pixel_areas_animations_dict = {}
        
        if(len(pixel_areas_animations_formatted_text) > 0):
            pixel_areas_animations = pixel_area_animations_initializer.create_animations_for_pixel_areas(text=pixel_areas_animations_formatted_text)
            if(pixel_areas_animations is None or len(pixel_areas_animations)==0):            
                return 
            
            for pixel_area_animation in pixel_areas_animations:
                pixel_areas_animations_dict[pixel_area_animation.id] = pixel_area_animation
        
         
        pixel_area_animations_groups_initializer = Pixel_area_animation_groups_initializer()
        pixel_areas_animations_groups_formatted_text = self.get_text_area_pixel_areas_animations_groups_formatted_text()
        pixel_areas_animations_groups = None
        pixel_areas_animations_groups_dict = {}

        if(len(pixel_areas_animations_groups_formatted_text) > 0):
            pixel_areas_animations_groups = pixel_area_animations_groups_initializer.create_animation_groups_for_pixel_areas(text=pixel_areas_animations_groups_formatted_text)
            if(pixel_areas_animations_groups is None or len(pixel_areas_animations_groups)==0):            
                return 
        
            for pixel_area_animation_group in pixel_areas_animations_groups:
                pixel_areas_animations_groups_dict[pixel_area_animation_group.id] = pixel_area_animation_group

        #pixel areas animations>

        #<pixel area animation manipulator
        
        pixel_area_animation_manipulator = None
        if(len(pixel_areas_animations_dict)>0 or len(pixel_areas_animations_groups_dict)>0):
            pixel_area_animation_manipulator = Pixel_area_animation_manipulator(pixel_areas_animations_dict=pixel_areas_animations_dict, pixel_areas_animations_groups_dict=pixel_areas_animations_groups_dict)
        
        #pixel area animation manipulator>

        self.pixel_areas_manipulator.apply_animations(animations_manipulator=pixel_area_animation_manipulator)
    


    """
    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def apply_selected_masks(self, img_for_colour_range_masks:np.ndarray[np.uint8] = None):
        
        rectangles_with_ids:dict[int, Rectangle] = self.pixel_areas_manipulator.get_all_main_areas_as_rectangles()
        
        masks = self.pixel_areas_masks_controller.apply_selected_masks(rectangles_with_ids=rectangles_with_ids, img_for_colour_range_masks=img_for_colour_range_masks)
        if(masks is not None):
            self.pixel_areas_manipulator.apply_masks(masks=masks)
    """
    """

    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def apply_all_masks(self, img_for_colour_range_masks:np.ndarray[np.uint8] = None):

        rectangles_with_ids:dict[int, Rectangle] = self.pixel_areas_manipulator.get_all_main_areas_as_rectangles()
        
        masks = self.pixel_areas_masks_controller.apply_all_masks(rectangles_with_ids=rectangles_with_ids, img_for_colour_range_masks=img_for_colour_range_masks)
        if(masks is not None):
            self.pixel_areas_manipulator.apply_masks(masks=masks)
    """
    def apply_masks(self, all_masks:bool):

        rectangles_with_ids:dict[int, Rectangle] = self.pixel_areas_manipulator.get_all_main_areas_as_rectangles()
        images_for_masks:list[np.ndarray[np.uint8]] = self.images_manipulator.get_images_in_range(index1=0, index2=-1)

        if(self.pixel_areas_masks_controller.form_window_draw_mask.checkBox_update_last_image_when_applying_masks.isChecked() == True):
            additional_image = None
            if(self.pixel_areas_masks_controller.form_window_draw_mask.radioButton_take_image_under_capture_window.isChecked() == True):
                additional_image = self.images_manipulator.get_image_under_capture_window() 
            else:
                additional_image = self.images_manipulator.get_transformed_image_from_capture_window()
            images_for_masks.append(additional_image)
            """
            print(additional_image.shape)#this line is used just to find out what causes the image to have less then 3 dimentions; it can be deleted after the bug is fixed; the bug appears to happen when the mask checkbox is checked and when the apply elements button is pressed many times in a row
            """
            
        masks = None
        if(all_masks == True):
            masks = self.pixel_areas_masks_controller.apply_all_masks(rectangles_with_ids=rectangles_with_ids, images_for_masks=images_for_masks)
        else:
            masks = self.pixel_areas_masks_controller.apply_selected_masks(rectangles_with_ids=rectangles_with_ids, images_for_masks=images_for_masks)

        if(masks is not None):
            self.pixel_areas_manipulator.apply_masks(masks=masks)
    """

    def remove_selected_masks(self):
        
        masks = self.pixel_areas_masks_controller.remove_selected_applied_masks()
        if(masks is not None):
            self.pixel_areas_manipulator.apply_masks(masks=masks)
    
    """
    def remove_selected_masks(self):
        
        remaining_masks = self.pixel_areas_masks_controller.remove_selected_applied_masks()
        if(remaining_masks is not None):
            self.pixel_areas_manipulator.apply_masks(masks=remaining_masks)


    
    def apply_convolutions_to__pixel_areas_manipulator(self):

        cks_manipulator: Convolutional_kernels_manipulator = self.convolutional_kernels_controller.get_convolutional_kernels_manipulator()
        self.pixel_areas_manipulator.apply_convolutional_kernels(cks_manipulator=cks_manipulator)

    def apply_image_version_controller(self):
        
        if(self.should_create_image_version_contoller()==True):
            
            image_version_start_index = -1 if self.form_window_pixel_areas.textBox_image_version_start_index.text() == "" else int(self.form_window_pixel_areas.textBox_image_version_start_index.text())
            image_version_end_index = -1 if self.form_window_pixel_areas.textBox_image_version_end_index.text() == "" else int(self.form_window_pixel_areas.textBox_image_version_end_index.text())
            image_version_increment = 0 if self.form_window_pixel_areas.textBox_image_version_increment.text() == "" else int(self.form_window_pixel_areas.textBox_image_version_increment.text())
            image_version_swap_frequency = 0 if self.form_window_pixel_areas.textBox_image_version_swap_frequency.text() == "" else int(self.form_window_pixel_areas.textBox_image_version_swap_frequency.text())
            image_versions_count = 1 if self.form_window_pixel_areas.textBox_image_version_count.text() == "" else int(self.form_window_pixel_areas.textBox_image_version_count.text())
            use_special_image_version = self.form_window_pixel_areas.checkBox_use_special_image_version.isChecked()

            self.pixel_areas_manipulator.apply_image_version_controller(image_version_start_index =image_version_start_index, image_version_end_index=image_version_end_index, image_version_increment = image_version_increment, image_version_swap_frequency = image_version_swap_frequency, image_versions_count=image_versions_count,  use_special_image_version=use_special_image_version)

    """
    def apply_images_manipulator(self, images_manipulator:Images_manipulator):
        self.pixel_areas_manipulator.apply_images_manipulator(images_manipulator=images_manipulator)
    """
    def apply_images_manipulator(self):
        self.pixel_areas_manipulator.apply_images_manipulator(images_manipulator=self.images_manipulator)

#functions for applying elements to the pixel area manipulator>



#<functions for removing elements for the pixel area manipulator

    def remove_pixel_areas_from__pixel_areas_manipulator(self):
        self.pixel_areas_manipulator.remove_pixel_areas()
    
    def remove_rgb_formulas_from__pixel_areas_manipulator(self):
        self.pixel_areas_manipulator.remove_rgb_formulas()
    
    def remove_animations_from__pixel_areas_manipulator(self):
        self.pixel_areas_manipulator.remove_animations()
    
    def remove_all_masks(self):
        self.pixel_areas_masks_controller.remove_all_applied_masks()
        self.pixel_areas_manipulator.remove_masks()
    
    def remove_convolutional_kernels(self):
        self.convolutional_kernels_controller.remove_convolutional_kernels()
        self.pixel_areas_manipulator.remove_convolutional_kernels()
    
    def remove_image_version_controller(self):
        self.pixel_areas_manipulator.remove_image_version_controller()

    def remove_images_manipulator(self):
        self.pixel_areas_manipulator.remove_images_manipulator()
    
#functions for removing elements for the pixel area manipulator>



#<fuctions for setting the values of boolean and enum elements in the pixel area manipulator

    def set__areas_resize_behaviour_to__pixel_areas_manipulator(self):

        areas_resize_behaviour = self.get_areas_resize_behaviour()
        self.pixel_areas_manipulator.set__areas_behaviour_when_resizing_main_window(areas_behiour_when_resizing_main_window=areas_resize_behaviour, aspect_ratio_width=self.canvas_window.canvas.width(), aspect_ratio_height=self.canvas_window.canvas.height())
    
    def set__use_copy_for_replicas_to__pixel_areas_manipulator(self):

        use_copy_for_replicas = self.form_window_pixel_areas.checkBox_use_copy_for_replicas.isChecked()
        self.pixel_areas_manipulator.set__use_copy_for_replicas(use_copy_for_replicas=use_copy_for_replicas)

    def set__use_copy_for_images_to__pixel_areas_manipulator(self):
    
        use_copy_for_images = self.form_window_pixel_areas.checkBox_use_copy_for_images.isChecked()
        self.pixel_areas_manipulator.set__use_copy_for_images(use_copy_for_images=use_copy_for_images)

#fuctions for setting the values of boolean and enum elements in the pixel area manipulator>


    def order_pixel_areas_ids(self):
        
        order_obj: Order_obj = self.form_window_pixel_areas.form_elements__order_ids.get__order_obj()
        if(order_obj is not None):
            self.pixel_areas_manipulator.order_pixel_areas_ids(order_obj=order_obj)
            pixel_areas_ids = self.pixel_areas_manipulator.get_pixel_areas_ids()
            print(f"the order of the pixel areas ids is: {pixel_areas_ids}")



## functions for applying/setting/removing elements for the pixel area manipulator>


    #<helper methods

    def get_areas_resize_behaviour(self) -> Areas_behaviour_when_resizing_main_window:
        
        areas_resize_behaviour = None

        if(self.form_window_pixel_areas.radioButton_areas_resize.isChecked()):
            areas_resize_behaviour = Areas_behaviour_when_resizing_main_window.Resize
        elif(self.form_window_pixel_areas.radioButton_areas_move.isChecked()):
            areas_resize_behaviour = Areas_behaviour_when_resizing_main_window.Move
        elif(self.form_window_pixel_areas.radioButton_areas_keep_aspect_ratio.isChecked()):
            areas_resize_behaviour = Areas_behaviour_when_resizing_main_window.Keep_aspect_ratio
        
        return areas_resize_behaviour

    def should_create_image_version_contoller(self):

        error_message = ""
        if(check_for_int_format(txt_value=self.form_window_pixel_areas.textBox_image_version_start_index.text()) == False):
            error_message += "the field with the image version start index was in wrong format (only int values whether positive or negative are allowed); "
        if(check_for_int_format(txt_value=self.form_window_pixel_areas.textBox_image_version_end_index.text()) == False):
            error_message += "the field with the image version end index was in wrong format (only int values whether positive or negative are allowed); "
        if(check_for_positive_int_format(txt_value=self.form_window_pixel_areas.textBox_image_version_increment.text()) == False):
            error_message += "the field with the image version step was in wrong format (only positive int values are allowed); "
        if(check_for_positive_int_format(txt_value=self.form_window_pixel_areas.textBox_image_version_swap_frequency.text()) == False):
            error_message += "the field with the image version swap frequency was in wrong format (only positive int values are allowed); "
        if(check_for_positive_int_format(txt_value=self.form_window_pixel_areas.textBox_image_version_count.text(), is_zero_allowed=False) == False):
            error_message += "the field with the image version count was in wrong format (only positive int values above 0 are allowed); "
        
        if(error_message != ""):
            error_message = "warning: the program will not apply your image version settings due to the following error/s: " + error_message
            print(error_message)
            return False

        return True



#when called this function will remove everything from the canvas and will put in there rectangles based on the coordinates written in the text area 
    def update_canvas(self, pixel_areas: list[Pixel_area]) -> list[Pixel_area]:       
           
        valid_rectangles = self.get_rectangles_inside_canvas(rectangles = pixel_areas)

        self.delete_insert_rectangles_to_canvas(rectangles = valid_rectangles)       
        
        return valid_rectangles




# get's only those areas whose top left corner and bottom right corner are inside the canvas
    def get_rectangles_inside_canvas(self, rectangles: list[Pixel_area]) -> list[Pixel_area]:   
        
        canvas_width = self.canvas_window.canvas.width()
        canvas_height = self.canvas_window.canvas.height()   

        valid_rectangles = []
        skipped_areas_ids = []

        for rectangle in rectangles:    

            if(rectangle.x + rectangle.w <= canvas_width and rectangle.y + rectangle.h <= canvas_height):
                valid_rectangles.append(rectangle)
            else:
                skipped_areas_ids.append(rectangle.id)

        if(len(skipped_areas_ids)>0):
            print(f"warning: the areas with ids {str(skipped_areas_ids)} will not be applied because they were outside the canvas")
        return valid_rectangles

