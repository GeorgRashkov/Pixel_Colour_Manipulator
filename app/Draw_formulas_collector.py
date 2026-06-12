import matplotlib.pyplot as plt
import numpy as np

from Draw_formula_pyplot import Draw_formula_pyplot
from Draw_formula_type import Draw_formula_resize_type

class Draw_formulas_collector: 
    
    def __init__(self):
        self.draw_formulas_pyplot:dict[int,Draw_formula_pyplot] = {}
        self.draw_formula_resize_type = Draw_formula_resize_type.equal
    

    def add_draw_formula(self, drawing_id:int, draw_formula_pyplot:Draw_formula_pyplot) -> bool:

        if(drawing_id in self.draw_formulas_pyplot.keys()):
            print("error: the drawing id is already used by other drawing")
            return False
        else:
            self.draw_formulas_pyplot[drawing_id] = draw_formula_pyplot
            return True
    

    def remove_draw_formula(self, drawing_id:int) -> bool:

        if(drawing_id not in self.draw_formulas_pyplot.keys()):
            print("error: the drawing id was not found")
            return False
        else:
            self.draw_formulas_pyplot.pop(drawing_id)
            return True
    
    def alter_draw_formula_resize_type(self, resize_type: Draw_formula_resize_type):
        self.draw_formula_resize_type = resize_type

    
    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def draw(self, img:np.ndarray[np.uint8]):

        for id in self.draw_formulas_pyplot.keys():
            self.draw_formulas_pyplot[id].draw(img=img)
        
        manager = plt.get_current_fig_manager()
        manager.toolbar.pan()

        plt.subplots_adjust(
            left=0,
            right=1,
            bottom=0,
            top=1
        )

        plt.axis(self.draw_formula_resize_type.name)
        plt.show()



    def to_string(self):

        message = ""
        for id in self.draw_formulas_pyplot.keys():
            message += f"\ndraw formula: {id}\n"
            message += self.draw_formulas_pyplot[id].to_string()
        
        return message



    