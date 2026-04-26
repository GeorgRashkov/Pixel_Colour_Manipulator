import ast
from Z_Pixel_area_animations import Pixel_area_animation_group
from Number_format_checker import check_for_positive_int_format, check_numbers_from_string

class Pixel_area_animation_groups_initializer:

    def __init__(self):      
        self.all_animation_group_properties_names = ["id", "a_ids"]
        self.animation_group_properties_with_int_value = ["id"]
        self.animation_group_properties_with_list_of_ints_value = ["a_ids"]
        self.id = "id"
      


    #the text input must contain rows of pixel area animation group notations
    #a pixel area animation group notation (animation group row) looks like this:
    #{id: 25; a_ids:[5,3]}
    def create_animation_groups_for_pixel_areas(self, text:str) -> list[Pixel_area_animation_group]:

        is_format_correct = self.check_animation_groups_str(text = text)

        if(is_format_correct == False):
            return None
        
        animation_groups_rows = self.get_animation_groups_rows(text=text)#this is a list of strings
        animation_groups = []#this is a list of objects of type `Pixel_area_animation_group`
        for row in animation_groups_rows:

            animation_group = self.create_pixel_area_animation_group(text=row)
            animation_groups.append(animation_group)
        
        return animation_groups


    #the text input must contain rows of pixel area animation group notations
    #a pixel area animation group notation (animation group row) looks like this:
    #{id: 25; a_ids:[5,3]}
    def check_animation_groups_str(self, text:str):

        animation_groups_rows = self.get_animation_groups_rows(text=text)
        if(animation_groups_rows == None):
            return False
        
        row_index = 0
        for row in animation_groups_rows:

            error_message = self.check_animation_group_id(text=row,row_index=row_index)
            if(error_message != ""):
                print(error_message)                
                return False
            
            error_message = self.check_animation_group_format(text=row)
            if(error_message != ""):
                animation_group_id = self.get_animation_group_property_value(text=row, animation_group_property_name=self.id)
                error_message = f"error: the animation group with id {animation_group_id} is in wrong format; " + error_message
                print(error_message)
                return False
            
            row_index+=1
        
        return True


    #the text input must contain rows of pixel area animation group notations
    def get_animation_groups_rows(self, text:str) -> list[str]:#each row contains the values of one pixel area animation group
        start_row_symbol = "{"
        end_row_symbol = "}"

        
        start_index = 0
        index = 0
        rows = []
    
        while(True):

            row_start_index = text.find(start_row_symbol, start_index)

            if(row_start_index!=-1 and row_start_index != start_index):
                print(f"error: the animation group at index {index} has content between `{end_row_symbol}` and `{start_row_symbol}`")
                return None

            if(row_start_index==-1):
                break
        
            row_end_index = text.find(end_row_symbol, row_start_index+1)
            if(row_end_index==-1):
                print(f"error: the animation group at index {index} has no closing curly bracket")
                return None      

            row = text[row_start_index+1: row_end_index]
            rows.append(row)

            start_index = row_end_index+1       

            index+=1
        
        return rows
    
    
    #the text input must be a pixel area animation group notation (the row content inside `{}`)
    def check_animation_group_id(self, text:str, row_index:int) -> str:
        
        animation_group_properties = text.split(";")
        ids_counter = 0
        error_message = ""
        
        for animation_group_property in animation_group_properties:
            
            if(ids_counter > 1):
                error_message = f"error: the animation group at row {row_index} has many ids"
                break

            animation_group_key_value = animation_group_property.split(":")
            animation_group_property_name = animation_group_key_value[0]

            if(animation_group_property_name == self.id):
                
                if(len(animation_group_key_value)<2):
                    error_message = f"error: the animation group at row {row_index} has id with no value"
                    break
                
                if(len(animation_group_key_value)>2):
                    error_message = f"error: the animation group at row {row_index} has id with many values"
                    break

                id_value = animation_group_key_value[1]
                is_format_valid = check_for_positive_int_format(txt_value=id_value, is_zero_allowed=True)
                if(is_format_valid == False):
                    error_message = f"error: the value of the id in the animation group at row {row_index} is in wrong format (only numbers are allowed)"
                    break
                
                ids_counter+=1
        

        if(ids_counter < 1):
            error_message = f"error: the animation group at row {row_index} has no id"
        elif(ids_counter > 1):
            error_message = f"error: the animation group at row {row_index} has many ids"

        return error_message
    
    
    #the text input must be a pixel area animation group notation (the row content inside `{}`)
    #the function get's the value of the property but it doesn't make any validation checks
    def get_animation_group_property_value(self, text:str, animation_group_property_name:str) -> str:

        animation_group_properties = text.split(";")

        for animation_group_property in animation_group_properties:

            animation_group_key_value = animation_group_property.split(":")
            if(animation_group_property_name == animation_group_key_value[0]):
                return animation_group_key_value[1]
        
        return ""


    #the text input must be a pixel area animation group notation (the row content inside `{}`)
    def check_animation_group_format(self, text:str):
        
        animation_group_properties = text.split(";")
        animation_group_properties_dict = {}        

        for animation_group_property in animation_group_properties:
            
            animation_group_key_value = animation_group_property.split(":")
            animation_group_property_name = animation_group_key_value[0]

            if(animation_group_property_name not in self.all_animation_group_properties_names):
                return f"the property `{animation_group_property_name}` is not allowed"
            
            if(len(animation_group_key_value) < 2):
                return f"the property `{animation_group_property_name}` has no value"

            if(len(animation_group_key_value) > 2):
                return f"the property `{animation_group_property_name}` has many values"
            
            if(animation_group_properties_dict.keys().__contains__(animation_group_property_name)):
                return f"the property `{animation_group_property_name}` is used many times"


            animation_group_property_value = animation_group_key_value[1]

            if(len(animation_group_property_value)==0):
                return f"the property `{animation_group_property_name}` has no value; if you don't want to use the property - delete it"


            if(animation_group_property_name in self.animation_group_properties_with_int_value):      
                
                is_format_valid = check_for_positive_int_format(txt_value=animation_group_property_value, is_zero_allowed=True)
                if(is_format_valid == False):
                    return f"the value of the animation group property `{animation_group_property_name}` is in wrong format (only positive numbers are allowed)"

            elif(animation_group_property_name in self.animation_group_properties_with_list_of_ints_value):   
                
                if(animation_group_property_value[0]!= "[" or animation_group_property_value[-1]!="]"):
                    return f"the value of the animation group property `{animation_group_property_name}` must start with `[` and end with `]`"
                elif(len(animation_group_property_value)<3):
                    return f"the list of the animation group property `{animation_group_property_name}` is empty; if you don't want to use the property - delete it"
                
                animation_group_property_value = animation_group_property_value[1:len(animation_group_property_value)-1]

                is_format_valid = check_numbers_from_string(txt_value=animation_group_property_value,separator=",")
                if(is_format_valid == False):
                    return f"the value of the area property `{animation_group_property_name}` is in wrong format (only numbers and commas are allowed)"

            else:
                raise Exception("animation group property name had no proper check case")
                    
        return ""
    

    
    #the text input must be a pixel area animation group notation (the row content inside `{}`)
    def create_pixel_area_animation_group(self, text:str) -> Pixel_area_animation_group:
        
        animation_group_properties = text.split(";")        
        animation_group_properties_dict = {property_name: None for property_name in self.all_animation_group_properties_names}
         

        for animation_group_property in animation_group_properties:
            
            animation_group_key_value = animation_group_property.split(":")
            animation_group_property_name = animation_group_key_value[0]
            animation_group_property_value = animation_group_key_value[1]
              
                 
            animation_group_properties_dict[animation_group_property_name] = animation_group_property_value 
        
        id = int(animation_group_properties_dict["id"])
        a_ids = ast.literal_eval(animation_group_properties_dict["a_ids"]) if animation_group_properties_dict["a_ids"] is not None else []

        animation_group = Pixel_area_animation_group(id=id, a_ids=a_ids)

        return animation_group    
