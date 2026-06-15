
import numpy as np

import Z_RGB_formula_checker as RGB_formula_checker#import RGB_formula_checker
from Z_RGB_formula import RGB_formula
from Formula_validation_collections import RGB_formula_validation_collections

class RGB_formula_initializer():
    
    def __init__(self, use_many_areas:bool):
        self.use_many_areas = use_many_areas
        self.rgb_formula_validation_collections = RGB_formula_validation_collections()

    #this function must be called from outside
    def create_rgb_formulas(self, r_formula:str, g_formula:str, b_formula:str) -> RGB_formula:

        #<format and executable checks
        
        is_r_formula_valid = RGB_formula_checker.check_RGB_formula_format(r_formula, "red")
        is_g_formula_valid = RGB_formula_checker.check_RGB_formula_format(g_formula, "green")
        is_b_formula_valid = RGB_formula_checker.check_RGB_formula_format(b_formula, "blue")

        if(is_r_formula_valid == False or is_g_formula_valid == False or is_b_formula_valid == False):
            return None
        
        is_r_formula_compatible_with_dxcam = RGB_formula_checker.is_RGB_formula_compatible_with_dxcam(rgb_formula=r_formula, channel="red", use_areas=self.use_many_areas)
        is_g_formula_compatible_with_dxcam = RGB_formula_checker.is_RGB_formula_compatible_with_dxcam(rgb_formula=g_formula, channel="green", use_areas=self.use_many_areas)
        is_b_formula_compatible_with_dxcam = RGB_formula_checker.is_RGB_formula_compatible_with_dxcam(rgb_formula=b_formula, channel="blue", use_areas=self.use_many_areas)

        if(is_r_formula_compatible_with_dxcam == False or is_g_formula_compatible_with_dxcam == False or is_b_formula_compatible_with_dxcam == False):
            return None
        
        #format and executable checks>
        
        #<updating format

        r_formula = self.rgb_formula_validation_collections.update_format(formula=r_formula)
        g_formula = self.rgb_formula_validation_collections.update_format(formula=g_formula)
        b_formula = self.rgb_formula_validation_collections.update_format(formula=b_formula)

        if(self.use_many_areas == False):
            r_formula = self.remove_indexes_from_rgb_channel_formula(rgb_channle_formula = r_formula)
            g_formula = self.remove_indexes_from_rgb_channel_formula(rgb_channle_formula = g_formula)
            b_formula = self.remove_indexes_from_rgb_channel_formula(rgb_channle_formula = b_formula)

        #updating format>

        rgb_formula = RGB_formula(red_func=r_formula, green_func=g_formula, blue_func=b_formula)

        return rgb_formula
    
    #this function must not be called from outside
    def remove_indexes_from_rgb_channel_formula(self, formula:str) -> str:
        
        rgb_chars = ['r','g','b']

        if(len(formula) <= 3):
            return formula
        
        allowed_operator_chars = self.rgb_formula_validation_collections.allowed_operator_chars

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

    
  