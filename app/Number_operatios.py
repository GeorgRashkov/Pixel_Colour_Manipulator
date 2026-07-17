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