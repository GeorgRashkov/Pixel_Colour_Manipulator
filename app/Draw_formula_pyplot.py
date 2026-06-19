import numpy as np

from Draw_formula import Draw_formula
from Draw_formula_type import Draw_formula_draw_type
from PyQt5.QtGui import QColor

import matplotlib.pyplot as plt

class Draw_formula_pyplot:

    def __init__(self):
        pass
    
    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def draw(self, img:np.ndarray[np.uint8]):
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
    

    def draw(self, img:np.ndarray[np.uint8]):
        
        x = np.linspace(self.x_start_value, self.x_end_value, self.x_values_count)
        y = np.linspace(self.y_start_value, self.y_end_value, self.y_values_count)

        h = min(len(y),img.shape[0])
        w = min(len(x),img.shape[1])
        
        img_crop = np.zeros([len(y),len(x),3])
        img_crop[:h,:w] = img[:h,:w]
        r = img_crop[:,:,0]
        g = img_crop[:,:,1]
        b = img_crop[:,:,2]

        x, y = np.meshgrid(x, y)

        plt.contour(x, y, self.Z.draw_function(x,y,r,g,b), levels=[self.levels], colors=self.line_colour.name(), linewidths=self.line_width)
    

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
    

    def draw(self, img:np.ndarray[np.uint8]):
        
        x = np.linspace(self.x_start_value, self.x_end_value, self.x_values_count)
        y = np.linspace(self.y_start_value, self.y_end_value, self.y_values_count)

        h = min(len(y),img.shape[0])
        w = min(len(x),img.shape[1])
        
        img_crop = np.zeros([len(y),len(x),3])
        img_crop[:h,:w] = img[:h,:w]
        r = img_crop[:,:,0]
        g = img_crop[:,:,1]
        b = img_crop[:,:,2]

        plt.plot(self.X.draw_function(x,y,r,g,b), self.Y.draw_function(x,y,r,g,b), color=self.line_colour.name(), linewidth=self.line_width)
    

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
    

    def draw(self, img:np.ndarray[np.uint8]):
        
        x = np.linspace(self.x_start_value, self.x_end_value, self.x_values_count)
        y = np.linspace(self.y_start_value, self.y_end_value, self.y_values_count)

        h = min(len(y),img.shape[0])
        w = min(len(x),img.shape[1])
        
        img_crop = np.zeros([len(y),len(x),3])
        img_crop[:h,:w] = img[:h,:w]
        r = img_crop[:,:,0]
        g = img_crop[:,:,1]
        b = img_crop[:,:,2]

        plt.scatter(self.X.draw_function(x,y,r,g,b), self.Y.draw_function(x,y,r,g,b), color=self.line_colour.name(), linewidth=self.line_width)
    

    def to_string(self):

        message = f"draw formula type: {self.draw_formula_type.name}\n"
        
        message += f"x| start:{self.x_start_value}; end{self.x_end_value}; count{self.x_values_count}\n"
        message += f"y| start:{self.y_start_value}; end{self.y_end_value}; count{self.y_values_count}\n"
        message += f"line| colour:[{self.line_colour.red()},{self.line_colour.green()},{self.line_colour.blue()}]; width{self.line_width}\n"

        message += f"X: {self.X.draw_function_str}\n"
        message += f"Y: {self.Y.draw_function_str}\n"
        
        return message
    