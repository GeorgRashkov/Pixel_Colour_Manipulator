from Window_form_convolutional_kernels import Window_form_convolutional_kernels, Window_info_convolutional_kernels

from Convolutional_kernels_initializer import Convolutional_kernels_initializer
from Convolutional_kernel_for_image import Convolutional_kernel_for_image
from Window_dynamic_variables import Window_dynamic_variables
from Dynamic_variable import Dynamic_variable

from PyQt5_Window_functions import open_or_minimize_window

class Convolutional_kernels_controller():
    def __init__(self):

        self.window_form_convolutional_kernels = Window_form_convolutional_kernels()
        self.window_form_convolutional_kernels.button_show_info.clicked.connect(self.open_window_info_convolutional_kernels)
        self.window_form_convolutional_kernels.button_show_dynamiv_variables.clicked.connect(self.open_window_dynamic_variables)

        self.window_info_convolutional_kernels = Window_info_convolutional_kernels()
        
        self.window_dynamic_variables = Window_dynamic_variables()
        self.window_dynamic_variables.button_apply_dynamic_variables.clicked.connect(self.set_dynamic_variables)
        self.window_dynamic_variables.button_remove_dynamic_variables.clicked.connect(self.remove_dynamic_variables)

        self.dynamic_variables:list[Dynamic_variable] = []
    
    def open_window_form_convolutional_kernels(self):
        open_or_minimize_window(self.window_form_convolutional_kernels)

    def open_window_info_convolutional_kernels(self):
        open_or_minimize_window(self.window_info_convolutional_kernels)
 
    def open_window_dynamic_variables(self):
        open_or_minimize_window(self.window_dynamic_variables)
    
    

    def set_dynamic_variables(self):
        dynamic_variables = self.window_dynamic_variables.get_dynamic_variables()
        if(dynamic_variables is not None):
            if(len(dynamic_variables)>0):
                self.dynamic_variables = dynamic_variables
        
    def remove_dynamic_variables(self):
        self.dynamic_variables = []

    def apply_convolutional_kernels(self) -> dict[int, Convolutional_kernel_for_image]:

        cks_parameters_for_image_str = self.window_form_convolutional_kernels.textArea_cks_for_image.toPlainText()
        cks_parameters_for_rgb_channel_str = self.window_form_convolutional_kernels.textArea_cks_for_rgb_channel.toPlainText()
        additional_value_formula_str = self.window_form_convolutional_kernels.textBox_additional_value_formula.text()

        convolutional_kernels_initializer = Convolutional_kernels_initializer()
        convolutional_kernels = convolutional_kernels_initializer.create_convolutional_kernels(cks_parameters_for_image_str=cks_parameters_for_image_str, cks_parameters_for_rgb_channel_str=cks_parameters_for_rgb_channel_str, dynamic_variables=self.dynamic_variables, additional_value_formula_str=additional_value_formula_str)
        return convolutional_kernels
    

