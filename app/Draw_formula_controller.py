from PyQt5.QtGui import QColor

from Window_Form_draw_formula import Window_Form_draw_formula
from Draw_formula import Draw_formula
from Draw_formula_pyplot import Draw_formula_pyplot_countour, Draw_formula_pyplot_plot, Draw_formula_pyplot_scatter
from Draw_formulas_collector import Draw_formulas_collector
from Draw_formula_checker import check_draw_formula_expressions_format
from Draw_formula_type import Draw_formula_resize_type
from Number_format_checker import check_for_positive_int_format, check_for_int_format, check_for_float_format, check_for_positive_float_format

class Draw_formula_controller: 
    
    def __init__(self):
        
        self.form_window_draw_formula = Window_Form_draw_formula()

        self.form_window_draw_formula.button_add_draw_formula.clicked.connect(self.add_draw_formula)
        self.form_window_draw_formula.button_remove_draw_formula.clicked.connect(self.remove_draw_formula)
        self.form_window_draw_formula.radioButtonGroup_draw_type.buttonToggled.connect(self.enable_only_elements_of_specific_draw_type)
        self.form_window_draw_formula.radioButtonGroup_resize_type.buttonToggled.connect(self.alter_resize_type)
        
        self.draw_formulas_collector:Draw_formulas_collector = Draw_formulas_collector()

        self.rgb_max_value = 255
        self.line_width_max_value = 99
        self.drawing_id_max_value = 999
        self.levels_min_value = -999
        self.levels_max_value = 999
        self.x_y_values_count_max_value = 999_999
        self.x_y_values_count_min_value = 2

        self.enable_only_elements_of_specific_draw_type()
        self.alter_resize_type()



    #< functions for adding a draw formula
    
    def add_draw_formula(self):

        if(self.check_drawing_id() == False or self.check_x_y_values() == False or
           self.check_rgb_values() == False or self.check_line_width() == False):
            return

        drawing_id = int(self.form_window_draw_formula.textBox_drawing_id.text())
       
        
        x_start_value= int(self.form_window_draw_formula.textBox_x_start_value.text().replace(" ", "").replace("\n",""))
        x_end_value=int(self.form_window_draw_formula.textBox_x_end_value.text().replace(" ", "").replace("\n","")) 
        x_values_count=int(self.form_window_draw_formula.textBox_x_values_count.text().replace(" ", "").replace("\n",""))
        y_start_value=int(self.form_window_draw_formula.textBox_y_start_value.text().replace(" ", "").replace("\n","")) 
        y_end_value=int(self.form_window_draw_formula.textBox_y_end_value.text().replace(" ", "").replace("\n",""))
        y_values_count=int(self.form_window_draw_formula.textBox_y_values_count.text().replace(" ", "").replace("\n",""))
        
        rgb_values = self.get_rgb_values()
        line_colour=QColor(int(rgb_values["r"]), int(rgb_values["g"]), int(rgb_values["b"]))
        line_width=int(self.form_window_draw_formula.textBox_line_width.text().replace(" ", "").replace("\n",""))
        
        is_formula_added = False

        if(self.form_window_draw_formula.radioButton_contour.isChecked() == True):
            is_formula_added = self.add_draw_formula__contour(drawing_id = drawing_id, x_start_value=x_start_value, x_end_value=x_end_value, x_values_count=x_values_count, y_start_value=y_start_value, y_end_value=y_end_value, y_values_count=y_values_count, line_colour=line_colour, line_width=line_width)
        elif(self.form_window_draw_formula.radioButton_plot.isChecked() == True):
            is_formula_added = self.add_draw_formula__plot(drawing_id = drawing_id, x_start_value=x_start_value, x_end_value=x_end_value, x_values_count=x_values_count, y_start_value=y_start_value, y_end_value=y_end_value, y_values_count=y_values_count, line_colour=line_colour, line_width=line_width)
        elif(self.form_window_draw_formula.radioButton_scatter.isChecked() == True):
            is_formula_added = self.add_draw_formula__scatter(drawing_id = drawing_id, x_start_value=x_start_value, x_end_value=x_end_value, x_values_count=x_values_count, y_start_value=y_start_value, y_end_value=y_end_value, y_values_count=y_values_count, line_colour=line_colour, line_width=line_width)
        else:
            raise Exception("invalid draw formula type")
        
        if(is_formula_added == True):
            self.display_draw_formulas_as_text()
        


    def add_draw_formula__contour(self, drawing_id:int,  x_start_value:int, x_end_value:int, x_values_count:int, y_start_value:int, y_end_value:int, y_values_count:int,line_colour: QColor, line_width:int) -> bool:
        
        if(self.check_Z_expressions() == False or self.check_levels() == False):
            return False

        expression_Z = self.form_window_draw_formula.textBox_Z.text().replace(" ", "").replace("\n","")
        sub_expressions = self.get_sub_expressions_from_user_input()
        draw_formula_Z = Draw_formula(main_expression=expression_Z, sub_expressions=sub_expressions)
        levels = int(self.form_window_draw_formula.textBox_levels.text().replace(" ", "").replace("\n",""))
        
        draw_formula_pyplot = Draw_formula_pyplot_countour(
                x_start_value=x_start_value, x_end_value=x_end_value, x_values_count=x_values_count,
                y_start_value=y_start_value, y_end_value=y_end_value, y_values_count=y_values_count,
                line_colour=line_colour, line_width=line_width,
                Z=draw_formula_Z, levels=levels)
        
        is_formula_added = self.draw_formulas_collector.add_draw_formula(drawing_id=drawing_id, draw_formula_pyplot=draw_formula_pyplot)
        return is_formula_added


    def add_draw_formula__plot(self, drawing_id:int,  x_start_value:int, x_end_value:int, x_values_count:int, y_start_value:int, y_end_value:int, y_values_count:int,line_colour: QColor, line_width:int) -> bool:
         
        if(x_values_count != y_values_count):
            print("error: x values count must be equal to y values count when the draw type is plot")
            return False

        if(self.check_X_Y_expressions() == False):
            return False
        

        expression_X = self.form_window_draw_formula.textBox_X.text().replace(" ", "").replace("\n","")
        expression_Y = self.form_window_draw_formula.textBox_Y.text().replace(" ", "").replace("\n","")
        sub_expressions = self.get_sub_expressions_from_user_input()
        draw_formula_X = Draw_formula(main_expression=expression_X, sub_expressions=sub_expressions)
        draw_formula_Y = Draw_formula(main_expression=expression_Y, sub_expressions=sub_expressions)
        
        draw_formula_pyplot = Draw_formula_pyplot_plot(
                x_start_value=x_start_value, x_end_value=x_end_value, x_values_count=x_values_count,
                y_start_value=y_start_value, y_end_value=y_end_value, y_values_count=y_values_count,
                line_colour=line_colour, line_width=line_width,
                X=draw_formula_X, Y=draw_formula_Y)
        
        is_formula_added = self.draw_formulas_collector.add_draw_formula(drawing_id=drawing_id, draw_formula_pyplot=draw_formula_pyplot)
        return is_formula_added


    def add_draw_formula__scatter(self, drawing_id:int,  x_start_value:int, x_end_value:int, x_values_count:int, y_start_value:int, y_end_value:int, y_values_count:int,line_colour: QColor, line_width:int) -> bool:
         
        if(x_values_count != y_values_count):
            print("error: x values count must be equal to y values count when the draw type is scatter")
            return False
        
        if(self.check_X_Y_expressions() == False):
            return False

        expression_X = self.form_window_draw_formula.textBox_X.text().replace(" ", "").replace("\n","")
        expression_Y = self.form_window_draw_formula.textBox_Y.text().replace(" ", "").replace("\n","")
        sub_expressions = self.get_sub_expressions_from_user_input()
        draw_formula_X = Draw_formula(main_expression=expression_X, sub_expressions=sub_expressions)
        draw_formula_Y = Draw_formula(main_expression=expression_Y, sub_expressions=sub_expressions)
        
        draw_formula_pyplot = Draw_formula_pyplot_scatter(
                x_start_value=x_start_value, x_end_value=x_end_value, x_values_count=x_values_count,
                y_start_value=y_start_value, y_end_value=y_end_value, y_values_count=y_values_count,
                line_colour=line_colour, line_width=line_width,
                X=draw_formula_X, Y=draw_formula_Y)
        
        is_formula_added = self.draw_formulas_collector.add_draw_formula(drawing_id=drawing_id, draw_formula_pyplot=draw_formula_pyplot)
        return is_formula_added
         

    # functions for adding a draw formula>
    

    def remove_draw_formula(self):
         
        if(self.check_drawing_id() == True):
            drawing_id = int(self.form_window_draw_formula.textBox_drawing_id.text())
            is_formula_removed = self.draw_formulas_collector.remove_draw_formula(drawing_id=drawing_id)
            if(is_formula_removed == True):
                self.display_draw_formulas_as_text()
    

              

    #<functions for checking user input
    
    def check_x_y_values(self) -> bool:
        
        x_start_value = self.form_window_draw_formula.textBox_x_start_value.text()
        if(x_start_value == "" or check_for_float_format(x_start_value) == False):
            print("error: x start value must be a float number")
            return False
        
        x_end_value = self.form_window_draw_formula.textBox_x_end_value.text()
        if(x_end_value == "" or check_for_float_format(x_end_value) == False):
            print("error: x end value must be a float number")
            return False

        x_values_count = self.form_window_draw_formula.textBox_x_values_count.text()
        if(x_values_count == "" or check_for_positive_float_format(x_values_count) == False):
            print("error: x values count must be a positive float number")
            return False
         
        x_values_count_int = int(x_values_count)
        if(x_values_count_int < self.x_y_values_count_min_value or x_values_count_int > self.x_y_values_count_max_value):
            print(f"error: x values count must be in range {self.x_y_values_count_min_value}-{self.x_y_values_count_max_value}")
            return False
        
        
        
        y_start_value = self.form_window_draw_formula.textBox_y_start_value.text()
        if(y_start_value == "" or check_for_float_format(y_start_value) == False):
            print("error: y start value must be a float number")
            return False
        
        y_end_value = self.form_window_draw_formula.textBox_y_end_value.text()
        if(y_end_value == "" or check_for_float_format(y_end_value) == False):
            print("error: y end value must be a float number")
            return False

        y_values_count = self.form_window_draw_formula.textBox_y_values_count.text()
        if(y_values_count == "" or check_for_positive_float_format(y_values_count) == False):
            print("error: y values count must be a positive float number")
            return False
        
        y_values_count_int = int(y_values_count)
        if(y_values_count_int < self.x_y_values_count_min_value or y_values_count_int > self.x_y_values_count_max_value):
            print(f"error: y values count must be in range {self.x_y_values_count_min_value}-{self.x_y_values_count_max_value}")
            return False
        
        return True
    
    


    def check_X_Y_expressions(self) -> bool:
        
        sub_expresssions = self.get_sub_expressions_from_user_input()

        expression_X = self.form_window_draw_formula.textBox_X.text().replace(" ", "").replace("\n","")
        is_expression_X_valid = check_draw_formula_expressions_format(main_expression=expression_X, sub_expressions=sub_expresssions)
        if(is_expression_X_valid == False):
            return False

        expression_Y = self.form_window_draw_formula.textBox_Y.text().replace(" ", "").replace("\n","")
        is_expression_Y_valid = check_draw_formula_expressions_format(main_expression=expression_Y, sub_expressions=sub_expresssions)
        if(is_expression_Y_valid == False):
            return False
        
        return True

    def check_Z_expressions(self) -> bool:

        sub_expresssions = self.get_sub_expressions_from_user_input()

        expression_Z = self.form_window_draw_formula.textBox_Z.text().replace(" ", "").replace("\n","")
        is_expression_Z_valid = check_draw_formula_expressions_format(main_expression=expression_Z, sub_expressions=sub_expresssions)
        if(is_expression_Z_valid == False):
            return False
        
        return True


    def check_rgb_values(self) -> bool:

        rgb_str_values = self.get_rgb_values()

        for rgb_str_value in rgb_str_values.values():
            
            if(rgb_str_value=="" or check_for_positive_int_format(rgb_str_value) == False):
                print(f"error: the rgb values must be integers in range 0-{self.rgb_max_value}")
                return False
            
            rgb_value = int(rgb_str_value)
            if(rgb_value > self.rgb_max_value):
                print(f"error: the rgb values must be integers in range 0-{self.rgb_max_value}")
                return False
            
        return True
        

            
    def check_line_width(self) -> bool:
        
        line_width_txt = self.form_window_draw_formula.textBox_line_width.text().replace(" ", "").replace("\n","")
        
        if(line_width_txt == "" or check_for_positive_int_format(line_width_txt) == False):
                print(f"error: the line width must be integer in range 0-{self.line_width_max_value}")
                return False
        
        line_width = int(line_width_txt)
        if(line_width > self.line_width_max_value):
                print(f"error: the line width must be integer in range 0-{self.line_width_max_value}")
                return False

        return True
    
    def check_levels(self) -> bool:
        
        levels_txt = self.form_window_draw_formula.textBox_levels.text().replace(" ", "").replace("\n","")
        
        if(levels_txt == "" or check_for_int_format(levels_txt) == False):
                print(f"error: the levels must be integer in range {self.levels_min_value}-{self.levels_max_value}")
                return False
        
        levels = int(levels_txt)
        if(levels < self.levels_min_value or levels > self.levels_max_value):
                print(f"error: the levels must be integer in range {self.levels_min_value}-{self.levels_max_value}")
                return False

        return True

    def check_drawing_id(self) -> bool:
        
        drawing_id_txt = self.form_window_draw_formula.textBox_drawing_id.text().replace(" ", "").replace("\n","")
        
        if(drawing_id_txt=="" or check_for_positive_int_format(drawing_id_txt) == False):
                print(f"error: the drawing id must be integer in range 0-{self.drawing_id_max_value}")
                return False
        
        drawing_id = int(drawing_id_txt)
        if(drawing_id > self.drawing_id_max_value):
                print(f"error: the drawing id must be integer in range 0-{self.drawing_id_max_value}")
                return False

        return True

    #functions for checking user input>


    #<functions for getting user input

    def get_sub_expressions_from_user_input(self) -> list[str]:
        
        sub_expresssions_txt:str = self.form_window_draw_formula.textBox_sub_expressions.text().replace(" ", "").replace("\n","")
        sub_expresssions:list[str] = sub_expresssions_txt.split(";")
        sub_expresssions_without_empty_entries = []
        
        for sub_expresssion in sub_expresssions:
            if(sub_expresssion != ""):
                sub_expresssions_without_empty_entries.append(sub_expresssion)
                
        return sub_expresssions_without_empty_entries
    
    def get_rgb_values(self) -> dict[str,str]:

        red = self.form_window_draw_formula.textBox_red.text().replace(" ", "").replace("\n","")
        green = self.form_window_draw_formula.textBox_green.text().replace(" ", "").replace("\n","")
        blue = self.form_window_draw_formula.textBox_blue.text().replace(" ", "").replace("\n","")

        rgb_str_values = {"r":red, "g":green, "b":blue}
        return rgb_str_values

    #functions for getting user input>

    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def show_drawing(self, img):
        try:
            self.draw_formulas_collector.draw(img=img)
        except ZeroDivisionError:
            print("division by zero detected in draw formula")
    

    def display_draw_formulas_as_text(self):

        self.form_window_draw_formula.text_area.clear()
        self.form_window_draw_formula.text_area.setPlainText(self.to_string())


    def enable_only_elements_of_specific_draw_type(self):
        
        if(self.form_window_draw_formula.radioButton_contour.isChecked() == True):
            self.form_window_draw_formula.enable_only_contour_draw_elements()
        
        elif(self.form_window_draw_formula.radioButton_plot.isChecked() == True):
            self.form_window_draw_formula.enable_only_plot_draw_elements()
        
        elif(self.form_window_draw_formula.radioButton_scatter.isChecked() == True):
            self.form_window_draw_formula.enable_only_scatter_draw_elements()
        
        else:
            raise Exception("cannot enable draw elements of non existing draw type")
    
    def alter_resize_type(self):

        if(self.form_window_draw_formula.radioButton_equal.isChecked() == True):
            self.draw_formulas_collector.alter_draw_formula_resize_type(resize_type=Draw_formula_resize_type.equal)
        elif(self.form_window_draw_formula.radioButton_tight.isChecked() == True):
            self.draw_formulas_collector.alter_draw_formula_resize_type(resize_type=Draw_formula_resize_type.tight)
        
        else:
            raise Exception("cannot alter resize behaviour to non existing resize type")

    def to_string(self):
        return self.draw_formulas_collector.to_string()