"""
import numpy as np
from Number_format_checker import check_for_positive_int_format



class Draw_formula_validation_collections():

    def __init__(self):

        self.letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        
        self.allowed_variable_chars = ['v','x','y','r','g','b']
        self.allowed_variable_collection_chars = ['v']
        self.allowed_operator_chars = ['+','-','*','/','^','%','<','>','=']
        self.allowed_num_chars = ['0','1','2','3','4','5','6','7','8','9']
        self.allowed_chars = ['.','(',')', 'v','x','y','r','g','b', '+','-','*','/','^','%','<','>','=', '0','1','2','3','4','5','6','7','8','9']
        self.allowed_special_formulas = ["sin(", "cos(", "tan(", "abs(", "exp(", "sqrt("]


def check_draw_formula_expressions_format(main_expression:str, sub_expressions:list[str]) -> bool:
    
    is_main_draw_formula_missing_necessary_variables = does_draw_formula_contain_specific_variable(draw_formula=main_expression, variable="x") == False and does_draw_formula_contain_specific_variable(draw_formula=main_expression, variable="y") == False
    if(is_main_draw_formula_missing_necessary_variables == True):
        print("error: the main expression must contain at least at least one value for `x` or `y`")
        return False

    sub_expressions_len = len(sub_expressions)

    for i in range(0, sub_expressions_len):
        is_expression_valid = check_draw_formula_expression_format(draw_formula = sub_expressions[i], expression_name = f"sub expression at index {i}", sub_expressions_last_index = i-1)
        if(is_expression_valid == False):
            return False
    
    is_expression_valid = check_draw_formula_expression_format(draw_formula = main_expression, expression_name="main expression",  sub_expressions_last_index = sub_expressions_len-1)
    if(is_expression_valid == False):
        return False
    else:
        return True



def check_draw_formula_expression_format(draw_formula: str, expression_name: str, sub_expressions_last_index: int) -> bool:
        
        draw_formula_validation_collections = Draw_formula_validation_collections()

        letters = draw_formula_validation_collections.letters #this is used to distinguish between variables (contain only 1 letter) and special formulas(contain 2 or more letters)

        #<allowed symbols collections
        allowed_variable_chars = draw_formula_validation_collections.allowed_variable_chars
        allowed_variable_collection_chars = draw_formula_validation_collections.allowed_variable_collection_chars
        allowed_operator_chars = draw_formula_validation_collections.allowed_operator_chars
        allowed_num_chars = draw_formula_validation_collections.allowed_num_chars
        allowed_chars = draw_formula_validation_collections.allowed_chars
        #allowed symbols collections>

        allowed_special_formulas = draw_formula_validation_collections.allowed_special_formulas
    
        if(draw_formula == ''):
            return False
        
        is_format_correct = True

        #error messages
        wrong_format_message = f"error: {expression_name} is in wrong format \n"
        invalid_symbol_message = lambda symbol: f"the symbol {symbol} is not allowed"
        vars_without_index_message = lambda symbol: f"the symbol {symbol} must be followed by `[`"
        invalid_placement_message = lambda symbol1, symbol2: f"the symbol {symbol1} cannot be placed before {symbol2}"
        square_brackets_not_closed_message = "error: square brackets were not closed"
        square_brackets_wrong_placement = f"error: openning square bracket cannot after anyting beside {allowed_variable_collection_chars}"
        expression_index_message = f"error: the index inside the square brackets must be a positive number not greater than {sub_expressions_last_index}"


        #<first and last symbol check

        first_char = draw_formula[0]
        last_char = draw_formula[len(draw_formula)-1]
        if(first_char=='.' or first_char==')' or first_char==']' or first_char in allowed_operator_chars):
            is_format_correct = False
            wrong_format_message+=f"the symbol {first_char} cannot be placed at the beginning of the formula"
        elif(last_char=='.' or last_char=='(' or last_char=='[' or last_char in allowed_operator_chars or last_char in allowed_variable_collection_chars):
            is_format_correct = False
            wrong_format_message+=f"the symbol {last_char} cannot be placed at the end of the formula"

        
        
        
        
        #first and last symbol check>

        #<cheking every symbol
        i = 1
        while(i < len(draw_formula)):
            
            if(is_format_correct==False):
                break

            #special formula check
            if(draw_formula[i-1] in letters and draw_formula[i] in letters):

                special_formula_found = False
                for allowed_special_formula in allowed_special_formulas:
                    if(draw_formula[ i-1 : (i-1)+len(allowed_special_formula)] == allowed_special_formula):
                        special_formula_found = True
                        i = i + ( len(allowed_special_formula)-2 )
                        break
                
                if(special_formula_found == False):
                    wrong_format_message += invalid_symbol_message (draw_formula[i-1])
                    is_format_correct = False
            

            #additional checks
            elif(draw_formula[i-1] not in allowed_chars):
                wrong_format_message += invalid_symbol_message (draw_formula[i-1])
                is_format_correct = False

            elif(draw_formula[i-1] in allowed_variable_collection_chars and draw_formula[i] != '['):
                wrong_format_message += vars_without_index_message (draw_formula[i-1])
                is_format_correct = False


            #square brackets check
            elif(draw_formula[i] not in allowed_chars and draw_formula[i] not in letters):

                if(draw_formula[i] == "["):
                    if(draw_formula[i-1] in allowed_variable_collection_chars):
                        closing_bracket_index = draw_formula.find("]", i)

                        if(closing_bracket_index != -1):
                            if(closing_bracket_index > i+1):
                                if(check_for_positive_int_format(draw_formula[i+1:closing_bracket_index]) == True):

                                    sub_expressions_index = int(draw_formula[i+1:closing_bracket_index])
                                    if(sub_expressions_index > sub_expressions_last_index):
                                        wrong_format_message+=expression_index_message
                                        is_format_correct = False
                                        break

                                    i = closing_bracket_index
                                    if(i < len(draw_formula)-1):
                                        i += 1 
                                        if(draw_formula[i] not in allowed_chars or draw_formula[i] =='(' or draw_formula[i]=='.' or draw_formula[i] in allowed_variable_chars or draw_formula[i] in allowed_num_chars):
                                            wrong_format_message += invalid_placement_message(draw_formula[i-1], draw_formula[i])
                                            is_format_correct = False
                                else:
                                    wrong_format_message+=expression_index_message
                                    is_format_correct = False
                            else:
                                wrong_format_message += invalid_placement_message('[',']')
                                is_format_correct = False
                        else:
                            wrong_format_message += square_brackets_not_closed_message
                            is_format_correct = False
                    else:
                        wrong_format_message += square_brackets_wrong_placement
                        is_format_correct = False
                else:
                    wrong_format_message += invalid_symbol_message (draw_formula[i])
                    is_format_correct = False

            #executes only if the current and the previous symbols are currect
            else:
                               
                #numbers check
                if(draw_formula[i-1] in allowed_num_chars):
                    if(draw_formula[i]=='(' or draw_formula[i] in allowed_variable_chars or draw_formula[i] in letters):
                        wrong_format_message += invalid_placement_message(draw_formula[i-1], draw_formula[i])
                        is_format_correct = False
                                       
                #variables check
                elif(draw_formula[i-1] in allowed_variable_chars):
                    if(draw_formula[i] =='(' or draw_formula[i]=='.' or draw_formula[i] in allowed_variable_chars or draw_formula[i] in allowed_num_chars or draw_formula[i] in letters):
                        wrong_format_message += invalid_placement_message(draw_formula[i-1], draw_formula[i])
                        is_format_correct = False
                                           
                #operators check
                elif(draw_formula[i-1] in allowed_operator_chars):
                    if(draw_formula[i]==')' or draw_formula[i]=='.' or draw_formula[i] in allowed_operator_chars):
                        wrong_format_message += invalid_placement_message(draw_formula[i-1], draw_formula[i])
                        is_format_correct = False
                                        
                #openning bracket check
                elif(draw_formula[i-1]=='('):
                    if(draw_formula[i]==')' or draw_formula[i]=='.' or draw_formula[i] in allowed_operator_chars):
                        wrong_format_message += invalid_placement_message(draw_formula[i-1], draw_formula[i])
                        is_format_correct = False
                                            
                #closing bracket check
                elif(draw_formula[i-1]==')'):
                    if(draw_formula[i]=='(' or draw_formula[i]=='.' or draw_formula[i] in allowed_num_chars or draw_formula[i] in allowed_variable_chars or draw_formula[i] in letters):
                        wrong_format_message += invalid_placement_message(draw_formula[i-1], draw_formula[i])
                        is_format_correct = False
                                           
                #decimal point check
                elif(draw_formula[i-1]=='.'):
                    if(draw_formula[i]=='(' or draw_formula[i]==')' or draw_formula[i]=='.' or draw_formula[i] in allowed_variable_chars or draw_formula[i] in allowed_operator_chars or draw_formula[i] in letters):
                        wrong_format_message += invalid_placement_message(draw_formula[i-1], draw_formula[i])
                        is_format_correct = False
            i +=1
        #cheking every symbol>
                                
        if(is_format_correct==False):
            print(wrong_format_message)
        
        wrong_format_message = check_draw_formula_expression_format_2(draw_formula, allowed_num_chars)

        if(wrong_format_message!=""):
            print(wrong_format_message)
            is_format_correct = False

        return is_format_correct         
    
    #the function returns an error message; if the formula is in corret format the message will be an empty string
def check_draw_formula_expression_format_2(draw_formula: str, allowed_num_chars) -> str:
        
        #<checking whether: the brackets are properly openned and closed
        counter = 0
        for i in range(0, len(draw_formula)):
            
            if(draw_formula[i]=="("):
                counter+=1
            elif(draw_formula[i]==")"):
                counter-=1
            
            if(counter)<0:
                return "error: some brackets were not properly openned or closed"
        
        if(counter!=0):
            return "error: some brackets were not properly openned or closed"
        #checking whether: the brackets are properly openned and closed>

        #<checking whether: there are numbers containing more than 1 decimal point
        i=0
        while(i<len(draw_formula)):
            
            if(draw_formula[i]=="."):
                i+=1
    
                while(i<len(draw_formula) and (draw_formula[i] in allowed_num_chars or draw_formula[i]==".")):
                    if(draw_formula[i]=="."):
                        return "error: too many decimal points per number"
                    i+=1
                i-=1
            i+=1

        #checking whether: there are numbers containing more than 1 decimal point>

        if(len(draw_formula)<3):
            return ""

        #<checking whether: there are numbers starting with a zero followed by another digit
        
        if(draw_formula[0]=='0' and draw_formula[1] in allowed_num_chars):
            return "error: wrong zeros format"

        last_index = len(draw_formula)-1
        i=1
        while(i<last_index):
            
            #the code logic in the body of this if statement assures that the body will be executed only once per number; which means when `draw_formula[i]=="0"` is `True` the "0" symbol will always be the first "0" symbol in the current number 
            if(draw_formula[i]=="0"):
               
                if(draw_formula[i-1] in allowed_num_chars or draw_formula[i-1]=='.'):
                    #cycle throug the current number
                    while((i < last_index) and (draw_formula[i]=='.' or  draw_formula in allowed_num_chars)):
                        i+=1
                
                elif(draw_formula[i+1] in allowed_num_chars):
                    return "error: wrong zeros format"
            i+=1
        
        #checking whether: there are numbers starting with a zero followed by another digit
        
        #<checking for: division by zero attempts

        if(draw_formula[last_index-1]=='/' and draw_formula[last_index]=='0'):
            return "error: division by zero is not allowed"
        i=1
        while(i<last_index):

            if(draw_formula[i-1]=='/' and draw_formula[i]=='0'):
                    
                if(draw_formula[i+1]!='.'):
                    return "error: division by zero is not allowed"
                
                i+=2
                if(i==last_index and draw_formula[i]=='0'):
                    return "error: division by zero is not allowed"
                
                while((i < last_index) and (draw_formula[i]=='0')):
                    if(draw_formula[i+1] not in allowed_num_chars or (i+1==last_index and draw_formula[i+1]=='0')):
                        return "error: division by zero is not allowed"
                    i+=1
            i+=1

        #checking for: division by zero attempts>

        return ""



#<not finished !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def is_draw_formula_runnable(draw_formula: str) -> bool:
    
    if(draw_formula is None):
        return False

    draw_formula = draw_formula
    x_ = np.linspace(-20, 20, 4_00)
    y_ = np.linspace(-20, 20, 4_00)
    x, y = np.meshgrid(x_, y_)
    draw_function = eval(f"lambda x, y: {draw_formula}")
    
    try:
        draw_result = draw_function(x,y)
        
    except:
        print(f"Error: the draw formula had unexpected wrong format")
        return False    
        
    return True



def does_draw_formula_contain_specific_variable(draw_formula:str, variable:str):

    
    if(len(variable) != 1):
        raise Exception("error: the input parameter `variable` had length different from 1")
    
    start_index = 0
    draw_formula_validation_collections = Draw_formula_validation_collections()
    letters_and_numbers = draw_formula_validation_collections.letters + draw_formula_validation_collections.allowed_num_chars
    
    
    if(len(draw_formula) < 2):
        if(draw_formula!=variable):
            return False
        else:
            return True
        

    is_variable_found = False

    while(True):
        
        start_index = draw_formula.find(variable, start_index)
        
        if(start_index == -1):
            break

        elif(start_index == 0):
            if(draw_formula[1] not in letters_and_numbers):
                is_variable_found = True
                break

        elif(start_index == len(draw_formula)-1):
            if(draw_formula[len(draw_formula)-2] not in letters_and_numbers):
                is_variable_found = True
            break
             
        elif(draw_formula[start_index-1] not in letters_and_numbers and draw_formula[start_index+1] not in letters_and_numbers):
            is_variable_found = True
            break
            

        start_index+=1
    
    return is_variable_found
"""



from Formula_validation_collections import Draw_formula_validation_collections
from Formula_checker import check_formula_format, does_formula_contain_specific_variables

def check_draw_formula_expressions_format(main_expression:str, sub_expressions:list[str]) -> bool:
    
    draw_formula_validation_collections = Draw_formula_validation_collections()
    does_formula_contain_atleast_one_x_y_value = does_formula_contain_specific_variables(formula=main_expression, variables=["x","y"], formula_validation_collections=draw_formula_validation_collections, find_all=False)
    if(does_formula_contain_atleast_one_x_y_value == False):
        print("error: the main expression must contain at least at least one value for `x` or `y`")
        return False

    sub_expressions_len = len(sub_expressions)

    for i in range(0, sub_expressions_len):
        is_expression_valid = check_formula_format(formula=sub_expressions[i], expression_name = f"sub expression at index {i}", square_brackets_biggest_value = i-1, formula_validation_collections=draw_formula_validation_collections)
        if(is_expression_valid == False):
            return False
    
    is_expression_valid = check_formula_format(formula=main_expression, expression_name="main expression",  square_brackets_biggest_value = sub_expressions_len-1, formula_validation_collections=draw_formula_validation_collections)
    if(is_expression_valid == False):
        return False
    else:
        return True
    