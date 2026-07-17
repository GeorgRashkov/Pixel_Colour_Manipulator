import numpy as np

from Convolutional_kernel_for_image import Convolutional_kernel_for_image
from Enums import Enum_order
import random


class Convolutional_kernels_manipulator:
    
    def __init__(self):
        self.convolutional_kernels:dict[int, Convolutional_kernel_for_image] = {} 
        self.cks_ids:list[int] = []
    
    def set_kernels(self, convolutional_kernels:dict[int, Convolutional_kernel_for_image]):
        self.convolutional_kernels = convolutional_kernels
        self.cks_ids = list(convolutional_kernels.keys())

    def get_copy_of_kernel_ids(self):
        return self.cks_ids.copy()

    #`step` should not be `None`, however its default value is `None` for consistency with the default values of the other "get range parameters"
    def order_kernels(self, order_type: Enum_order = Enum_order.ascending, start:int=None, end:int=None, step:int=None):
        
        if(step == 0 or step is None or len(cks_ids) <= 1):
            return
        cks_ids = np.array(self.cks_ids)

        #order the ids of the kernels
        if(order_type == Enum_order.ascending):
            random.shuffle(cks_ids[start:end:step])
        elif(order_type == Enum_order.descending):
            cks_ids[start:end:step] = cks_ids.sort(cks_ids[start:end:step])
        elif(order_type == Enum_order.random):
            cks_ids[start:end:step] = cks_ids.sort(cks_ids[start:end:step])[::-1]
        
        #make sure the order is not reversed when the step is negative
        if(step<0):
            cks_ids[start:end:step] = cks_ids[start:end:step][::-1]

        self.cks_ids = list[cks_ids]
    
    def transform_image_0(self, img:np.ndarray[np.uint8]) -> np.ndarray:
        
        for ck_id in self.cks_ids:
            img = self.convolutional_kernels[ck_id].transform_image(img=img)
        
        return img

    def transform_image_1(self, img:np.ndarray[np.uint8], cks_count_to_process:int=1) -> np.ndarray:
        
        for ck_id in self.cks_ids:
            
            self.convolutional_kernels[ck_id].transform_image(img=img)
            cks_count_to_process -= 1
            if(cks_count_to_process <= 0):
                break
        
        return img

    def transform_image_2(self, img:np.ndarray[np.uint8], cks_ids:list[int]) -> np.ndarray:

        for ck_id in cks_ids:
            
            if(ck_id in self.convolutional_kernels.keys()):
                self.convolutional_kernels[ck_id].transform_image(img=img)
            
        return img
                
        