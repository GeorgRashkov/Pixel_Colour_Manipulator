import numpy as np
import random

from Enums import Enum_order

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