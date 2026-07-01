from enum import Enum

class Enum__behaviour_get_enums_as_string_when_number_out_of_range(Enum):

    modulo = 0
    min = 1
    max = 2
    min_max = 3
    none = 4

#warning: this function must be used only by "get enum as string" functions
#warning: this function works correctly only when the elements in the chosen enum are increasing with 1 and when the first element is equal to 0
def get_Enum_as_string(elements:list[str], num:int, out_of_range_behaviour:Enum__behaviour_get_enums_as_string_when_number_out_of_range) -> str:

    elements_count = len(elements)

    if(num >= 0 and num< elements_count):
        pass

    elif(out_of_range_behaviour == Enum__behaviour_get_enums_as_string_when_number_out_of_range.modulo):
        num = num%elements_count
    
    elif(out_of_range_behaviour == Enum__behaviour_get_enums_as_string_when_number_out_of_range.min):
        num = 0
    
    elif(out_of_range_behaviour == Enum__behaviour_get_enums_as_string_when_number_out_of_range.max):
        num = elements_count-1
    
    elif(out_of_range_behaviour == Enum__behaviour_get_enums_as_string_when_number_out_of_range.min_max):
        num = 0 if num<0 else elements_count-1
    
    elif(out_of_range_behaviour == Enum__behaviour_get_enums_as_string_when_number_out_of_range.none):
        return None
    
    return elements[num]





class Enum__rgb_channels(Enum):

    r = 0
    g = 1
    b = 2

def get_Enum__rgb_channels__as_string(num:int, out_of_range_behaviour:Enum__behaviour_get_enums_as_string_when_number_out_of_range = Enum__behaviour_get_enums_as_string_when_number_out_of_range.modulo) -> str:
    
    elements = ["r", "g", "b"]
    output = get_Enum_as_string(elements=elements, num=num, out_of_range_behaviour=out_of_range_behaviour)
    return output





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




class Enum__image_pad_modes(Enum):
    
    constant=0
    edge=1
    linear_ramp=2
    maximum=3
    mean=4
    median=5
    minimum=6
    reflect=7
    symmetric=8
    wrap=9

def get_Enum__image_pad_modes__as_string(num:int, out_of_range_behaviour:Enum__behaviour_get_enums_as_string_when_number_out_of_range = Enum__behaviour_get_enums_as_string_when_number_out_of_range.modulo) -> str:
    
    elements = ["constant", "edge", "linear_ramp", "maximum", "mean", "median", "minimum", "reflect", "symmetric", "wrap"]
    output = get_Enum_as_string(elements=elements, num=num, out_of_range_behaviour=out_of_range_behaviour)
    return output




class Bracket(Enum):

    round = 0
    square = 1
    curly = 2

    