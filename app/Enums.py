from enum import Enum


#<helper enum elements

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




class Enum__range(Enum):

    min = 0
    max = 1

#helper enum elements>

#<enum elements for "rgb formulas"
class Enum_rgb_formulas_parameters(Enum):

    id = 0
    r = 1
    g = 2
    b = 3

class Functions_for__Enum__rgb_formulas_parameters():
    def get_rgb_formulas_parameter_value_separator(self)->str:
        return "->"

    def get_rgb_formulas_parameters_separator(self)->str:
        return ";"

#elements for "rgb formulas">

#<enum elements for "rgb channles"

class Enum__rgb_channels(Enum):

    r = 0
    g = 1
    b = 2

#enum elements for "rgb channles">


#<enum elements for "image pad modes"

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

class Functions_for__Enum__image_pad_modes():
    def get_image_pad_modes_as_strings(self)  -> list[str]:
        
        elements = [
            Enum__image_pad_modes.constant.name, 
            Enum__image_pad_modes.edge.name, 
            Enum__image_pad_modes.linear_ramp.name, 
            
            Enum__image_pad_modes.maximum.name, 
            Enum__image_pad_modes.mean.name, 
            Enum__image_pad_modes.median.name, 
            Enum__image_pad_modes.minimum.name, 
            
            Enum__image_pad_modes.reflect.name, 
            Enum__image_pad_modes.symmetric.name, 
            Enum__image_pad_modes.wrap.name
        ]
        
        return elements

    def get_image_pad_modes_as_string(self, num:int, out_of_range_behaviour:Enum__behaviour_get_enums_as_string_when_number_out_of_range = Enum__behaviour_get_enums_as_string_when_number_out_of_range.modulo) -> str:
        
        elements = self.get_image_pad_modes_as_strings()
        output = get_Enum_as_string(elements=elements, num=num, out_of_range_behaviour=out_of_range_behaviour)
        return output

#enum elements for "image pad modes">

#<enum elements for "brackets"

class Enum__brackets(Enum):

    round = 0
    square = 1
    curly = 2

#enum elements for "brackets">


class Enum_order(Enum):

    ascending = 0
    descending = 1
    random = 2

    