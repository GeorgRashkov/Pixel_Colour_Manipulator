import numpy as np
from typing import Callable


from Convolutional_kernel_parameters import Convolutional_kernel_parameters
from Dynamic_variable import Dynamic_variable

from Enums import Enum__rgb_channels, get_Enum__image_pad_modes__as_string

class Convolutional_kernel_for_rgb_channel:
    # `values` must be a numpy array which has width and heigh, containing all the values of the kernel (both hole values and non hole values)
    #each list in `non_hole_values` must have the same number of floats
    # `non_hole_values_as_formulas` can contain `None` values and it must have the same shape as `non_hole_values`;
    #`non_hole_values_as_formulas_row_indexes` must contain the row indexes in `non_hole_values_as_formulas` where the values of `non_hole_values_as_formulas` are not `None`
    #`non_hole_values_as_formulas_column_indexes` must contain the column indexes in `non_hole_values_as_formulas` where the values of `non_hole_values_as_formulas` are not `None`
    def __init__(self, c_k_parameters: Convolutional_kernel_parameters, is_hole_content_formula:bool,
                 values:np.ndarray, non_hole_values:list[list[float]], row_indexes_of__non_hole_values_in_values:list[int], column_indexes_of__non_hole_values_in_values:list[int],
                 non_hole_values_as_formulas:list[list[Callable[[list[float]], float]]], row_indexes_of__non_hole_values_as_formulas:list[int], column_indexes_of__non_hole_values_as_formulas:list[int],
                 dynamic_variables:list[Dynamic_variable], dynamic_variables_values:list[float]):
        
        #<convolutional kernel parameters
        self.c_k_parameters:Convolutional_kernel_parameters = c_k_parameters

        self.max_height = 999
        self.max_width = 999

        self.height:int = 0
        self.width:int = 0

        self.dilation_height:int = 0
        self.dilation_width:int = 0

        self.stride_height:int = 0
        self.stride_width:int = 0

        self.hole_height:int = 0
        self.hole_width:int = 0
        self.vertical_hole_frequency:int = 0
        self.horizontal_hole_frequency:int = 0
        self.hole_content:float = 0

        self.min_kernel_value:float = 0
        self.max_kernel_value:float = 0

        self.min_hole_value:float = 0
        self.max_hole_value:float = 0

        self.move_x:float = 0
        self.move_y:float = 0

        self.convolutions_count:float = 0

        self.image_pad_mode:int = 0

            #<frequencies
        # each frequency is intialized with the user formula; 
        # after that when code execution reaches the frequency, the frequency will be lowered by one
        # when the frequency is equal to zero, the frequency will be intialized again with the user formula; 
        # each frequency is connected to another kernel property
        # the kernel properties which have a frequency will be intialized again with the user formula only when their frequency is equal to 0
        # each frequency has a corresponding boolean value indicating whether the frequency will be used
        # if that boolean value is equal to `False` then the frequency will never change as well as the kernel property which uses the frequency

        self.frequency__move_x:int = 0
        self.frequency__move_y:int = 0

        self.frequency__recreate_kernel:int = 0
        self.frequency__update_kernel_values:int = 0
        self.frequency__update_kernel_hole_values:int = 0

        self.frequency__update_dynamic_variables__using_kernel_value:int = 0
        self.frequency__update_dynamic_variables__using_kernel_hole_row:int = 0
        self.frequency__update_dynamic_variables_using_kernel_hole_column:int = 0
        
        self.frequency__update_dynamic_variables__while_processing_rgb_channel:int = 0
        self.frequency__update_dynamic_variables__after_processing_rgb_channel:int = 0

        self.should_update_move_x:bool = self.c_k_parameters.should_update_move_x
        self.should_update_move_y:bool = self.c_k_parameters.should_update_move_y

        self.should_recreate_kernel:bool = self.c_k_parameters.should_recreate_kernel
        self.should_update_kernel_values:bool = self.c_k_parameters.should_update_kernel_values
        self.should_update_kernel_hole_values:bool = self.c_k_parameters.should_update_kernel_hole_values

        self.should_update_dynamic_variables__using_kernel_value:bool = self.c_k_parameters.should_update_dynamic_variables__using_kernel_value
        self.should_update_dynamic_variables__using_kernel_hole_row:bool = self.c_k_parameters.should_update_dynamic_variables__using_kernel_hole_row
        self.should_update_dynamic_variables__using_kernel_hole_column:bool = self.c_k_parameters.should_update_dynamic_variables__using_kernel_hole_column
        
        self.should_update_dynamic_variables__while_processing_rgb_channel:bool = self.c_k_parameters.should_update_dynamic_variables__while_processing_rgb_channel
        self.should_update_dynamic_variables__after_processing_rgb_channel:bool = self.c_k_parameters.should_update_dynamic_variables__after_processing_rgb_channel
        
            #frequencies>

        self.process_image_fast:bool = self.c_k_parameters.process_image_fast

        self.input_rgb_channel:Enum__rgb_channels = self.c_k_parameters.input_rgb_channel

        self.update_convolutional_kernel_parameters()
        #convolutional kernel parameters>

        self.is_hole_content_formula:bool = is_hole_content_formula

        #<convolutional kernel values
        self.values = values #it represents the kernel because it contains all kernel values including non hole values and hole values (stride and dilation are not part of it) 
        self.non_hole_values = non_hole_values #contains only non hole values
        self.row_indexes_of__non_hole_values_in_values = row_indexes_of__non_hole_values_in_values #contains the row indexes in `values` where the value is a non hole value
        self.column_indexes_of__non_hole_values_in_values = column_indexes_of__non_hole_values_in_values #contains the column indexes in `values` where the value is a non hole value
        
        #contains the user defined formulas which are used to obtain the values in the collection of non hole values; 
        #if the user entered just a number instead of an expression then the collection will add the value `None` instead of a lambda funtion;
        #it has the same shape as `non_hole_values`
        self.non_hole_values_as_formulas = non_hole_values_as_formulas 
        
        self.row_indexes_of__non_hole_values_as_formulas = row_indexes_of__non_hole_values_as_formulas #contains the row indexes inside `non_hole_values` where the values are obtained by user defined formula
        self.column_indexes_of__non_hole_values_as_formulas = column_indexes_of__non_hole_values_as_formulas #contains the column indexes inside `non_hole_values` where the values are obtained by user defined formula
        #convolutional kernel values>

        #<dynamic variables
        self.dynamic_variables:list[Dynamic_variable] = dynamic_variables
        self.dynamic_variables_values:list[float] = dynamic_variables_values
        #dynamic variables>
    
    
    #<functions for updating convolutional kernel values and parameters
    
    #this function is the entry point for updating the kernel
    #the other functions for updating convolutional kernel values and parameters should not be called directly because they will be executed when this function executes
    def recreate_kernel(self):

        self.update_move_x()
        self.update_move_y()

        if(self.should_recreate_kernel == True):
            if(self.frequency__recreate_kernel <= 0):
                self.update_convolutional_kernel_parameters()
                self.frequency__recreate_kernel = self.c_k_parameters.get__frequency__recreate_kernel(v = self.dynamic_variables_values)
            else:
                self.frequency__recreate_kernel -= 1
        
        if(self.should_update_kernel_values == True):
            if(self.frequency__update_kernel_values <= 0):
                self.update_convolutional_kernel_values()
                self.frequency__update_kernel_values = self.c_k_parameters.get__frequency__update_kernel_values(v = self.dynamic_variables_values)
            else:
                self.frequency__update_kernel_values -= 1
        
        if(self.should_update_kernel_hole_values == True):
            if(self.frequency__update_kernel_hole_values <= 0):
                self.update_convolutional_kernel_hole_values()
                self.frequency__update_kernel_hole_values = self.c_k_parameters.get__frequency__update_kernel_hole_values(v = self.dynamic_variables_values)
            else:
                self.frequency__update_kernel_hole_values -= 1

    #function for updating move behaviour of the kernel on the x axis
    def update_move_x(self):
        
        if(self.should_update_move_x == True):
            if(self.frequency__move_x <= 0):
                self.move_x = self.c_k_parameters.move_x(self.dynamic_variables_values)
                self.frequency__move_x = self.c_k_parameters.get__frequency__move_x(v=self.dynamic_variables_values)
            else:
                self.frequency__move_x -= 1
    
    #function for updating move behaviour of the kernel on the y axis
    def update_move_y(self):
        
        if(self.should_update_move_y == True):
            if(self.frequency__move_y <= 0):
                self.move_y = self.c_k_parameters.move_y(self.dynamic_variables_values)
                self.frequency__move_y = self.c_k_parameters.get__frequency__move_y(v=self.dynamic_variables_values)
            else:
                self.frequency__move_y -= 1

    
    def update_convolutional_kernel_parameters(self):

        height = self.c_k_parameters.get__height(v = self.dynamic_variables_values)
        width = self.c_k_parameters.get__width(v = self.dynamic_variables_values)

        self.dilation_height = self.c_k_parameters.get__dilation_height(v = self.dynamic_variables_values)
        self.dilation_width = self.c_k_parameters.get__dilation_width(v = self.dynamic_variables_values)

        self.stride_height = self.c_k_parameters.get__stride_height(v = self.dynamic_variables_values)
        self.stride_width = self.c_k_parameters.get__stride_width(v = self.dynamic_variables_values)

        hole_height = self.c_k_parameters.get__hole_height(v = self.dynamic_variables_values)
        hole_width = self.c_k_parameters.get__hole_width(v = self.dynamic_variables_values)
        vertical_hole_frequency = self.c_k_parameters.get__vertical_hole_frequency(v = self.dynamic_variables_values)
        horizontal_hole_frequency = self.c_k_parameters.get__horizontal_hole_frequency(v = self.dynamic_variables_values)
        
        #make sure the kernel has proper values when resized or when the size or frequency of the holes is changed
        if(self.height != height or self.width != width
           or self.hole_height != hole_height or self.hole_width != hole_width 
           or self.vertical_hole_frequency != vertical_hole_frequency or self.horizontal_hole_frequency != horizontal_hole_frequency):
            
            self.values = np.zeros([width, height])

            self.height = min(height, self.max_height)
            self.width = min(width, self.max_width)
            self.hole_height = hole_height
            self.hole_width = hole_width
            self.vertical_hole_frequency = vertical_hole_frequency
            self.horizontal_hole_frequency = horizontal_hole_frequency

            self.update_convolutional_kernel_hole_values()
        
        
        #no need to update those as they will be updated by the `recreate_kernel` function when it calls `update_convolutional_kernel_hole_values`
        """
        self.hole_content = self.c_k_parameters.get__hole_content(v = self.dynamic_variables_values)
        self.hole_content = self.fit__convolutional_kernel_value__in_range(value=self.hole_content)
        """

        self.min_kernel_value = self.c_k_parameters.get__min_kernel_value(v = self.dynamic_variables_values)
        self.max_kernel_value = self.c_k_parameters.get__max_kernel_value(v = self.dynamic_variables_values)

        self.min_hole_value = self.c_k_parameters.get__min_hole_value(v = self.dynamic_variables_values)
        self.max_hole_value = self.c_k_parameters.get__max_hole_value(v = self.dynamic_variables_values)

        #no need to update those as they will be updated by the `recreate_kernel` function when it calls `update_move_x` and `update_move_y`
        """
        self.move_x = self.c_k_parameters.get__move_x(v = self.dynamic_variables_values)
        self.move_y = self.c_k_parameters.get__move_y(v = self.dynamic_variables_values)
        """

        self.convolutions_count = self.c_k_parameters.get__convolutions_count(v = self.dynamic_variables_values)

        self.image_pad_mode = self.c_k_parameters.get__image_pad_mode(v = self.dynamic_variables_values)

        #no need to update those as they will be updated by the `recreate_kernel` function
        """
        self.frequency__move_x = self.c_k_parameters.get__frequency__move_x(v = self.dynamic_variables_values)
        self.frequency__move_y = self.c_k_parameters.get__frequency__move_y(v = self.dynamic_variables_values)
        
        self.frequency__recreate_kernel = self.c_k_parameters.get__frequency__recreate_kernel(v = self.dynamic_variables_values)
        self.frequency__update_kernel_values = self.c_k_parameters.get__frequency__update_kernel_values(v = self.dynamic_variables_values)
        self.frequency__update_kernel_hole_values = self.c_k_parameters.get__frequency__update_kernel_hole_values(v = self.dynamic_variables_values)
        """
        
         #no need to update those as they will be updated
        """
        self.frequency__update_dynamic_variables__using_kernel_value = self.c_k_parameters.get__frequency__update_dynamic_variables__using_kernel_value(v = self.dynamic_variables_values)
        self.frequency__update_dynamic_variables__using_kernel_hole_row = self.c_k_parameters.get__frequency__update_dynamic_variables__using_kernel_hole_row(v = self.dynamic_variables_values)
        self.frequency__update_dynamic_variables_using_kernel_hole_column = self.c_k_parameters.get__frequency__update_dynamic_variables_using_kernel_hole_column(v = self.dynamic_variables_values)
        
        self.frequency__update_dynamic_variables__while_processing_rgb_channel = self.c_k_parameters.get__frequency__update_dynamic_variables__while_processing_rgb_channel(v = self.dynamic_variables_values)
        self.frequency__update_dynamic_variables__after_processing_rgb_channel = self.c_k_parameters.get__frequency__update_dynamic_variables__after_processing_rgb_channel(v = self.dynamic_variables_values)
        """






    """
    def update_convolutional_kernel_hole_values_v1(self):

        non_hole_values_rows_count = len(self.non_hole_values)
        non_hole_values_columns_count = len(self.non_hole_values[0])

        values_columns_count = self.values.shape[1]

        vertical_hole_frequency = self.vertical_hole_frequency
        horizontal_hole_frequency = self.horizontal_hole_frequency

        values_row = 0
        values_column = 0
        
        for non_hole_values_row in range(0, non_hole_values_rows_count):
            
            vertical_hole_frequency -= 1 

            #<creates a vertical hole; the vertical hole has width and height; the vertical hole height is specified by the hole height while the vertical hole width is specified by the kernel values width
            if(vertical_hole_frequency <= 0):
                
                for vertical_hole_row in range(0, self.hole_height):
                    
                    for values_col in range(0, values_columns_count):

                        self.update__hole_content_value()
                        self.values[values_row][values_col] = self.hole_content                      
                        self.update_dynamic_variables__using_kernel_hole_row()

                    values_row+=1
                
                vertical_hole_frequency = self.vertical_hole_frequency
            #creates a vertical hole; the vertical hole has width and height; the vertical hole height is specified by the hole height while the vertical hole width is specified by the kernel values width>

            values_column = 0

            for non_hole_values_column in range(0, non_hole_values_columns_count):
                
                horizontal_hole_frequency -= 1 

                #<creates a horizontal hole; the horizontal hole has width; the horizontal hole width is specified by the hole width
                if(horizontal_hole_frequency <= 0):

                    for hole_values_column in range(0, self.hole_width):

                        self.update__hole_content_value()
                        self.values[values_row][values_column] = self.hole_content
                        self.update_dynamic_variables__using_kernel_hole_column()

                        values_column += 1
                    
                    horizontal_hole_frequency = self.horizontal_hole_frequency
                #creates a horizontal hole; the horizontal hole has width; the horizontal hole width is specified by the hole width>

                self.values[values_row][values_column] = self.non_hole_values[non_hole_values_row][non_hole_values_column]
                values_column += 1
            
            values_row+=1 
    """

    def update_convolutional_kernel_hole_values(self):

        non_hole_values_rows_count = len(self.non_hole_values)
        non_hole_values_columns_count = len(self.non_hole_values[0])

        kernel_row = 0
        kernel_column = 0

        updated_indexes_for__row_indexes_of__non_hole_values_in_values:list[int] = []
        updated_indexes_for__column_indexes_of__non_hole_values_in_values:list[int] = []
        
        for non_hole_values_row in range(0, non_hole_values_rows_count):

            #<creates a vertical hole; the vertical hole has width and height; the vertical hole height is specified by the hole height while the vertical hole width is specified by the kernel values width
            if(self.vertical_hole_frequency <= 0):
                
                for vertical_hole_row in range(0, self.hole_height):
                    
                    if(kernel_row >= self.height):
                        break

                    for values_col in range(0, self.width):

                        self.update__hole_content_value()
                        self.values[kernel_row, values_col] = self.hole_content                      
                        self.update_dynamic_variables__using_kernel_hole_row()

                    kernel_row+=1
                
                self.vertical_hole_frequency = self.c_k_parameters.get__vertical_hole_frequency(v=self.dynamic_variables_values)
            
            self.vertical_hole_frequency -= 1 
            #creates a vertical hole; the vertical hole has width and height; the vertical hole height is specified by the hole height while the vertical hole width is specified by the kernel values width>

            if(kernel_row >= self.height):
                break

            kernel_column = 0

            for non_hole_values_column in range(0, non_hole_values_columns_count):
                
                self.horizontal_hole_frequency -= 1 

                #<creates a horizontal hole; the horizontal hole has width; the horizontal hole width is specified by the hole width
                if(self.horizontal_hole_frequency <= 0):

                    for hole_values_column in range(0, self.hole_width):
                        
                        if(kernel_column > self.width):
                            break

                        self.update__hole_content_value()
                        self.values[kernel_row, kernel_column] = self.hole_content
                        self.update_dynamic_variables__using_kernel_hole_column()

                        kernel_column += 1
                    
                    self.horizontal_hole_frequency = self.c_k_parameters.get__horizontal_hole_frequency(v=self.dynamic_variables_values)
                #creates a horizontal hole; the horizontal hole has width; the horizontal hole width is specified by the hole width>

                updated_indexes_for__row_indexes_of__non_hole_values_in_values.append(kernel_row)
                updated_indexes_for__column_indexes_of__non_hole_values_in_values.append(kernel_column)
                self.values[kernel_row, kernel_column] = self.non_hole_values[non_hole_values_row][non_hole_values_column]

                kernel_column += 1
                if(kernel_column > self.width):
                    break
            
            kernel_row+=1 
            if(kernel_row >= self.height):
                break
        
        self.row_indexes_of__non_hole_values_in_values = updated_indexes_for__row_indexes_of__non_hole_values_in_values
        self.column_indexes_of__non_hole_values_in_values = updated_indexes_for__column_indexes_of__non_hole_values_in_values


    def update__hole_content_value(self):

        if(self.is_hole_content_formula == True):
            hole_content = self.c_k_parameters.get__hole_content(v = self.dynamic_variables_values)
            self.hole_content = self.fit__convolutional_kernel_value__in_range(value=hole_content, is_hole_value=True)

    
    
    def update_convolutional_kernel_values(self):
        
        for row in self.row_indexes_of__non_hole_values_as_formulas:
            for column in self.column_indexes_of__non_hole_values_as_formulas:
                self.non_hole_values[row][column] = self.get__convolutional_kernel_value(kernel_values__row=row, kernel_values__column=column)
                
                self.update_dynamic_variables__using_kernel_value()
        
        for non_hole_values_row in self.row_indexes_of__non_hole_values_in_values:
            for non_hole_values_column in self.column_indexes_of__non_hole_values_in_values:
                
                kernel_row = self.row_indexes_of__non_hole_values_in_values[non_hole_values_row]
                kernel_column = self.column_indexes_of__non_hole_values_in_values[non_hole_values_column]
                
                self.values[kernel_row, kernel_column] = self.non_hole_values[non_hole_values_row, non_hole_values_column]
    
    #functions for updating convolutional kernel values and parameters>

    def get__convolutional_kernel_value(self, kernel_values__row:int, kernel_values__column:int) -> float:
        
        kernel_value = 0
        try:
            kernel_value = self.non_hole_values_as_formulas[kernel_values__row][kernel_values__column](self.dynamic_variables_values)
        except ZeroDivisionError:
            return 0

        kernel_value = self.fit__convolutional_kernel_value__in_range(value=kernel_value, is_hole_value=False)
        return kernel_value
    
    
        
        

    def fit__convolutional_kernel_value__in_range(self, value: float, is_hole_value:bool) -> float:
        
        min_value = self.min_hole_value if is_hole_value==True else self.min_kernel_value
        max_value = self.max_hole_value if is_hole_value==True else self.max_kernel_value

        if(value < min_value):
            
            if( max_value > -0.000_001 and max_value < 0.000_001):
                value = max_value
            else:
                value %= max_value
        
        elif(value > max_value):
            
            if( min_value > -0.000_001 and min_value < 0.000_001 ):
                value = min_value
            else:
                value %= min_value
        
        return value
    
    




    #<functions for updating dynamic variables


    def update_dynamic_variables_values(self):

        updated_values_for_dynamic_variables:list[float] = []

        for dynamic_variable in self.dynamic_variables:
            
            dynamic_variable_updated_value = dynamic_variable.get_variable(v=self.dynamic_variables_values)
            
            updated_values_for_dynamic_variables.append(dynamic_variable_updated_value)

            dynamic_variable.update_frequency()
        
        if(len(updated_values_for_dynamic_variables)>0):
            self.dynamic_variables_values = updated_values_for_dynamic_variables
        else:
            self.dynamic_variables_values = [0]
    
    
    def update_dynamic_variables__using_kernel_value(self):
        
        if(self.should_update_dynamic_variables__using_kernel_value == True):
            if(self.frequency__update_dynamic_variables__using_kernel_value <= 0):
                self.update_dynamic_variables_values()
                self.frequency__update_dynamic_variables__using_kernel_value = self.c_k_parameters.get__frequency__update_dynamic_variables__using_kernel_value(v=self.dynamic_variables_values)
            else:
                self.frequency__update_dynamic_variables__using_kernel_value -= 1

    def update_dynamic_variables__using_kernel_hole_row(self):
        
        if(self.should_update_dynamic_variables__using_kernel_hole_row == True):
            if(self.frequency__update_dynamic_variables__using_kernel_hole_row <= 0):
                self.update_dynamic_variables_values()
                self.frequency__update_dynamic_variables__using_kernel_hole_row = self.c_k_parameters.get__frequency__update_dynamic_variables__using_kernel_hole_row(v=self.dynamic_variables_values) 
            else:
                self.frequency__update_dynamic_variables__using_kernel_hole_row -= 1

    def update_dynamic_variables__using_kernel_hole_column(self):
        
        if(self.should_update_dynamic_variables__using_kernel_hole_column == True):
            if(self.frequency__update_dynamic_variables_using_kernel_hole_column <= 0):
                self.update_dynamic_variables_values()
                self.frequency__update_dynamic_variables_using_kernel_hole_column = self.c_k_parameters.get__frequency__update_dynamic_variables_using_kernel_hole_column(v=self.dynamic_variables_values)
            else:
                self.frequency__update_dynamic_variables_using_kernel_hole_column -= 1

    def update_dynamic_variables__while_processing_rgb_channel(self):
        
        if(self.should_update_dynamic_variables__while_processing_rgb_channel == True):
            if(self.frequency__update_dynamic_variables__while_processing_rgb_channel <= 0):
                self.update_dynamic_variables_values()
                self.frequency__update_dynamic_variables__while_processing_rgb_channel = self.c_k_parameters.get__frequency__update_dynamic_variables__while_processing_rgb_channel(v=self.dynamic_variables_values)
            else:
                self.frequency__update_dynamic_variables__while_processing_rgb_channel -= 1
    
    def update_dynamic_variables__after_processing_rgb_channel(self):
        
        if(self.should_update_dynamic_variables__after_processing_rgb_channel == True):
            if(self.frequency__update_dynamic_variables__after_processing_rgb_channel <= 0):
                self.update_dynamic_variables_values()
                self.frequency__update_dynamic_variables__after_processing_rgb_channel = self.c_k_parameters.get__frequency__update_dynamic_variables__after_processing_rgb_channel(v=self.dynamic_variables_values)
            else:
                self.frequency__update_dynamic_variables__after_processing_rgb_channel -= 1


    #functions for updating dynamic variables>




    #this function must be called from outside
    def set_dynamic_variables(self, dynamic_variables:list[Dynamic_variable]):
        self.dynamic_variables = dynamic_variables
    
    #this function must be called from outside
    def get_dynamic_variables(self):
        return self.dynamic_variables
    

    #<functions for applying convolution to colour channel

    #this function must be called from outside
    def apply_convolution_to_color_channel(self, channel_values: np.ndarray) -> np.ndarray:

        if(self.values.shape[0]==0 or self.values.shape[1]==0):#if the kernel has 0 columns or 0 rows - return the input channel values unchanged
            return channel_values

        img_height, img_width = channel_values.shape
        kernel_height, kernel_width = self.values.shape

        dilated_kernel_height = (kernel_height - 1) * self.dilation_height + 1#this is the heigh which the kernel will have after adding the dilation (the holes) to it
        dilated_kernel_width = (kernel_width - 1) * self.dilation_width + 1#this is the width which the kernel will have after adding the dilation (the holes) to it

        # Calculate necessary padding to maintain same output size
        #padding makes sure the image size of the convolved image will always be equal to the size of the original image no matter the values of (stride, dilation, image/kernel width/height)
        image_pad_y = ((img_height - 1) * self.stride_height + dilated_kernel_height - img_height) // 2 + 1 #this is the number of pixel values to add above and below the image;
        image_pad_x = ((img_width - 1) * self.stride_width + dilated_kernel_width - img_width) // 2 + 1 #this is the number of pixel values to add left and right the image;

        image_pad_mode = get_Enum__image_pad_modes__as_string(num=self.image_pad_mode)

        # apply zero-padding to the image; 
        # the padded image will be the same as the original one but it will also have `pad_y` pixels (each with value 0) placed above and below the original image 
        # and it will also have `pad_x` pixels (each with value 0) placed left and right from the original image
        padded_image = np.pad(channel_values, ((image_pad_y, image_pad_y), (image_pad_x, image_pad_x)), mode=image_pad_mode)

        while(self.convolutions_count > 0):

            if(self.process_image_fast == True):
                padded_image = self.apply_convolution_to_color_channel_fast(padded_image=padded_image, dilated_kernel_height=dilated_kernel_height, dilated_kernel_width=dilated_kernel_width)
            else:
                padded_image = self.apply_convolution_to_color_channel_slow(padded_image=padded_image, original_image_height=img_height, original_image_width=img_width, dilated_kernel_height=dilated_kernel_height, dilated_kernel_width=dilated_kernel_width)

            self.convolutions_count-=1
        
        self.convolutions_count = self.c_k_parameters.get__convolutions_count(v = self.dynamic_variables_values)
        self.update_dynamic_variables__after_processing_rgb_channel()

        return padded_image


    def apply_convolution_to_color_channel_fast(self, padded_image: np.ndarray, dilated_kernel_height:int, dilated_kernel_width:int) -> np.ndarray:

        #takes every possible image area from the padded image where the width and height of the area is equal to the width and height of the dilated kernel
        image_areas = np.lib.stride_tricks.sliding_window_view(
            padded_image,
            (dilated_kernel_height, dilated_kernel_width)
        )

        #don't delete the next comment - it might be needed
        """
        #apply stride and dilation to the image areas 
        image_areas = image_areas[
            ::self.stride_height,      # image area height
            ::self.stride_width,      # image area width
            ::self.dilation_height,    # rows containing image areas
            ::self.dilation_width     # columns containing image areas
        ]
        """

        #apply stride and dilation to the image areas 
        image_areas = image_areas[
            ::self.stride_height,                   # image area height
            ::self.stride_width,                    # image area width
            ::self.dilation_height+self.move_y,     # rows containing image areas
            ::self.dilation_width+self.move_x       # columns containing image areas
        ]

        
        #the string parameter in `np.einsum` represents the dimetions of the second parameter, the third parameter and the array which the function returns:
        # the first letters before the comma are used to name the dimensions of the second parameter (`image_areas`);
        # the values between the comma and the arrow specify the demensions of the second and the third parameter which will be used for perform a (element-by-element) multiplication
        # the values after the arrow indicate the dimesions of the second parameter which will be preserved in the array (a value in the output array is obtained from the summation of the element-by-element multiplication) which the function returns
        #Apply the kernel to the image areas:
        #take the image areas on every row and column (every row and column is specified with `ij`); 
        #multiply the curent image area (element-by-element) with the kernel - the demensions which will be used for the element-by-element multiplication for both the current image area and the kernel are specified by `kl`;
        #sum the multipliaction and store the result from the sumation in the output image at index [i,j] specified by the values after the arrow
        output = np.einsum(
            "ijkl,kl->ij",
            image_areas,
            self.values
        )

        self.recreate_kernel()
        self.update_dynamic_variables__while_processing_rgb_channel()

        return output
    
    def apply_convolution_to_color_channel_slow(self, padded_image: np.ndarray, original_image_height:int, original_image_width:int, dilated_kernel_height:int, dilated_kernel_width:int) -> np.ndarray:

        # Output dimensions
        out_height = original_image_height
        out_width = original_image_width
        output = np.zeros((out_height, out_width))

        # Perform convolution
        for y in range(out_height):
            for x in range(out_width):
                
                x += self.move_x
                y += self.move_y

                image_area = padded_image[
                    y * self.stride_height : y * self.stride_height + dilated_kernel_height : self.dilation_height,
                    x * self.stride_width : x * self.stride_width + dilated_kernel_width : self.dilation_width
                ]

                # Handle edges where the image area is smaller than the kernel - occurs when the kernel goes outside the image (overlaps the left or bottom end of the padded image)
                if image_area.shape != self.values.shape:
                    
                    #if the heigh of the image area is equal to zero it means that the kernel is under the padded image (the top left corner of the kernel is placed below the bottom left corner of the padded image)  
                    if(image_area.shape[0] == 0):
                        return output
                    
                    #if the width of the image area is equal to zero it means that the kernel is located on the right of the padded image (the left corners of the kernel are located right from the right corners of the padded image)  
                    if(image_area.shape[1] == 0):
                        break

                    # Pad the region to match kernel size
                    region_padded = np.zeros_like(self.values)
                    region_padded[:image_area.shape[0], :image_area.shape[1]] = image_area
                    image_area = region_padded

                output[y, x] = np.sum(image_area * self.values)

                self.recreate_kernel()
                self.update_dynamic_variables__while_processing_rgb_channel()

        return output
    
    #functions for applying convolution to colour channel>
    




    """
    def apply_convolution_to_image(self, img: np.ndarray):
        
        if (self.rgb_kernels == None):
            return img

        rgb_kernels = self.rgb_kernels

        red_convolution = self.apply_convolution_to_color_channel(stride = rgb_kernels.r_kernel.stride, holes_count =rgb_kernels.r_kernel.holes_count, kernel_values = rgb_kernels.r_kernel.kernel_values, channel_values = img[:,:,0])
        green_convolution = self.apply_convolution_to_color_channel(stride = rgb_kernels.g_kernel.stride, holes_count = rgb_kernels.g_kernel.holes_count, kernel_values = rgb_kernels.g_kernel.kernel_values, channel_values = img[:,:,1])
        blue_convolution = self.apply_convolution_to_color_channel(stride = rgb_kernels.b_kernel.stride, holes_count = rgb_kernels.b_kernel.holes_count, kernel_values = rgb_kernels.b_kernel.kernel_values, channel_values = img[:,:,2])
        
        img_h = min(red_convolution.shape[0], green_convolution.shape[0], blue_convolution.shape[0])
        img_w = min(red_convolution.shape[1], green_convolution.shape[1], blue_convolution.shape[1])
        convolved_image = np.dstack((red_convolution[:img_h, :img_w], green_convolution[:img_h, :img_w], blue_convolution[:img_h, :img_w]))
        
        return convolved_image

    def apply_convolution_to_color_channel(self, stride: int, holes_count: int, kernel_values: np.ndarray, channel_values: np.ndarray) -> np.ndarray:
       
        if(kernel_values.shape[0]==0 or kernel_values.shape[1]==0):#if the kernel has 0 columns or 0 rows - return the input channel values unchanged
            return channel_values

        img_height, img_width = channel_values.shape
        kernel_height, kernel_width = kernel_values.shape

        dilation = holes_count + 1
        eff_height = (kernel_height - 1) * dilation + 1
        eff_width = (kernel_width - 1) * dilation + 1

        # Calculate necessary padding to maintain same output size
        pad_y = ((img_height - 1) * stride + eff_height - img_height) // 2
        pad_x = ((img_width - 1) * stride + eff_width - img_width) // 2

        # Apply zero-padding
        padded = np.pad(channel_values, ((pad_y, pad_y), (pad_x, pad_x)), mode='constant', constant_values=0)

        # Output dimensions
        out_height = img_height
        out_width = img_width
        output = np.zeros((out_height, out_width))


        windows = np.lib.stride_tricks.sliding_window_view(
            padded,
            kernel_values.shape
        )

        output = np.einsum(
            "ijkl,kl->ij",
            windows,
            kernel_values
        )
       
        return output
    """