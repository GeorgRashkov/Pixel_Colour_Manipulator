
import Window_canvas, Canvas_switch_pixel_values, Window_switch_pixel_values
from PyQt5.QtCore import Qt

import ast

import Check_input_for_switching_pixel_values

class Windows_for_switching_pixel_values: 
    
    def __init__(self):
        canvas_switch_pixel_values = Canvas_switch_pixel_values.DrawingWidget()
        self.canvas_window = Window_canvas.CanvasWindow(canvas = canvas_switch_pixel_values)
        self.form_window = Window_switch_pixel_values.FormWindow_SwichPixelValies()
                
        self.form_window.button_update_canvas.clicked.connect(lambda: self.update_canvas(False))
        self.form_window.button_update_canvas_and_text_area.clicked.connect(lambda: self.update_canvas(True))
        self.form_window.button_clear_canvas.clicked.connect(self.clear_canvas)
        
        self.canvas_window.canvas.mousePressed.connect(self.canvas_clicked)        
    
    def clear_canvas(self):
        self.canvas_window.canvas.clear()

    #when called this function will remove everything from the canvas and will put in there rectangles based on the coordinates written in the text area 
    def update_canvas(self, update_text):
        
        text = self.form_window.text_area.toPlainText()#gets the text in the text area
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
        wrong_rectangle_pair_indexes = Check_input_for_switching_pixel_values.get_wrong_rectangle_pair_indexes(canvas_width = canvas_width, canvas_height = canvas_height, rectangle_pairs = rectangle_pairs, rgb_channel_allowed_values = [0,1])

        
        correct_rectangle_pairs = [v for i, v in enumerate(rectangle_pairs) if i not in wrong_rectangle_pair_indexes]
        self.delete_insert_rectangles_to_canvas(correct_rectangle_pairs)
        
        if(update_text == True):
            self.update_text_area(correct_rectangle_pairs)
        
    
    def delete_insert_rectangles_to_canvas(self, rectangle_pairs: list):
        self.canvas_window.canvas.clear()
        self.canvas_window.canvas.insert_rectangle_pairs(rectangle_pairs=rectangle_pairs)
    
        
    def update_text_area(self, rectangle_pairs: list):
        
        text = str(rectangle_pairs)
        text = text[1:len(text)-1]#remove the first and last bracket of the whole expression
        text = f"{text},"#add a comma at the end so the string format of all rectangle pairs is the same
        
        text = text.replace("[[[", "[   [ [").replace("]]],","] ]   ],\n").replace("[[", "[ [").replace("]]", "] ]").replace(", [ [", ",   [ [") #adding some spaces and new lines for readability      

        self.form_window.text_area.setText(text)    


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

            #< append the coordinates of the drawn rectangle to the text area
            #text = f"{[[x, y, size], [int(use_red), int(use_green), int(use_blue)]]}"
            text = f"[ [{x}, {y}, {size}], [{int(use_red)}, {int(use_green)}, {int(use_blue)}] ]"

            if(self.canvas_window.canvas.is_first_half == True):
                text = f"[   {text},   "
                self.form_window.text_area.append(text)
            else:
                text =  f"{text}   ],"
                self.form_window.text_area.append_on_same_line(text)               
            #append the coordinates of the drawn rectangle to the text area >

            self.canvas_window.canvas.is_first_half = not self.canvas_window.canvas.is_first_half            
            
            