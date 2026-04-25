from Z_Pixel_area_animations import Pixel_area_animation, Pixel_area_animation_xywh, Pixel_area_animation_for_list_of_ints, Pixel_area_animation_for_list_of_lists_of_ints
import ast
from Number_format_checker import check_for_positive_int_format, check_numbers_from_string, check_lists_of_numbers_from_string, check_for_int_format

class Pixel_area_animations_initializer:

    def __init__(self):
        
        self.all_properties_names = [
            "id", "a_type", "step", "step_img_s", "step_img_w", "step_img_h", "frequency", 
            "initial_value", "border", "border_exact", "values", "values_exact",
            "values"            
            ]
        
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  
        self.animation_xyhw_properties_names = [
            "id", "a_type", "step", "step_img_s", "step_img_w", "step_img_h", "frequency", 
            "initial_value", "border", "border_exact", "values", "values_exact",           
        ]
        self.animation_xyhw_type_values = [ "x", "y", "w", "h"]
        #-------
        self.animation_for_list_of_ints_properties_names = [
            "id", "a_type", "step", "step_img_s", "step_img_w", "step_img_h", "frequency",
            "values",          
        ]       
        self.animation_for_list_of_ints_type_values = ["f_id", "img_in_v", "img_out_v", "img_out_stack"]
        #-------
        self.animation_for_list_of_lists_of_ints_properties_names = [
            "id", "a_type", "step", "step_img_s", "step_img_w", "step_img_h", "frequency", 
            "values",            
        ]        
        self.animation_for_list_of_lists_of_ints_type_values = ["a_ids", "ag_ids", "p_ids", "p_x", "p_y", "x_rep_start", "y_rep_start", "x_rep_end", "y_rep_end", "x_rep_step", "y_rep_step", "x_rep_count", "y_rep_count"]

        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.animation_types_with_non_zero_int_value = ["w", "h", "img_out_v"]

        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.animation_properties_with_int_value = [ "id", "step", "step_img_s", "step_img_w", "step_img_h", "frequency", "initial_value", "border", "border_exact"]
        self.animation_properties_with_positive_int_value = ["id", "frequency", "initial_value", "border", "border_exact"]
        self.animation_properties_with_positive_or_negative_int_value = ["step", "step_img_s", "step_img_w", "step_img_h"]
        

        #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        self.animation_type_values = ["x", "y", "w", "h", "a_ids", "ag_ids", "f_id", "p_ids", "p_x", "p_y", "img_in_v", "img_out_v", "img_out_stack", "x_rep_start", "y_rep_start", "x_rep_end", "y_rep_end", "x_rep_step", "y_rep_step", "x_rep_count", "y_rep_count"]
        self.animation_value_properties_names = ["values", "values_exact"]

        """
        self.area_properties_with_list_of_ints_value = ["a_ids", "ag_ids", "p_ids", "p_x", "p_y", "x_rep_start", "y_rep_start", "x_rep_end", "y_rep_end", "x_rep_step", "y_rep_step", "x_rep_count", "y_rep_count"]
        self.area_properties_with_list_of_list_of_ints_value = ["f_ids_rep", "rotations_rep"]
        """
        self.id = "id"
        self.a_type = "a_type"
        


    #the text input must contain rows of pixel area animation notations
    #a pixel area animation notation (animation row) looks like this:
    #animation_xyhw - {id:2; a_type:w; step:2; step_img_s:3; step_img_w:7; step_img_h:-6; frequency:1; initial_value:20; border:20; border_exact:50; values:[]; values_exact:[]}
    #animation_xyhw - {id:2; a_type:w; step:2; step_img_s:3; step_img_w:7; step_img_h:-6; frequency:1; initial_value:20; border:20; border_exact:50; values:[1,5,2,5,3]; values_exact:[3]}
    #animation_for_list_of_ints - {id:5; a_type:f_id; step:100; step_img_s:0; step_img_w:0; step_img_h:0; frequency:1; values:[1,2,5,7,3]}
    #animation_for_list_of_lists_of_ints - {id:3; a_type:p_ids; step:10; step_img_s:-5; step_img_w:0; step_img_h:0; frequency:3; values:[(1,2,3),(2,5),(1,6,8,2)]}
    def create_animations_for_pixel_areas(self, text:str) -> list[Pixel_area_animation]:

        is_format_correct = self.check_animations_str(text = text)

        if(is_format_correct == False):
            return None
        
        animations_rows = self.get_animations_rows(text=text)#this is a list of strings
        animations = []#this is a list of objects of type `Pixel_area_animation`
        for row in animations_rows:

            animation = self.create_pixel_area_animation(text=row)
            animations.append(animation)
        
        return animations


    #the text input must contain rows of pixel area animation notations
    #a pixel area animation notation (animation row) looks like this:
    #animation_xyhw - {id:2; a_type:w; step:2; step_img_s:3; step_img_w:7; step_img_h:-6; frequency:1; initial_value:20; border:20; border_exact:50; values:[]; values_exact:[]}
    #animation_xyhw - {id:2; a_type:w; step:2; step_img_s:3; step_img_w:7; step_img_h:-6; frequency:1; initial_value:20; border:20; border_exact:50; values:[1,5,2,5,3]; values_exact:[3]}
    #animation_for_list_of_ints - {id:5; a_type:f_id; step:100; step_img_s:0; step_img_w:0; step_img_h:0; frequency:1; values:[1,2,5,7,3]}
    #animation_for_list_of_lists_of_ints - {id:3; a_type:p_ids; step:10; step_img_s:-5; step_img_w:0; step_img_h:0; frequency:3; values:[(1,2,3),(2,5),(1,6,8,2)]}
    def check_animations_str(self, text:str):

        animations_rows = self.get_animations_rows(text=text)
        if(animations_rows == None):
            return False
        
        row_index = 0
        for row in animations_rows:

            error_message = self.check_animation_id(text=row,row_index=row_index)
            if(error_message != ""):
                print(error_message)                
                return False
            
            error_message = self.check_animation_type(text=row,row_index=row_index)
            if(error_message != ""):
                print(error_message)                
                return False
            
            animation_type_value = self.get_animation_property_value(text=row, animation_property_name=self.a_type)
            
            error_message = self.check_animation_format(text=row, animation_type_value=animation_type_value)
            if(error_message != ""):
                animation_id = self.get_animation_property_value(text=row, animation_property_name=self.id)
                error_message = f"error: the animation with id {animation_id} is in wrong format; " + error_message
                print(error_message)
                return False
            
            row_index+=1
        
        return True


    #the text input must contain rows of pixel area animation notations
    def get_animations_rows(self, text:str) -> list[str]:#each row contains the values of one pixel area animation
        start_row_symbol = "{"
        end_row_symbol = "}"

        
        start_index = 0
        index = 0
        rows = []
    
        while(True):

            row_start_index = text.find(start_row_symbol, start_index)

            if(row_start_index!=-1 and row_start_index != start_index):
                print(f"error: the animation at index {index} has content between `{end_row_symbol}` and `{start_row_symbol}`")
                return None

            if(row_start_index==-1):
                break
        
            row_end_index = text.find(end_row_symbol, row_start_index+1)
            if(row_end_index==-1):
                print(f"error: the animation at index {index} has no closing curly bracket")
                return None      

            row = text[row_start_index+1: row_end_index]
            rows.append(row)

            start_index = row_end_index+1       

            index+=1
        
        return rows
    
    
    #the text input must be a pixel area animation notation (the row content inside `{}`)
    def check_animation_id(self, text:str, row_index:int) -> str:
        
        animation_properties = text.split(";")
        ids_counter = 0
        error_message = ""
        
        for animation_property in animation_properties:
            
            if(ids_counter > 1):
                error_message = f"error: the animation at row {row_index} has many ids"
                break

            animation_key_value = animation_property.split(":")
            animation_property_name = animation_key_value[0]

            if(animation_property_name == self.id):
                
                if(len(animation_key_value)<2):
                    error_message = f"error: the animation at row {row_index} has id with no value"
                    break
                
                if(len(animation_key_value)>2):
                    error_message = f"error: the animation at row {row_index} has id with many values"
                    break

                id_value = animation_key_value[1]
                is_format_valid = check_for_positive_int_format(txt_value=id_value, is_zero_allowed=True)
                if(is_format_valid == False):
                    error_message = f"error: the value of the id in the animation at row {row_index} is in wrong format (only numbers are allowed)"
                    break
                
                ids_counter+=1
        

        if(ids_counter < 1):
            error_message = f"error: the animation at row {row_index} has no id"
        elif(ids_counter > 1):
            error_message = f"error: the animation at row {row_index} has many ids"

        return error_message
    
    #the text input must be a pixel area animation notation (the row content inside `{}`)
    def check_animation_type(self, text:str, row_index:int) -> str:
        
        animation_properties = text.split(";")
        animation_types_counter = 0
        error_message = ""

        for animation_property in animation_properties:
            
            if(animation_types_counter > 1):
                error_message = f"error: the animation at row {row_index} has many animation types"
                break

            animation_key_value = animation_property.split(":")
            animation_property_name = animation_key_value[0]

            if(animation_property_name == self.a_type):
                
                if(len(animation_key_value)<2):
                    error_message = f"error: the animation at row {row_index} has animation type with no value"
                    break
                
                if(len(animation_key_value)>2):
                    error_message = f"error: the animation at row {row_index} has animation type with many values"
                    break

                a_type_value = animation_key_value[1]                
                if(a_type_value not in self.animation_type_values):
                    error_message = f"error: at row {row_index} the value {a_type_value} is not a valid animation type"
                    break
                
                animation_types_counter+=1
        
        if(animation_types_counter < 1):
            error_message = f"error: the animation at row {row_index} has no animation type"
        elif(animation_types_counter > 1):
            error_message = f"error: the animation at row {row_index} has many animation types"

        return error_message
    
    #the text input must be a pixel area animation notation (the row content inside `{}`)
    #the function get's the value of the property but it doesn't make any validation checks
    def get_animation_property_value(self, text:str, animation_property_name:str) -> str:

        animation_properties = text.split(";")

        for animation_property in animation_properties:

            animation_key_value = animation_property.split(":")
            if(animation_property_name == animation_key_value[0]):
                return animation_key_value[1]
        
        return ""


    #the text input must be a pixel area animation notation (the row content inside `{}`)
    def check_animation_format(self, text:str, animation_type_value:str):
        
        animation_properties = text.split(";")
        animation_properties_dict = {}        

        for animation_property in animation_properties:
            
            animation_key_value = animation_property.split(":")
            animation_property_name = animation_key_value[0]
            
            #since the type is already checked there is no need to check it again
            if(animation_property_name == self.a_type):
                continue

            if(animation_property_name not in self.all_properties_names):
                return f"the property `{animation_property_name}` is not allowed"
            
            if(len(animation_key_value) < 2):
                return f"the property `{animation_property_name}` has no value"

            if(len(animation_key_value) > 2):
                return f"the property `{animation_property_name}` has many values"
            
            if(animation_properties_dict.keys().__contains__(animation_property_name)):
                return f"the property `{animation_property_name}` is used many times"


            animation_property_value = animation_key_value[1]

            if(len(animation_property_value)==0):
                return f"the property `{animation_property_name}` has no value; if you don't want to use the property - delete it"


            is_animation_type_compatible_with_animation_property = self.check_compatibility_between_animation_property_and_animation_type(animation_property_name=animation_property_name, animation_type_value=animation_type_value)
            if(is_animation_type_compatible_with_animation_property == False):
                return f"the property `{animation_property_name}` is not compatible with animation type `{animation_type_value}`"


            if(animation_property_name in self.animation_value_properties_names):
                error_message = self.check_compatibility_between_animation_values_and_animation_type(animation_property_name=animation_property_name, animation_property_value=animation_property_value, animation_type_value=animation_type_value)
                if(error_message != ""):
                    return error_message
                else:
                    continue

            if(animation_property_name in self.animation_properties_with_int_value):
                                
                if(animation_property_name in self.animation_properties_with_positive_int_value):
                    is_format_valid = check_for_positive_int_format(txt_value=animation_property_value, is_zero_allowed=True)
                    if(is_format_valid == False):
                        return f"the value of the animation property `{animation_property_name}` is in wrong format (only positive numbers are allowed)"
                else:
                    is_format_valid = check_for_int_format(txt_value=animation_property_value)
                    if(is_format_valid == False):
                        return f"the value of the animation property `{animation_property_name}` is in wrong format (only numbers are allowed)"
            
            else:
                raise Exception("animation property name had no proper check case")
                    
        return ""
    


    def check_compatibility_between_animation_property_and_animation_type(self, animation_property_name:str, animation_type_value:str) -> bool:
        
        if(animation_type_value in self.animation_xyhw_type_values and 
           animation_property_name in self.animation_xyhw_properties_names):
            return True
        
        if(animation_type_value in self.animation_for_list_of_ints_type_values and 
           animation_property_name in self.animation_for_list_of_ints_properties_names):
            return True
        
        if(animation_type_value in self.animation_for_list_of_lists_of_ints_type_values and 
           animation_property_name in self.animation_for_list_of_lists_of_ints_properties_names):
            return True
        
        return False
    
    def check_compatibility_between_animation_values_and_animation_type(self, animation_property_name:str, animation_property_value:str, animation_type_value:str) -> str:
        
        if(animation_property_name not in self.animation_value_properties_names):
            raise Exception("property name for animation values was not found!")
        

        if(animation_property_value[0]!= "[" or animation_property_value[-1]!="]"):
            return f"the value of the animation property `{animation_property_name}` must start with `[` and end with `]`"
        elif(len(animation_property_value)<3):
            return f"the list of the animation property `{animation_property_name}` is empty; if you don't want to use the property - delete it"
        
        animation_property_value = animation_property_value[1:len(animation_property_value)-1]


        if( (animation_type_value in self.animation_xyhw_type_values and animation_property_name in self.animation_xyhw_properties_names) or
           (animation_type_value in self.animation_for_list_of_ints_type_values and animation_property_name in self.animation_for_list_of_ints_properties_names) ):
                                            
            is_format_valid = check_numbers_from_string(txt_value=animation_property_value,separator=",")

            if(is_format_valid == False):
                return f"the value of the animation property `{animation_property_name}` is in wrong format (only positive numbers and commas are allowed)"
        
        
        elif(animation_type_value in self.animation_for_list_of_lists_of_ints_type_values and 
           animation_property_name in self.animation_for_list_of_lists_of_ints_properties_names):
           
            animation_property_value = animation_property_value.replace("),",");")
            is_format_valid = check_lists_of_numbers_from_string(txt_value=animation_property_value, outer_separator=";", inner_separator=",", opening_bracket_symbol="(", closing_bracket_symbol=")")
            if(is_format_valid == False):
                return f"the value of the animation property `{animation_property_name}` is in wrong format; the values inside the square brackets must be collections (each collection must start with `(` and end with `)`) of positive integers separated by comma"
        
        else:
            raise Exception("the animation type was not compatible with the animation property name")

        return ""
        




    
    #the text input must be a pixel area animation notation (the row content inside `{}`)
    def create_pixel_area_animation(self, text:str) -> Pixel_area_animation:
        
        animation_properties = text.split(";")        
        animation_properties_dict = {property_name: None for property_name in self.all_properties_names}
         
        animation_type_value = ""

        for animation_property in animation_properties:
            
            animation_key_value = animation_property.split(":")
            animation_property_name = animation_key_value[0]
            animation_property_value = animation_key_value[1]

            if(animation_property_name == self.a_type):
                animation_type_value = animation_property_value
              
                 
            animation_properties_dict[animation_property_name] = animation_property_value

        animation = None    
        
        if(animation_type_value in self.animation_xyhw_type_values):
            animation = self.create_animation_xyhw(animation_properties_dict=animation_properties_dict)
        
        elif(animation_type_value in self.animation_for_list_of_ints_type_values):
            animation = self.create_animation_for_list_of_ints(animation_properties_dict=animation_properties_dict)
        
        elif(animation_type_value in self.animation_for_list_of_lists_of_ints_type_values):
            animation = self.create_animation_for_list_of_lists_of_ints(animation_properties_dict=animation_properties_dict)
    
        return animation    
    
    def create_animation_xyhw(self, animation_properties_dict:dict[str,str]) -> Pixel_area_animation_xywh:
                
        id = int(animation_properties_dict["id"])
        a_type = animation_properties_dict["a_type"]

        step = int(animation_properties_dict["step"]) if animation_properties_dict["step"] is not None else 0
        step_img_s = int(animation_properties_dict["step_img_s"]) if animation_properties_dict["step_img_s"] is not None else 0
        step_img_w = int(animation_properties_dict["step_img_w"]) if animation_properties_dict["step_img_w"] is not None else 0
        step_img_h = int(animation_properties_dict["step_img_h"]) if animation_properties_dict["step_img_h"] is not None else 0
        frequency = int(animation_properties_dict["frequency"]) if animation_properties_dict["frequency"] is not None else 0
        
        initial_value = int(animation_properties_dict["initial_value"]) if animation_properties_dict["initial_value"] is not None else 0
        border = int(animation_properties_dict["border"]) if animation_properties_dict["border"] is not None else 0
        border_exact = int(animation_properties_dict["border_exact"]) if animation_properties_dict["border_exact"] is not None else 0

        values = ast.literal_eval(animation_properties_dict["values"]) if animation_properties_dict["values"] is not None else []
        values_exact = ast.literal_eval(animation_properties_dict["values_exact"]) if animation_properties_dict["values_exact"] is not None else []
        
        pixel_area_animation_xywh = Pixel_area_animation_xywh(id=id, a_type=a_type, step=step, step_img_s=step_img_s, step_img_w=step_img_w, step_img_h=step_img_h, frequency=frequency, initial_value=initial_value, border=border, border_exact=border_exact, values=values, values_exact=values_exact)
        return pixel_area_animation_xywh

    def create_animation_for_list_of_ints(self, animation_properties_dict:dict[str,str]) -> Pixel_area_animation_for_list_of_ints:
        
        id = int(animation_properties_dict["id"])
        a_type = animation_properties_dict["a_type"]

        step = int(animation_properties_dict["step"]) if animation_properties_dict["step"] is not None else 0
        step_img_s = int(animation_properties_dict["step_img_s"]) if animation_properties_dict["step_img_s"] is not None else 0
        step_img_w = int(animation_properties_dict["step_img_w"]) if animation_properties_dict["step_img_w"] is not None else 0
        step_img_h = int(animation_properties_dict["step_img_h"]) if animation_properties_dict["step_img_h"] is not None else 0
        frequency = int(animation_properties_dict["frequency"]) if animation_properties_dict["frequency"] is not None else 0

        values = ast.literal_eval(animation_properties_dict["values"]) if animation_properties_dict["values"] is not None else []

        pixel_area_animation_for_list_of_ints = Pixel_area_animation_for_list_of_ints(id=id, a_type=a_type, step=step, step_img_s=step_img_s, step_img_w=step_img_w, step_img_h=step_img_h, frequency=frequency, values=values)
        return pixel_area_animation_for_list_of_ints

    def create_animation_for_list_of_lists_of_ints(self, animation_properties_dict:dict[str,str]) -> Pixel_area_animation_for_list_of_lists_of_ints:
        
        id = int(animation_properties_dict["id"])
        a_type = animation_properties_dict["a_type"]

        step = int(animation_properties_dict["step"]) if animation_properties_dict["step"] is not None else 0
        step_img_s = int(animation_properties_dict["step_img_s"]) if animation_properties_dict["step_img_s"] is not None else 0
        step_img_w = int(animation_properties_dict["step_img_w"]) if animation_properties_dict["step_img_w"] is not None else 0
        step_img_h = int(animation_properties_dict["step_img_h"]) if animation_properties_dict["step_img_h"] is not None else 0
        frequency = int(animation_properties_dict["frequency"]) if animation_properties_dict["frequency"] is not None else 0

        values = self.get__animation_property_with_list_of_lists_of_ints_value(area_property=animation_properties_dict["values"])

        pixel_area_animation_for_list_of_lists_of_ints = Pixel_area_animation_for_list_of_lists_of_ints(id=id, a_type=a_type, step=step, step_img_s=step_img_s, step_img_w=step_img_w, step_img_h=step_img_h, frequency=frequency, values=values)
        return pixel_area_animation_for_list_of_lists_of_ints


    def get__animation_property_with_list_of_lists_of_ints_value(self, animation_property_values:str) -> list[str]:

        main_list = []
        if animation_property_values is not None:

            #the result is list of strings which will be something like that `["[1,2]","[]","[5,2,5,2]","[1]"]`
            collections_of_values = animation_property_values[1:-1].replace("(", "[").replace(")","]").replace("],","];").split(";")
            for collection_of_values in collections_of_values:
                main_list.append(ast.literal_eval(collection_of_values))

        return main_list

