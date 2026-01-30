
import Window_canvas, Z_Window_Canvas_swap_pixel_values, Z_Window_Form_swap_pixel_values
from PyQt5.QtCore import Qt

import ast

from Number_format_checker import check_for_positive_int_format, check_numbers_from_string, check_str_format_for_lists_of_lists_of_ints
from Z_RGB_formula_checker import check_rgb_formulas_format_for_pixel_areas, get_closing_square_bracket

from RGB_formula_class import RGB_formula_class
from Z_Pixel_area_class import Pixel_area

class Swap_pixel_values_controller: 
    
    def __init__(self):
        canvas_swap_pixel_values = Z_Window_Canvas_swap_pixel_values.DrawingWidget()
        self.canvas_window = Window_canvas.CanvasWindow(canvas = canvas_swap_pixel_values)
        self.form_window = Z_Window_Form_swap_pixel_values.FormWindow_SwapPixelValues()
                
        self.form_window.button_update_canvas.clicked.connect(lambda: self.update_canvas(False))
        self.form_window.button_update_canvas_and_text_area.clicked.connect(lambda: self.update_canvas(True))
        self.form_window.button_clear_canvas.clicked.connect(self.clear_canvas)

        self.form_window.button_add_rgb_formula.clicked.connect(self.add_rgb_function)
        self.form_window.button_apply_brush_width_changes.clicked.connect(lambda _, change_width=True: self.change_brush_size_parameters(change_width))
        self.form_window.button_apply_brush_height_changes.clicked.connect(lambda _, change_width=False: self.change_brush_size_parameters(change_width))
        self.form_window.button_set_brush_size.clicked.connect(self.set_brush_size)
        
        self.canvas_window.canvas.mousePressed.connect(self.canvas_clicked)  
        
        self.swap_pixel_areas = []#the list contains rectangles; a rectangle looks like this f"[ [{id}],[{x},{y}],[{width},{height}],[{areas_ids}],[{rgb_func_id}], [{movement_id}, {resize_id}] ] "       
        """
        self.rgb_formulas_strings = {}#this is a dictionary which has numbers (ids) for keys and dictionaries for values; the inner dictionaries contain the RGB channels with their RGB functions represented as strings
        self.rgb_formulas_strings[0] = {"r":"r", "g":"g", "b":"b"}#this is the default RGB function id `0` with it's default RGB function which is represented by inner dictionary which has RGB channels for keys and channles' functions for values
        
        self.default_rgb_lambda_formula = RGB_formula_class(use_pixel_areas = True).rgb_function
        self.rgb_formulas_lambda_funcs = {}#this is a dictionary which has numbers (ids) for keys and RGB fommulas (represented as lamda functions) for values
        
        self.rgb_funcs_str = ""
        """

        self.inner_lists_elements_count = [1, 2, 2, 0, 1, 2]#defines the required number of int values inside the most inner lists (the value zero means that the inner list can take any number of int values)

        self.area_id = 0

        self.pixel_area_objects = []#the list contains objects of type `Pixel_area`



    #<code for showing windows
    def show_form_window(self):
        self.form_window.show()
    
    def show_canvas_window(self):
        self.canvas_window.show()
    #code for showing windows>





    #<code for manipulating the canvas
    def clear_canvas(self):
        self.canvas_window.canvas.clear()

    def delete_insert_rectangles_to_canvas(self, rectangles: list):
        
        self.clear_canvas()

        for rectangle in rectangles:

            position = rectangle[1]
            size = rectangle[2]
            
            x = position[0]
            y = position[1]
            width = size[0]
            height = size[1]

            self.canvas_window.canvas.insert_rectangle(x = x, y = y, width=width, height=height)

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

    def get_text_area_swap_pixel_areas_formatted_text_for_validation(self):
        text = self.form_window.text_area_swap_pixel_areas.toPlainText()#gets the text in the text area
        text = text[0:-1].replace(" ","").replace("\n", "").replace("[|", "[[").replace("|", "]")#replaces `|` with `[` or `]`; removes the spaces, the new lines and the last symbol which is a comma
        return text

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
            x, y, width, height = self.canvas_window.canvas.left_mouse_button_pressed(x = x, y = y)

            #get a proper value for the id of the drawn area
            swap_pixel_areas_from_text_area = self.get_text_area_swap_pixel_areas_formatted_text()
            swap_pixel_area_id = self.get_first_unused_id(text = swap_pixel_areas_from_text_area, id_separator="|", id_max_digits=6)
            if(swap_pixel_area_id == -1):
                print("error: the maximum number of areas was reached")
                return

            #get data which will be inserted in the text area for pixel swap values and the text area for rgb functions
            self.area_id = str(swap_pixel_area_id)
            area_ids = self.form_window.text_box_area_ids.text().replace(" ", "")
            rgb_function_id = self.form_window.text_box_rgb_formula_id.text()
            movement_id = self.form_window.text_box_movement_id.text()
            resize_id = self.form_window.text_box_resize_id.text()

            #get proper value for the rgb, movement and resize ids
            rgb_function_id = self.get_proper_element_id(rgb_function_id, "0", "rgb", "which means no RGB function will be applied to the area")
            movement_id = self.get_proper_element_id(movement_id, "0", "movement", "which means no movement will be applied to the area")
            resize_id = self.get_proper_element_id(resize_id, "0", "resize", "which means no resizement will be applied to the area")

            #get proper value for the areas ids
            if(area_ids == ""):
                area_ids = "0" 
            are_areas_ids_in_correct_format = check_numbers_from_string(txt_value=area_ids,separator=",", search_for_floats=False, search_for_positives_only=True)
            if( are_areas_ids_in_correct_format == False): 
                area_ids = "0"  
                print("warning: since the ids of the areas' ids were in wrong format (only numbers and commas are allowed), the value `0`(which means the RGB function will use for input parameters the rgb values of the current area ) will be used instead")
            

            #< append the coordinates of the drawn rectangle to the text area
            #text_coordinates = f"[ #id#[{id}], #x, y#[{x}, {y}], #width, height#[{width}, {height}], #area ids#[{area_ids}], #RGB function id#[{rgb_function_id}], #move and resize ids#[{movement_id}{resize_id}] ]"
            text_coordinates = f"[ |{self.area_id}|, [{x}, {y}], [{width}, {height}], [{area_ids.replace(",",", ")}], [{rgb_function_id}], [{movement_id}, {resize_id}] ],"
            self.form_window.text_area_swap_pixel_areas.append(text_coordinates)
    

    def get_proper_element_id(self, element_id:str, default_id:str, element:str = "", default_value_description_in_error_message:str = ""):
        if(element_id == ""):
            element_id = "0" 
        if(check_for_positive_int_format(element_id) == False): 
            element_id = "0" 
            print(f"warning: since the {element} id was in wrong format (only numbers are allowed), the value `{default_id}`({default_value_description_in_error_message}) will be used instead")
                    
        return element_id
    #code for working with the text inside the text area containing the information for the pixel swap areas>

    
    
    

    
    #explores the text inside the provided text; selects all valid ids; determines the first number which is not used as an id in the text (allowed ids should be in this range 1-999_999)
    def get_first_unused_id(self, text: str, id_separator: str, id_max_digits:int):#each element which is inside 2 `id_separator` values will be considered as an id; only ids which are positive integer will be considered as valid (not valid ids are ignored)
        
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





    #<code for working with the text inside the text area containing the information for the rgb formulas

    def get_text_area_rgb_functions_formatted_text(self):
        rgb_funcs_str = self.form_window.text_area_rgb_formulas.toPlainText()
        rgb_funcs_str = rgb_funcs_str.replace(" ", "").replace("\n", "")
        return rgb_funcs_str
    
    def add_rgb_function(self):       
        
        rgb_function_from_text_area = self.get_text_area_rgb_functions_formatted_text()
        rgb_function_id = self.get_first_unused_id(text = rgb_function_from_text_area, id_separator="|", id_max_digits=6)
        if(rgb_function_id == -1):
            print("error: the maximum number of RGB formulas was reached")
            return
        
        self.form_window.rgb_elements.change_RGB_formula()

        rgb_formulas_str = f"|{rgb_function_id}|  r->[ {self.form_window.rgb_elements.red_func} ]  g->[ {self.form_window.rgb_elements.green_func} ]  b->[ {self.form_window.rgb_elements.blue_func} ]"
        rgb_formulas_str = "{ " + rgb_formulas_str + " }\n"

        self.form_window.text_area_rgb_formulas.append(rgb_formulas_str)


    

    #code for working with the text inside the text area containing the information for the rgb formulas>
    
    



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

                