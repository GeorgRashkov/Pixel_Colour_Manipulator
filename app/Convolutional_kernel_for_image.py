import numpy as np

from Convolutional_kernel_for_rgb_channel import Convolutional_kernel_for_rgb_channel
from Dynamic_variable import Dynamic_variable

from Enums import Enum__rgb_channels

class Convolutional_kernel_for_image:

    #the convolutional filter parameters can be `None`; the convolutional filters must use the same dynamic variables
    def __init__(self, id:int, convolutional_kernel_r:Convolutional_kernel_for_rgb_channel, convolutional_kernel_g:Convolutional_kernel_for_rgb_channel, convolutional_kernel_b:Convolutional_kernel_for_rgb_channel):
        
        self.id = id
        self.convolutional_kernel_r:Convolutional_kernel_for_rgb_channel = convolutional_kernel_r
        self.convolutional_kernel_g:Convolutional_kernel_for_rgb_channel = convolutional_kernel_g
        self.convolutional_kernel_b:Convolutional_kernel_for_rgb_channel = convolutional_kernel_b
    
    #this is the main function for applying convolution on an image
    #this function must be called from outside
    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def transform_image(self, img:np.ndarray[np.uint8]):
        
        #this code might be need if the convolution changes the image size 
        """"
        img_h = min(red_convolution.shape[0], green_convolution.shape[0], blue_convolution.shape[0])
        img_w = min(red_convolution.shape[1], green_convolution.shape[1], blue_convolution.shape[1])
        convolved_image = np.dstack((red_convolution[:img_h, :img_w], green_convolution[:img_h, :img_w], blue_convolution[:img_h, :img_w]))
        """

        dynamic_variables:list[Dynamic_variable] = []

        #applies convolution to the red channel
        if(self.convolutional_kernel_r is not None):
            
            if(self.convolutional_kernel_b is not None):
                dynamic_variables = self.convolutional_kernel_b.get_dynamic_variables()
                self.convolutional_kernel_r.set_dynamic_variables(dynamic_variables=dynamic_variables)
            
            elif(self.convolutional_kernel_g is not None):
                dynamic_variables = self.convolutional_kernel_g.get_dynamic_variables()
                self.convolutional_kernel_r.set_dynamic_variables(dynamic_variables=dynamic_variables)
            
            input_rgb_channel_values = self.get_rgb_channel_values(img=img, rgb_channel=self.convolutional_kernel_r.input_rgb_channel)
            img[:,:,0] = self.convolutional_kernel_r.apply_convolution_to_color_channel(rgb_channel_values=input_rgb_channel_values)


        #applies convolution to the green channel
        if(self.convolutional_kernel_g is not None):

            if(self.convolutional_kernel_r is not None):
                dynamic_variables = self.convolutional_kernel_r.get_dynamic_variables()
                self.convolutional_kernel_g.set_dynamic_variables(dynamic_variables=dynamic_variables)
            
            elif(self.convolutional_kernel_b is not None):
                dynamic_variables = self.convolutional_kernel_b.get_dynamic_variables()
                self.convolutional_kernel_g.set_dynamic_variables(dynamic_variables=dynamic_variables)
            
            input_rgb_channel_values = self.get_rgb_channel_values(img=img, rgb_channel=self.convolutional_kernel_g.input_rgb_channel)
            img[:,:,1] = self.convolutional_kernel_g.apply_convolution_to_color_channel(rgb_channel_values=input_rgb_channel_values)


        #applies convolution to the blue channel
        if(self.convolutional_kernel_b is not None):
            
            if(self.convolutional_kernel_g is not None):
                dynamic_variables = self.convolutional_kernel_g.get_dynamic_variables()
                self.convolutional_kernel_b.set_dynamic_variables(dynamic_variables=dynamic_variables)
            
            elif(self.convolutional_kernel_r is not None):
                dynamic_variables = self.convolutional_kernel_r.get_dynamic_variables()
                self.convolutional_kernel_b.set_dynamic_variables(dynamic_variables=dynamic_variables)
            
            input_rgb_channel_values = self.get_rgb_channel_values(img=img, rgb_channel=self.convolutional_kernel_b.input_rgb_channel)
            img[:,:,2] = self.convolutional_kernel_b.apply_convolution_to_color_channel(rgb_channel_values=input_rgb_channel_values)
    


    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    #The ouput is a "numpy.ndarray" with shape of (Height, Width, 1)
    def get_rgb_channel_values(self, img:np.ndarray[np.uint8], rgb_channel:Enum__rgb_channels) -> np.ndarray[np.uint8]:
        
        input_rgb_channel_values = None
        
        if(rgb_channel == Enum__rgb_channels.r):
            input_rgb_channel_values = img[:,:,0]
        elif(rgb_channel == Enum__rgb_channels.g):
            input_rgb_channel_values = img[:,:,1]
        elif(rgb_channel == Enum__rgb_channels.b):
            input_rgb_channel_values = img[:,:,2]
        
        return input_rgb_channel_values