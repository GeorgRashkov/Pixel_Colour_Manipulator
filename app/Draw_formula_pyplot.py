import numpy as np

from Draw_formula import Draw_formula
from Draw_formula_type import Draw_formula_draw_type
from PyQt5.QtGui import QColor

import matplotlib.pyplot as plt

class Draw_formula_pyplot:

    def __init__(self):
        pass

    def draw(self):
        pass

    def to_string(self):
        pass

        

class Draw_formula_pyplot_countour(Draw_formula_pyplot):
    
    def __init__(self,
                x_start_value:float, x_end_value:float, x_values_count:float,
                y_start_value:float, y_end_value:float, y_values_count:float,
                line_colour:QColor, line_width:int,
                Z:Draw_formula, levels:int
                ):
         
        self.x_start_value = x_start_value
        self.x_end_value = x_end_value
        self.x_values_count = x_values_count

        self.y_start_value = y_start_value
        self.y_end_value = y_end_value
        self.y_values_count = y_values_count

        self.draw_formula_type = Draw_formula_draw_type.Contour
        self.line_colour = line_colour
        self.line_width = line_width

        self.Z = Z
        self.levels = levels
    

    def draw(self):
        
        x = np.linspace(self.x_start_value, self.x_end_value, self.x_values_count)
        y = np.linspace(self.y_start_value, self.y_end_value, self.y_values_count)
        x, y = np.meshgrid(x, y)

        plt.contour(x, y, self.Z.draw_function(x,y), levels=[self.levels], colors=self.line_colour.name(), linewidths=self.line_width)
    

    def to_string(self):

        message = f"draw formula type: {self.draw_formula_type.name}\n"
        
        message += f"x| start:{self.x_start_value}; end{self.x_end_value}; count{self.x_values_count}\n"
        message += f"y| start:{self.y_start_value}; end{self.y_end_value}; count{self.y_values_count}\n"
        message += f"line| colour:[{self.line_colour.red()},{self.line_colour.green()},{self.line_colour.blue()}]; width{self.line_width}\n"

        message += f"Z: {self.Z.draw_function_str}\n"
        message += f"levels: {self.levels}\n"
        
        return message





class Draw_formula_pyplot_plot(Draw_formula_pyplot):
    
    def __init__(self,
                x_start_value:float, x_end_value:float, x_values_count:float,
                y_start_value:float, y_end_value:float, y_values_count:float,
                line_colour:QColor, line_width:int,
                X:Draw_formula, Y:Draw_formula,
                ):
        
        self.x_start_value = x_start_value
        self.x_end_value = x_end_value
        self.x_values_count = x_values_count

        self.y_start_value = y_start_value
        self.y_end_value = y_end_value
        self.y_values_count = y_values_count

        self.draw_formula_type = Draw_formula_draw_type.Plot
        self.line_colour = line_colour
        self.line_width = line_width

        self.X = X
        self.Y = Y
    

    def draw(self):
        
        x = np.linspace(self.x_start_value, self.x_end_value, self.x_values_count)
        y = np.linspace(self.y_start_value, self.y_end_value, self.y_values_count)
        
        plt.plot(self.X.draw_function(x,y), self.Y.draw_function(x,y), color=self.line_colour.name(), linewidth=self.line_width)
    

    def to_string(self):

        message = f"draw formula type: {self.draw_formula_type.name}\n"
        
        message += f"x| start:{self.x_start_value}; end{self.x_end_value}; count{self.x_values_count}\n"
        message += f"y| start:{self.y_start_value}; end{self.y_end_value}; count{self.y_values_count}\n"
        message += f"line| colour:[{self.line_colour.red()},{self.line_colour.green()},{self.line_colour.blue()}]; width{self.line_width}\n"

        message += f"X: {self.X.draw_function_str}\n"
        message += f"Y: {self.Y.draw_function_str}\n"
        
        return message



class Draw_formula_pyplot_scatter(Draw_formula_pyplot):
    
    def __init__(self,
                x_start_value:float, x_end_value:float, x_values_count:float,
                y_start_value:float, y_end_value:float, y_values_count:float,
                line_colour:QColor, line_width:int,
                X:Draw_formula, Y:Draw_formula,
                ):
        
        self.x_start_value = x_start_value
        self.x_end_value = x_end_value
        self.x_values_count = x_values_count

        self.y_start_value = y_start_value
        self.y_end_value = y_end_value
        self.y_values_count = y_values_count

        self.draw_formula_type = Draw_formula_draw_type.Scatter
        self.line_colour = line_colour
        self.line_width = line_width

        self.X = X
        self.Y = Y
    

    def draw(self):
        
        x = np.linspace(self.x_start_value, self.x_end_value, self.x_values_count)
        y = np.linspace(self.y_start_value, self.y_end_value, self.y_values_count)

        plt.scatter(self.X.draw_function(x,y), self.Y.draw_function(x,y), color=self.line_colour.name(), linewidth=self.line_width)
    

    def to_string(self):

        message = f"draw formula type: {self.draw_formula_type.name}\n"
        
        message += f"x| start:{self.x_start_value}; end{self.x_end_value}; count{self.x_values_count}\n"
        message += f"y| start:{self.y_start_value}; end{self.y_end_value}; count{self.y_values_count}\n"
        message += f"line| colour:[{self.line_colour.red()},{self.line_colour.green()},{self.line_colour.blue()}]; width{self.line_width}\n"

        message += f"X: {self.X.draw_function_str}\n"
        message += f"Y: {self.Y.draw_function_str}\n"
        
        return message
    




        
"""
class Draw_formula_pyplot:
    
    def __init__(self, draw_formula_type:Draw_formula_type,
                x_start_value:float, x_end_value:float, x_values_count:float,
                y_start_value:float, y_end_value:float, y_values_count:float,
                line_colour:QColor, line_width:int,
                Z:Draw_formula, levels:int
                ):
        
        if(draw_formula_type != Draw_formula_type.Contour):
            raise Exception("invalid draw formula type")
         
        self.x_start_value = x_start_value
        self.x_end_value = x_end_value
        self.x_values_count = x_values_count

        self.y_start_value = y_start_value
        self.y_end_value = y_end_value
        self.y_values_count = y_values_count

        self.draw_formula_type = draw_formula_type
        self.line_colour = line_colour
        self.line_width = line_width

        self.Z = Z
        self.levels = levels
    

    def __init__(self, draw_formula_type:Draw_formula_type,
                x_start_value:float, x_end_value:float, x_values_count:float,
                y_start_value:float, y_end_value:float, y_values_count:float,
                line_colour:QColor, line_width:int,
                X:Draw_formula, Y:Draw_formula,
                ):
        
        if(draw_formula_type != Draw_formula_type.Plot and draw_formula_type != Draw_formula_type.Scatter):
            raise Exception("invalid draw formula type")
        
        self.x_start_value = x_start_value
        self.x_end_value = x_end_value
        self.x_values_count = x_values_count

        self.y_start_value = y_start_value
        self.y_end_value = y_end_value
        self.y_values_count = y_values_count

        self.draw_formula_type = draw_formula_type
        self.line_colour = line_colour
        self.line_width = line_width

        self.X = X
        self.Y = Y
    
    #<draw functions

    #this function must be called from outside; the other draw functions must not be called from outside
    def draw(self):
        
        x = np.linspace(self.x_start_value, self.x_end_value, self.x_values_count)
        y = np.linspace(self.y_start_value, self.y_end_value, self.y_values_count)
        x, y = np.meshgrid(x, y)

        if(self.draw_formula_type == Draw_formula_type.Contour):
            self.contour(x=x, y=y)

        elif(self.draw_formula_type == Draw_formula_type.Plot):
            self.plot(x=x, y=y)
        
        elif(self.draw_formula_type == Draw_formula_type.Scatter):
            self.scatter(x=x, y=y)
        
    
    def contour(self, x, y):
        plt.contour(x, y, self.Z.draw_function(x,y), levels=[self.levels], colors=self.line_colour.name(), linewidths=self.line_width)

    def plot(self, x, y):
        plt.plot(self.X.draw_function(x,y), self.Y.draw_function(x,y), color=self.line_colour.name(), linewidth=self.line_width)

    def scatter(self, x, y):
        plt.scatter(self.X.draw_function(x,y), self.Y.draw_function(x,y), color=self.line_colour.name(), linewidth=self.line_width)
    
    #draw functions>

    def to_string(self):

        message = f"draw formula type: {self.draw_formula_type}\n"
        
        message += f"x| start:{self.x_start_value}; end{self.x_end_value}; count{self.x_values_count}\n"
        message += f"y| start:{self.y_start_value}; end{self.y_end_value}; count{self.y_values_count}\n"
        message += f"line| colour:[{self.line_colour.red()},{self.line_colour.green()},{self.line_colour.blue()}]; width{self.line_width}\n"

        if(self.draw_formula_type == Draw_formula_type.Contour):
            message += f"Z: {self.Z.draw_function_str}\n"
            message += f"levels: {self.levels}\n"
        else:
            message += f"X: {self.X.draw_function_str}\n"
            message += f"Y: {self.Y.draw_function_str}\n"
        
        return message
"""      