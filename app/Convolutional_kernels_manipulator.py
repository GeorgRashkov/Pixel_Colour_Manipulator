import numpy as np

from Convolutional_kernel_for_image import Convolutional_kernel_for_image

from Order_obj import Order_obj

from Number_operatios import order_numbers

class Convolutional_kernels_manipulator:
    
    def __init__(self):
        self.convolutional_kernels:dict[int, Convolutional_kernel_for_image] = {} 
        self.cks_ids:list[int] = []
    
    def set_kernels(self, convolutional_kernels:dict[int, Convolutional_kernel_for_image]):
        self.convolutional_kernels = convolutional_kernels
        self.cks_ids = list(convolutional_kernels.keys())

    def get_copy_of_kernel_ids(self):
        return self.cks_ids.copy()

    def order_kernels(self, order_obj: Order_obj):
        self.cks_ids = order_numbers(nums=self.cks_ids, order_type=order_obj.order_type, start=order_obj.start, end=order_obj.end, step=order_obj.step)
        
    
    def transform_image_0(self, img:np.ndarray[np.uint8]) -> np.ndarray:
        
        for ck_id in self.cks_ids:
            img = self.convolutional_kernels[ck_id].transform_image(img=img)
        
        return img

    def transform_image_1(self, img:np.ndarray[np.uint8], cks_count_to_process:int=1) -> np.ndarray:
        
        for ck_id in self.cks_ids:

            if(cks_count_to_process <= 0):
                break
            
            self.convolutional_kernels[ck_id].transform_image(img=img)
            cks_count_to_process -= 1
        
        return img

    def transform_image_2(self, img:np.ndarray[np.uint8], cks_ids:list[int]) -> np.ndarray:

        for ck_id in cks_ids:
            
            if(ck_id in self.convolutional_kernels.keys()):
                self.convolutional_kernels[ck_id].transform_image(img=img)
            
        return img
                
        