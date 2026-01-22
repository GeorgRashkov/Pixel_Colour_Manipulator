

#< this code ckecks strings and makes sure they a format similar to this one (spaces and new lines are not valid but are presented in the example for readability)
"""
"
[   [ [0, 79, 85], [0, 0, 0] ],   [ [293, 292, 85], [0, 0, 0] ]   ],
[   [ [203, 44, 175], [0, 0, 0] ],   [ [0, 203, 175], [0, 0, 0] ]   ],
[   [ [0, 0, 200], [0, 0, 0] ],   [ [146, 136, 200], [0, 0, 0] ]   ],
"
"""


#returns an error message
def is_switch_pixel_text_valid(text: str):    
   
    index = 0
    opening_brackets_count = 3
    current_row_array_index = 0
    row_arrays_count = 4

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

            if(closing_bracket_index - opening_bracket_index < 5):#if the symbols inside the inner brackets is less than 5 then the format is wrong for sure
                return inner_content_error_message

            is_content_correct = is_inner_content_correct(text=text[opening_bracket_index+1: closing_bracket_index])
            
            if( is_content_correct == False):
                return inner_content_error_message
            
            if(current_row_array_index == 1):
                closing_bracket_index +=1
            elif(current_row_array_index == 3):
                closing_bracket_index +=2

            if(closing_bracket_index < len(text)-1):#if the closing bracket is located before the final symbol in the `text` execute the code
                if(text[closing_bracket_index+1] == ","):
                    index = closing_bracket_index+2
                else:
                    return dimension_format_error_message
            else:
                return dimension_format_error_message

            if(
                (current_row_array_index == 1 and text[closing_bracket_index] != "]") or
                (current_row_array_index == 3 and (text[closing_bracket_index] != "]" or text[closing_bracket_index-1] != "]") )
               ):
                return dimension_format_error_message

            current_row_array_index+=1

            if(current_row_array_index>=row_arrays_count):#if this executes it means all elements of the current row were checked
                current_row_array_index = 0
            
            
            if(current_row_array_index==0):
                opening_brackets_count = 3
                is_last_processed_row_complete = True
            elif(current_row_array_index==1):
                opening_brackets_count = 1
            elif(current_row_array_index==2):
                opening_brackets_count = 2
            elif(current_row_array_index==3):
                opening_brackets_count = 1
                

        else:
            return dimension_format_error_message
    
    
    if(is_last_processed_row_complete == False):
        return dimension_format_error_message

    return ""#the format was correct, which is why it returns no error messages



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



# this code ckecks strings and makes sure they a format similar to this one (spaces and new lines are not valid but are presented in the example for readability)> 
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

            


        

            