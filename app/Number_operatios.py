import numpy as np
import random

from Enums import Enum_order
from Number_format_checker import check_for_positive_int_format

#step should not be equal to zero
def order_numbers(nums:list[int], order_type: Enum_order = Enum_order.ascending, start:int=None, end:int=None, step:int=None) -> list[int]:
    
    if(step == 0 or len(nums) <= 1):
        return nums
    ordered_nums = np.array(nums)

    #order the numbers
    if(order_type == Enum_order.ascending):
        ordered_nums[start:end:step] = np.sort(ordered_nums[start:end:step])
    elif(order_type == Enum_order.descending):
        ordered_nums[start:end:step] = np.sort(ordered_nums[start:end:step])[::-1]
    elif(order_type == Enum_order.random):
        random.shuffle(ordered_nums[start:end:step])
    
    #make sure the order is not reversed when the step is negative
    if(step is not None):
        if(step<0):
            ordered_nums[start:end:step] = ordered_nums[start:end:step][::-1]
    
    return ordered_nums.tolist()

#returns a tuple whose elements are the positive representations of the two input indexes; the smaller index is the first element in the tuple
def get_proper_positive_indexes(index1:int, index2:int, elements_count:int) -> tuple[int, int]:
      
    index1 = get_proper_positive_index(index=index1, elements_count=elements_count)
    index2 = get_proper_positive_index(index=index2, elements_count=elements_count)

    if(index1 > index2):
        index1_copy = index1
        index1 = index2
        index2 = index1_copy

    return (index1, index2)

#returns the positive representation of the input index
def get_proper_positive_index(index:int, elements_count:int) -> int:

    if(elements_count <= 0):
        raise Exception("`elements_count` must be a positive integer above zero")

    if(index >= elements_count):
        index = elements_count-1
    elif(index < 0 and index < 0-elements_count):
        index = 0-elements_count

    index = index %elements_count
    return index

#get's the smallest unique positive integer from a text input; the integers for comparison will be extracted from the text input using the opening and closing separators;
def get_smallest_unique_positive_integer(text: str, opening_separator: str, closing_separator: str, start_integer:int=1, end_integer:int=1_000_000) -> int|None:
        
    closing_separator_index = 0-len(closing_separator)
    used_int_values = []

    if(len(opening_separator)==0 or len(closing_separator)==0):
        raise Exception("the opening and closing separators must not be empty strings")
    if(start_integer < 0 or end_integer < 0):
        raise Exception("the start and end integers must be positive")
    if(start_integer>=end_integer):
        raise Exception("the start integer must be lower than the end integer")

    #get integers inside the opening and closing separators
    while True:
            
        opening_separator_index = text.find(opening_separator, closing_separator_index+len(closing_separator))
        if(opening_separator_index == -1):
            break
            
        closing_separator_index = text.find(closing_separator, opening_separator_index+len(opening_separator))
        if(closing_separator_index == -1):
            break

        #skip the separators which have no content inside them
        if(closing_separator_index == opening_separator_index+len(opening_separator)):
            continue

        content_inside_separators = text[opening_separator_index+len(opening_separator):closing_separator_index]
        is_int_value_correct = check_for_positive_int_format(txt_value = content_inside_separators)
        if(is_int_value_correct == True):
            used_int_values.append(int(content_inside_separators))
        

    #finds the smallest unique integer
    for i in range (start_integer, end_integer):
        if(i not in used_int_values):
            return i

    return None