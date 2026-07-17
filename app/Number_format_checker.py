
def check_for_float_format(txt_value:str):
        
        if(txt_value == ''):
            return True      
        elif( 
            (txt_value.__contains__('-') and txt_value[0] != '-') or
            (txt_value[0] == '-' and len(txt_value)==1) or
            (txt_value[0] == '-' and txt_value[1]== '.') or
            (txt_value[0] == '.' or txt_value[len(txt_value)-1] == '.')
            ):
            return False
        
        allowed_chars = ['0','1','2','3','4','5','6','7','8','9', '.', '-']

        minus_counter = 0
        decimal_points_counter = 0
        
        for symbol in txt_value:
            
            if(symbol not in allowed_chars):
                return False
            
            if(symbol == '-'):
                minus_counter+=1
            elif(symbol == '.'):
                decimal_points_counter+=1
            
            if(minus_counter> 1 or decimal_points_counter > 1):
                return False
        
        return check_for_leading_zeros(txt_value)


def check_for_positive_float_format(txt_value:str, is_zero_allowed:bool=True):
        
        if(txt_value == ''):
            return True      
        elif(txt_value[0] == '.' or txt_value[len(txt_value)-1] == '.'):
            return False
        
        allowed_chars = ['0','1','2','3','4','5','6','7','8','9', '.']

        decimal_points_counter = 0
        
        for symbol in txt_value:
            
            if(symbol not in allowed_chars):
                return False
            
            elif(symbol == '.'):
                decimal_points_counter += 1
            
            if(decimal_points_counter > 1):
                return False
               
        if(check_for_leading_zeros(txt_value)==False):
            return False

        if(is_zero_allowed==False and is_equal_to_zero(txt_value)==True):                       
            return False
       
        return True
       

#the input must be a valid int or float value
def is_equal_to_zero(txt_value):
                
    if(txt_value=='0'):
        return True
    
    elif(len(txt_value)>2 and txt_value[0]=='0' and  txt_value[1]=='.'):
        
        for i in range(2, len(txt_value)):
            if(txt_value[i]!='0'):
                return False
        return True
    
    else:
        return False
    


def check_for_int_format(txt_value:str):
        
        if(txt_value == ''):
            return True      
        elif( 
            (txt_value.__contains__('-') and txt_value[0] != '-') or
            (txt_value[0] == '-' and len(txt_value) == 1)
            ):
            return False
        
        allowed_chars = ['0','1','2','3','4','5','6','7','8','9', '-']

        minus_counter = 0
        
        for symbol in txt_value:
            
            if(symbol not in allowed_chars):
                return False
            
            if(symbol == '-'):
                minus_counter += 1
            
            if(minus_counter > 1):
                return False
        
        return check_for_leading_zeros(txt_value)

def check_for_positive_int_format(txt_value:str, is_zero_allowed:bool=True):
    if(txt_value == ''):
        return True     

    allowed_chars = ['0','1','2','3','4','5','6','7','8','9'] 

    for symbol in txt_value:
            
        if(symbol not in allowed_chars):
            return False
    
    if(is_zero_allowed==False and txt_value=='0'):
        return False

    return check_for_leading_zeros(txt_value)

def is_number_in_range(num_as_str:str, min:float, max:float):
    
    is_number_valid = check_for_float_format(num_as_str)
    if(is_number_valid == False):
        return False
    
    num = float(num_as_str)
    if(num<min or num>max):
        return False
    
    return True

#the input must be a valid int or float value (leading zeros are allowed - for instance the function works good with values like '001' )
#if the function returns `True` it means that the input contains no leading zeros
def check_for_leading_zeros(txt_value:str):

    if(len(txt_value) < 2):
        return True

    digits = ['0','1','2','3','4','5','6','7','8','9']
    
    if(
        (txt_value[0] == "0" and txt_value[1] != ".")
        or (len(txt_value) > 2 and txt_value[0] == "-" and txt_value[1] == "0" and txt_value[2] != ".")
        ):
        return False
    
    return True


def check_numbers_from_string(txt_value:str, separator:str, search_for_floats:bool = False, search_for_positives_only:bool = True, max_numbers = None, min_numbers = None):

    elements = txt_value.split(separator)#creates a list of strings using the separator
    if("" in elements):
        return False

    if(max_numbers is not None):
        if(len(elements) > max_numbers):
            return False
    
    if(min_numbers is not None):
        if(len(elements) < min_numbers):
            return False

    for element in elements:
        
        is_element_in_valid_format = True

        if(search_for_floats == True and search_for_positives_only == True):
            is_element_in_valid_format = check_for_positive_float_format(txt_value = element)
        elif(search_for_floats == True and search_for_positives_only == False):
            is_element_in_valid_format = check_for_float_format(txt_value = element)
        elif(search_for_floats == False and search_for_positives_only == True):
            is_element_in_valid_format = check_for_positive_int_format(txt_value = element)
        elif(search_for_floats == False and search_for_positives_only == False):
            is_element_in_valid_format = check_for_int_format(txt_value = element)
        
        if(is_element_in_valid_format == False):
            return False
    
    return True

def check_lists_of_numbers_from_string(txt_value:str, outer_separator:str, inner_separator:str, opening_bracket_symbol:str, closing_bracket_symbol:str, search_for_floats:bool = False, search_for_positives_only:bool = True, max_numbers = None, min_numbers = None):

    valid_opening_brackets = ["(","[","{"]
    valid_closing_brackets = [")","]","}"]

    if (inner_separator == outer_separator):
        raise ValueError("the inner separator must be different from outer separator")
    elif(opening_bracket_symbol not in valid_opening_brackets):
        raise ValueError(f"the openning bracket must be one of those values {valid_opening_brackets}")
    elif(closing_bracket_symbol not in valid_closing_brackets):
        raise ValueError(f"the closing bracket must be one of those values {valid_closing_brackets}")

    elements = txt_value.split(outer_separator)#creates a list of strings using the separator; if the input is in valid format each element obtained from the split will be string which is a collection of ints separated by `inner_separator` (empty collections are also valid as long as they have the proper openning and closing bracket)
    if("" in elements):
        return False

    if(max_numbers is not None):
        if(len(elements) > max_numbers):
            return False
    
    if(min_numbers is not None):
        if(len(elements) < min_numbers):
            return False
    
    #cycling trough the collections (each element is a string which will be a collection of ints if the format is correct)
    for element in elements:
        
        #the collection must contain at least the opening and closing bracket
        if(len(element)<2):
            return False
        elif(element[0]!=opening_bracket_symbol or element[-1]!=closing_bracket_symbol):
            return False
        elif(len(element)==2):#empty collections are valid if the have the proper openning and closing bracket
            continue
        
        is_element_in_valid_format = check_numbers_from_string(txt_value=element[1:-1], separator=inner_separator,search_for_floats=search_for_floats, search_for_positives_only=search_for_positives_only, max_numbers=max_numbers, min_numbers=min_numbers)
        if(is_element_in_valid_format==False):
            return False
    
    return True






#`text` must be a string which is supposed to contain lists of lists of ints (for example - `[ [1], [0, 79] [150, 150], [1], [3, 2, 7, 8], [2, 3] ],  [ [2], [40, 40] [150, 100], [7],[1, 3, 5], [1, 2] ],  [ [1], [0, 0] [1, 1], [10], [2], [1, 3] ]`)
#`inner_lists_elements_count` must be a list which contains int values; each int value must define the required number of elements of the inner list with index equal to the index of the int value; the length of `inner_lists_elements_count` determines the number of inner lists
def check_str_format_for_lists_of_lists_of_ints(text: str, inner_lists_elements_count:list):   

    outer_list_first_index = 0
    outer_list_current_index = 0

    while(outer_list_first_index < len(text)):
        
        if (text[outer_list_first_index]!="["):
            return f"outer list at index {outer_list_current_index} had no opening square bracket"
    
        outer_list_last_index = text.find("]]", outer_list_first_index)+1
        if(outer_list_last_index == 0):
            return f"outer list at index {outer_list_current_index} had no closing square bracket"
        
        inner_content = text[outer_list_first_index+1 : outer_list_last_index]
        inner_content_error_message = check_str_format_for_lists_of_ints(text = inner_content, elements_counts = inner_lists_elements_count)
        if(inner_content_error_message != ""):
            return f"outer list at index {outer_list_current_index} was in wrong format - {inner_content_error_message}"

        if(outer_list_last_index == len(text)-1):
            break
        elif(text[outer_list_last_index+1] == ","):
            outer_list_first_index = outer_list_last_index+2
        else:
            return f"outer list at index {outer_list_current_index+1} had no comma before it"
        
        outer_list_current_index+=1

    return ""#executes when no errors are found


#`text` must be a string which is supposed to contain lists (for example - `[1], [0, 79] [150, 150], [1], [3, 2, 7, 8], [2, 3]`)
#`elements_count` must be a list which contains int values; each int value must define the required number of elements of the list with index equal to the index of the int value; the length of `elements_count` determines the number of lists
def check_str_format_for_lists_of_ints(text: str, elements_counts:list):    
    
    opening_bracket_index = 0
    list_index = 0
    
    while(opening_bracket_index < len(text)):

        if(list_index > len(elements_counts)-1):
            return f"the number of inner lists cannot be above {len(elements_counts)}"

        if (text[opening_bracket_index]!="["):
            return f"inner list at index {list_index} had no opening square bracket"
        
        closing_bracket_index = text.find("]", opening_bracket_index)
        if(closing_bracket_index == -1):
            return f"inner list at index {list_index} had no closing square bracket"
        
        inner_content = text[opening_bracket_index+1 : closing_bracket_index]
        required_count = elements_counts[list_index]
        are_ints_valid = check_numbers_from_string(txt_value = inner_content, separator=",", search_for_floats=False, search_for_positives_only=True, max_numbers=required_count,min_numbers=required_count) if required_count>0 else check_numbers_from_string(txt_value = inner_content, separator=",", search_for_floats=False, search_for_positives_only=True)
        
        if(are_ints_valid == False):
            return f"the integers inside inner list at index {list_index} were either in wrong format or their count was not equal to {elements_counts[list_index]}"  
              
        list_index+=1

        if(closing_bracket_index == len(text)-1):
            break
        elif(text[closing_bracket_index+1] == ","):
            opening_bracket_index = closing_bracket_index+2
        else:
            return f"inner list at index {list_index} had no comma before it"
    
    if(list_index != len(elements_counts)):
        return f"the number of inner lists cannot be below {len(elements_counts)}"

    return ""#executes when no errors are found