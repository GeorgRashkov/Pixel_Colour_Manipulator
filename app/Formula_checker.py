import numpy as np

from Number_format_checker import check_for_positive_int_format
from Formula_validation_collections import Formula_validation_collections


#this function must be called from outside
def check_formula_format(formula: str, expression_name: str, square_brackets_biggest_value: int, formula_validation_collections:Formula_validation_collections) -> bool:

        letters = formula_validation_collections.letters #this is used to distinguish between variables (contain only 1 letter) and special formulas(contain 2 or more letters)

        #<allowed symbols collections
        allowed_variable_chars = formula_validation_collections.allowed_variable_chars
        allowed_variable_collection_chars = formula_validation_collections.allowed_variable_collection_chars
        allowed_operator_chars = formula_validation_collections.allowed_operator_chars
        allowed_num_chars = formula_validation_collections.allowed_num_chars
        allowed_chars = formula_validation_collections.allowed_chars
        #allowed symbols collections>

        allowed_special_formulas = formula_validation_collections.allowed_special_formulas
    
        if(formula == ''):
            return False
        
        is_format_correct = True

        #error messages
        wrong_format_message = f"error: {expression_name} is in wrong format \n"
        invalid_symbol_message = lambda symbol: f"the symbol {symbol} is not allowed"
        invalid_placement_message = lambda symbol1, symbol2: f"the symbol {symbol1} cannot be placed before {symbol2}"
        square_brackets_not_closed_message = "error: square brackets were not closed"
        square_brackets_wrong_placement = f"error: openning square bracket cannot be placed after anyting beside {allowed_variable_collection_chars}"
        special_formula_without_opening_bracket_message = f"error: a special formula must be followed by a opening bracket"
        square_brackets_wrong_index_message = f"error: the index inside the square brackets must be a positive number not greater than {square_brackets_biggest_value}"


        #<first and last symbol check

        first_char = formula[0]
        last_char = formula[len(formula)-1]
        if(first_char=='.' or first_char==')' or first_char==']' or first_char in allowed_operator_chars):
            is_format_correct = False
            wrong_format_message+=f"the symbol {first_char} cannot be placed at the beginning of the formula"
        elif(last_char=='.' or last_char=='(' or last_char=='[' or last_char in allowed_operator_chars or last_char not in allowed_chars):
            is_format_correct = False
            wrong_format_message+=f"the symbol {last_char} cannot be placed at the end of the formula"
        
        #first and last symbol check>

        #<cheking every symbol
        i = 1
        while(i < len(formula)):
            
            if(is_format_correct==False):
                break

            #special formula check
            if(formula[i-1] in letters and formula[i] in letters):

                special_formula_found = False
                for allowed_special_formula in allowed_special_formulas:
                    if(formula[ i-1 : (i-1)+len(allowed_special_formula)] == allowed_special_formula):
                        special_formula_found = True
                        i = (i-1) + ( len(allowed_special_formula)-1 )
                        break
               
                if(special_formula_found == False):
                    wrong_format_message += invalid_symbol_message (formula[i-1])
                    is_format_correct = False

                elif( i==len(formula)-1 or formula[i+1]!="(" ):
                    wrong_format_message += special_formula_without_opening_bracket_message
                    is_format_correct = False
            

            #invalid symbol check
            elif(formula[i-1] not in allowed_chars):
                wrong_format_message += invalid_symbol_message (formula[i-1])
                is_format_correct = False


            #square brackets check
            elif(formula[i] == "["):

                if(formula[i-1] in allowed_variable_collection_chars):
                    closing_bracket_index = formula.find("]", i)

                    if(closing_bracket_index != -1):
                        if(closing_bracket_index > i+1):
                            if(check_for_positive_int_format(formula[i+1:closing_bracket_index]) == True):

                                square_brackets_index = int(formula[i+1:closing_bracket_index])
                                if(square_brackets_index > square_brackets_biggest_value):
                                    wrong_format_message+=square_brackets_wrong_index_message
                                    is_format_correct = False
                                    break

                                i = closing_bracket_index
                                if(i < len(formula)-1):
                                    i += 1 
                                    if(formula[i] not in allowed_chars or formula[i] =='[' or formula[i] ==']' or formula[i] =='(' or formula[i]=='.' or formula[i] in allowed_variable_chars or formula[i] in allowed_num_chars):
                                        wrong_format_message += invalid_placement_message(formula[i-1], formula[i])
                                        is_format_correct = False
                            else:
                                wrong_format_message+=square_brackets_wrong_index_message
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
                
            #executes only if the current and the previous symbols are currect
            else:
                               
                #numbers check
                if(formula[i-1] in allowed_num_chars):
                    if(formula[i]=='(' or formula[i] in allowed_variable_chars or formula[i] in letters):
                        wrong_format_message += invalid_placement_message(formula[i-1], formula[i])
                        is_format_correct = False
                                       
                #variables check
                elif(formula[i-1] in allowed_variable_chars):
                    if(formula[i] =='(' or formula[i]=='.' or formula[i] in allowed_variable_chars or formula[i] in allowed_num_chars or formula[i] in letters):
                        wrong_format_message += invalid_placement_message(formula[i-1], formula[i])
                        is_format_correct = False
                                           
                #operators check
                elif(formula[i-1] in allowed_operator_chars):
                    if(formula[i]==')' or formula[i]=='.' or formula[i] in allowed_operator_chars):
                        wrong_format_message += invalid_placement_message(formula[i-1], formula[i])
                        is_format_correct = False
                                        
                #openning bracket check
                elif(formula[i-1]=='('):
                    if(formula[i]==')' or formula[i]=='.' or formula[i] in allowed_operator_chars):
                        wrong_format_message += invalid_placement_message(formula[i-1], formula[i])
                        is_format_correct = False
                                            
                #closing bracket check
                elif(formula[i-1]==')'):
                    if(formula[i]=='(' or formula[i]=='.' or formula[i] in allowed_num_chars or formula[i] in allowed_variable_chars or formula[i] in letters):
                        wrong_format_message += invalid_placement_message(formula[i-1], formula[i])
                        is_format_correct = False
                                           
                #decimal point check
                elif(formula[i-1]=='.'):
                    if(formula[i]=='(' or formula[i]==')' or formula[i]=='.' or formula[i] in allowed_variable_chars or formula[i] in allowed_operator_chars or formula[i] in letters):
                        wrong_format_message += invalid_placement_message(formula[i-1], formula[i])
                        is_format_correct = False
            i +=1
        #cheking every symbol>
                                
        if(is_format_correct==False):
            print(wrong_format_message)
        
        wrong_format_message = check_formula_format_2(formula, allowed_num_chars)

        if(wrong_format_message!=""):
            print(wrong_format_message)
            is_format_correct = False

        return is_format_correct         
    
#this function must not be called from outside
#the function returns an error message; if the formula is in corret format the message will be an empty string
def check_formula_format_2(formula: str, allowed_num_chars) -> str:
        
        #<checking whether: the brackets are properly openned and closed
        counter = 0
        for i in range(0, len(formula)):
            
            if(formula[i]=="("):
                counter+=1
            elif(formula[i]==")"):
                counter-=1
            
            if(counter)<0:
                return "error: some brackets were not properly openned or closed"
        
        if(counter!=0):
            return "error: some brackets were not properly openned or closed"
        #checking whether: the brackets are properly openned and closed>

        #<checking whether: there are numbers containing more than 1 decimal point
        i=0
        while(i<len(formula)):
            
            if(formula[i]=="."):
                i+=1
    
                while(i<len(formula) and (formula[i] in allowed_num_chars or formula[i]==".")):
                    if(formula[i]=="."):
                        return "error: too many decimal points per number"
                    i+=1
                i-=1
            i+=1

        #checking whether: there are numbers containing more than 1 decimal point>

        if(len(formula)<3):
            return ""

        #<checking whether: there are numbers starting with a zero followed by another digit
        
        if(formula[0]=='0' and formula[1] in allowed_num_chars):
            return "error: wrong zeros format"

        last_index = len(formula)-1
        i=1
        while(i<last_index):
            
            #the code logic in the body of this if statement assures that the body will be executed only once per number; which means when `draw_formula[i]=="0"` is `True` the "0" symbol will always be the first "0" symbol in the current number 
            if(formula[i]=="0"):
               
                if(formula[i-1] in allowed_num_chars or formula[i-1]=='.'):
                    #cycle throug the current number
                    while((i < last_index) and (formula[i]=='.' or  formula in allowed_num_chars)):
                        i+=1
                
                elif(formula[i+1] in allowed_num_chars):
                    return "error: wrong zeros format"
            i+=1
        
        #checking whether: there are numbers starting with a zero followed by another digit
        
        #<checking for: division by zero attempts

        if(formula[last_index-1]=='/' and formula[last_index]=='0'):
            return "error: division by zero is not allowed"
        i=1
        while(i<last_index):

            if(formula[i-1]=='/' and formula[i]=='0'):
                    
                if(formula[i+1]!='.'):
                    return "error: division by zero is not allowed"
                
                i+=2
                if(i==last_index and formula[i]=='0'):
                    return "error: division by zero is not allowed"
                
                while((i < last_index) and (formula[i]=='0')):
                    if(formula[i+1] not in allowed_num_chars or (i+1==last_index and formula[i+1]=='0')):
                        return "error: division by zero is not allowed"
                    i+=1
            i+=1

        #checking for: division by zero attempts>

        return ""




#this function must be called from outside
def does_formula_contain_specific_variable(formula:str, variable:str, formula_validation_collections:Formula_validation_collections) -> bool:

    
    if(len(variable) != 1):
        raise Exception("error: the input parameter `variable` had length different from 1")
    
    start_index = 0
    separators = formula_validation_collections.allowed_special_chars + formula_validation_collections.allowed_operator_chars
    
    if(len(formula) < 2):
        if(formula!=variable):
            return False
        else:
            return True
        

    is_variable_found = False

    while(start_index < len(formula)):
        
        start_index = formula.find(variable, start_index)
        
        if(start_index == -1):
            break

        elif(start_index == 0):
            if(formula[1] in separators):
                is_variable_found = True
                break

        elif(start_index == len(formula)-1):
            if(formula[len(formula)-2] in separators):
                is_variable_found = True
            break
             
        elif( formula[start_index-1] in separators  and formula[start_index+1] in separators):
            is_variable_found = True
            break
            

        start_index+=1
    
    return is_variable_found