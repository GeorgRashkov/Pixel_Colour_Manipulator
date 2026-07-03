from enum import Enum, auto
from typing import Callable


from Convolutional_kernel_for_rgb_channel import Convolutional_kernel_for_rgb_channel
from Convolutional_kernel_for_image import Convolutional_kernel_for_image
from Convolutional_kernel_parameters import Convolutional_kernel_parameters

from Bracket_expressions_getter import get_expressions_in_brackets, get_subjects_represented_as__parameters_and_values_from_bracket_expressions
from Dynamic_variable_initializer import Dynamic_variable_initializer
from Dynamic_variable import Dynamic_variable

from Enums import Enum__brackets, Enum__range, Enum__rgb_channels

from Formula_validation_collections import Convolutional_kernel_lambda_parameters_validation_collections
from Formula_checker import check_formula_format
from Number_format_checker import check_for_positive_int_format, is_number_in_range, check_for_float_format


class ck_enum(Enum):

    id = auto()

    min_h = auto()
    max_h = auto()
    min_w = auto()
    max_w = auto()

    min_dilation_h = auto()
    max_dilation_h= auto()
    min_dilation_w = auto()
    max_dilation_w = auto()

    min_stride_h = auto()
    max_stride_h = auto()
    min_stride_w = auto()
    max_stride_w = auto()


    h = auto()
    w = auto()

    dilation_h = auto()
    dilation_w = auto()

    stride_h = auto()
    stride_w = auto()

    hole_h = auto()
    hole_w = auto()
    freq_row_hole = auto()
    freq_col_hole = auto()
    hole_v = auto()

    min_k_v = auto()
    max_k_v = auto()

    min_hole_v = auto()
    max_hole_v = auto()

    move_x = auto()
    move_y = auto()

    convolutions_count = auto()

    pad_mode = auto()


    freq_update_img_y = auto()
    freq_update_img_x = auto()

    freq_move_x = auto()
    freq_move_y = auto()

    freq_recreate_k = auto()
    freq_update_k_v = auto()
    freq_update_k_hole_v = auto()

    freq_update_d_v_using_k_v = auto()
    freq_update_d_v_using_k_hole_row = auto()
    freq_update_d_v_using_k_hole_col = auto()

    freq_update_d_v_while_processing = auto()
    freq_update_d_v_after_processing = auto()

    process_fast = auto()
    input_channel = auto()

class ck2_enum(Enum):

    id = auto()

    r = auto()
    g = auto()
    b = auto()

    r_id = auto()
    g_id = auto()
    b_id = auto()


class Convolutional_kernels_initializer():

    def __init__(self):

        self.ck_for_rgb_channel_valid_parameters:list[str] = [
            ck_enum.id.name,
            ck_enum.min_h.name, ck_enum.max_h.name, ck_enum.min_w.name, ck_enum.max_w.name,
            ck_enum.min_dilation_h.name, ck_enum.max_dilation_h.name, ck_enum.min_dilation_w.name, ck_enum.max_dilation_w.name,
            ck_enum.min_stride_h.name, ck_enum.max_stride_h.name, ck_enum.min_stride_w.name, ck_enum.max_stride_w.name,
            ck_enum.h.name, ck_enum.w.name, 
            ck_enum.dilation_h.name, ck_enum.dilation_w.name, 
            ck_enum.stride_h.name, ck_enum.stride_w.name, 
            ck_enum.hole_h.name, ck_enum.hole_w.name, ck_enum.freq_row_hole.name, ck_enum.freq_col_hole.name, ck_enum.hole_v.name, 
            ck_enum.min_k_v.name, ck_enum.max_k_v.name, 
            ck_enum.min_hole_v.name, ck_enum.max_hole_v.name,
            ck_enum.move_x.name, ck_enum.move_y.name, 
            ck_enum.convolutions_count.name, 
            ck_enum.pad_mode.name, 
            ck_enum.freq_update_img_y.name, ck_enum.freq_update_img_x.name,
            ck_enum.freq_move_x.name, ck_enum.freq_move_y.name, 
            ck_enum.freq_recreate_k.name, ck_enum.freq_update_k_v.name, ck_enum.freq_update_k_hole_v.name, 
            ck_enum.freq_update_d_v_using_k_v.name, ck_enum.freq_update_d_v_using_k_hole_row.name, ck_enum.freq_update_d_v_using_k_hole_col.name, 
            ck_enum.freq_update_d_v_while_processing.name, ck_enum.freq_update_d_v_after_processing.name,
            ck_enum.process_fast.name, ck_enum.input_channel.name
        ]
        
        self.ck_for_rgb_channel_required_parameters:list[str] = [
            ck_enum.id.name,
            ck_enum.h.name, ck_enum.w.name
        ]

        self.ck_for_rgb_channel_lambda_parameters:list[str] = [
            ck_enum.h.name, ck_enum.w.name, 
            ck_enum.dilation_h.name, ck_enum.dilation_w.name, 
            ck_enum.stride_h.name, ck_enum.stride_w.name, 
            ck_enum.hole_h.name, ck_enum.hole_w.name, ck_enum.freq_row_hole.name, ck_enum.freq_col_hole.name, ck_enum.hole_v.name, 
            ck_enum.min_k_v.name, ck_enum.max_k_v.name, 
            ck_enum.min_hole_v.name, ck_enum.max_hole_v.name,
            ck_enum.move_x.name, ck_enum.move_y.name, 
            ck_enum.convolutions_count.name, 
            ck_enum.pad_mode.name, 
            ck_enum.freq_update_img_y.name, ck_enum.freq_update_img_x.name,
            ck_enum.freq_move_x.name, ck_enum.freq_move_y.name, 
            ck_enum.freq_recreate_k.name, ck_enum.freq_update_k_v.name, ck_enum.freq_update_k_hole_v.name, 
            ck_enum.freq_update_d_v_using_k_v.name, ck_enum.freq_update_d_v_using_k_hole_row.name, ck_enum.freq_update_d_v_using_k_hole_col.name, 
            ck_enum.freq_update_d_v_while_processing.name, ck_enum.freq_update_d_v_after_processing.name,
        ]

        self.ck_for_rgb_channel_positive_int_parameters:list[str] = [
            ck_enum.id.name, 
            ck_enum.min_h.name, ck_enum.max_h.name, ck_enum.min_w.name, ck_enum.max_w.name,
            ck_enum.min_dilation_h.name, ck_enum.max_dilation_h.name, ck_enum.min_dilation_w.name, ck_enum.max_dilation_w.name,
            ck_enum.min_stride_h.name, ck_enum.max_stride_h.name, ck_enum.min_stride_w.name, ck_enum.max_stride_w.name,
            ck_enum.process_fast.name, ck_enum.input_channel.name
        ]

        self.ck_for_rgb_channel_positive_int_in_range_parameters:dict[str,dict[Enum__range, int]] = {
            ck_enum.min_h.name:{Enum__range.min:1, Enum__range.max:999}, ck_enum.max_h.name:{Enum__range.min:1, Enum__range.max:999}, 
            ck_enum.min_w.name:{Enum__range.min:1, Enum__range.max:999}, ck_enum.max_w.name:{Enum__range.min:1, Enum__range.max:999},
            ck_enum.min_dilation_h.name:{Enum__range.min:1, Enum__range.max:999}, ck_enum.max_dilation_h.name:{Enum__range.min:1, Enum__range.max:999}, 
            ck_enum.min_dilation_w.name:{Enum__range.min:1, Enum__range.max:999}, ck_enum.max_dilation_w.name:{Enum__range.min:1, Enum__range.max:999},
            ck_enum.min_stride_h.name:{Enum__range.min:1, Enum__range.max:999}, ck_enum.max_stride_h.name:{Enum__range.min:1, Enum__range.max:999}, 
            ck_enum.min_stride_w.name:{Enum__range.min:1, Enum__range.max:999}, ck_enum.max_stride_w.name:{Enum__range.min:1, Enum__range.max:999},
            ck_enum.process_fast.name:{Enum__range.min:0, Enum__range.max:1},  
            ck_enum.input_channel.name:{Enum__range.min:0, Enum__range.max:2}
        }
        


        self.ck_for_image_valid_parameters:list[str] = [
            ck2_enum.id.name,
            ck2_enum.r.name, ck2_enum.g.name, ck2_enum.b.name,
            ck2_enum.r_id.name, ck2_enum.g_id.name, ck2_enum.b_id.name
        ]

        self.ck_for_image_required_parameters:list[str] = [ck2_enum.id.name]

        self.ck_for_image_positive_int_parameters:list[str] = [ck2_enum.id.name, 
            ck2_enum.r_id.name, ck2_enum.g_id.name, ck2_enum.b_id.name
        ]

        self.ck_for_image_lambda_collection_parameters:list[str] = [ck2_enum.r.name, ck2_enum.g.name, ck2_enum.b.name]

        self.id = ck2_enum.id.name

        self.r = ck2_enum.r.name
        self.g = ck2_enum.g.name
        self.b = ck2_enum.b.name

        self.r_id = ck2_enum.r_id.name
        self.g_id = ck2_enum.g_id.name
        self.b_id = ck2_enum.b_id.name

        self.additional_value_formula_str:str = "0"
        self.convolutional_kernel_lambda_parameters__validation_collections = Convolutional_kernel_lambda_parameters_validation_collections()

    def create_convolutional_kernels(self, cks_parameters_for_rgb_channel_str:str, cks_parameters_for_image_str:str, dynamic_variables:list[Dynamic_variable], additional_value_formula_str:str) -> dict[int, Convolutional_kernel_for_image]:
        
        additional_value_formula_str = additional_value_formula_str.replace(" ","").replace("\n","")
        if(len(additional_value_formula_str) > 0):
            is_additional_value_formula_valid = check_formula_format(formula=additional_value_formula_str, expression_name="additional value formula", square_brackets_biggest_value=999_999, 
                                                                    formula_validation_collections=self.convolutional_kernel_lambda_parameters__validation_collections)
            if(is_additional_value_formula_valid == True):
                self.additional_value_formula_str = additional_value_formula_str
            else:
                print("warning: the additional value formula will not be used because it was in wrong format")

        cks_parameters_for_rgb_channel_str = cks_parameters_for_rgb_channel_str.replace(" ","").replace("\n","")
        cks_parameters_for_image_str = cks_parameters_for_image_str.replace(" ","").replace("\n","")

        are_ck_parameters_for_rgb_channel_valid = self.check_cks_parameters_for_rgb_channel(cks_parameters_for_rgb_channel_str = cks_parameters_for_rgb_channel_str)
        if(are_ck_parameters_for_rgb_channel_valid == False):
            return None
        
        are_ck_parameters_for_image_valid = self.check_cks_parameters_for_image(cks_parameters_for_image_str=cks_parameters_for_image_str)
        if(are_ck_parameters_for_image_valid == False):
            return None
        
        convolutional_kernels_for_image:dict[int, Convolutional_kernel_for_image] = self.create_cks_for_image__without_checking_format(cks_parameters_for_rgb_channel_str=cks_parameters_for_rgb_channel_str, dynamic_variables=dynamic_variables)
        self.reset_dynamic_variables()
        return convolutional_kernels_for_image
    

    def check_cks_parameters_for_rgb_channel(self, cks_parameters_for_rgb_channel_str:str) -> bool:
        
        convolutional_kernels_as_strings:list[str] = get_expressions_in_brackets(bracket_type=Enum__brackets.curly, expressions_str=cks_parameters_for_rgb_channel_str)
        if(convolutional_kernels_as_strings[-1] is None):
            print(f"error: kernel expression (for rgb channel) at index {len(convolutional_kernels_as_strings)-1} was not placed properly in brackets")
            return False

        i1 = 0
        for convolutional_kernel_as_string in convolutional_kernels_as_strings:
            
            found_parameters = []

            convolutional_kernel_parameters_and_values__as_strings = convolutional_kernel_as_string.split(";")
            if(len(convolutional_kernel_parameter_and_value__as_string == 0)):
                    print(f"error: kernels without parameters are not allowed")
                    print(f"the previous error occured at the kernel expression (for rgb channel) on index {i1}")
                    return False

            for convolutional_kernel_parameter_and_value__as_string in convolutional_kernel_parameters_and_values__as_strings:
                
                if(len(convolutional_kernel_parameter_and_value__as_string == 0)):
                    print(f"error: the symbol `;` cannot be placed next to another `;`")
                    print(f"the previous error occured at the kernel expression (for rgb channel) on index {i1}")
                    return False

                convolutional_kernel_parameter_and_value__as_list = convolutional_kernel_parameter_and_value__as_string.split(":")


                ck_parameter_str = convolutional_kernel_parameter_and_value__as_list[0]

                if(ck_parameter_str not in self.ck_for_rgb_channel_valid_parameters):
                    print(f"error: the parameter {ck_parameter_str} is not allowed for kernel expression (for rgb channel)")
                    print(f"the previous error occured at the kernel expression (for rgb channel) on index {i1}")
                    return False
                
                if(ck_parameter_str in found_parameters):
                    print(f"error: the parameter {ck_parameter_str} was used many times")
                    print(f"the previous error occured at the kernel expression (for rgb channel) on index {i1}")
                    return False
                
                if(len(convolutional_kernel_parameter_and_value__as_list)<2):
                    print(f"error: the parameter {ck_parameter_str} had no value; if you don't want to use it delete it")
                    print(f"the previous error occured at the kernel expression (for rgb channel) on index {i1}")
                    return False
                
                if(len(convolutional_kernel_parameter_and_value__as_list)>2):
                    print(f"error: the parameter {ck_parameter_str} had many values")
                    print(f"the previous error occured at the kernel expression (for rgb channel) on index {i1}")
                    return False
                

                ck_value_str = convolutional_kernel_parameter_and_value__as_list[1]

                if(ck_parameter_str in self.ck_for_rgb_channel_lambda_parameters):
                    is_convolutional_kernel_value_valid = check_formula_format(formula=ck_value_str, expression_name=f"{ck_parameter_str} formula", 
                                                                                square_brackets_biggest_value=999_999, formula_validation_collections=self.convolutional_kernel_lambda_parameters__validation_collections)
                    if(is_convolutional_kernel_value_valid == False):
                        print(f"the previous error occured for the parameter {ck_parameter_str} inside the kernel expression (for rgb channel) on index {i1}")
                        return False

                if(ck_parameter_str in self.ck_for_rgb_channel_positive_int_parameters):
                    is_convolutional_kernel_value_valid = check_for_positive_int_format(txt_value=ck_value_str)
                    if(is_convolutional_kernel_value_valid == False):
                        print(f"error: the value for the parameter {ck_parameter_str} must be a positive integer")
                        print(f"the previous error occured for the parameter {ck_parameter_str} inside the kernel expression (for rgb channel) on index {i1}")
                        return False

                if(ck_parameter_str in self.ck_for_rgb_channel_positive_int_in_range_parameters):

                    min = self.ck_for_rgb_channel_positive_int_in_range_parameters[ck_parameter_str][Enum__range.min]
                    max = self.ck_for_rgb_channel_positive_int_in_range_parameters[ck_parameter_str][Enum__range.max]
                    
                    is_value_in_range = is_number_in_range(num_as_str=ck_value_str, min=min, max=max)
                    if(is_value_in_range == False):
                        print(f"error: the value for the parameter {ck_parameter_str} must be a positive integer in range {min}-{max}")
                        print(f"the previous error occured for the parameter {ck_parameter_str} inside the kernel expression (for rgb channel) on index {i1}")
                        return False
                
                found_parameters.append(ck_parameter_str)
            

            for required_parameter in self.ck_for_rgb_channel_required_parameters:
                if(required_parameter not in found_parameters):
                    print(f"error: the parameter {ck_parameter_str} is required for kernel expression (for rgb channel)")
                    print(f"the previous error occured at the kernel expression (for rgb channel) on index {i1}")
                    return False
            i1 +=1

        return True
    
    def check_cks_parameters_for_image(self, cks_parameters_for_image_str:str) -> bool:

        convolutional_kernels_as_strings:list[dict[str, str]] = get_subjects_represented_as__parameters_and_values_from_bracket_expressions(txt=cks_parameters_for_image_str, subject_name="kernel expression (for image)", 
        outer_bracket_type=Enum__brackets.curly, inner_bracket_type=Enum__brackets.square, valid_parameters=set(self.ck_for_image_valid_parameters), required_parameters=self.ck_for_image_required_parameters, parameter_value_separator=":")
        
        if(convolutional_kernels_as_strings == None):
            return False
        i1 = 0
        for convolutional_kernel_parameters_and_values__as_strings in convolutional_kernels_as_strings:
            
            for ck_parameter_str in convolutional_kernel_parameters_and_values__as_strings.keys():

                ck_value_str = convolutional_kernel_parameters_and_values__as_strings[ck_parameter_str]

                if(ck_parameter_str in self.ck_for_image_positive_int_parameters):
                    is_convolutional_kernel_value_valid = check_for_positive_int_format(txt_value=ck_value_str)
                    if(is_convolutional_kernel_value_valid == False):
                        print(f"error: the value for the parameter {ck_parameter_str} must be a positive integer")
                        print(f"the previous error occured for the parameter {ck_parameter_str} inside the kernel expression (for image) on index {i1}")
                        return False
                    
                if(ck_parameter_str in self.ck_for_image_lambda_collection_parameters):
                    
                    ck_rows_as_strings:list[str] = get_expressions_in_brackets(bracket_type=Enum__brackets.square, expressions_str=ck_value_str)
                    if(len(ck_rows_as_strings) > 0):
                        if(ck_rows_as_strings[-1] is None):
                            print(f"error: kernel expression (for image) at index {len(convolutional_kernels_as_strings)-1} was not placed properly in brackets")
                            return False
                    
                    row_index = 0
                    for ck_row_as_string in ck_rows_as_strings:

                        ck_cols_for_current_row_as_strings = ck_row_as_string.split(",")
                        column_index = 0

                        for ck_cell_as_string in ck_cols_for_current_row_as_strings:
                            
                            if(len(ck_cell_as_string) == 0):
                                print("error: kernel expression (for image) is not allowed to have emtpy cells in the kernel values")
                                print(f"the previous error occured for the parameter {ck_parameter_str} inside the kernel expression (for image) on index {i1}, for the kernel values at row {row_index} and column {column_index}")
                                return False
                            
                            is_kernel_cell_value_valid = check_formula_format(formula=ck_cell_as_string, expression_name="kernel expression (for image)", 
                                square_brackets_biggest_value=999_999, formula_validation_collections=self.convolutional_kernel_lambda_parameters__validation_collections)
                            
                            if(is_kernel_cell_value_valid == False):
                                print(f"the previous error occured for the parameter {ck_parameter_str} inside the kernel expression (for image) on index {i1}, for the kernel values at row {row_index} and column {column_index}")
                                return False
                            
                            column_index+=1
                        
                        row_index += 1
            
            i1 += 1
        
        return True
    
    
    

    
    def create_cks_for_image__without_checking_format(self, cks_parameters_for_rgb_channel_str:str, ck_parameters_for_image_str:str, dynamic_variables:list[Dynamic_variable]) -> dict[int, Convolutional_kernel_for_image]:
        
        ck_parameters_for_rgb_channel__dict:dict[str, str] = self.get_str_dict_for__cks_parameters_for_rgb_channel(cks_parameters_for_rgb_channel_str=cks_parameters_for_rgb_channel_str)

        cks_parameters_and_values_for_image:list[dict[str, str]] = get_subjects_represented_as__parameters_and_values_from_bracket_expressions(txt=ck_parameters_for_image_str, subject_name="kernel expression (for image)", 
        outer_bracket_type=Enum__brackets.curly, inner_bracket_type=Enum__brackets.square, valid_parameters=set(self.ck_for_image_valid_parameters), required_parameters=self.ck_for_image_required_parameters, parameter_value_separator=":")
        
        convolutional_kernels_for_image:dict[int,Convolutional_kernel_for_image] = {}

        for ck_parameters_and_values_for_image in cks_parameters_and_values_for_image:
            
            id_str = ""
            
            cks_for_rgb_channels__non_hole_values:dict[Enum__rgb_channels, str] = {}#contains the non hole values for each kernel (for rgb channel) for each rgb channel; the key indicates the rgb channel
            ck_for_image__rgb_ids:dict[Enum__rgb_channels, str] = {}#contains the ids of the kernels (for rgb channel) for each rgb channel; the key indicates the rgb channel
            cks_for_rgb_channels__parameters:dict[Enum__rgb_channels, str] = {}#contains the parameters and values of the kernels (for rgb channel) for each rgb channel; the key indicates the rgb channel

            for ck_parameter_str in ck_parameters_and_values_for_image.keys():

                ck_value_str = ck_parameters_and_values_for_image[ck_parameter_str]

                if(ck_parameter_str == self.id):
                    id_str = ck_value_str
                elif(ck_parameter_str == self.r or ck_parameter_str == self.g or ck_parameter_str == self.b):
                    cks_for_rgb_channels__non_hole_values[getattr(Enum__rgb_channels, ck_parameter_str)] = ck_value_str
                elif(ck_parameter_str == self.r_id or ck_parameter_str == self.g_id or ck_parameter_str == self.b_id):
                    ck_for_image__rgb_ids[getattr(Enum__rgb_channels,ck_parameter_str)] = ck_value_str

            for rgb_channel in ck_for_image__rgb_ids.keys():
                rgb_id = ck_for_image__rgb_ids[rgb_channel]
                if(rgb_id in ck_parameters_for_rgb_channel__dict.keys()):
                    cks_for_rgb_channels__parameters[rgb_channel] = ck_parameters_for_rgb_channel__dict[rgb_id]
            
            id = int(id_str)
            convolutional_kernel_for_image = self.create_ck_for_image__without_checking_format(id=id, cks_for_rgb_channels__non_hole_values=cks_for_rgb_channels__non_hole_values, ck_for_image__rgb_ids=ck_for_image__rgb_ids, cks_for_rgb_channels__parameters=cks_for_rgb_channels__parameters, dynamic_variables=dynamic_variables)
            
            if(convolutional_kernel_for_image is not None):
                convolutional_kernels_for_image[id] = convolutional_kernel_for_image
        
        return convolutional_kernels_for_image
           

            
    def create_ck_for_image__without_checking_format(self, id:int, cks_for_rgb_channels__non_hole_values:dict[Enum__rgb_channels, str], ck_for_image__rgb_ids:dict[Enum__rgb_channels, str], cks_for_rgb_channels__parameters:dict[Enum__rgb_channels, str], dynamic_variables:list[Dynamic_variable]) -> Convolutional_kernel_for_image:

        rbg_channels:list[Enum__rgb_channels] = self.get_matching_rgb_channels_from_string_expressions(expressions=[cks_for_rgb_channels__non_hole_values, ck_for_image__rgb_ids, cks_for_rgb_channels__parameters])
        if(len(rbg_channels) == 0):
            print(f"warning: the image kernel with id {id} was not created;")
            print("make sure the image kernel uses at least one rgb channel id owned by rgb channel kernel and make sure it has at least 1 kernel value")
            return None
        
        cks_for_rgb_channel:dict[Enum__rgb_channels, Convolutional_kernel_for_rgb_channel] = {}
        for rbg_channel in rbg_channels:
            ck_for_rgb_channel__non_hole_values = cks_for_rgb_channels__non_hole_values[rbg_channel]
            ck_for_rgb_channel__parameters = cks_for_rgb_channels__parameters[rbg_channel]

            ck_for_rgb_channel:Convolutional_kernel_for_rgb_channel = self.create_ck_for_rgb_channel__without_checking_format(ck_parameters_str=ck_for_rgb_channel__parameters, ck_non_hole_values_str=ck_for_rgb_channel__non_hole_values, dynamic_variables=dynamic_variables)
            cks_for_rgb_channel[rbg_channel] = ck_for_rgb_channel
        
        convolutional_kernel_for_image = Convolutional_kernel_for_image(id=id, 
                convolutional_kernel_r=cks_for_rgb_channel[Enum__rgb_channels.r], convolutional_kernel_g=cks_for_rgb_channel[Enum__rgb_channels.g], convolutional_kernel_b=cks_for_rgb_channel[Enum__rgb_channels.b],
                dynamic_variables=dynamic_variables)

        return convolutional_kernel_for_image
        

    def create_ck_for_rgb_channel__without_checking_format(self, ck_parameters_str:str, ck_non_hole_values_str:str, dynamic_variables:list[Dynamic_variable]) -> Convolutional_kernel_for_rgb_channel:
        
        ck_parameters_obj:Convolutional_kernel_parameters = self.create_ck_parameters(ck_parameters_str=ck_parameters_str)
        
        self.reset_dynamic_variables(dynamic_variables=dynamic_variables)
        dynamic_variables_values = self.get_dynamic_variables_values(dynamic_variables=dynamic_variables)
        kernel_height = ck_parameters_obj.get__height(v = dynamic_variables_values)
        kernel_width=ck_parameters_obj.get__width(v = dynamic_variables_values)
        
        ck_non_hole_values_as_strings__rows_columns:list[list[str]] = self.create_ck_non_hole_values_as_strings__rows_columns(ck_non_hole_values_str=ck_non_hole_values_str, kernel_height=kernel_height, kernel_width=kernel_width)
        ck_non_hole_values_as_formulas__rows_columns:list[list[Callable[[list[float]], float]]]  = self.create_ck_non_hole_values_as_formulas__rows_columns(ck_non_hole_values__rows_columns=ck_non_hole_values_as_strings__rows_columns)
        ck_non_hole_values__rows_columns:list[list[float]] = self.get_ck_non_hole_values__rows_columns(ck_non_hole_values_as_strings__rows_columns=ck_non_hole_values_as_strings__rows_columns, ck_non_hole_values_as_formulas__rows_columns=ck_non_hole_values_as_formulas__rows_columns, dynamic_variables=dynamic_variables)
        ck_row_indexes_of__non_hole_values_as_formulas, ck_column_indexes_of__non_hole_values_as_formulas =self.get_ck_row_and_column_indexes_of__non_hole_values_as_formulas(ck_non_hole_values_as_formulas__rows_columns=ck_non_hole_values_as_formulas__rows_columns)
        
        convolutional_kernel_for_rgb_channel = Convolutional_kernel_for_rgb_channel(c_k_parameters=ck_parameters_obj,
                 non_hole_values=ck_non_hole_values__rows_columns, non_hole_values_as_formulas=ck_non_hole_values_as_formulas__rows_columns, 
                 row_indexes_of__non_hole_values_as_formulas=ck_row_indexes_of__non_hole_values_as_formulas, column_indexes_of__non_hole_values_as_formulas=ck_column_indexes_of__non_hole_values_as_formulas)
        
        return convolutional_kernel_for_rgb_channel
        
    
    def create_ck_parameters(self, ck_parameters_str:str) -> Convolutional_kernel_parameters:

        ck_parameters_list = ck_parameters_str.split(";")
        ck_parameters_dict:dict[ck_enum, str] = {}

        for ck_parameter in ck_parameters_list:
            
            ck_parameter__name_and_value = ck_parameter.split(":")
            ck_parameter__name = ck_parameter__name_and_value[0]
            ck_parameter__value = ck_parameter__name_and_value[1]
            
            ck_parameters_dict[getattr(ck_enum, ck_parameter__name)] = ck_parameter__value
        
        ck_parameters_obj = self.create_ck_parameters_2(k = ck_parameters_dict)
        return ck_parameters_obj


    def create_ck_parameters_2(sekf, ck_parameters_dict:dict[ck_enum, str]) -> Convolutional_kernel_parameters:

        should_update_move_x:bool = True
        should_update_move_y:bool = True

        should_recreate_kernel:bool = True
        should_update_kernel_values:bool = True
        should_update_kernel_hole_values:bool = True

        should_update_dynamic_variables__using_kernel_value:bool = True
        should_update_dynamic_variables__using_kernel_hole_row:bool = True
        should_update_dynamic_variables__using_kernel_hole_column:bool = True

        should_update_dynamic_variables__while_processing_rgb_channel:bool = True
        should_update_dynamic_variables__after_processing_rgb_channel:bool = True

        
        k = ck_parameters_dict
        n0 = "0"
        n1 = "1"
        n999 = "999999"
        n_minus_999 = "-999999"

        if ck_enum.id not in k:
            k[ck_enum.id] = n1
        
        
        if ck_enum.min_h not in k:
            k[ck_enum.min_h] = n1
        
        if ck_enum.max_h not in k:
            k[ck_enum.max_h] = n999
        
        if ck_enum.min_w not in k:
            k[ck_enum.min_w] = n1
        
        if ck_enum.max_w not in k:
            k[ck_enum.max_w] = n999
        

        if ck_enum.min_dilation_h not in k:
            k[ck_enum.min_dilation_h] = n1
        
        if ck_enum.max_dilation_h not in k:
            k[ck_enum.max_dilation_h] = n999
        
        if ck_enum.min_dilation_w not in k:
            k[ck_enum.min_dilation_w] = n1
        
        if ck_enum.max_dilation_w not in k:
            k[ck_enum.max_dilation_w] = n999
        

        if ck_enum.min_stride_h not in k:
            k[ck_enum.min_stride_h] = n1
        
        if ck_enum.max_stride_h not in k:
            k[ck_enum.max_stride_h] = n999
        
        if ck_enum.min_stride_w not in k:
            k[ck_enum.min_stride_w] = n1
        
        if ck_enum.max_stride_w not in k:
            k[ck_enum.max_stride_w] = n999
        

        
        if ck_enum.h not in k:
            k[ck_enum.h] = n1
        
        if ck_enum.w not in k:
            k[ck_enum.w] = n1

        
        if ck_enum.dilation_h not in k:
            k[ck_enum.dilation_h] = n1
        
        if ck_enum.dilation_w not in k:
            k[ck_enum.dilation_w] = n1
        
        
        if ck_enum.stride_h not in k:
            k[ck_enum.stride_h] = n1
        
        if ck_enum.stride_w not in k:
            k[ck_enum.stride_w] = n1
        
        
        if ck_enum.hole_h not in k:
            k[ck_enum.hole_h] = n0
        
        if ck_enum.hole_w not in k:
            k[ck_enum.hole_w] = n0
        
        if ck_enum.freq_row_hole not in k:
            k[ck_enum.freq_row_hole] = n0
        
        if ck_enum.freq_col_hole not in k:
            k[ck_enum.freq_col_hole] = n0

        if ck_enum.hole_v not in k:
            k[ck_enum.hole_v] = n0
        
        
        if ck_enum.min_k_v not in k:
            k[ck_enum.min_k_v] = n_minus_999
        
        if ck_enum.max_k_v not in k:
            k[ck_enum.max_k_v] = n999
        
        if ck_enum.min_hole_v not in k:
            k[ck_enum.min_hole_v] = n_minus_999
        
        if ck_enum.max_hole_v not in k:
            k[ck_enum.max_hole_v] = n999
        

        if ck_enum.move_x not in k:
            k[ck_enum.move_x] = n0
        
        if ck_enum.move_y not in k:
            k[ck_enum.move_y] = n0
        

        if ck_enum.convolutions_count not in k:
            k[ck_enum.convolutions_count] = n1
        

        if ck_enum.pad_mode not in k:
            k[ck_enum.pad_mode] = n0
        


        if ck_enum.freq_update_img_y not in k:
            k[ck_enum.freq_update_img_y] = n0
        
        if ck_enum.freq_update_img_x not in k:
            k[ck_enum.freq_update_img_x] = n0
        

        if ck_enum.freq_move_x not in k:
            k[ck_enum.freq_move_x] = n0
            should_update_move_x = False
        
        if ck_enum.freq_move_y not in k:
            k[ck_enum.freq_move_y] = n0
            should_update_move_y = False 
        

        if ck_enum.freq_recreate_k not in k:
            k[ck_enum.freq_recreate_k] = n0
            should_recreate_kernel = False 
        

        if ck_enum.freq_update_k_v not in k:
            k[ck_enum.freq_update_k_v] = n0
            should_update_kernel_values = False
        
        if ck_enum.freq_update_k_hole_v not in k:
            k[ck_enum.freq_update_k_hole_v] = n0
            should_update_kernel_hole_values = False
        

        if ck_enum.freq_update_d_v_using_k_v not in k:
            k[ck_enum.freq_update_d_v_using_k_v] = n0
            should_update_dynamic_variables__using_kernel_value = False
        
        if ck_enum.freq_update_d_v_using_k_hole_row not in k:
            k[ck_enum.freq_update_d_v_using_k_hole_row] = n0
            should_update_dynamic_variables__using_kernel_hole_row = False
        
        if ck_enum.freq_update_d_v_using_k_hole_col not in k:
            k[ck_enum.freq_update_d_v_using_k_hole_col] = n0
            should_update_dynamic_variables__using_kernel_hole_column = False
        

        if ck_enum.freq_update_d_v_while_processing not in k:
            k[ck_enum.freq_update_d_v_while_processing] = n0
            should_update_dynamic_variables__while_processing_rgb_channel = False
        
        if ck_enum.freq_update_d_v_after_processing not in k:
            k[ck_enum.freq_update_d_v_after_processing] = n0
            should_update_dynamic_variables__after_processing_rgb_channel = False
        

        if ck_enum.process_fast not in k:
            k[ck_enum.process_fast] = n1
        
        if ck_enum.input_channel not in k:
            k[ck_enum.input_channel] = n0
        

        convolutional_kernel_parameters_obj = Convolutional_kernel_parameters(id=k[ck_enum.id], 
              
              height=k[ck_enum.h], width=k[ck_enum.w], dilation_height=k[ck_enum.dilation_h], dilation_width=k[ck_enum.dilation_w], stride_height=k[ck_enum.stride_h], stride_width=k[ck_enum.stride_w], 
              hole_height=k[ck_enum.hole_h], hole_width=k[ck_enum.hole_w], vertical_hole_frequency=k[ck_enum.freq_row_hole], horizontal_hole_frequency=k[ck_enum.freq_col_hole], hole_content=k[ck_enum.hole_v],
              min_kernel_value=k[ck_enum.min_k_v], max_kernel_value=k[ck_enum.max_k_v], min_hole_value=k[ck_enum.min_hole_v], max_hole_value=k[ck_enum.max_hole_v],
              move_x=k[ck_enum.move_x], move_y=k[ck_enum.move_y],
              convolutions_count=k[ck_enum.convolutions_count], 
              image_pad_mode=k[ck_enum.pad_mode], 
              frequency__update_image_y=k[ck_enum.freq_update_img_y], frequency__update_image_x=k[ck_enum.freq_update_img_x],
              frequency__move_x=k[ck_enum.freq_move_x], frequency__move_y=k[ck_enum.freq_move_y],
              frequency__recreate_kernel=k[ck_enum.freq_recreate_k], frequency__update_kernel_values=k[ck_enum.freq_update_k_v], frequency__update_kernel_hole_values=k[ck_enum.freq_update_k_hole_v],
              frequency__update_dynamic_variables__using_kernel_value=k[ck_enum.freq_update_d_v_using_k_v], frequency__update_dynamic_variables__using_kernel_hole_row=k[ck_enum.freq_update_d_v_using_k_hole_row], frequency__update_dynamic_variables_using_kernel_hole_column=k[ck_enum.freq_update_d_v_using_k_hole_col], 
              frequency__update_dynamic_variables__while_processing_rgb_channel=k[ck_enum.freq_update_d_v_while_processing], frequency__update_dynamic_variables__after_processing_rgb_channel=k[ck_enum.freq_update_d_v_after_processing],
              
              should_update_move_x=should_update_move_x, should_update_move_y=should_update_move_y,
              should_recreate_kernel=should_recreate_kernel, should_update_kernel_values=should_update_kernel_values, should_update_kernel_hole_values=should_update_kernel_hole_values,
              should_update_dynamic_variables__using_kernel_value=should_update_dynamic_variables__using_kernel_value, should_update_dynamic_variables__using_kernel_hole_row=should_update_dynamic_variables__using_kernel_hole_row, should_update_dynamic_variables__using_kernel_hole_column=should_update_dynamic_variables__using_kernel_hole_column, 
              should_update_dynamic_variables__while_processing_rgb_channel=should_update_dynamic_variables__while_processing_rgb_channel, should_update_dynamic_variables__after_processing_rgb_channel=should_update_dynamic_variables__after_processing_rgb_channel,
              
              process_image_fast=bool(int(k[ck_enum.process_fast])),
              
              input_rgb_channel=Enum__rgb_channels(int(k[ck_enum.input_channel])))

        return convolutional_kernel_parameters_obj
    

    
    def create_ck_non_hole_values_as_strings__rows_columns(self, ck_non_hole_values_str:str, kernel_height:int, kernel_width:int) -> list[list[str]]:
        
        ck_non_hole_values_list:list[str] = get_expressions_in_brackets(bracket_type=Enum__brackets.square, expressions_str=ck_non_hole_values_str)
        ck_non_hole_values__rows_columns:list[list[str]] = []
        columns_per_row = kernel_width

        for ck_non_hole_values__row in ck_non_hole_values_list:
            
            ck_non_hole_values__current_row_columns = ck_non_hole_values__row.split(",")
            if(len(ck_non_hole_values__current_row_columns) > columns_per_row):
                columns_per_row = len(ck_non_hole_values__current_row_columns)
            
            ck_non_hole_values__rows_columns.append(ck_non_hole_values__current_row_columns.copy())
        
        for ck_non_hole_values__row in ck_non_hole_values__rows_columns:
            while( len(ck_non_hole_values__row) < columns_per_row ):
                ck_non_hole_values__row.append(self.additional_value_formula_str)
        
        while(len(ck_non_hole_values__rows_columns) < kernel_height):
            ck_non_hole_values__rows_columns.append(ck_non_hole_values__rows_columns[-1].copy())
        
        return ck_non_hole_values__rows_columns

    
    def create_ck_non_hole_values_as_formulas__rows_columns(self, ck_non_hole_values__rows_columns:list[list[str]]) -> list[list[Callable[[list[float]], float]]]:

        ck_non_hole_values_as_formulas__rows_columns:list[list[Callable[[list[float]], float]]] = []

        for ck_non_hole_values__row in ck_non_hole_values__rows_columns:
            
            ck_non_hole_values_as_formulas__row = []
            for ck_non_hole_value in ck_non_hole_values__row:

                is_non_hole_value_a_formula = check_for_float_format(txt_value=ck_non_hole_value) == False
                if(is_non_hole_value_a_formula == True):
                    ck_non_hole_value_as_formula = eval(f"lambda v=[0]: {ck_non_hole_value}")
                    ck_non_hole_values_as_formulas__row.append(ck_non_hole_value_as_formula)
                else:
                    ck_non_hole_values_as_formulas__row.append(None)
            
            ck_non_hole_values_as_formulas__rows_columns.append(ck_non_hole_values_as_formulas__row)
        
        return ck_non_hole_values_as_formulas__rows_columns




    def get_str_dict_for__cks_parameters_for_rgb_channel(self, cks_parameters_for_rgb_channel_str:str) -> dict[str, str]:

        ck_parameters_for_rgb_channel__dict:dict[str, str] = {}

        convolutional_kernels_as_strings:list[str] = get_expressions_in_brackets(bracket_type=Enum__brackets.curly, expressions_str=cks_parameters_for_rgb_channel_str)
        
        for convolutional_kernel_as_string in convolutional_kernels_as_strings:
            convolutional_kernel_parameters_and_values__as_strings = convolutional_kernel_as_string.split(";")
            for convolutional_kernel_parameter_and_value__as_string in convolutional_kernel_parameters_and_values__as_strings:
                
                convolutional_kernel_parameter_and_value__as_list = convolutional_kernel_parameter_and_value__as_string.split(":")
                ck_parameter_str = convolutional_kernel_parameter_and_value__as_list[0]
                ck_value_str = convolutional_kernel_parameter_and_value__as_list[1]

                if(ck_parameter_str == self.id):
                    ck_parameters_for_rgb_channel__dict[ck_value_str] = convolutional_kernel_as_string
                    break
        
        return ck_parameters_for_rgb_channel__dict
    
    
    def get_ck_non_hole_values__rows_columns(self, ck_non_hole_values_as_strings__rows_columns:list[list[str]], ck_non_hole_values_as_formulas__rows_columns:list[list[Callable[[list[float]], float]]], dynamic_variables:list[Dynamic_variable]) -> list[list[float]]:
        
        self.reset_dynamic_variables(dynamic_variables=dynamic_variables)
        ck_non_hole_values__rows_columns:list[list[float]] = []
        
        row = 0
        for ck_non_hole_values_as_formulas__row in ck_non_hole_values_as_formulas__rows_columns:
            
            ck_non_hole_values__row:list[float] = []
            
            col = 0
            for ck_non_hole_value_as_formula in ck_non_hole_values_as_formulas__row:
                
                if(ck_non_hole_value_as_formula is not None):
                    dynamic_variables_values = self.get_dynamic_variables_values(dynamic_variables=dynamic_variables)
                    ck_non_hole_value = ck_non_hole_value_as_formula(v=dynamic_variables_values)
                    ck_non_hole_values__row.append(ck_non_hole_value)
                else:
                    ck_non_hole_value = float(ck_non_hole_values_as_strings__rows_columns[row][col])
                    ck_non_hole_values__row.append(ck_non_hole_value)
                
                col += 1
            
            ck_non_hole_values__rows_columns.append(ck_non_hole_values__row)

            row += 1
        
        return ck_non_hole_values__rows_columns


    def get_ck_row_and_column_indexes_of__non_hole_values_as_formulas(self, ck_non_hole_values_as_formulas__rows_columns:list[list[Callable[[list[float]], float]]]) -> tuple[list[int], list[int]]:
        
        row_indexes_of__non_hole_values_as_formulas:list[int] = []
        column_indexes_of__non_hole_values_as_formulas:list[int] = []

        for row in range(0, len(ck_non_hole_values_as_formulas__rows_columns)):

            for col in range(0, len(ck_non_hole_values_as_formulas__rows_columns[row])):
                
                ck_non_hole_values_as_formula = ck_non_hole_values_as_formulas__rows_columns[row][col]
                
                if(ck_non_hole_values_as_formula is not None):
                    row_indexes_of__non_hole_values_as_formulas.append(row)
                    column_indexes_of__non_hole_values_as_formulas.append(col)
        
        return (row_indexes_of__non_hole_values_as_formulas, column_indexes_of__non_hole_values_as_formulas)



    def remove_non_matching_string_rgb_expressions(self, expressions:list[dict[Enum__rgb_channels, str]]):
        
        rgb_channels:list[Enum__rgb_channels] = [Enum__rgb_channels.r, Enum__rgb_channels.g, Enum__rgb_channels.b]
        
        for rgb_channel in rgb_channels:
            
            do_all_expression_have_current_rgb_channel = True
            
            for expression in expressions:
                if(rgb_channel not in expression.keys()):
                    do_all_expression_have_current_rgb_channel = False
                    break
            
            if(do_all_expression_have_current_rgb_channel == False):
                for expression in expressions:
                    if(rgb_channel in expression.keys()):
                        del expression[rgb_channel]
        

    def get_matching_rgb_channels_from_string_expressions(self, expressions:list[dict[Enum__rgb_channels, str]]) -> list[Enum__rgb_channels]:
        
        rgb_channels:list[Enum__rgb_channels] = [Enum__rgb_channels.r, Enum__rgb_channels.g, Enum__rgb_channels.b]
        found_rgb_channels:list[Enum__rgb_channels] = []
        
        for rgb_channel in rgb_channels:
            
            do_all_expression_have_current_rgb_channel = True
            
            for expression in expressions:
                if(rgb_channel not in expression.keys()):
                    do_all_expression_have_current_rgb_channel = False
                    break
            
            if(do_all_expression_have_current_rgb_channel == True):
                found_rgb_channels.append(rgb_channel)
        
        return found_rgb_channels


    def get_dynamic_variables_values(self, dynamic_variables:list[Dynamic_variable]) -> list[float]:
        
        dynamic_variables_values:list[float] = []

        for dynamic_variable in dynamic_variables:
            
            dynamic_variable_value = dynamic_variable.get_value()
            dynamic_variables_values.append(dynamic_variable_value)
            dynamic_variable.update_frequency()
        
        if(len(dynamic_variables_values) == 0):
            dynamic_variables_values.append(0)

        return dynamic_variables_values

    def reset_dynamic_variables(self, dynamic_variables:list[Dynamic_variable]):

        for dynamic_variable in dynamic_variables:
            dynamic_variable.reset_value_and_frequency()



    