import numpy as np
from Number_format_checker import check_for_positive_int_format
from Formula_validation_collections import RGB_formula_validation_collections
from Formula_checker import check_formula_format, does_formula_contain_specific_variables
from Formula_validation_collections import RGB_formula_validation_collections


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
    does_formula_contain_atleast_one_rgb_channel = does_formula_contain_specific_variables(formula=rgb_formula, variables={'r','g','b'},  formula_validation_collections=rgb_formula_validation_collections, find_all=False)
    if(does_formula_contain_atleast_one_rgb_channel == False):
        return False
    
    is_format_correct = check_formula_format(formula=rgb_formula, expression_name=f"{channel} channel formula",  square_brackets_biggest_value=999_999, formula_validation_collections=rgb_formula_validation_collections)  
    if(is_format_correct == True):
        is_format_correct = is_RGB_formula_compatible_with_dxcam(rgb_formula=rgb_formula, channel=channel, use_areas=use_areas)

    return is_format_correct




def check_rgb_formulas_format_for_pixel_areas(rgb_formulas_for_pixel_areas: str) -> bool:
    
    rgb_formulas_pixel_area_start_index = 0
    rgb_formulas_pixel_area_end_index = 0
    index = 0
    
    while(True):

        rgb_formulas_pixel_area_start_index = rgb_formulas_for_pixel_areas.find("{", rgb_formulas_pixel_area_end_index)
        if(rgb_formulas_pixel_area_start_index==-1):
            break
    
        rgb_formulas_pixel_area_end_index = rgb_formulas_for_pixel_areas.find("}", rgb_formulas_pixel_area_start_index)
        if(rgb_formulas_pixel_area_end_index==-1):
            print(f"error: the rgb formula at index {index} had no closing curly bracket")
            return False      

        rgb_formulas_current_pixel_area = rgb_formulas_for_pixel_areas[rgb_formulas_pixel_area_start_index+1: rgb_formulas_pixel_area_end_index]
        are_rgb_formulas_for_current_pixel_area_valid = check_rgb_formulas_format_for_pixel_area(rgb_formulas_for_pixel_area = rgb_formulas_current_pixel_area, index = index)

        if(are_rgb_formulas_for_current_pixel_area_valid == False):
            return False

        index+=1
    
    return True

def check_rgb_formulas_format_for_pixel_area(rgb_formulas_for_pixel_area: str, index) -> bool:   
                
    rgb_formula_id_index_start = rgb_formulas_for_pixel_area.find("|", 0)
    if(rgb_formula_id_index_start == -1):
        print(f"error: the rgb formula at index {index} has no id")
        return False
        
    rgb_formula_id_index_end = rgb_formulas_for_pixel_area.find("|", rgb_formula_id_index_start + 1)
    if(rgb_formula_id_index_start == -1):
        print(f"error: the id of the rgb formula at index {index} was not closed")
        return False
    
    rgb_formula_id_wrong_index = rgb_formulas_for_pixel_area.find("|", rgb_formula_id_index_end + 1)
    if(rgb_formula_id_wrong_index != -1):
        print(f"error: the rgb formula at index {index} cannot have more than 2 `|` symbols")
        return False

    rgb_formula_id = rgb_formulas_for_pixel_area[rgb_formula_id_index_start+1:rgb_formula_id_index_end]
    is_rgb_formula_id_valid = check_for_positive_int_format(rgb_formula_id)

    if(is_rgb_formula_id_valid == False):
        print(f"error: the rgb formula at index {index} has wrong format for the id; the id must be a positive integer")
        return False
        
    formulas_counter = 0
    rgb_formula_start_index = 0
    rgb_formula_end_index = 0
    rgb_channels = ["red", "green", "blue"]

    while (formulas_counter < 3):

        rgb_formula_start_index = rgb_formulas_for_pixel_area.find("[", rgb_formula_end_index)
        if(rgb_formula_start_index==-1):
            print(f"error: the rgb formula at index {index} (id {rgb_formula_id}) has less than 3 colour channel formulas")
            return False

        
        rgb_formula_end_index = get_closing_square_bracket(text=rgb_formulas_for_pixel_area, start_index=rgb_formula_start_index)       
        
        if(rgb_formula_end_index==-1):
            print(f"error: the rgb formula at index {index} (id {rgb_formula_id}) had no closing curly square bracket for {rgb_channels[formulas_counter]} channel")
            return False
        
        if(rgb_formula_end_index - rgb_formula_start_index < 2):
            print(f"error: the rgb formula at index {index} (id {rgb_formula_id}) had no content for the {rgb_channels[formulas_counter]} channel")
            return False
        
        rgb_formula = rgb_formulas_for_pixel_area[rgb_formula_start_index+1:rgb_formula_end_index]

        if (check_RGB_formula_format(rgb_formula, channel=rgb_channels[formulas_counter], use_areas=True) == False):
            print(f"the previous error occurred at rgb formula index {index} (id {rgb_formula_id})")
            return False
       
        formulas_counter+=1
    
    if(rgb_formulas_for_pixel_area.find("[", rgb_formula_end_index) != -1):
        print(f"error: the rgb formula at index {index} (id {rgb_formula_id}) has more than 3 colour channel formulas")
        return False

    return True
    

def get_closing_square_bracket(text:str, start_index:int) -> int:
    
    index = start_index+1
    int_helper = 1
    searched_index = -1

    while (index < len(text)):
        
        if(text[index] == "["):
            int_helper+=1
        elif(text[index] == "]"):
            int_helper-=1
        
        if(int_helper == 0):
            searched_index = index
            break

        index+=1
    
    return searched_index