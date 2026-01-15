import numpy as np

def check_RGB_formula_format(rgb_formula: str, channel: str):
        
        #<allowed symbols collections
        allowed_RGB_chars = ['r','g','b']
        allowed_operator_chars = ['+','-','*','/','^','%','<','>','=']
        allowed_num_chars = ['0','1','2','3','4','5','6','7','8','9']
        allowed_chars = ['.','(',')','r','g','b','+','-','*','/','^','%','<','>','=','0','1','2','3','4','5','6','7','8','9']
    
        if(rgb_formula == ''):
            return False
        
        is_format_correct = True

        #error messages
        wrong_format_message = f"error: the {channel} channel formula is in wrong format \n"
        invalid_symbol_message = lambda symbol: f"the symbol {symbol} is not allowed"
        invalid_placement_message = lambda symbol1, symbol2: f"the symbol {symbol1} cannot be placed before {symbol2}"

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
        for i in range(1, len(rgb_formula)):
            
            if(is_format_correct==False):
                break

            #checking for valid symbols
            if(rgb_formula[i-1] not in allowed_chars):
                wrong_format_message += invalid_symbol_message (rgb_formula[i-1])
                is_format_correct = False
                
            elif(rgb_formula[i] not in allowed_chars):
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





def is_RGB_formula_compatible_with_dxcam(rgb_formula: str, channel: str):
    
    img = np.array([[[1,2,3],[10,20,30]],[[5,7,9],[50,70,90]]], dtype=np.uint8)    
    rgb_function = eval(f"lambda r,g,b: {rgb_formula}")
           
    try:
        transformed_img = rgb_function(img[:,:,0], img[:,:,1], img[:,:,2])
    except:
        print(f"Error: the formula for the {channel} channel was not compatible with dxcam. Try making the int values (or results of arithmetic operations between 2 variables) fit in the range 0-255.")
        return False    
        
    return True
