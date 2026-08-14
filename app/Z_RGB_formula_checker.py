import numpy as np
from Number_format_checker import check_for_positive_int_format
from Formula_validation_collections import RGB_formula_validation_collections
from Formula_checker import check_formula_format, does_formula_contain_specific_variables
from Formula_validation_collections import RGB_formula_validation_collections
from Bracket_expressions_getter import get_subjects_represented_as__parameters_and_values_from_bracket_expressions
from Enums import Enum__brackets, Enum_rgb_formulas_parameters, Functions_for__Enum__rgb_formulas_parameters


def remove_indexes_from_rgb_channel_formula(formula:str) -> str:
        
        rgb_chars = ['r','g','b']

        if(len(formula) <= 3):
            return formula
        
        rgb_formula_validation_collections = RGB_formula_validation_collections()
        allowed_operator_chars = rgb_formula_validation_collections.allowed_operator_chars

        for rgb_char in rgb_chars:

            i = 0
            while(True):
                
                i = formula.find(rgb_char,i)
                if(i==-1 or i==len(formula)-1):
                    break
                
                elif( formula[i+1] == "["):
                    
                    if(i==0 or formula[i-1] == '(' or formula[i-1] in allowed_operator_chars):
                        closing_square_bracket_index = formula.find("]",i)
                        formula = formula[:i+1] + formula[closing_square_bracket_index+1:]

                i+=1
        
        return formula


def is_RGB_formula_compatible_with_dxcam(rgb_formula: str, channel: str, use_areas: bool = False):
    
    if(rgb_formula is None):
        return False
    
    rgb_formula_validation_collections = RGB_formula_validation_collections()
    rgb_formula = rgb_formula_validation_collections.update_format(formula=rgb_formula)
    
    if(use_areas == False):
        rgb_formula = remove_indexes_from_rgb_channel_formula(formula=rgb_formula)

    rgb_function = eval(f"lambda r,g,b,areas_count=1,v=np.array([0], dtype=np.uint8): {rgb_formula}")
    
    try:
        if(use_areas == False):
            img =  np.array([ [[1,2,3],[10,20,30]],[[5,7,9],[50,70,90]] ], dtype=np.uint8)
            transformed_img = rgb_function(img[:,:,0], img[:,:,1], img[:,:,2])
        else:
            img = np.array([ [[[1,2,3],[10,20,30]],[[5,7,9],[50,70,90]]], [[[11,22,33],[110,220,35]],[[55,77,99],[150,170,190]]] ], dtype=np.uint8)
            transformed_img = rgb_function(img[:,:,:,0], img[:,:,:,1], img[:,:,:,2], img.shape[0])
    except:
        print(f"Error: the formula for the {channel} channel was not compatible with dxcam. Try making the int values (or results of arithmetic operations between 2 variables) fit in the range 0-255.")
        return False    
        
    return True


def check_RGB_formula_format(rgb_formula: str, channel: str,  use_areas: bool = False) -> bool:
    
    rgb_formula_validation_collections = RGB_formula_validation_collections()
    does_formula_contain_atleast_one_rgb_channel = does_formula_contain_specific_variables(formula=rgb_formula, variables=['r','g','b'],  formula_validation_collections=rgb_formula_validation_collections, find_all=False)
    if(does_formula_contain_atleast_one_rgb_channel == False):
        print(f"error: the rgb formula for the {channel} channel must contain at least one rgb channel")
        return False
    
    is_format_correct = check_formula_format(formula=rgb_formula, expression_name=f"{channel} channel formula",  square_brackets_biggest_value=999_999, formula_validation_collections=rgb_formula_validation_collections)  
    if(is_format_correct == True):
        is_format_correct = is_RGB_formula_compatible_with_dxcam(rgb_formula=rgb_formula, channel=channel, use_areas=use_areas)

    return is_format_correct


def check_rgb_formulas_format(rgb_formulas:str,  use_areas: bool = False) -> bool:

    id = Enum_rgb_formulas_parameters.id.name
    r = Enum_rgb_formulas_parameters.r.name
    g = Enum_rgb_formulas_parameters.g.name
    b = Enum_rgb_formulas_parameters.b.name
    rbg_formulas_parameters = (id, r, g, b)

    parameter_value_separator = Functions_for__Enum__rgb_formulas_parameters().get_rgb_formulas_parameter_value_separator()
    parameters_separator = Functions_for__Enum__rgb_formulas_parameters().get_rgb_formulas_parameters_separator()

    rbg_formulas_represented_as__parameters_and_values = get_subjects_represented_as__parameters_and_values_from_bracket_expressions(txt=rgb_formulas, subject_name="rgb formula", outer_bracket_type=Enum__brackets.curly, inner_bracket_type=Enum__brackets.square,
                                            valid_parameters=rbg_formulas_parameters, required_parameters=rbg_formulas_parameters, parameter_value_separator=parameter_value_separator, parameters_separator=parameters_separator, parameter_for_error_messages=id)
    if(rbg_formulas_represented_as__parameters_and_values is None):
        return False
    
    for i in range(0, len(rbg_formulas_represented_as__parameters_and_values)):

        rbg_formula_represented_as__parameters_and_values = rbg_formulas_represented_as__parameters_and_values[i]
        
        id_txt = rbg_formula_represented_as__parameters_and_values[id]
        r_txt = rbg_formula_represented_as__parameters_and_values[r]
        g_txt = rbg_formula_represented_as__parameters_and_values[g]
        b_txt = rbg_formula_represented_as__parameters_and_values[b]

        is_id_valid = check_for_positive_int_format(txt_value=id_txt, is_zero_allowed=False)
        if(is_id_valid == False or id_txt==""):
            print(f"error: the rgb formula at index {i} has wrong format for the id; the id must be a positive integer")
            return False

        is_r_valid = check_RGB_formula_format(rgb_formula=r_txt, channel=r, use_areas=use_areas)
        is_g_valid = check_RGB_formula_format(rgb_formula=g_txt, channel=g, use_areas=use_areas)
        is_b_valid = check_RGB_formula_format(rgb_formula=b_txt, channel=b, use_areas=use_areas)
        if(is_r_valid == False or is_g_valid == False or is_b_valid == False):
            print(f"the previous error occured for the rgb formula with id {id_txt} at index {i}")
            return False
    return True
