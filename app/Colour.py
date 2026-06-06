import numpy as np

class Colour:
    def __init__(self, r:np.uint8, g:np.uint8, b:np.uint8):
        
        self.r = r
        self.g = g
        self.b = b
    
    def copy(self):

        self_copy = Colour(r=self.r, g=self.g, b=self.b)
        return self_copy

def does_colour_exist(colours:list[Colour], colour:Colour):

    for current_colour in colours:
        if(colour.r == current_colour.r and colour.g == current_colour.g and colour.b == current_colour.b):
            return True
    
    return False



class Colour_range:
    def __init__(self, r_from:np.uint8, g_from:np.uint8, b_from:np.uint8, r_to:np.uint8, g_to:np.uint8, b_to:np.uint8):
        
        self.r_from = r_from
        self.g_from = g_from
        self.b_from = b_from

        self.r_to = r_to
        self.g_to = g_to
        self.b_to = b_to
    
    def copy(self):

        self_copy = Colour_range(r_from=self.r_from, g_from=self.g_from, b_from=self.b_from, r_to=self.r_to, g_to=self.g_to, b_to=self.b_to)
        return self_copy


def does_colour_range_exist(colour_ranges:list[Colour_range], colour_range:Colour_range):

    for current_colour_range in colour_ranges:
        if(colour_range.r_from == current_colour_range.r_from and colour_range.r_to == current_colour_range.r_to and
           colour_range.g_from == current_colour_range.g_from and colour_range.g_to == current_colour_range.g_to and
           colour_range.b_from == current_colour_range.b_from and colour_range.b_to == current_colour_range.b_to):
            return True
    
    return False