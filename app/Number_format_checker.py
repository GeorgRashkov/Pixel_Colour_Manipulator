
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