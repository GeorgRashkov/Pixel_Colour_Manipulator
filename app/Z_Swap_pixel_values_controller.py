
import Window_canvas, Z_Window_Canvas_swap_pixel_values, Z_Window_Form_swap_pixel_values
from PyQt5.QtCore import Qt

import ast

from Number_format_checker import check_for_positive_int_format, check_numbers_from_string, check_for_int_format
from Z_RGB_formula_checker import check_rgb_formulas_format_for_pixel_areas, get_closing_square_bracket

from Z_RGB_formula import RGB_formula
from Z_Pixel_area import Pixel_area
from Z_Pixel_area_initializer import Pixel_area_initializer
from Z_Pixel_areas_manipulator import Pixel_areas_manipulator
from Z_Areas_behiour_when_resizing_main_window import Areas_behaviour_when_resizing_main_window

class Swap_pixel_values_controller: 
    
    def __init__(self):

        canvas_swap_pixel_values = Z_Window_Canvas_swap_pixel_values.DrawingWidget()
        self.canvas_window = Window_canvas.CanvasWindow(canvas = canvas_swap_pixel_values)
        self.form_window = Z_Window_Form_swap_pixel_values.FormWindow_SwapPixelValues()
                
        self.form_window.button_clear_canvas.clicked.connect(self.clear_canvas)

        self.form_window.button_add_rgb_formula.clicked.connect(self.add_rgb_function)
        self.form_window.button_apply_brush_width_changes.clicked.connect(lambda _, change_width=True: self.change_brush_size_parameters(change_width))
        self.form_window.button_apply_brush_height_changes.clicked.connect(lambda _, change_width=False: self.change_brush_size_parameters(change_width))
        self.form_window.button_set_brush_size.clicked.connect(self.set_brush_size)
        
        self.canvas_window.canvas.mousePressed.connect(self.canvas_clicked)  
        
        self.swap_pixel_areas = []#the list contains objects of type `Pixel_area`            



    #<code for showing windows
    def show_form_window(self):
        self.form_window.show()
    
    def show_canvas_window(self):
        self.canvas_window.show()
    #code for showing windows>





    #<code for manipulating the canvas
    def clear_canvas(self):
        self.canvas_window.canvas.clear()

    def delete_insert_rectangles_to_canvas(self, rectangles: list[Pixel_area]):

        self.clear_canvas()

        for rectangle in rectangles:
            self.canvas_window.canvas.insert_rectangle(x = rectangle.x, y = rectangle.y, width=rectangle.w, height=rectangle.h)

    def set_brush_size(self):
        width = self.form_window.textBox_brush_width_set.text()
        height = self.form_window.textBox_brush_height_set.text()

        if(check_for_positive_int_format(width, is_zero_allowed=False) == False or check_for_positive_int_format(height, is_zero_allowed=False)==False):
            print("Error: the brush width or height was either in wrong format or it was equal to 0")
            return
        
        self.canvas_window.canvas.set_brush_size(brush_width=int(width), brush_height=int(height))


    def change_brush_size_parameters(self, change_width: bool):

        #take the brush size parameters
        brush_size_min_value, brush_size_max_value, brush_size_delta = None, None, None
        if(change_width == True):
            brush_size_min_value = self.form_window.textBox_brush_width_min_value.text()
            brush_size_max_value = self.form_window.textBox_brush_width_max_value.text()
            brush_size_delta = self.form_window.textBox_brush_width_delta.text()
        else:
            brush_size_min_value = self.form_window.textBox_brush_height_min_value.text()
            brush_size_max_value = self.form_window.textBox_brush_height_max_value.text()
            brush_size_delta = self.form_window.textBox_brush_height_delta.text()

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

    #code for manipulating the canvas>







    #<code for working with the text inside the text area containing the information for the pixel swap areas
    
    """
    def get_text_area_swap_pixel_areas_formatted_text_for_validation(self)
        text = self.form_window.text_area_swap_pixel_areas.toPlainText()#gets the text in the text area
        text = text[0:-1].replace(" ","").replace("\n", "").replace("[|", "[[").replace("|", "]")#replaces `|` with `[` or `]`; removes the spaces, the new lines and the last symbol which is a comma
        return text
    """

    def get_text_area_swap_pixel_areas_formatted_text(self):
        swap_pixel_areas_str = self.form_window.text_area_swap_pixel_areas.toPlainText()
        swap_pixel_areas_str = swap_pixel_areas_str.replace(" ", "").replace("\n", "")
        return swap_pixel_areas_str
    
    #draws the rectangle and gets its coordinates
    def canvas_clicked(self, pos, button):
        
        if button == Qt.LeftButton:
            
            x = pos.x()
            y = pos.y()
               
            
            #draws the rectangle and get's its coordinates
            x, y, w, h = self.canvas_window.canvas.left_mouse_button_pressed(x = x, y = y)

            #get a proper value for the id of the drawn area
            swap_pixel_areas_from_text_area = self.get_text_area_swap_pixel_areas_formatted_text()
            swap_pixel_area_id = self.get_first_unique_positive_number(text = swap_pixel_areas_from_text_area, start_separator = "id:", end_separator = ";", allowed_symbols_before_start_separator = ["{",";"] ,is_zero_allowed=False)
            if(swap_pixel_area_id == -1):
                print("error: the maximum number of areas was reached")
                return

            #get data which will be inserted in the text area for pixel swap values and the text area for rgb functions
            area_id = str(swap_pixel_area_id)
                        
            #<pixel area properties
            a_ids = self.form_window.text_box_animation_ids.text().replace(" ", "")
            ag_ids = self.form_window.text_box_animations_group_ids.text().replace(" ", "")
            f_id = self.form_window.text_box_rgb_formula_id.text().replace(" ", "")
            p_ids = self.form_window.text_box_pixel_area_ids_as_input_for_rgb_func.text().replace(" ", "")
            p_x = self.form_window.text_box_pixel_area_x_locations_as_input_for_rgb_func.text().replace(" ", "")
            p_y = self.form_window.text_box_pixel_area_y_locations_as_input_for_rgb_func.text().replace(" ", "")
            img_in_v = self.form_window.text_box_image_version_as_input_for_rgb_func.text().replace(" ", "")
            img_out_v = self.form_window.text_box_image_version_as_output_from_rgb_func.text().replace(" ", "")
            img_out_stack = self.form_window.text_box_image_version_as_output_from_rgb_func_stack.text().replace(" ", "")
            
            a_ids = self.get_proper_int_values(values=a_ids, element_name = "a_ids")#animation ids
            ag_ids = self.get_proper_int_values(values=ag_ids, element_name = "ag_ids")#animation groups ids
            f_id = self.get_proper_int_value(value=f_id, element_name = "f_id")#rgb function id
            p_ids = self.get_proper_int_values(values=p_ids, element_name = "p_ids")#pixel areas ids
            p_x = self.get_proper_int_values(values=p_x, element_name = "p_x")#pixel areas x coordinates
            p_y = self.get_proper_int_values(values=p_y, element_name = "p_y")#pixel areas y coordinates
            img_in_v = self.get_proper_int_value(value=img_in_v, element_name = "img_in_v")#image input version
            img_out_v = self.get_proper_int_value(value=img_out_v, element_name = "img_out_v")#image output version
            img_out_stack = self.get_proper_int_value(value=img_out_stack, element_name = "img_out_stack")#image ouput stack
            #pixel area properties>
                       

            #append the pixel are properties of the drawn rectangle to the text area
            self.insertTextIn_formWindow_textArea_swapPixelAreas( id=area_id, x=x, y=y, w=w, h=h, a_ids=a_ids, ag_ids=ag_ids,
            f_id=f_id, p_ids=p_ids, p_x=p_x, p_y=p_y, img_in_v=img_in_v, img_out_v=img_out_v, img_out_stack=img_out_stack)
    
    def get_first_unique_positive_number(self, text:str, start_separator:str, end_separator:str, allowed_symbols_before_start_separator:list, is_zero_allowed:bool):

        start_index = 0      
        used_numbers = [] 

        while (True):
                        
            start_separator_index = text.find(start_separator, start_index)#get's the index of the first symbol of the separator
            if(start_separator_index == -1):
                break
            num_index = start_separator_index + len(start_separator) #get's the index of the first symbol of the number

            end_separator_index = text.find(end_separator, num_index)#get's the index of the first symbol of the separator
            if(end_separator_index == -1):
                break
            
            if(num_index == end_separator_index):#execute this code if there is nothing between the start separator and the end separator
                start_index = end_separator_index + len(end_separator) #get's the index placed after the last symbol of the separator
                continue

            if(num_index > 0):
                if(text[num_index-len(start_separator)-1] not in allowed_symbols_before_start_separator):
                    start_index = end_separator_index + len(end_separator) #get's the index placed after the last symbol of the separator
                    continue

            num = text[num_index:end_separator_index]
            is_number_correct = check_for_positive_int_format(txt_value = num, is_zero_allowed=is_zero_allowed)
            if(is_number_correct == True):
                used_numbers.append(int(num))

            start_index = end_separator_index + len(end_separator) #get's the index placed after the last symbol of the separator
        
        #finds the first unused number
        for i in range (1, 1_000_000):
            if(i not in used_numbers):
                return i
        
        return -1 #this code should never be reached unless the user defines over 999_999 valid numbers

            


    def get_proper_int_value(self, value:str, element_name:str = ""):
        
        if(value == ""):
            return None 
        
        is_number_in_correct_format = check_for_positive_int_format(value)
        if(is_number_in_correct_format == False): 
            value = None 
            print(f"warning: the value of the element `{element_name}` is not applied because the element was in wrong format (only numbers are allowed)")
                    
        return value
    
    def get_proper_int_values(self, values:str, element_name:str = ""):
        
        if(values == ""):
            return None 
        
        are_numbers_in_correct_format = check_numbers_from_string(txt_value=values,separator=",", search_for_floats=False, search_for_positives_only=True)
        if( are_numbers_in_correct_format == False): 
            values = None  
            print(f"warning: the values of the element `{element_name}` are not applied because the element was in wrong format (only numbers and commas are allowed).")
        
        return values

    def insertTextIn_formWindow_textArea_swapPixelAreas(self, id:str, x:str, y:str, w:str, h:str, a_ids:str, ag_ids:str, f_id:str, p_ids:str, p_x:str, p_y:str, img_in_v:str, img_out_v:str, img_out_stack:str): 
        text = "{"
        if(id is not None):
            text = f"{text}id:{id}; "

        if(x is not None):
            text = f"{text}x:{x}; "

        if(y is not None):
            text = f"{text}y:{y}; "

        if(w is not None):
            text = f"{text}w:{w}; "

        if(h is not None):
            text = f"{text}h:{h}; "
        
        if(a_ids is not None):
            text = f"{text}a_ids:[{a_ids}]; "
        
        if(ag_ids is not None):
            text = f"{text}ag_ids:[{ag_ids}]; "

        if(f_id is not None):
            text = f"{text}f_id:{f_id}; "

        if(p_ids is not None):
            text = f"{text}p_ids:[{p_ids}]; "
                
        if(p_x is not None):
            text = f"{text}p_x:[{p_x}]; "
            
        if(p_y is not None):
            text = f"{text}p_y:[{p_y}]; "
            
        if(img_in_v is not None):
            text = f"{text}img_in_v:{img_in_v}; "
            
        if(img_out_v is not None):
            text = f"{text}img_out_v:{img_out_v}; "
            
        if(img_out_stack is not None):
            text = f"{text}img_out_stack:{img_out_stack}; "
        
        text = text[0:-2] + "}" 

        self.form_window.text_area_swap_pixel_areas.append(text)
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

            if stard_index_current_id == -1:
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
        rgb_funcs_str = self.form_window.text_area_rgb_formulas.toPlainText()
        rgb_funcs_str = rgb_funcs_str.replace(" ", "").replace("\n", "")
        return rgb_funcs_str
    
    def add_rgb_function(self):       
        
        rgb_function_from_text_area = self.get_text_area_rgb_functions_formatted_text()
        rgb_function_id = self.get_first_unused_rgb_func_id(text = rgb_function_from_text_area, id_separator="|", id_max_digits=6)
        if(rgb_function_id == -1):
            print("error: the maximum number of RGB formulas was reached")
            return
        
        self.form_window.rgb_elements.change_RGB_formula()

        rgb_formulas_str = f"|{rgb_function_id}|  r->[ {self.form_window.rgb_elements.red_func} ]  g->[ {self.form_window.rgb_elements.green_func} ]  b->[ {self.form_window.rgb_elements.blue_func} ]"
        rgb_formulas_str = "{ " + rgb_formulas_str + " }\n"

        self.form_window.text_area_rgb_formulas.append(rgb_formulas_str)


    

    #code for working with the text inside the text area containing the information for the rgb formulas>
    



    
    
#<not checked!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  



#when called this function will remove everything from the canvas and will put in there rectangles based on the coordinates written in the text area 
    def get_pixel_areas_manipulator(self) -> Pixel_areas_manipulator:
        
        #<rgb formulas

        rgb_formulas_str = self.get_text_area_rgb_functions_formatted_text()

        #execute this code if the format of the rgb formulas is wrong 
        if(check_rgb_formulas_format_for_pixel_areas(rgb_formulas_for_pixel_areas=rgb_formulas_str)== False):
            return None
        
        #the dictionary has rgb formula id (type int) as a key and a dictinary for value; the inner dictionaries have an rgb channels (values `r`,`g`,`b`) for keys and rgb formulas (represented as strings) for values
        rgb_formulas_dict = self.get_dictionary_of_rgb_formulas(rgb_formulas_for_pixel_areas = rgb_formulas_str)
        
        if(rgb_formulas_dict is None or len(rgb_formulas_dict) == 0):
            print("warning: the areas will not be applied because there was no rgb formula")
            return None

        for id in rgb_formulas_dict.keys():
            rgb_formulas_dict[id] = RGB_formula(red_func=rgb_formulas_dict[id]["r"],green_func=rgb_formulas_dict[id]["g"],blue_func=rgb_formulas_dict[id]["b"],use_pixel_areas=True)

        #rgb formulas>


        #<pixel areas

        pixel_area_initializer = Pixel_area_initializer()

        #returns a list  of objects of type `Pixel_area`
        pixel_areas = pixel_area_initializer.create_pixel_areas(text=self.get_text_area_swap_pixel_areas_formatted_text())

        #execute this code if the format of the pixel areas is wrong 
        if(pixel_areas is None or len(pixel_areas)==0):            
            return None          

        pixel_areas = self.update_canvas(pixel_areas=pixel_areas)# get's those areas whose top left corner and bottom left corner are inside the canvas
        
        #execute this code if all pixel areas with valid format were outside the canvas
        if(pixel_areas is None or len(pixel_areas)==0):            
            return None               

        pixel_areas_dict = {}
        for pixel_area in pixel_areas:
            pixel_areas_dict[pixel_area.id] = pixel_area

        
        #pixel areas>


        #<pixel area manipulator
        areas_resize_behaviour = self.get_areas_resize_behaviour()
        pixel_areas_manipulator = Pixel_areas_manipulator(pixel_areas_dict=pixel_areas_dict, rgb_formulas_dict=rgb_formulas_dict, areas_behiour_when_resizing_main_window=areas_resize_behaviour)
        if(areas_resize_behaviour == Areas_behaviour_when_resizing_main_window.Keep_aspect_ratio):
            pixel_areas_manipulator.set_aspect_ratio(initial_image_width=self.canvas_window.canvas.width(), initial_image_height=self.canvas_window.canvas.height())

        self.try_to_create_image_version_controller(pixel_areas_manipulator=pixel_areas_manipulator)
        #pixel area manipulator>
        
        
        return pixel_areas_manipulator
    
    def get_areas_resize_behaviour(self) -> Areas_behaviour_when_resizing_main_window:
        
        areas_resize_behaviour = None

        if(self.form_window.radioButton_areas_resize.isChecked()):
            areas_resize_behaviour = Areas_behaviour_when_resizing_main_window.Resize
        elif(self.form_window.radioButton_areas_move.isChecked()):
            areas_resize_behaviour = Areas_behaviour_when_resizing_main_window.Move
        elif(self.form_window.radioButton_areas_keep_aspect_ratio.isChecked()):
            areas_resize_behaviour = Areas_behaviour_when_resizing_main_window.Keep_aspect_ratio
        
        return areas_resize_behaviour

    def should_create_image_version_contoller(self):

        if(self.form_window.textBox_image_version_start_index.text()=="" and self.form_window.textBox_image_version_increment.text()=="" and self.form_window.textBox_image_version_swap_frequency.text()==""):
            return False

        error_message = ""
        if(check_for_int_format(txt_value=self.form_window.textBox_image_version_start_index.text()) == False):
            error_message += "the field with the image version start index was in wrong format (only int values whether positive or negative are allowed); "
        if(check_for_int_format(txt_value=self.form_window.textBox_image_version_increment.text()) == False):
            error_message += "the field with the image version increment was in wrong format (only int values whether positive or negative are allowed); "
        if(check_for_positive_int_format(txt_value=self.form_window.textBox_image_version_swap_frequency.text()) == False):
            error_message += "the field with the image version frequency was in wrong format (only positive int values are allowed); "
        
        if(error_message != ""):
            error_message = "warning: the program will not apply your image version settings due to the following error/s: " + error_message
            print(error_message)
            return False

        return True
    
    def try_to_create_image_version_controller(self, pixel_areas_manipulator:Pixel_areas_manipulator):
        
        if(self.should_create_image_version_contoller()==True):
            
            image_version_start_index = 0 if self.form_window.textBox_image_version_start_index.text() == "" else int(self.form_window.textBox_image_version_start_index.text())
            image_version_increment = 1 if self.form_window.textBox_image_version_increment.text() == "" else int(self.form_window.textBox_image_version_increment.text())
            image_version_swap_frequency = 1 if self.form_window.textBox_image_version_swap_frequency.text() == "" else int(self.form_window.textBox_image_version_swap_frequency.text())
            
            pixel_areas_manipulator.create_image_version_controller(image_version_start_index =image_version_start_index, image_version_increment = image_version_increment, image_version_swap_frequency = image_version_swap_frequency)
        
            
    
    #creates a dictonary which has rgb formula id (type int) as a key and a dictinary for value; the inner dictionaries have an rgb channels (values `r`,`g`,`b`) for keys and rgb formulas (represented as strings) for values
    #the input parameter `rgb_formulas_for_pixel_areas` must be in a valid format before calling the function
    def get_dictionary_of_rgb_formulas(self, rgb_formulas_for_pixel_areas:str)  -> dict[int,dict[str,str]] :

        rgb_formulas_pixel_area_start_index = 0
        rgb_formulas_pixel_area_end_index = 0        
        rgb_formulas_pixel_areas_dict = {}
        
        while(rgb_formulas_pixel_area_end_index < len(rgb_formulas_for_pixel_areas)-1):

            rgb_formulas_pixel_area_start_index = rgb_formulas_for_pixel_areas.find("{", rgb_formulas_pixel_area_end_index)
            rgb_formulas_pixel_area_end_index = rgb_formulas_for_pixel_areas.find("}", rgb_formulas_pixel_area_start_index)

            rgb_formulas_current_pixel_area = rgb_formulas_for_pixel_areas[rgb_formulas_pixel_area_start_index+1: rgb_formulas_pixel_area_end_index]
            (rgb_formula_id, rgb_formulas_dict) = self.get_rgb_formulas(rgb_formulas_for_pixel_area = rgb_formulas_current_pixel_area)
            rgb_formulas_pixel_areas_dict[rgb_formula_id] = rgb_formulas_dict
        
        return rgb_formulas_pixel_areas_dict


    def get_rgb_formulas(self, rgb_formulas_for_pixel_area: str):   
                
        rgb_formula_id_index_start = rgb_formulas_for_pixel_area.find("|", 0)
        rgb_formula_id_index_end = rgb_formulas_for_pixel_area.find("|", rgb_formula_id_index_start+1)

        rgb_formula_id = rgb_formulas_for_pixel_area[rgb_formula_id_index_start+1:rgb_formula_id_index_end]
            
        rgb_channel_index = 0
        rgb_formula_start_index = 0
        rgb_formula_end_index = 0
        rgb_channels = ["r", "g", "b"]
        rgb_formulas = {}

        while (rgb_channel_index < 3):

            rgb_formula_start_index = rgb_formulas_for_pixel_area.find("[", rgb_formula_end_index)
            rgb_formula_end_index = get_closing_square_bracket(text=rgb_formulas_for_pixel_area,start_index=rgb_formula_start_index)#rgb_formulas_for_pixel_area.find("]", rgb_formula_start_index)
           
            rgb_formula = rgb_formulas_for_pixel_area[rgb_formula_start_index+1:rgb_formula_end_index]
            rgb_formulas[rgb_channels[rgb_channel_index]] = rgb_formula
            
            rgb_channel_index+=1

        return (int(rgb_formula_id), rgb_formulas)




















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







#<not checked!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  

"""

#when called this function will remove everything from the canvas and will put in there rectangles based on the coordinates written in the text area 
    def update_canvas(self, update_text):
        
        self.swap_pixel_areas = []
        text = self.get_text_area_swap_pixel_areas_formatted_text_for_validation()
        error_message = check_str_format_for_lists_of_lists_of_ints(text=text, inner_lists_elements_count=self.inner_lists_elements_count)
        
        if(error_message!=""):
            print(error_message)
            return
        
        text = f"[{text}]"#add square brackets at the beginning and the end (it is necessary for converting the text into a list)
        rectangles = ast.literal_eval(text)#converting the text into a list
        print(rectangles)

        canvas_width = self.canvas_window.canvas.width()
        canvas_height = self.canvas_window.canvas.height()

        valid_rectangles = self.get_rectangles_inside_canvas(canvas_width = canvas_width, canvas_height = canvas_height, rectangles = rectangles)
        self.delete_insert_rectangles_to_canvas(rectangles = valid_rectangles)
        
        if(update_text == True):
            self.update_text_area_pixel_swap_areas(valid_rectangles)
        
        self.swap_pixel_areas = valid_rectangles


    
    # a rectangle looks like this f"[ [{id}],[{x},{y}],[{width},{height}],[{areas_ids}],[{rgb_func_id}], [{movement_id}, {resize_id}] ] " (all elements in the rectangle must be integers exept for `areas_ids` which must be a list of integers)
    def get_rectangles_inside_canvas(self, canvas_width: int, canvas_height: int, rectangles: list):   
        
        valid_rectangles = []
        for i in range(0, len(rectangles)):
                        
            rectangle = rectangles[i]
            position_rectangle = rectangle[1]
            size_rectangle = rectangle[2]
            
            x_rectangle = position_rectangle[0]
            y_rectangle = position_rectangle[1]
            width_rectangle = size_rectangle[0]
            height_rectangle = size_rectangle[1]

            if(x_rectangle + width_rectangle <= canvas_width or y_rectangle + height_rectangle <= canvas_height):
                valid_rectangles.append(rectangle)
                

        return valid_rectangles
       
    #the rectangles which are passed to the method must be valid
    def update_text_area_pixel_swap_areas(self, rectangles: list):
        
        text = str(rectangles)
        text = text[1:len(text)-1]#remove the first and last bracket of the whole expression
        text = f"{text},"#add a comma at the end so the string format of all rectangle pairs is the same
        
        #<make area ids appear in `||` instead of `[]`
        text = text.replace("[[", "[ |")
        indexes_for_replacement = []
        index = 0
        
        while(True):
            
            id_start_index = text.find("|", index)
            if(id_start_index == -1):
                break

            id_end_index = text.find("]", id_start_index)
            if(id_end_index == -1):
                break

            indexes_for_replacement.append(id_end_index)
            index = id_end_index
        
        chars = list(text)
        for i in indexes_for_replacement:
            chars[i] = "|"
        
        text = "".join(chars)
        #make area ids appear in `||` instead of `[]`>

        text = text.replace("]],","] ],\n") #adding some spaces and new lines for readability      

        self.form_window.text_area_swap_pixel_areas.setText(text)    
    

    def get_swaped_areas(self):
       
        rgb_formulas_str = self.get_text_area_rgb_functions_formatted_text()
        if(check_rgb_formulas_format_for_pixel_areas(rgb_formulas_for_pixel_areas=rgb_formulas_str)== False):
            return []
        
        #the dictionary has rgb formula id (type int) as a key and a dictinary for value; the inner dictionaries have an rgb channels (values `r`,`g`,`b`) for keys and rgb formulas (represented as strings) for values
        rgb_formulas_dict = self.get_dictionary_of_rgb_formulas(rgb_formulas_for_pixel_areas = rgb_formulas_str)

        self.update_canvas(update_text=True)# populates `self.swap_pixel_areas` with the valid swap pixel areas
        
        self.create_pixel_area_objects(rgb_formulas_for_pixel_areas_dict=rgb_formulas_dict)#initializes `self.pixel_area_objects` using `self.swap_pixel_areas`

        return self.pixel_area_objects
    
    #creates a dictonary which has rgb formula id (type int) as a key and a dictinary for value; the inner dictionaries have an rgb channels (values `r`,`g`,`b`) for keys and rgb formulas (represented as strings) for values
    #the input parameter `rgb_formulas_for_pixel_areas` must be in a valid format before calling the function
    def get_dictionary_of_rgb_formulas(self, rgb_formulas_for_pixel_areas):

        rgb_formulas_pixel_area_start_index = 0
        rgb_formulas_pixel_area_end_index = 0
        index = 0
        rgb_formulas_pixel_areas_dict = {}
        
        while(rgb_formulas_pixel_area_end_index < len(rgb_formulas_for_pixel_areas)-1):

            rgb_formulas_pixel_area_start_index = rgb_formulas_for_pixel_areas.find("{", rgb_formulas_pixel_area_end_index)
            rgb_formulas_pixel_area_end_index = rgb_formulas_for_pixel_areas.find("}", rgb_formulas_pixel_area_start_index)

            rgb_formulas_current_pixel_area = rgb_formulas_for_pixel_areas[rgb_formulas_pixel_area_start_index+1: rgb_formulas_pixel_area_end_index]
            (rgb_formula_id, rgb_formulas_dict) = self.get_rgb_formulas_for_current_pixel_area(rgb_formulas_for_pixel_area = rgb_formulas_current_pixel_area, index = index)
            rgb_formulas_pixel_areas_dict[rgb_formula_id] = rgb_formulas_dict
        
        return rgb_formulas_pixel_areas_dict


    def get_rgb_formulas_for_current_pixel_area(self, rgb_formulas_for_pixel_area: str, index):   
                
        rgb_formula_id_index_start = rgb_formulas_for_pixel_area.find("|", 0)
        rgb_formula_id_index_end = rgb_formulas_for_pixel_area.find("|", rgb_formula_id_index_start+1)

        rgb_formula_id = rgb_formulas_for_pixel_area[rgb_formula_id_index_start+1:rgb_formula_id_index_end]
            
        rgb_channel_index = 0
        rgb_formula_start_index = 0
        rgb_formula_end_index = 0
        rgb_channels = ["r", "g", "b"]
        rgb_formulas = {}

        while (rgb_channel_index < 3):

            rgb_formula_start_index = rgb_formulas_for_pixel_area.find("[", rgb_formula_end_index)
            rgb_formula_end_index = get_closing_square_bracket(text=rgb_formulas_for_pixel_area,start_index=rgb_formula_start_index)#rgb_formulas_for_pixel_area.find("]", rgb_formula_start_index)
           
            rgb_formula = rgb_formulas_for_pixel_area[rgb_formula_start_index+1:rgb_formula_end_index]
            rgb_formulas[rgb_channels[rgb_channel_index]] = rgb_formula
            
            rgb_channel_index+=1

        return (int(rgb_formula_id), rgb_formulas)
    
    #`rgb_formulas_for_pixel_areas_dict` must be a dictonary which has rgb formula id (type int) for a key and a dictinary for value; the inner dictionaries must have an rgb channels (values `r`,`g`,`b`) for keys and rgb formulas (represented as strings) for values
    #this function is creating objects of type `Pixel_area` and appends to the list `self.pixel_area_objects`
    def create_pixel_area_objects(self, rgb_formulas_for_pixel_areas_dict:dict):
        
        rgb_formulas_existing_ids = rgb_formulas_for_pixel_areas_dict.keys()
        self.pixel_area_objects = []

        red_func = None
        green_func = None
        blue_func = None

        #`self.swap_pixel_areas` is a list which contains rectangles; a rectangle looks like this f"[ [{id}],[{x},{y}],[{width},{height}],[{areas_ids}],[{rgb_func_id}], [{movement_id}, {resize_id}] ] "
        for swap_pixel_area in self.swap_pixel_areas:
            
            id = swap_pixel_area[0][0]
            x = swap_pixel_area[1][0]
            y = swap_pixel_area[1][1]
            width = swap_pixel_area[2][0]
            height = swap_pixel_area[2][1]
            pixel_areas_ids = swap_pixel_area[3]
            
            rgb_function_id = swap_pixel_area[4][0]

            if(rgb_function_id in rgb_formulas_existing_ids):

                red_func = rgb_formulas_for_pixel_areas_dict[rgb_function_id]["r"]
                green_func = rgb_formulas_for_pixel_areas_dict[rgb_function_id]["g"]
                blue_func = rgb_formulas_for_pixel_areas_dict[rgb_function_id]["b"]
            else:
                red_func = "r"
                green_func = "g"
                blue_func = "b"
            
            rgb_function_object = RGB_formula_class(red_func= red_func, green_func=green_func, blue_func=blue_func, use_pixel_areas = True)
            rgb_function_str = rgb_function_object.rgb_function_str
            rgb_function_lambda = rgb_function_object.rgb_function
            pixel_area_object = Pixel_area(id = id, x = x, y = y, width= width, height= height, pixel_areas_ids=pixel_areas_ids, rgb_function_str=rgb_function_str, rgb_function_lambda = rgb_function_lambda)

            self.pixel_area_objects.append(pixel_area_object)

"""