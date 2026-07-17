from Enums import Enum__brackets

# the function returns a list containing the found expressions
# expression is considered anything inside the brackets
# if there is a content outside the brackets that content is considered as invalid expression
# the function returns an empty list only when the input string of expressions was empty
# if the last element in the output list is `None` this means the last expression was not valid and nothing after that expression was checked; 
# invalid expression is: any content outside the brackets; any expression whose brackets are not properly closed
# the number of expressions specifies the maximum number of expressions which the function will return
# there will be no maximum number of expressions if `expressions_count` is equal to zero (the function tries to extract all expressions)
def get_expressions_in_brackets(bracket_type:Enum__brackets, expressions_str:str, expressions_count:int=0) -> list[str]:
    
    if (expressions_count < 0):
        raise Exception(f"`expressions_count` must be a positive number")

    expressions:list[str] = []

    if(len(expressions_str) == 0):
        return expressions

    openning_bracket, closing_bracket = get_opening_closing_brackets(bracket_type=bracket_type)  
    
    #content outside the brackets (in this case at the beggining of the input string expessions value) is considered as invalid expression
    if(expressions_str[0] != openning_bracket):
        expressions.append(None)
        return expressions

    infinite_number_of_expressions = expressions_count == 0

    openning_bracket_index = 0
    closing_bracket_index = 0
    non_closed_brackets_count = 0
    
    while(expressions_count > 0 or infinite_number_of_expressions == True):

        openning_bracket_index = expressions_str.find(openning_bracket, closing_bracket_index) 
        if(openning_bracket_index == -1):
            break
        
        #if there is a content between 2 expressions that content is considered as invalid expression
        if(closing_bracket_index+1 != openning_bracket_index):
            if(closing_bracket_index != 0):
                expressions.append(None)
                break
        
        non_closed_brackets_count += 1
        expression_start_index = openning_bracket_index+1
        index = openning_bracket_index

        #<cycle trhough the elements in the current expression
        while(non_closed_brackets_count != 0):
            
            index+=1

            if(index == len(expressions_str)):
                break

            if(expressions_str[index] == openning_bracket):
                non_closed_brackets_count +=1
                openning_bracket_index = index
            elif(expressions_str[index] == closing_bracket):
                non_closed_brackets_count -=1
                closing_bracket_index = index
        #cycle trhough the elements in the current expression>

        #occurs when the current expression was not properly closed
        if(non_closed_brackets_count != 0):
            expressions.append(None)
            break

        non_closed_brackets_count = 0

        if(infinite_number_of_expressions == False):
            expressions_count-=1
        
        expressions.append(expressions_str[expression_start_index:closing_bracket_index])

    #content outside the last closing bracket is considered as invalid expression when the desired number of found expressions was not reached
    if(closing_bracket_index != len(expressions_str)-1 and (expressions_count != 0 or infinite_number_of_expressions==True)):
        expressions.append(None)

    return expressions


def get_opening_closing_brackets(bracket_type:Enum__brackets) -> tuple[str, str]:
    
    if(bracket_type ==Enum__brackets.round):
        return ("(", ")")
    
    elif(bracket_type ==Enum__brackets.square):
       return ("[", "]")

    elif(bracket_type ==Enum__brackets.curly):
        return ("{", "}")

#get's the index of the proper closing bracket based on the first openning bracket
#if the input text has no proper closing bracket the function returns `-1`
#the input text must start with a bracket
def get_closing_bracket_index(txt:str) -> int:

    brackets = {'(':')','[':']','{':'}'}

    if(len(txt) == 0 or txt[0] not in brackets.keys()):
        raise Exception("the text input must start with a bracket")
        
    openning_bracket = txt[0]
    closing_bracket = brackets[txt[0]]

    non_closed_brackets_count = 1
    txt_index = 1

    while(non_closed_brackets_count != 0 and txt_index<len(txt)):

            if(txt[txt_index] == openning_bracket):
                non_closed_brackets_count +=1
                
            elif(txt[txt_index] == closing_bracket):
                non_closed_brackets_count -=1
               
            txt_index+=1
    
    if(non_closed_brackets_count != 0):
        return -1
    
    txt_index -= 1
    return txt_index


#the function returns a dictionary whose keys are the parameters while the values are the values of the parameters
#the values must be placed in the brackets
def get_parameters_and_values_from_bracket_expressions(txt:str, bracket_type:Enum__brackets, valid_parameters:set[str], required_parameters:set[str], parameter_value_separator:str) -> dict[str, str]:
    
    check_parameters(valid_parameters=valid_parameters, required_parameters=required_parameters, parameter_value_separator=parameter_value_separator)

    parameters = {}
    if(txt == ""):
        return parameters
    
    parameter_start_index = 0
    while(parameter_start_index<len(txt)):
        
        #<check whether the current parameter is valid
        separator_start_index = -1
        found_parameter = None
        for valid_parameter in valid_parameters:
            separator_start_index = parameter_start_index+len(valid_parameter)
            if( separator_start_index < len(txt) ):
                if( txt[parameter_start_index:separator_start_index] == valid_parameter and txt[separator_start_index:separator_start_index+len(parameter_value_separator)] == parameter_value_separator):
                    #separator_start_index = separator_start_index-1
                    found_parameter = valid_parameter
                    break
        
        if(separator_start_index == -1):
            print("error: invalid parameter")
            return None
        
        if(found_parameter in parameters.keys()):
            print(f"error: the parameter `{found_parameter}` is used many times")
            return None
        #check whether the current parameter is valid>


        #<check whether the parameter-value separator is valid
        #separator_start_index = separator_start_index + 1
        separator_end_index = separator_start_index + len(parameter_value_separator) - 1
        if (separator_end_index >= len(txt)):
            print(f"error: the parameter `{found_parameter}` had invalid separator")
            return None

        if(txt[separator_start_index:separator_end_index+1] != parameter_value_separator):
            print(f"error: the parameter `{found_parameter}` had invalid separator")
            return None
        
        #check whether the parameter-value separator is valid>
        
        
        #<check whether the value of the current parameter has proper openning and closing bracket
        value_openning_bracket_index = separator_end_index+1
        if(value_openning_bracket_index == len(txt)):
            print(f"error: the parameter `{found_parameter}` had no value")
            return None
        
        expressions_in_brackets = get_expressions_in_brackets(bracket_type=bracket_type, expressions_str=txt[value_openning_bracket_index:], expressions_count=1)
        expression_in_brackets = expressions_in_brackets[0]
        if(expression_in_brackets is None):
            print(f"error: the brackets around the value of the parameter `{found_parameter}` were not properly openned or closed")
            return None
        #check whether the value of the current parameter has proper openning and closing bracket>
        
        parameters[found_parameter] = expression_in_brackets

        value_closing_bracket_index = value_openning_bracket_index + len(expression_in_brackets) + 1
        parameter_start_index = value_closing_bracket_index + len(parameter_value_separator) + 1
    
    for required_parameter in required_parameters:
        if(required_parameter not in parameters.keys()):
            print(f"error: the required parameter `{required_parameter}` was not found")
            return None
    
    return parameters


def check_parameters(valid_parameters:set[str], required_parameters:set[str], parameter_value_separator:str):
    
    if(len(parameter_value_separator) == 0):
        raise Exception(f"`parameter_value_separator` had no characters")

    for required_parameter in required_parameters:
        if(required_parameter not in valid_parameters):
            raise Exception(f"`required_parameters` had values not presented in `valid_parameters`")



def get_subjects_represented_as__parameters_and_values_from_bracket_expressions(txt:str, subject_name:str, outer_bracket_type:Enum__brackets, inner_bracket_type:Enum__brackets, valid_parameters:set[str], required_parameters:set[str], parameter_value_separator:str) -> list[dict[str, str]]:
    
    check_parameters(valid_parameters=valid_parameters, required_parameters=required_parameters, parameter_value_separator=parameter_value_separator)

    subjects_represented_as__parameters_and_values = []
    if(txt == ""):
        return subjects_represented_as__parameters_and_values
    
    subjects = get_expressions_in_brackets(bracket_type=outer_bracket_type, expressions_str=txt)
    if(subjects[-1] is None):
        print(f"error: the brackets around the {subject_name} on index {len(subjects)-1} were not properly openned or closed")
        return None

    subject_index = 0
    for subject in subjects:
        
        subject_represented_as__parameters_and_values = get_parameters_and_values_from_bracket_expressions(txt=subject, bracket_type=inner_bracket_type, valid_parameters=valid_parameters, required_parameters=required_parameters, parameter_value_separator=parameter_value_separator)
        if(subject_represented_as__parameters_and_values is None):
            print(f"the previous error occurred on the {subject_name} at index {subject_index}")
            return None
        
        subjects_represented_as__parameters_and_values.append(subject_represented_as__parameters_and_values)

        subject_index+=1
    
    return subjects_represented_as__parameters_and_values
