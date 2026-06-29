from enum import Enum

class Enum__rgb_channels(Enum):

    r = 0
    g = 1
    b = 2



class Enum__convolutional_kernel_parameters(Enum):
    
    height = 0
    width = 1

    hole_height = 2
    hole_width = 3
    vertical_hole_frequency = 4
    horizontal_hole_frequency = 5
    hole_content = 6

    min_kernel_value = 7
    max_kernel_value = 8

    recreate_kernel_frequency = 9
    
    frequency__update_dynamic_variables__using_kernel_value = 10
    frequency__update_dynamic_variables__using_kernel_hole_row = 11
    frequency__update_dynamic_variables_using_kernel_hole_column = 12
    frequency__update_dynamic_variables__using_rgb_channel = 13



class Bracket(Enum):

    round = 0
    square = 1
    curly = 2

    