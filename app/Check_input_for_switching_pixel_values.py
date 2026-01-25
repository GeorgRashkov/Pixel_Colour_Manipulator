from RGB_formula_checker import check_RGB_formula_format, is_RGB_formula_compatible_with_dxcam
from Number_format_checker import check_for_positive_int_format


#< this code ckecks strings and makes sure they have a format similar to this one (spaces and new lines are not valid but are presented in the example for readability)
"""
"
[   [ [0, 79, 85], [0, 0, 0] ],   [ [293, 292, 85], [0, 0, 0] ]   ],
[   [ [203, 44, 175], [0, 0, 0] ],   [ [0, 203, 175], [0, 0, 0] ]   ],
[   [ [0, 0, 200], [0, 0, 0] ],   [ [146, 136, 200], [0, 0, 0] ]   ],
"
"""

def is_switch_pixel_text_valid(text: str):    
    
    index = 0
    opening_brackets_count = 3
    current_row_array_index = 0
    row_arrays_count = 6

    dimension_format_error_message = "error: dimensions were in wrong format or their count was not acceptable"
    inner_content_error_message = "error: the inner elements were in wrong format or their count was not acceptable"
    
    is_last_processed_row_complete = False

    while(index<len(text)):

        is_last_processed_row_complete = False
        
        if(index+opening_brackets_count >= len(text)-1):
            return dimension_format_error_message
        
        elif(text[index:index+opening_brackets_count]=="["*opening_brackets_count):#this is the beginning of the current line
            index+=opening_brackets_count
            opening_bracket_index = index - 1 
            
            while(text[index]!="]"):
                index+=1
                if(index>=len(text)-1):
                    return dimension_format_error_message
            
            closing_bracket_index = index

            if(closing_bracket_index - opening_bracket_index < 2):#if the symbols inside the inner brackets is less than 2 then the format is wrong for sure
                return inner_content_error_message
            
            content = text[opening_bracket_index+1: closing_bracket_index]
            is_content_correct = check_for_positive_int_format(txt_value=content) if (current_row_array_index == row_arrays_count//2-1 or current_row_array_index == row_arrays_count - 1) else is_inner_content_correct(text=content)
            
            if( is_content_correct == False):
                return inner_content_error_message
            
            if(current_row_array_index == row_arrays_count//2 -1):
                closing_bracket_index +=1
            elif(current_row_array_index == row_arrays_count -1):
                closing_bracket_index +=2

            if(closing_bracket_index < len(text)-1):#if the closing bracket is located before the final symbol in the `text` execute the code
                if(text[closing_bracket_index+1] == ","):
                    index = closing_bracket_index+2
                else:
                    return dimension_format_error_message
            else:
                return dimension_format_error_message

            if(
                (current_row_array_index == row_arrays_count//2 and text[closing_bracket_index] != "]") or
                (current_row_array_index == row_arrays_count and (text[closing_bracket_index] != "]" or text[closing_bracket_index-1] != "]") )
               ):
                return dimension_format_error_message

            current_row_array_index+=1

            if(current_row_array_index>=row_arrays_count):#if this executes it means all elements of the current row were checked
                current_row_array_index = 0
            
            
            if(current_row_array_index==0):
                opening_brackets_count = 3
                is_last_processed_row_complete = True
            elif(current_row_array_index == row_arrays_count//2):
                opening_brackets_count = 2
            else:
                opening_brackets_count = 1
                

        else:
            return dimension_format_error_message
    
    
    if(is_last_processed_row_complete == False):
        return dimension_format_error_message

    return ""#the format was correct, which is why it returns no error messages


#this function checks the most inner content
def is_inner_content_correct(text: str):#checks wether the input contains only numbers and commas (the commas must be exactly 3)

    allowed_nums = ["0", "1","2","3","4","5","6","7","8","9"]
    commas_count = 0
    required_commas_count = 2

    if(text[0] not in allowed_nums  or text[-1] not in allowed_nums):
        return False
    
    if(check_text_for_leading_zeros_and_missing_content(text=text, start_index=0) == False):
        return False
    
    for i in range(1,len(text)-1):
        
        if(text[i] not in allowed_nums and text[i]!=","):
            return False

        if(text[i]=="," and text[i+1]==","):
            return False
        
        if(text[i]==","):
            commas_count+=1
            
            if(commas_count > required_commas_count):
                return False
            
            if(check_text_for_leading_zeros_and_missing_content(text=text, start_index=i+1)== False):
                return False
    
    if(commas_count != required_commas_count):
        return False

    return True


def check_text_for_leading_zeros_and_missing_content(text: str, start_index:int):
    
    if( text == "" or start_index >= len(text) ):
        return False

    if (text[start_index] == "0"):
        
        if(start_index+1 == len(text)):
            return True
       
        if(text[start_index+1]!=","):
            return False
    
    return True



# this code ckecks strings and makes sure they have a format similar to this one (spaces and new lines are not valid but are presented in the example for readability)> 
"""
"
[   [ [0, 79, 85], [0, 0, 0] ],   [ [293, 292, 85], [0, 0, 0] ]   ],
[   [ [203, 44, 175], [0, 0, 0] ],   [ [0, 203, 175], [0, 0, 0] ]   ],
[   [ [0, 0, 200], [0, 0, 0] ],   [ [146, 136, 200], [0, 0, 0] ]   ],
"
"""


# each element in `rectangle_pairs` must be a list of two rectangles
# a rectangle looks like this f"[ [{x}, {y}, {size}], [{int(use_red)}, {int(use_green)}, {int(use_blue)}] ]" (all elements in the rectangle must be integers)
def get_wrong_rectangle_pair_indexes(canvas_width: int, canvas_height: int, rectangle_pairs: list, rgb_channel_allowed_values: list):   
    
    invalid_rectangle_pairs_indexes = []

    for i in range(0, len(rectangle_pairs)):
        
        for j in range(0, len(rectangle_pairs[i])):
            
            rectangle = rectangle_pairs[i][j]
            coordinates_rectangle = rectangle[0]
            rgb_values_rectangle = rectangle[1]

            x_rectangle = coordinates_rectangle[0]
            y_rectangle = coordinates_rectangle[1]
            size_rectangle = coordinates_rectangle[2]

            if(x_rectangle + size_rectangle > canvas_width or 
               y_rectangle + size_rectangle > canvas_height):
                invalid_rectangle_pairs_indexes.append(i)
            
            for rgb_value in rgb_values_rectangle:
                if(rgb_value not in rgb_channel_allowed_values):
                    invalid_rectangle_pairs_indexes.append(i)
            
            if(j==0):
                second_rectangle = rectangle_pairs[i][1]
                size_second_rectangle = second_rectangle[0][2]
                if(size_second_rectangle!=size_rectangle):
                    invalid_rectangle_pairs_indexes.append(i)
    
    return invalid_rectangle_pairs_indexes

            











#<this code checks rgb formulas

#this function is responsible for getting the valid rgb functions; if the string format in an RGB channel formula is wrong or if it is not compatible with dxcam the function will use the default RGB channel formula
def get_valid_rgb_function(rgb_function_dict: dict):#`rgb_function_dict` is a dictionary which is supposed to have `r`,`g`,`b` for keys and 3 strings for values where each string is supposed to be a formula for one of the RGB channels

    is_red_channel_formula_correct = check_RGB_formula_format(rgb_formula=rgb_function_dict["r"], channel="red")
    is_blue_channel_formula_correct = check_RGB_formula_format(rgb_formula=rgb_function_dict["g"], channel="green")
    is_green_channel_formula_correct = check_RGB_formula_format(rgb_formula=rgb_function_dict["b"], channel="blue")
            
    if(is_red_channel_formula_correct == True):
        is_red_channel_formula_correct = is_RGB_formula_compatible_with_dxcam(rgb_formula= rgb_function_dict["r"].replace('^','**').replace('=','=='), channel="red")
            
    if(is_green_channel_formula_correct == True):
        is_green_channel_formula_correct = is_RGB_formula_compatible_with_dxcam(rgb_formula=rgb_function_dict["g"].replace('^','**').replace('=','=='), channel="green")
            
    if(is_blue_channel_formula_correct == True):
        is_blue_channel_formula_correct = is_RGB_formula_compatible_with_dxcam(rgb_formula=rgb_function_dict["b"].replace('^','**').replace('=','=='), channel="blue")

    rgb_formula_dict = {}
    rgb_formula_dict["r"] = rgb_function_dict["r"] if is_red_channel_formula_correct==True else "r"
    rgb_formula_dict["g"] =green_formula = rgb_function_dict["g"] if is_green_channel_formula_correct==True else "g"
    rgb_formula_dict["b"] =blue_formula = rgb_function_dict["b"] if is_blue_channel_formula_correct==True else "b"

    # the returned result is dictionary with 3 elements where the keys are the RGB channles while the values are their RGB functions
    return rgb_formula_dict 
    
    




def get_valid_rgb_functions(rgb_funcs_str: str):

    rgb_funcs_str = rgb_funcs_str.replace(" ", "").replace("\n","")
    rgb_funcs_dict = {}
    rgb_funcs_dict[0] = {"r":"r", "g":"g", "b":"b"}#this is the default RGB function id `0` with it's default RGB function which is represented by inner dictionary which has RGB channels for keys and channles' functions for values

    # this is list which contains strings which are supposed to look like this `{|2| r->[r] g->[g] b->[b]}`
    # everyhting in `||` should be an RGB function id while everything in `[]` should be an RGB function where the first `[]` is for the red channel, the second `[]`` is for the green channel and the third `[]`  is for the blue channel
    #symbols which 
    rgb_functions_rows = get_rgb_functions_list_of_rows(rgb_funcs_str = rgb_funcs_str)
    
    for i in range(0, len(rgb_functions_rows)):
        
        rgb_function_id = get_rgb_functions_id(rgb_function = rgb_functions_rows[i])

        #if the current row has invalid value for the RGB function id (the id must be a positive number above zero) the RGB function will not be used;
        if(rgb_function_id == 0):
            continue
            
        #this is string which is supposed to have one formula for each RGB channel
        rgb_functions_dict = get_rgb_functions_dictionary_of_channels(rgb_funcs_str=rgb_functions_rows[i])
        rgb_function = get_valid_rgb_function(rgb_function_dict=rgb_functions_dict)
        
        rgb_funcs_dict[rgb_function_id] = rgb_function

    return rgb_funcs_dict #returns a dictionary which has numbers (ids) for keys and dictionaries for values; the inner dictionaries contain the RGB channels with their RGB functions



def get_rgb_functions_list_of_rows(rgb_funcs_str: str):

    rgb_formulas_row = []
    row_start_symbol = "{"
    row_end_symbol = "}"
    start_index = 0
    min_symbols_per_row = 10

    while True:# this code is trying to find the colour functions for each RGB channel; everything iside square brackets `[]` (except other square brackets) is consider as part of RGB formula
        
        opening_bracket_index = rgb_funcs_str.find(row_start_symbol, start_index)
        closing_bracket_index = rgb_funcs_str.find(row_end_symbol, opening_bracket_index+1)

        start_index = opening_bracket_index + 1
        

        if ( opening_bracket_index == -1 or closing_bracket_index == -1):
            break
            
        if(closing_bracket_index - opening_bracket_index < min_symbols_per_row ):
            continue

        rgb_formulas_row.append(rgb_funcs_str[opening_bracket_index+1:closing_bracket_index])

    
    return rgb_formulas_row


# the function is searching for the first occurrence of two of those symbols "|" and if they don't exist or if the value inside them is invalid RGB function id, the function will return `0`
def get_rgb_functions_id(rgb_function:str):

    separator = "|"
    
    separator_opening_index = rgb_function.find(separator, 0)
    separator_closing_index = rgb_function.find(separator, separator_opening_index+1)

    #this code executes when there are 0 separators or 1 separator without anything after it
    if(separator_opening_index == -1 or  separator_closing_index == -1 ):
        return 0
    
    #this code executes when there are no symbols between the separators
    if(separator_closing_index - separator_opening_index < 2):
        return 0

    rgb_functions_id = rgb_function[separator_opening_index+1:separator_closing_index]
    if(check_for_positive_int_format(txt_value = rgb_functions_id, is_zero_allowed=False) == False):
        return 0
    
    return int(rgb_functions_id)

    

def get_rgb_functions_dictionary_of_channels(rgb_funcs_str: str):
    
    dict_keys = ["r", "g", "b"]

    rgb_functions_dict = {}
    rgb_function_start_symbol = "["
    rgb_function_end_symbol = "]"
    start_index = 0
    counter = 0

    while True:# this code is trying to find the colour functions for each RGB channel; everything inside square brackets `[]` (except other square brackets) is consider as part of RGB formula
        
        opening_bracket_index = rgb_funcs_str.find(rgb_function_start_symbol, start_index)
        closing_bracket_index = rgb_funcs_str.find(rgb_function_end_symbol, opening_bracket_index+1)

        start_index = opening_bracket_index + 1
        counter+=1

        if ( opening_bracket_index == -1 or closing_bracket_index == -1 or counter > len(dict_keys) ):

            if( opening_bracket_index == len(rgb_funcs_str) -1):
                print("warning: RGB formulas after the third (blue) RGB formula are ignored if there are no separators (`|`, `;`) between them")

            counter -=1
            break 

        rgb_functions_dict[dict_keys[counter-1]] = rgb_funcs_str[opening_bracket_index+1:closing_bracket_index]

    
    while(counter < len(dict_keys)):#this code will assign the default value for each channel which didn't manage to get a user defined RGB formula
        rgb_functions_dict[dict_keys[counter]] = dict_keys[counter]
        counter+=1
    
    return rgb_functions_dict
        


            
#this code checks rgb formulas>      