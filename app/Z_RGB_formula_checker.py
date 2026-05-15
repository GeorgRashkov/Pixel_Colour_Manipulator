import numpy as np
from Number_format_checker import check_for_positive_int_format


class RGB_formula_validators:
    rgb_formula_valid_symbols = ['.','(',')','r','g','b','v','+','-','*','/','^','%','<','>','=','0','1','2','3','4','5','6','7','8','9']
    rgb_formula_valid_symbols_regex = "[.()rgbv+\\-*\\/^%<>=0123456789]"
    rgb_formula_valid_symbols_for_swap_areas_regex = "[.()rgbv+\\-*\\/^%<>=0123456789 \\[\\]]"
    rgb_default_formula_for_swap_areas = "r->[r] g->[g] b->[b]"

def check_RGB_formula_format(rgb_formula: str, channel: str,  use_areas: bool = False):
        
        #<allowed symbols collections
        allowed_RGB_chars = ['r','g','b', 'v']#`v` is not a rgb channel; it is a list containing int values
        allowed_operator_chars = ['+','-','*','/','^','%','<','>','=']
        allowed_num_chars = ['0','1','2','3','4','5','6','7','8','9']
        allowed_chars = ['.','(',')','r','g','b','v','+','-','*','/','^','%','<','>','=','0','1','2','3','4','5','6','7','8','9']
    
        if(rgb_formula == ''):
            return False
        
        is_format_correct = True

        #error messages
        wrong_format_message = f"error: the {channel} channel formula is in wrong format \n"
        invalid_symbol_message = lambda symbol: f"the symbol {symbol} is not allowed"
        invalid_placement_message = lambda symbol1, symbol2: f"the symbol {symbol1} cannot be placed before {symbol2}"
        square_brackets_not_closed_message = "error: square brackets were not closed"
        square_brackets_wrong_placement = f"error: openning square bracket cannot after anyting beside {allowed_RGB_chars}"
        area_index_message = f"error: the index inside the square brackets must be a positive number"


        #<first and last symbol check

        first_char = rgb_formula[0]
        last_char = rgb_formula[len(rgb_formula)-1]
        if(first_char=='.' or first_char==')' or first_char in allowed_operator_chars):
            is_format_correct = False
            wrong_format_message+=f"the symbol {first_char} cannot be placed at the beginning of the formula"
        elif(last_char=='.' or last_char=='(' or last_char in allowed_operator_chars):
            is_format_correct = False
            wrong_format_message+=f"the symbol {last_char} cannot be placed at the end of the formula"
        elif(rgb_formula.__contains__('r')==False and rgb_formula.__contains__('g')==False and rgb_formula.__contains__('b')==False):
            is_format_correct = False
            wrong_format_message+=f"error: no channels; you have to enter at least one RBG channel using 'r' or 'b' or 'g' "
        #first and last symbol check>

        #<cheking every symbol
        i = 1
        while(i < len(rgb_formula)):
            
            if(is_format_correct==False):
                break

            #checking for valid symbols
            if(rgb_formula[i-1] not in allowed_chars):
                wrong_format_message += invalid_symbol_message (rgb_formula[i-1])
                is_format_correct = False
                
            elif(rgb_formula[i] not in allowed_chars):
                
                if(rgb_formula[i] == "[" and use_areas == True):
                    if(rgb_formula[i-1] in allowed_RGB_chars):
                        closing_bracket_index = rgb_formula.find("]", i)

                        if(closing_bracket_index != -1):
                            if(check_for_positive_int_format(rgb_formula[i+1:closing_bracket_index]) == True):
                                i = closing_bracket_index
                                if(i < len(rgb_formula)-1):
                                    i += 1 
                                    if(rgb_formula[i] not in allowed_chars or rgb_formula[i] =='(' or rgb_formula[i]=='.' or rgb_formula[i] in allowed_RGB_chars or rgb_formula[i] in allowed_num_chars):
                                        wrong_format_message += invalid_placement_message(rgb_formula[i-1], rgb_formula[i])
                                        is_format_correct = False
                            else:
                                wrong_format_message+=area_index_message
                                is_format_correct = False
                        else:
                            wrong_format_message += square_brackets_not_closed_message
                            is_format_correct = False
                    else:
                        wrong_format_message += square_brackets_wrong_placement
                        is_format_correct = False
                else:
                    wrong_format_message += invalid_symbol_message (rgb_formula[i])
                    is_format_correct = False

            #executes only if the current and the previous symbols are currect
            else:
                               
                #numbers check
                if(rgb_formula[i-1] in allowed_num_chars):
                    if(rgb_formula[i]=='(' or rgb_formula[i] in allowed_RGB_chars):
                        wrong_format_message += invalid_placement_message(rgb_formula[i-1], rgb_formula[i])
                        is_format_correct = False
                                       
                #RGB channles check
                elif(rgb_formula[i-1] in allowed_RGB_chars):
                    if(rgb_formula[i] =='(' or rgb_formula[i]=='.' or rgb_formula[i] in allowed_RGB_chars or rgb_formula[i] in allowed_num_chars):
                        wrong_format_message += invalid_placement_message(rgb_formula[i-1], rgb_formula[i])
                        is_format_correct = False
                                           
                #operators check
                elif(rgb_formula[i-1] in allowed_operator_chars):
                    if(rgb_formula[i]==')' or rgb_formula[i]=='.' or rgb_formula[i] in allowed_operator_chars):
                        wrong_format_message += invalid_placement_message(rgb_formula[i-1], rgb_formula[i])
                        is_format_correct = False
                                        
                #openning bracket check
                elif(rgb_formula[i-1]=='('):
                    if(rgb_formula[i]==')' or rgb_formula[i]=='.' or rgb_formula[i] in allowed_operator_chars):
                        wrong_format_message += invalid_placement_message(rgb_formula[i-1], rgb_formula[i])
                        is_format_correct = False
                                            
                #closing bracket check
                elif(rgb_formula[i-1]==')'):
                    if(rgb_formula[i]=='(' or rgb_formula[i]=='.' or rgb_formula[i] in allowed_num_chars or rgb_formula[i] in allowed_RGB_chars):
                        wrong_format_message += invalid_placement_message(rgb_formula[i-1], rgb_formula[i])
                        is_format_correct = False
                                           
                #decimal point check
                elif(rgb_formula[i-1]=='.'):
                    if(rgb_formula[i]=='(' or rgb_formula[i]==')' or rgb_formula[i]=='.' or rgb_formula[i] in allowed_RGB_chars or rgb_formula[i] in allowed_operator_chars):
                        wrong_format_message += invalid_placement_message(rgb_formula[i-1], rgb_formula[i])
                        is_format_correct = False
            i +=1
        #cheking every symbol>
                                
        if(is_format_correct==False):
            print(wrong_format_message)
        
        wrong_format_message = check_RGB_formula_format_2(rgb_formula, allowed_num_chars)

        if(wrong_format_message!=""):
            print(wrong_format_message)
            is_format_correct = False

        return is_format_correct         
    
    #the function returns an error message; if the formula is in corret format the message will be an empty string
def check_RGB_formula_format_2(rgb_formula: str, allowed_num_chars):
        
        #<checking whether: the brackets are properly openned and closed
        counter = 0
        for i in range(0, len(rgb_formula)):
            
            if(rgb_formula[i]=="("):
                counter+=1
            elif(rgb_formula[i]==")"):
                counter-=1
            
            if(counter)<0:
                return "error: some brackets were not properly openned or closed"
        
        if(counter!=0):
            return "error: some brackets were not properly openned or closed"
        #checking whether: the brackets are properly openned and closed>

        #<checking whether: there are numbers containing more than 1 decimal point
        i=0
        while(i<len(rgb_formula)):
            
            if(rgb_formula[i]=="."):
                i+=1
    
                while(i<len(rgb_formula) and (rgb_formula[i] in allowed_num_chars or rgb_formula[i]==".")):
                    if(rgb_formula[i]=="."):
                        return "error: too many decimal points per number"
                    i+=1
                i-=1
            i+=1

        #checking whether: there are numbers containing more than 1 decimal point>

        if(len(rgb_formula)<3):
            return ""

        #<checking whether: there are numbers starting with a zero followed by another digit
        
        if(rgb_formula[0]=='0' and rgb_formula[1] in allowed_num_chars):
            return "error: wrong zeros format"

        last_index = len(rgb_formula)-1
        i=1
        while(i<last_index):
            
            #the code logic in the body of this if statement assures that the body will be executed only once per number; which means when `rgb_formula[i]=="0"` is `True` the "0" symbol will always be the first "0" symbol in the current number 
            if(rgb_formula[i]=="0"):
               
                if(rgb_formula[i-1] in allowed_num_chars or rgb_formula[i-1]=='.'):
                    #cycle throug the current number
                    while((i < last_index) and (rgb_formula[i]=='.' or  rgb_formula in allowed_num_chars)):
                        i+=1
                
                elif(rgb_formula[i+1] in allowed_num_chars):
                    return "error: wrong zeros format"
            i+=1
        
        #checking whether: there are numbers starting with a zero followed by another digit
        
        #<checking for: division by zero attempts

        if(rgb_formula[last_index-1]=='/' and rgb_formula[last_index]=='0'):
            return "error: division by zero is not allowed"
        i=1
        while(i<last_index):

            if(rgb_formula[i-1]=='/' and rgb_formula[i]=='0'):
                    
                if(rgb_formula[i+1]!='.'):
                    return "error: division by zero is not allowed"
                
                i+=2
                if(i==last_index and rgb_formula[i]=='0'):
                    return "error: division by zero is not allowed"
                
                while((i < last_index) and (rgb_formula[i]=='0')):
                    if(rgb_formula[i+1] not in allowed_num_chars or (i+1==last_index and rgb_formula[i+1]=='0')):
                        return "error: division by zero is not allowed"
                    i+=1
            i+=1

        #checking for: division by zero attempts>

        return ""





def is_RGB_formula_compatible_with_dxcam(rgb_formula: str, channel: str, use_areas: bool = False):
    
    if(rgb_formula is None):
        return False

    rgb_formula = rgb_formula if use_areas == False else make_areas_indexes_in_RGB_formula_fit_areas_count(rgb_formula)
    img = np.array([ [[1,2,3],[10,20,30]],[[5,7,9],[50,70,90]] ], dtype=np.uint8) if use_areas == False else np.array([ [[[1,2,3],[10,20,30]],[[5,7,9],[50,70,90]]], [[[11,22,33],[110,220,35]],[[55,77,99],[150,170,190]]] ], dtype=np.uint8)
    rgb_function = eval(f"lambda r,g,b,v=0: {rgb_formula}")if use_areas == False else eval(f"lambda r,g,b,areas_count,v=np.array([0], dtype=np.uint8): {rgb_formula}")
    
    try:
        if(use_areas == False):
            transformed_img = rgb_function(img[:,:,0], img[:,:,1], img[:,:,2])
        else:
            transformed_img = rgb_function(img[:,:,:,0], img[:,:,:,1], img[:,:,:,2], img.shape[0])
    except:
        print(f"Error: the formula for the {channel} channel was not compatible with dxcam. Try making the int values (or results of arithmetic operations between 2 variables) fit in the range 0-255.")
        return False    
        
    return True






#<functions for checking RGB fomulas which use image areas



#this functions can be used by any RGB channel formula which is supposed to work with image areas; it will replace things like `r[5]` with `r[5 if 5<areas_count else 0]}`
def make_areas_indexes_in_RGB_formula_fit_areas_count(rgb_formula: str):

    start_index = 0
    while(True):

        openining_bracket_index = rgb_formula.find("[",start_index)
        if(openining_bracket_index == -1):
            break

        closing_bracket_index = rgb_formula.find("]",openining_bracket_index+1)
        if(closing_bracket_index == -1):
            break

        current_index_in_brackets = rgb_formula[openining_bracket_index+1:closing_bracket_index]

        values_count_variable = "len(v)" if(rgb_formula[openining_bracket_index-1]=="v") else "areas_count"
        
        rgb_formula = rgb_formula[:closing_bracket_index] + f" if {current_index_in_brackets}<{values_count_variable} else 0" + rgb_formula[closing_bracket_index:]

        start_index = rgb_formula.find("]",closing_bracket_index+1)
    
    return rgb_formula





def check_rgb_formulas_format_for_pixel_areas(rgb_formulas_for_pixel_areas: str):
    
    rgb_formulas_pixel_area_start_index = 0
    rgb_formulas_pixel_area_end_index = 0
    index = 0
    
    while(True):

        rgb_formulas_pixel_area_start_index = rgb_formulas_for_pixel_areas.find("{", rgb_formulas_pixel_area_end_index)
        if(rgb_formulas_pixel_area_start_index==-1):
            break
    
        rgb_formulas_pixel_area_end_index = rgb_formulas_for_pixel_areas.find("}", rgb_formulas_pixel_area_start_index)
        if(rgb_formulas_pixel_area_end_index==-1):
            print(f"error: the rgb formula at index {index} had no closing curly bracket")
            return False      

        rgb_formulas_current_pixel_area = rgb_formulas_for_pixel_areas[rgb_formulas_pixel_area_start_index+1: rgb_formulas_pixel_area_end_index]
        are_rgb_formulas_for_current_pixel_area_valid = check_rgb_formulas_format_for_pixel_area(rgb_formulas_for_pixel_area = rgb_formulas_current_pixel_area, index = index)

        if(are_rgb_formulas_for_current_pixel_area_valid == False):
            return False

        index+=1
    
    return True

def check_rgb_formulas_format_for_pixel_area(rgb_formulas_for_pixel_area: str, index):   
                
    rgb_formula_id_index_start = rgb_formulas_for_pixel_area.find("|", 0)
    if(rgb_formula_id_index_start == -1):
        print(f"error: the rgb formula at index {index} has no id")
        return False
        
    rgb_formula_id_index_end = rgb_formulas_for_pixel_area.find("|", rgb_formula_id_index_start + 1)
    if(rgb_formula_id_index_start == -1):
        print(f"error: the id of the rgb formula at index {index} was not closed")
        return False
    
    rgb_formula_id_wrong_index = rgb_formulas_for_pixel_area.find("|", rgb_formula_id_index_end + 1)
    if(rgb_formula_id_wrong_index != -1):
        print(f"error: the rgb formula at index {index} cannot have more than 3 `|`")
        return False

    rgb_formula_id = rgb_formulas_for_pixel_area[rgb_formula_id_index_start+1:rgb_formula_id_index_end]
    is_rgb_formula_id_valid = check_for_positive_int_format(rgb_formula_id)

    if(is_rgb_formula_id_valid == False):
        print(f"error: the rgb formula at index {index} has wrong format for the id; the id must be a positive integer")
        return False
        
    formulas_counter = 0
    rgb_formula_start_index = 0
    rgb_formula_end_index = 0
    rgb_channels = ["red", "green", "blue"]

    while (formulas_counter < 3):

        rgb_formula_start_index = rgb_formulas_for_pixel_area.find("[", rgb_formula_end_index)
        if(rgb_formula_start_index==-1):
            print(f"error: the rgb formula at index {index} (id {rgb_formula_id}) has less than 3 colour channel formulas")
            return False

        
        rgb_formula_end_index = get_closing_square_bracket(text=rgb_formulas_for_pixel_area, start_index=rgb_formula_start_index)       
        
        if(rgb_formula_end_index==-1):
            print(f"error: the rgb formula at index {index} (id {rgb_formula_id}) had no closing curly square bracket for {rgb_channels[formulas_counter]} channel")
            return False
        
        if(rgb_formula_end_index - rgb_formula_start_index < 2):
            print(f"error: the rgb formula at index {index} (id {rgb_formula_id}) had no content for the {rgb_channels[formulas_counter]} channel")
            return False
        
        rgb_formula = rgb_formulas_for_pixel_area[rgb_formula_start_index+1:rgb_formula_end_index]

        if (check_RGB_formula_format(rgb_formula, channel=rgb_channels[formulas_counter], use_areas=True) == False):
            print(f"the previous error occurred at rgb formula index {index} (id {rgb_formula_id})")
            return False

        if(is_RGB_formula_compatible_with_dxcam(rgb_formula=rgb_formula,channel=rgb_channels[formulas_counter], use_areas=True) == False):
            print(f"the previous error occurred at rgb formula index {index} (id {rgb_formula_id})")
            return False

        formulas_counter+=1
    
    if(rgb_formulas_for_pixel_area.find("[", rgb_formula_end_index) != -1):
        print(f"error: the rgb formula at index {index} (id {rgb_formula_id}) has more than 3 colour channel formulas")
        return False

    return True
    

def get_closing_square_bracket(text:str, start_index:int):
    
    index = start_index+1
    int_helper = 1
    searched_index = -1

    while (index < len(text)):
        
        if(text[index] == "["):
            int_helper+=1
        elif(text[index] == "]"):
            int_helper-=1
        
        if(int_helper == 0):
            searched_index = index
            break

        index+=1
    
    return searched_index


#functions for checking RGB fomulas which use image areas>