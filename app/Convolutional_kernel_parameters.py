from typing import Callable

from Enums import Enum__rgb_channels

#Warning: do not use directly the fields which are lambda functions; use the methods in the class which call the lambda function fields
class Convolutional_kernel_parameters:

    def __init__(self, 
                  height:str, width:str, dilation_height:str, dilation_width:str, stride_height:str, stride_width:str, 
                  hole_height:str, hole_width:str, vertical_hole_frequency:str, horizontal_hole_frequency:str, hole_content:str,
                  min_kernel_value:str, max_kernel_value:str, min_hole_value:str, max_hole_value:str,
                  move_x:str, move_y:str,
                  convolutions_count:str, 
                  image_pad_mode:str, 
                  frequency__move_x:str, frequency__move_y:str,
                  recreate_kernel_frequency:str, frequency__update_kernel_values:str, frequency__update_kernel_hole_values:str,
                  frequency__update_dynamic_variables__using_kernel_value:str, frequency__update_dynamic_variables__using_kernel_hole_row:str, frequency__update_dynamic_variables_using_kernel_hole_column:str, 
                  frequency__update_dynamic_variables__while_processing_rgb_channel:str, frequency__update_dynamic_variables__after_processing_rgb_channel:str,
                  should_update_move_x:bool, should_update_move_y:bool,
                  should_recreate_kernel:bool, should_update_kernel_values:bool, should_update_kernel_hole_values:bool,
                  should_update_dynamic_variables__using_kernel_value:bool, should_update_dynamic_variables__using_kernel_hole_row:bool, should_update_dynamic_variables__using_kernel_hole_column:bool, 
                  should_update_dynamic_variables__while_processing_rgb_channel:bool, should_update_dynamic_variables__after_processing_rgb_channel:bool,
                  process_image_fast:bool,
                  input_rgb_channel:Enum__rgb_channels):
     

        self.height:Callable[[list[float]], float] = eval(f"lambda v=[0]: {height}")
        self.width:Callable[[list[float]], float] = eval(f"lambda v=[0]: {width}")

        self.dilation_height:Callable[[list[float]], float] = eval(f"lambda v=[0]: {dilation_height}")
        self.dilation_width:Callable[[list[float]], float] = eval(f"lambda v=[0]: {dilation_width}")

        self.stride_height:Callable[[list[float]], float] = eval(f"lambda v=[0]: {stride_height}")
        self.stride_width:Callable[[list[float]], float] = eval(f"lambda v=[0]: {stride_width}")

        self.hole_height:Callable[[list[float]], float] = eval(f"lambda v=[0]: {hole_height}")
        self.hole_width:Callable[[list[float]], float] = eval(f"lambda v=[0]: {hole_width}")
        self.vertical_hole_frequency:Callable[[list[float]], float] = eval(f"lambda v=[0]: {vertical_hole_frequency}")
        self.horizontal_hole_frequency:Callable[[list[float]], float] = eval(f"lambda v=[0]: {horizontal_hole_frequency}")
        self.hole_content:Callable[[list[float]], float] = eval(f"lambda v=[0]: {hole_content}")

        self.min_kernel_value:Callable[[list[float]], float] = eval(f"lambda v=[0]: {min_kernel_value}")
        self.max_kernel_value:Callable[[list[float]], float] = eval(f"lambda v=[0]: {max_kernel_value}")

        self.min_hole_value:Callable[[list[float]], float] = eval(f"lambda v=[0]: {min_hole_value}")
        self.max_hole_value:Callable[[list[float]], float] = eval(f"lambda v=[0]: {max_hole_value}")

        self.move_x:Callable[[list[float]], float] = eval(f"lambda v=[0]: {move_x}")
        self.move_y:Callable[[list[float]], float] = eval(f"lambda v=[0]: {move_y}")

        self.convolutions_count:Callable[[list[float]], float] = eval(f"lambda v=[0]: {convolutions_count}")

        self.image_pad_mode:Callable[[list[float]], float] = eval(f"lambda v=[0]: {image_pad_mode}")


        self.frequency__move_x:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__move_x}")
        self.frequency__move_y:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__move_y}")

        self.recreate_kernel_frequency:Callable[[list[float]], float] = eval(f"lambda v=[0]: {recreate_kernel_frequency}")
        self.frequency__update_kernel_values:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__update_kernel_values}")
        self.frequency__update_kernel_hole_values:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__update_kernel_hole_values}")

        self.frequency__update_dynamic_variables__using_kernel_value:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__update_dynamic_variables__using_kernel_value}")
        self.frequency__update_dynamic_variables__using_kernel_hole_row:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__update_dynamic_variables__using_kernel_hole_row}")
        self.frequency__update_dynamic_variables_using_kernel_hole_column:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__update_dynamic_variables_using_kernel_hole_column}")
        
        self.frequency__update_dynamic_variables__while_processing_rgb_channel:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__update_dynamic_variables__while_processing_rgb_channel}")
        self.frequency__update_dynamic_variables__after_processing_rgb_channel:Callable[[list[float]], float] = eval(f"lambda v=[0]: {frequency__update_dynamic_variables__after_processing_rgb_channel}")
        
        self.should_update_move_x:bool = should_update_move_x
        self.should_update_move_y:bool = should_update_move_y

        self.should_recreate_kernel:bool = should_recreate_kernel
        self.should_update_kernel_values:bool = should_update_kernel_values
        self.should_update_kernel_hole_values:bool = should_update_kernel_hole_values

        self.should_update_dynamic_variables__using_kernel_value:bool = should_update_dynamic_variables__using_kernel_value
        self.should_update_dynamic_variables__using_kernel_hole_row:bool = should_update_dynamic_variables__using_kernel_hole_row
        self.should_update_dynamic_variables__using_kernel_hole_column:bool = should_update_dynamic_variables__using_kernel_hole_column
        
        self.should_update_dynamic_variables__while_processing_rgb_channel:bool = should_update_dynamic_variables__while_processing_rgb_channel
        self.should_update_dynamic_variables__after_processing_rgb_channel:bool = should_update_dynamic_variables__after_processing_rgb_channel
        


        self.process_image_fast = process_image_fast

        self.input_rgb_channel:Enum__rgb_channels = input_rgb_channel
        

    def get__height(self, v:list[float]) -> int:
        try:
            height = max(1, int(self.height(v)) )
            return height
        except ZeroDivisionError:
            return 1
    
    def get__width(self, v:list[float]) -> int:
        try:
            width = max(1, int(self.width(v)) )
            return width
        except ZeroDivisionError:
            return 1
    
    def get__dilation_height(self, v:list[float]) -> int:
        try:
            dilation_height = max(1, int(self.dilation_height(v)) )
            return dilation_height
        except ZeroDivisionError:
            return 1
    
    def get__dilation_width(self, v:list[float]) -> int:
        try:
            dilation_width = max(1, int(self.dilation_width(v)) )
            return dilation_width
        except ZeroDivisionError:
            return 1
    
    def get__stride_height(self, v:list[float]) -> int:
        try:
            stride_height = max(1, int(self.stride_height(v)) )
            return stride_height
        except ZeroDivisionError:
            return 1
    
    def get__stride_width(self, v:list[float]) -> int:
        try:
            stride_width = max(1, int(self.stride_width(v)) )
            return stride_width
        except ZeroDivisionError:
            return 1
        


    def get__hole_height(self, v:list[float]) -> int:
        try:
            hole_height = max(0, int(self.hole_height(v)) )
            return hole_height
        except ZeroDivisionError:
            return 0
    
    def get__hole_width(self, v:list[float]) -> int:
        try:
            hole_width = max(0, int(self.hole_width(v)) )
            return hole_width
        except ZeroDivisionError:
            return 0
    
    def get__vertical_hole_frequency(self, v:list[float]) -> int:
        try:
            vertical_hole_frequency = max(0, int(self.vertical_hole_frequency(v)) )
            return vertical_hole_frequency
        except ZeroDivisionError:
            return 0
    
    def get__horizontal_hole_frequency(self, v:list[float]) -> int:
        try:
            horizontal_hole_frequency = max(0, int(self.horizontal_hole_frequency(v)) )
            return horizontal_hole_frequency
        except ZeroDivisionError:
            return 0
    
    def get__hole_content(self, v:list[float]) -> float:
        try:
            hole_content = self.hole_content(v)
            return hole_content
        except ZeroDivisionError:
            return 0
    


    def get__min_kernel_value(self, v:list[float]) -> float:
        try:
            min_kernel_value = self.min_kernel_value(v)
            return min_kernel_value
        except ZeroDivisionError:
            return 0
    
    def get__max_kernel_value(self, v:list[float]) -> float:
        try:
            max_kernel_value = self.max_kernel_value(v)
            return max_kernel_value
        except ZeroDivisionError:
            return 0
    

    def get__min_hole_value(self, v:list[float]) -> float:
        try:
            min_hole_value = self.min_hole_value(v)
            return min_hole_value
        except ZeroDivisionError:
            return 0
    
    def get__max_hole_value(self, v:list[float]) -> float:
        try:
            max_hole_value = self.max_hole_value(v)
            return max_hole_value
        except ZeroDivisionError:
            return 0
    

    def get__move_x(self, v:list[float]) -> int:
        try:
            move_x = int(self.move_x(v))
            return move_x
        except ZeroDivisionError:
            return 0
    
    def get__move_y(self, v:list[float]) -> int:
        try:
            move_y = int(self.move_y(v))
            return move_y
        except ZeroDivisionError:
            return 0
    

    def get__convolutions_count(self, v:list[float]) -> int:
        try:
            convolutions_count = max(1, int(self.convolutions_count(v)) )
            return convolutions_count
        except ZeroDivisionError:
            return 0
    

    def get__image_pad_mode(self, v:list[float]) -> int:
        try:
            image_pad_mode = int(self.image_pad_mode(v))
            return image_pad_mode
        except ZeroDivisionError:
            return 0
    


    def get__frequency__move_x(self, v:list[float]) -> int:
        try:
            frequency__move_x = max(0, int(self.frequency__move_x(v)) )
            return frequency__move_x
        except ZeroDivisionError:
            return 0
    
    def get__frequency__move_y(self, v:list[float]) -> int:
        try:
            frequency__move_y = max(0, int(self.frequency__move_y(v)) )
            return frequency__move_y
        except ZeroDivisionError:
            return 0
    

    def get__frequency__recreate_kernel(self, v:list[float]) -> int:
        try:
            recreate_kernel_frequency = max(0, int(self.recreate_kernel_frequency(v)) )
            return recreate_kernel_frequency
        except ZeroDivisionError:
            return 0
    
    def get__frequency__update_kernel_values(self, v:list[float]) -> int:
        try:
            frequency__update_kernel_values = max(0, int(self.frequency__update_kernel_values(v)) )
            return frequency__update_kernel_values
        except ZeroDivisionError:
            return 0
    
    def get__frequency__update_kernel_hole_values(self, v:list[float]) -> int:
        try:
            frequency__update_kernel_hole_values = max(0, int(self.frequency__update_kernel_hole_values(v)) )
            return frequency__update_kernel_hole_values
        except ZeroDivisionError:
            return 0


    def get__frequency__update_dynamic_variables__using_kernel_value(self, v:list[float]) -> int:
        try:
            frequency__update_dynamic_variables__using_kernel_value = max(0, int(self.frequency__update_dynamic_variables__using_kernel_value(v)) )
            return frequency__update_dynamic_variables__using_kernel_value
        except ZeroDivisionError:
            return 0
    
    def get__frequency__update_dynamic_variables__using_kernel_hole_row(self, v:list[float]) -> int:
        try:
            frequency__update_dynamic_variables__using_kernel_hole_row = max(0, int(self.frequency__update_dynamic_variables__using_kernel_hole_row(v)) )
            return frequency__update_dynamic_variables__using_kernel_hole_row
        except ZeroDivisionError:
            return 0
    
    def get__frequency__update_dynamic_variables_using_kernel_hole_column(self, v:list[float]) -> int:
        try:
            frequency__update_dynamic_variables_using_kernel_hole_column = max(0, int(self.frequency__update_dynamic_variables_using_kernel_hole_column(v)) )
            return frequency__update_dynamic_variables_using_kernel_hole_column
        except ZeroDivisionError:
            return 0
    
    def get__frequency__update_dynamic_variables__while_processing_rgb_channel(self, v:list[float]) -> int:
        try:
            frequency__update_dynamic_variables__while_processing_rgb_channel = max(0, int(self.frequency__update_dynamic_variables__while_processing_rgb_channel(v)) )
            return frequency__update_dynamic_variables__while_processing_rgb_channel
        except ZeroDivisionError:
            return 0
    
    def get__frequency__update_dynamic_variables__after_processing_rgb_channel(self, v:list[float]) -> int:
        try:
            frequency__update_dynamic_variables__after_processing_rgb_channel = max(0, int(self.frequency__update_dynamic_variables__after_processing_rgb_channel(v)) )
            return frequency__update_dynamic_variables__after_processing_rgb_channel
        except ZeroDivisionError:
            return 0