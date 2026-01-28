
import Window_canvas, Canvas_switch_pixel_values, Window_switch_pixel_values
from PyQt5.QtCore import Qt

import ast
import numpy as np

import Check_input_for_switching_pixel_values

from Number_format_checker import check_for_positive_int_format

import RGB_formula_class

class Windows_for_switching_pixel_values: 
    
    def __init__(self):
        canvas_switch_pixel_values = Canvas_switch_pixel_values.DrawingWidget()
        self.canvas_window = Window_canvas.CanvasWindow(canvas = canvas_switch_pixel_values)
        self.form_window = Window_switch_pixel_values.FormWindow_SwichPixelValies()
                
        self.form_window.button_update_canvas.clicked.connect(lambda: self.update_canvas(False))
        self.form_window.button_update_canvas_and_text_area.clicked.connect(lambda: self.update_canvas(True))
        self.form_window.button_clear_canvas.clicked.connect(self.clear_canvas)

        self.form_window.button_add_rgb_formula.clicked.connect(self.add_rgb_function)
        self.form_window.button_apply_brush_size_changes.clicked.connect(self.change_brush_size_parameters)
        
        self.canvas_window.canvas.mousePressed.connect(self.canvas_clicked)  
        
        self.swap_pixel_areas = []      
        
        self.rgb_formulas_strings = {}#this is a dictionary which has numbers (ids) for keys and dictionaries for values; the inner dictionaries contain the RGB channels with their RGB functions represented as strings
        self.rgb_formulas_strings[0] = {"r":"r", "g":"g", "b":"b"}#this is the default RGB function id `0` with it's default RGB function which is represented by inner dictionary which has RGB channels for keys and channles' functions for values
        
        self.default_rgb_lambda_formula = RGB_formula_class.RGB_formula_class().rgb_function
        self.rgb_formulas_lambda_funcs = {}#this is a dictionary which has numbers (ids) for keys and RGB fommulas (represented as lamda functions) for values
        
        self.rgb_funcs_str = ""
    
    def clear_canvas(self):
        self.canvas_window.canvas.clear()

    #when called this function will remove everything from the canvas and will put in there rectangles based on the coordinates written in the text area 
    def update_canvas(self, update_text):
        
        self.swap_pixel_areas = []

        text = self.form_window.text_area_swap_pixel_areas.toPlainText()#gets the text in the text area
        text = text.replace(" ","").replace("\n", "")
        error_message = Check_input_for_switching_pixel_values.is_switch_pixel_text_valid(text=text)
        
        if(error_message!=""):
            print(error_message)
            return
        
        text = text[0:-1]#remove the last symbol which is a comma
        text = f"[{text}]"#add square brackets at the beginning and the end (it is necessary for converting the text into a list)
        rectangle_pairs = ast.literal_eval(text)#converting the text into a list
        print(rectangle_pairs)
        
        canvas_width = self.canvas_window.canvas.width()
        canvas_height = self.canvas_window.canvas.height()
        wrong_rectangle_pairs_indexes = Check_input_for_switching_pixel_values.get_wrong_rectangle_pair_indexes(canvas_width = canvas_width, canvas_height = canvas_height, rectangle_pairs = rectangle_pairs, rgb_channel_allowed_values = [0, 1, 2])

        
        correct_rectangle_pairs = [v for i, v in enumerate(rectangle_pairs) if i not in wrong_rectangle_pairs_indexes]
        self.delete_insert_rectangles_to_canvas(correct_rectangle_pairs)
        
        if(update_text == True):
            self.update_text_area_pixel_swap_areas(correct_rectangle_pairs)
        
        self.swap_pixel_areas = correct_rectangle_pairs
        
    
    def delete_insert_rectangles_to_canvas(self, rectangle_pairs: list):
        self.canvas_window.canvas.clear()
        self.canvas_window.canvas.insert_rectangle_pairs(rectangle_pairs=rectangle_pairs)
    
        
    def update_text_area_pixel_swap_areas(self, rectangle_pairs: list):
        
        text = str(rectangle_pairs)
        text = text[1:len(text)-1]#remove the first and last bracket of the whole expression
        text = f"{text},"#add a comma at the end so the string format of all rectangle pairs is the same
        
        text = text.replace("[[[", "[   [ [").replace("]]],","] ]   ],\n").replace("[[", "[ [").replace("]]", "] ]").replace(", [ [", ",   [ [") #adding some spaces and new lines for readability      

        self.form_window.text_area_swap_pixel_areas.setText(text)    


    def show_form_window(self):
        self.form_window.show()
    
    def show_canvas_window(self):
        self.canvas_window.show()
    
    #draws the rectangle and gets its coordinates
    def canvas_clicked(self, pos, button):
        
        if button == Qt.LeftButton:
            
            x = pos.x()
            y = pos.y()
            
            use_red = self.form_window.r_check_box.isChecked() 
            use_green = self.form_window.g_check_box.isChecked()
            use_blue = self.form_window.b_check_box.isChecked()          
            
            #draws the rectangle and get's its coordinates
            x, y, size = self.canvas_window.canvas.left_mouse_button_pressed(x = x, y = y, r_channel=use_red, g_channel=use_green, b_channel=use_blue)

            #get rgb function id
            rgb_function_id = self.form_window.text_box_rgb_formula_id.text()
            if(check_for_positive_int_format(rgb_function_id) == False or rgb_function_id is None or rgb_function_id==""): 
                rgb_function_id = "0" 
        
            #< append the coordinates of the drawn rectangle to the text area
            #text_coordinates = f"[ [{x}, {y}, {size}], [{int(use_red)}, {int(use_green)}, {int(use_blue)}] ]"
            text_coordinates = f"[ [{x}, {y}, {size}], [{int(use_red)}, {int(use_green)}, {int(use_blue)}], [{int(rgb_function_id)}] ]"
            
            if(self.canvas_window.canvas.is_first_half == True):
                text_coordinates = f"[   {text_coordinates},   "
                self.form_window.text_area_swap_pixel_areas.append(text_coordinates)
            else:
                text_coordinates =  f"{text_coordinates}   ],"
                self.form_window.text_area_swap_pixel_areas.append_on_same_line(text_coordinates)               
            #append the coordinates of the drawn rectangle to the text area >

            self.canvas_window.canvas.is_first_half = not self.canvas_window.canvas.is_first_half    


    def get_swaped_areas(self):
        self.update_canvas(update_text=True)# assures that only valid swap areas are passed

        if(len(self.swap_pixel_areas) == 0):#avoids empty list errors which will happen when `swap_pixel_areas` is empty and is used with `np.array(self.swap_pixel_areas[:,:,0,0])`
            return np.array([]), {}

        #the areas will be tranformed into a numpy array; this is what a rectangle looks like `f"[ [{x}, {y}, {size}], [{int(use_red)}, {int(use_green)}, {int(use_blue)}], [{int(rgb_function_id)}] ]"`
        
        self.make_swap_pixel_areas_compatible_for_numpy()
        swap_pixel_areas = np.array(self.swap_pixel_areas)   


        # assures that only valid rgb functions will be used
        self.update_rgb_functions()# selects the proper string representations of the RGB functions
        self.transform_rgb_formulas_to_lambda_functions(rgb_formulas_needed_ids=swap_pixel_areas[:,:,2,0].reshape(-1))# creates lambda functions by using the string representations of the RGB functions (only the RGB functions strings with the needed ids will be transoformed to lambad functions)
        swap_pixel_areas = self.append_proper_rgb_formulas_ids(swap_pixel_areas)# the result may remain unchanged (only the RGB functions ids may change by being set to `0` if not presented in the keys of the dictionary containing the RGB lambda functions)
                    
        print(self.rgb_formulas_lambda_funcs)

        return swap_pixel_areas, self.rgb_formulas_lambda_funcs
    
    #in testing state
    def make_swap_pixel_areas_compatible_for_numpy(self):
        
        for i in range(0,len(self.swap_pixel_areas)):#cycle through all rectangle pairs
            for j in range(0, len(self.swap_pixel_areas[i])):# cycle through all (the two) rectangles in the rectangle pair
                
                #adding dummy values to the thrid dimentation (which contains the id of the colour function) to make it's size match the size of the other most inner arrays
                self.swap_pixel_areas[i][j][2].append(0)
                self.swap_pixel_areas[i][j][2].append(0)







    def get_text_area_rgb_functions_formatted_text(self):
        rgb_funcs_str = self.form_window.text_area_rgb_formulas.toPlainText()
        rgb_funcs_str = rgb_funcs_str.replace(" ", "").replace("\n", "")
        return rgb_funcs_str

    def add_rgb_function(self):       
        
        rgb_function_id = self.get_first_unused_rgb_function_index()
        if(rgb_function_id == -1):
            print("error: the maximum number of RGB formulas was reached")
            return
        
        self.form_window.rgb_elements.change_RGB_formula()

        rgb_formulas_str = f"|{rgb_function_id}|  r->[ {self.form_window.rgb_elements.red_func} ]  g->[ {self.form_window.rgb_elements.green_func} ]  b->[ {self.form_window.rgb_elements.blue_func} ]"
        rgb_formulas_str = "{ " + rgb_formulas_str + " }\n"

        self.form_window.text_area_rgb_formulas.append(rgb_formulas_str)

    #explores the text inside the rgb function's text area, selects all valid ids, determines the first number which is not used as an id for rgb function
    def get_first_unused_rgb_function_index(self):
        
        rgb_funcs_str = self.get_text_area_rgb_functions_formatted_text()
        index_separator = "|"
        start_index = 0
        rgb_funcs_ids = []

        #this code get's the valid ids written in the text area
        while True:
            
            stard_index_current_id = rgb_funcs_str.find(index_separator, start_index)
            start_index = stard_index_current_id + 1

            if stard_index_current_id == -1:
                break
            
            end_index_current_id = rgb_funcs_str.find(index_separator, stard_index_current_id+1)
            if(end_index_current_id == -1):
                break
            
            if(end_index_current_id - stard_index_current_id < 2):
                continue

            end_index_current_id = end_index_current_id if end_index_current_id - stard_index_current_id <= 7 else  stard_index_current_id + 5 #allowed ids for RGB functions should be in this range 1-999_999
            current_id = rgb_funcs_str[stard_index_current_id+1:end_index_current_id]

            is_id_correct = check_for_positive_int_format(txt_value = current_id, is_zero_allowed=False)
            if(is_id_correct == True):
                rgb_funcs_ids.append(int(current_id))

        #this code get's the valid ids written in the text area

        #finds the first unused index
        for i in range (1, 1_000_000):
            if(i not in rgb_funcs_ids):
                return i
        
        return -1 #this code should never be reached unless the user defines over 999_999 valid indexes



    def update_rgb_functions(self):
        
        rgb_funcs_str = self.get_text_area_rgb_functions_formatted_text()
        
        if(self.rgb_funcs_str != rgb_funcs_str):
            rgb_funcs_dictonary = Check_input_for_switching_pixel_values.get_valid_rgb_functions(rgb_funcs_str)
            self.rgb_formulas_strings = rgb_funcs_dictonary
            self.rgb_funcs_str = rgb_funcs_str
    
    
    def transform_rgb_formulas_to_lambda_functions(self, rgb_formulas_needed_ids):
        
        existing_rgb_fomulas_ids = self.rgb_formulas_strings.keys()

        #clears the values from the dictionary with RGB lambda functions and adds a default RGB function id with default RGB lambda function
        self.rgb_formulas_lambda_funcs = {}
        self.rgb_formulas_lambda_funcs[0] = self.default_rgb_lambda_formula

        selected_ids = []

        for needed_id in rgb_formulas_needed_ids:
            if( (needed_id in existing_rgb_fomulas_ids) and (needed_id not in selected_ids)):
                
                rgb_formula_dict = self.rgb_formulas_strings[needed_id]
                rgb_formula_object = RGB_formula_class.RGB_formula_class(red_func = rgb_formula_dict["r"], green_func = rgb_formula_dict["g"], blue_func = rgb_formula_dict["b"])

                self.rgb_formulas_lambda_funcs[needed_id] = rgb_formula_object.rgb_function
                selected_ids.append(needed_id)
        
        
    def append_proper_rgb_formulas_ids(self, swap_pixel_areas: np.array):
               
        rgb_formulas_ids = self.rgb_formulas_lambda_funcs.keys()
        
        for i in range (0, swap_pixel_areas.shape[0]):
            for j in range (0, swap_pixel_areas.shape[1]):
                
                rgb_formula_id = swap_pixel_areas[i,j,2,0]
                if(rgb_formula_id not in rgb_formulas_ids):
                    swap_pixel_areas[i,j,2,0] = 0
        
        return swap_pixel_areas


    


    def change_brush_size_parameters(self):

        #take the brush size parameters
        brush_size_min_value = self.form_window.textBox_brush_size_min_value.text()
        brush_size_max_value = self.form_window.textBox_brush_size_max_value.text()
        brush_size_delta = self.form_window.textBox_brush_size_delta.text()

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

        self.canvas_window.canvas.set_brush_size_arguments(brush_min_size = brush_min_size, brush_max_size=brush_max_size, brush_delta=brush_delta) 

                
                
                

        
        

            