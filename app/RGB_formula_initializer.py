import Z_RGB_formula_checker as RGB_formula_checker
from Z_RGB_formula import RGB_formula
from Formula_validation_collections import RGB_formula_validation_collections
from Bracket_expressions_getter import get_subjects_represented_as__parameters_and_values_from_bracket_expressions
from Enums import Enum__brackets, Enum_rgb_formulas_parameters

class RGB_formula_initializer():
    
    def __init__(self):
        self.rgb_formula_validation_collections = RGB_formula_validation_collections()


    #this function must be called from outside
    def create_rgb_formulas_without_pixel_areas(self, r_formula:str, g_formula:str, b_formula:str) -> RGB_formula:

        r_formula = r_formula.replace(" ", "").replace("\n", "")
        g_formula = g_formula.replace(" ", "").replace("\n", "")
        b_formula = b_formula.replace(" ", "").replace("\n", "")

        #<format checks
        
        is_r_formula_valid = RGB_formula_checker.check_RGB_formula_format(r_formula, "red")
        is_g_formula_valid = RGB_formula_checker.check_RGB_formula_format(g_formula, "green")
        is_b_formula_valid = RGB_formula_checker.check_RGB_formula_format(b_formula, "blue")

        if(is_r_formula_valid == False or is_g_formula_valid == False or is_b_formula_valid == False):
            return None
        
        #format checks>
        
        #<updating format

        r_formula = self.rgb_formula_validation_collections.update_format(formula=r_formula)
        g_formula = self.rgb_formula_validation_collections.update_format(formula=g_formula)
        b_formula = self.rgb_formula_validation_collections.update_format(formula=b_formula)

        
        r_formula = RGB_formula_checker.remove_indexes_from_rgb_channel_formula(formula = r_formula)
        g_formula = RGB_formula_checker.remove_indexes_from_rgb_channel_formula(formula = g_formula)
        b_formula = RGB_formula_checker.remove_indexes_from_rgb_channel_formula(formula = b_formula)

        #updating format>

        rgb_formula = RGB_formula(red_func=r_formula, green_func=g_formula, blue_func=b_formula)

        return rgb_formula


    def create_many_rgb_formulas(self, rgb_formulas:str, use_pixel_areas:bool) -> dict[int,RGB_formula]:

        rgb_formulas = rgb_formulas.replace(" ", "").replace("\n", "")
        rgb_formulas_dict:dict[int,RGB_formula] = {}

        id = Enum_rgb_formulas_parameters.id.name
        r = Enum_rgb_formulas_parameters.r.name
        g = Enum_rgb_formulas_parameters.g.name
        b = Enum_rgb_formulas_parameters.b.name
        rbg_formulas_parameters = (id, r, g, b)

        #check whether the format of the rgb formula is correct
        are_rgb_formulas_in_valid_format = RGB_formula_checker.check_rgb_formulas_format(rgb_formulas=rgb_formulas, use_areas=use_pixel_areas)
        if(are_rgb_formulas_in_valid_format == False):
            return None

        rbg_formulas_represented_as__parameters_and_values = get_subjects_represented_as__parameters_and_values_from_bracket_expressions(txt=rgb_formulas, subject_name="rgb formula", outer_bracket_type=Enum__brackets.curly, inner_bracket_type=Enum__brackets.square, valid_parameters=rbg_formulas_parameters, required_parameters=rbg_formulas_parameters, parameter_value_separator="->")
        if(rbg_formulas_represented_as__parameters_and_values is None):
            return None
        
        for i in range(0, len(rbg_formulas_represented_as__parameters_and_values)):

            r_formula = rbg_formulas_represented_as__parameters_and_values[i][r]
            g_formula = rbg_formulas_represented_as__parameters_and_values[i][g]
            b_formula = rbg_formulas_represented_as__parameters_and_values[i][b]

            r_formula = self.rgb_formula_validation_collections.update_format(formula=r_formula)
            g_formula = self.rgb_formula_validation_collections.update_format(formula=g_formula)
            b_formula = self.rgb_formula_validation_collections.update_format(formula=b_formula)

            if(use_pixel_areas == False):
                r_formula = RGB_formula_checker.remove_indexes_from_rgb_channel_formula(formula=r_formula)
                g_formula = RGB_formula_checker.remove_indexes_from_rgb_channel_formula(formula=g_formula)
                b_formula = RGB_formula_checker.remove_indexes_from_rgb_channel_formula(formula=b_formula)

            rbg_formulas_represented_as__parameters_and_values[i][r] = r_formula
            rbg_formulas_represented_as__parameters_and_values[i][g] = g_formula
            rbg_formulas_represented_as__parameters_and_values[i][b] = b_formula

            id_value = int(rbg_formulas_represented_as__parameters_and_values[i][id])
            rgb_formulas_dict[id_value] = RGB_formula(red_func=r_formula,green_func=g_formula,blue_func=b_formula)

        
        return rgb_formulas_dict
#the bottom code might be redundant so when all its references are removed it can be deleted !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




    #this function must be called from outside
    def create_rgb_formulas_with_pixel_areas(self, rgb_formulas:str) -> dict[int,RGB_formula]:
        
        rgb_formulas = rgb_formulas.replace(" ", "").replace("\n", "")

        #check whether the format of the rgb formula is correct
        if(RGB_formula_checker.check_rgb_formulas_format_for_pixel_areas(rgb_formulas_for_pixel_areas=rgb_formulas) == False):
            return None
        
        #the dictionary has rgb formula id (type int) as a key and a dictinary for value; the inner dictionaries have an rgb channels (values `r`,`g`,`b`) for keys and rgb formulas (represented as strings) for values
        rgb_formulas_dict_str = self.get_dictionary_of_rgb_formulas(rgb_formulas_for_pixel_areas = rgb_formulas)
        rgb_formulas_dict:dict[int,RGB_formula] = {}
        

        for id in rgb_formulas_dict_str.keys():
            
            r_formula = rgb_formulas_dict_str[id]["r"]
            r_formula = self.rgb_formula_validation_collections.update_format(formula=r_formula)

            g_formula = rgb_formulas_dict_str[id]["g"]
            g_formula = self.rgb_formula_validation_collections.update_format(formula=g_formula)

            b_formula = rgb_formulas_dict_str[id]["b"]
            b_formula = self.rgb_formula_validation_collections.update_format(formula=b_formula)
            

            rgb_formulas_dict[id] = RGB_formula(red_func=r_formula,green_func=g_formula,blue_func=b_formula)
        
        return rgb_formulas_dict
    

    #creates a dictonary which has rgb formula id (type int) as a key and a dictinary for value; the inner dictionaries have an rgb channels (values `r`,`g`,`b`) for keys and rgb formulas (represented as strings) for values
    #the input parameter `rgb_formulas_for_pixel_areas` must be in a valid format before calling the function
    def get_dictionary_of_rgb_formulas(self, rgb_formulas_for_pixel_areas:str)  -> dict[int,dict[str,str]] :

        rgb_formulas_pixel_area_start_index = 0
        rgb_formulas_pixel_area_end_index = 0        
        rgb_formulas_pixel_areas_dict = {}
        
        while(rgb_formulas_pixel_area_end_index < len(rgb_formulas_for_pixel_areas)-1):

            rgb_formulas_pixel_area_start_index = rgb_formulas_for_pixel_areas.find("{", rgb_formulas_pixel_area_end_index)
            rgb_formulas_pixel_area_end_index = rgb_formulas_for_pixel_areas.find("}", rgb_formulas_pixel_area_start_index)

            rgb_formulas_current_pixel_area = rgb_formulas_for_pixel_areas[rgb_formulas_pixel_area_start_index+1: rgb_formulas_pixel_area_end_index]
            (rgb_formula_id, rgb_formulas_dict) = self.get_rgb_formulas(rgb_formulas_for_pixel_area = rgb_formulas_current_pixel_area)
            rgb_formulas_pixel_areas_dict[rgb_formula_id] = rgb_formulas_dict
        
        return rgb_formulas_pixel_areas_dict

    

    def get_rgb_formulas(self, rgb_formulas_for_pixel_area: str):   
                
        rgb_formula_id_index_start = rgb_formulas_for_pixel_area.find("|", 0)
        rgb_formula_id_index_end = rgb_formulas_for_pixel_area.find("|", rgb_formula_id_index_start+1)

        rgb_formula_id = rgb_formulas_for_pixel_area[rgb_formula_id_index_start+1:rgb_formula_id_index_end]
            
        rgb_channel_index = 0
        rgb_formula_start_index = 0
        rgb_formula_end_index = 0
        rgb_channels = ["r", "g", "b"]
        rgb_formulas = {}

        while (rgb_channel_index < 3):

            rgb_formula_start_index = rgb_formulas_for_pixel_area.find("[", rgb_formula_end_index)
            rgb_formula_end_index = RGB_formula_checker.get_closing_square_bracket(text=rgb_formulas_for_pixel_area,start_index=rgb_formula_start_index)
           
            rgb_formula = rgb_formulas_for_pixel_area[rgb_formula_start_index+1:rgb_formula_end_index]
            rgb_formulas[rgb_channels[rgb_channel_index]] = rgb_formula
            
            rgb_channel_index+=1

        return (int(rgb_formula_id), rgb_formulas)

    
  