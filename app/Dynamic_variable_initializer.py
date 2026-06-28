from Number_format_checker import check_for_positive_int_format, check_for_float_format
from Dynamic_variable import Dynamic_variable
from Formula_validation_collections import Dynamic_variable_formula_validation_collections
from Formula_checker import check_formula_format

class Dynamic_variable_initializer:

    def __init__(self):
        self.properties_names = ["id", "frequency", "modulo_loop", "start", "end", "step"]
        
        self.properties_with_positive_int_value = ["id", "frequency", "modulo_loop"]
        self.properties_with_float_value = ["start", "end"]
        self.properties_with_formula_value = ["step"]
    
        self.id = "id"

        self.dynamic_variable_formula_validation_collections = Dynamic_variable_formula_validation_collections()

    #the text input must contain rows of dynamic variables notations
    #a dynamic variables notation (dynamic variables row) looks like this:
    #{id:1; start:25; end:256; step:"4*3+v[24]"; frequency:7}
    def create_dynamic_variables(self, text:str) -> list[Dynamic_variable]:#returns a list  of objects of type `Dynamic_variable`

        is_format_correct = self.check_dynamic_variables_str(text = text)

        if(is_format_correct == False):
            return None
        
        dynamic_variables_rows = self.get_dynamic_variables_rows(text=text)#this is a list of strings
        dynamic_variables:list[Dynamic_variable] = []#this is a list of objects of type `Dynamic_variable`
        for row in dynamic_variables_rows:
            dynamic_variable = self.create_dynamic_variable(text=row)
            dynamic_variables.append(dynamic_variable)
        
        return dynamic_variables


    #the text input must contain rows of dynamic variables notations
    #a dynamic variables notation (dynamic variables row) looks like this:
    #{id:1; start:25; end:256; step:"4*3+v[24]"; frequency:7}
    def check_dynamic_variables_str(self, text:str):

        dynamic_variables_rows = self.get_dynamic_variables_rows(text=text)
        if(dynamic_variables_rows == None):
            return False
        
        row_index = 0
        for row in dynamic_variables_rows:

            error_message = self.check_dynamic_variable_id(text=row,row_index=row_index)
            if(error_message != ""):
                print(error_message)                
                return False
            
            error_message = self.check_dynamic_variable_format(text=row)
            if(error_message != ""):
                dynamic_variable_id = self.get_dynamic_variable_property_value(text=row, dynamic_variable_property_name=self.id)
                error_message = f"error: the dynamic variable with id {dynamic_variable_id} is in wrong format; " + error_message
                print(error_message)
                return False
            
            row_index+=1
        
        return True


    #the text input must contain rows of dynamic_variables notations
    def get_dynamic_variables_rows(self, text:str):#each row contains the values of one dynamic_variables
        start_row_symbol = "{"
        end_row_symbol = "}"

        
        start_index = 0
        index = 0
        rows = []
    
        while(True):

            row_start_index = text.find(start_row_symbol, start_index)

            if(row_start_index!=-1 and row_start_index != start_index):
                print(f"error: the dynamic variable at index {index} has content between `{end_row_symbol}` and `{start_row_symbol}`")
                return None

            if(row_start_index==-1):
                break
        
            row_end_index = text.find(end_row_symbol, row_start_index+1)
            if(row_end_index==-1):
                print(f"error: the dynamic variable at index {index} has no closing curly bracket")
                return None      

            row = text[row_start_index+1: row_end_index]
            rows.append(row)

            start_index = row_end_index+1       

            index+=1
        
        return rows
   
    
    #the text input must be a dynamic_variable notation (the row content inside `{}`)
    def check_dynamic_variable_id(self, text:str, row_index:int) -> str:
        
        dynamic_variable_properties = text.split(";")
        ids_counter = 0
        error_message = ""
        
        for dynamic_variable_property in dynamic_variable_properties:
            
            if(ids_counter > 1):
                error_message = f"error: the dynamic variable at row {row_index} has many ids"

            dynamic_variable_key_value = dynamic_variable_property.split(":")
            dynamic_variable_property_name = dynamic_variable_key_value[0]

            if(dynamic_variable_property_name == self.id):
                
                if(len(dynamic_variable_key_value)<2):
                    error_message = f"error: the dynamic variable at row {row_index} has id with no value"
                
                if(len(dynamic_variable_key_value)>2):
                    error_message = f"error: the dynamic variable at row {row_index} has id with many values"

                id_value = dynamic_variable_key_value[1]
                is_format_valid = check_for_positive_int_format(txt_value=id_value, is_zero_allowed=True)
                if(is_format_valid == False):
                    error_message = f"error: the value of the id in the dynamic variable at row {row_index} is in wrong format (only numbers are allowed)"
                
                ids_counter+=1
            
            if(error_message != ""):
                break
        
        if(ids_counter < 1):
            error_message = f"error: the dynamic variable at row {row_index} has no id"
        elif(ids_counter > 1):
            error_message = f"error: the dynamic variable at row {row_index} has many ids"

        return error_message
    
    #the text input must be a dynamic variable notation (the row content inside `{}`)
    #the function get's the value of the property but it doesn't make any validation checks
    def get_dynamic_variable_property_value(self, text:str, dynamic_variable_property_name:str) -> str:

        dynamic_variable_properties = text.split(";")

        for dynamic_variable_property in dynamic_variable_properties:

            area_key_value = dynamic_variable_property.split(":")
            if(dynamic_variable_property_name == area_key_value[0]):
                return area_key_value[1]
        
        return ""

    #the text input must be a dynamic variable notation (the row content inside `{}`)
    def check_dynamic_variable_format(self, text:str):
        
        dynamic_variable_properties = text.split(";")
        dynamic_variable_properties_dict = {}        

        for dynamic_variable_property in dynamic_variable_properties:
            
            dynamic_variable_key_value = dynamic_variable_property.split(":")
            dynamic_variable_property_name = dynamic_variable_key_value[0]

            if(dynamic_variable_property_name not in self.properties_names):
                return f"the property `{dynamic_variable_property_name}` is not allowed"
            
            if(len(dynamic_variable_key_value) < 2):
                return f"the property `{dynamic_variable_property_name}` has no value"

            if(len(dynamic_variable_key_value) > 2):
                return f"the property `{dynamic_variable_property_name}` has many values"
            
            if(dynamic_variable_properties_dict.keys().__contains__(dynamic_variable_property_name)):
                return f"the property `{dynamic_variable_property_name}` is used many times"


            dynamic_variable_property_value = dynamic_variable_key_value[1]

            if(len(dynamic_variable_property_value)==0):
                return f"the property `{dynamic_variable_property_name}` has no value; if you don't want to use the property - delete it"

            if(dynamic_variable_property_name in self.properties_with_positive_int_value):
                                
                is_format_valid = check_for_positive_int_format(txt_value=dynamic_variable_property_value, is_zero_allowed=True)
                if(is_format_valid == False):
                        return f"the value of the area property `{dynamic_variable_property_name}` is in wrong format (only positive int numbers are allowed)"

            elif(dynamic_variable_property_name in self.properties_with_float_value):
                                
                is_format_valid = check_for_float_format(txt_value=dynamic_variable_property_value)
                if(is_format_valid == False):
                        return f"the value of the area property `{dynamic_variable_property_name}` is in wrong format (only float numbers are allowed)"

            elif(dynamic_variable_property_name in self.properties_with_formula_value):

                step_formula =  dynamic_variable_property_value               
                is_format_valid = check_formula_format(formula=step_formula, expression_name="dynamic variable step", 
                square_brackets_biggest_value=999_999, formula_validation_collections=self.dynamic_variable_formula_validation_collections)

                if(is_format_valid == False):
                    return "\n"       
        return ""
    
    #the text input must be a dynamic variable notation (the row content inside `{}`)
    def create_dynamic_variable(self, text:str):
        
        dynamic_variables = text.split(";")        
        dynamic_variables_dict:dict[str,str] = {property_name: None for property_name in self.properties_names}
         

        for dynamic_variable_property in dynamic_variables:
            
            dynamic_variable_key_value = dynamic_variable_property.split(":")
            dynamic_variable_property_name = dynamic_variable_key_value[0]
            dynamic_variable_property_value = dynamic_variable_key_value[1]
            dynamic_variables_dict[dynamic_variable_property_name] = dynamic_variable_property_value
        
        #makes the string values into ints
        id = int(dynamic_variables_dict["id"]) if dynamic_variables_dict["id"] is not None else 0
        frequency = int(dynamic_variables_dict["frequency"]) if dynamic_variables_dict["frequency"] is not None else 0
        modulo_loop = int(dynamic_variables_dict["modulo_loop"]) if dynamic_variables_dict["modulo_loop"] is not None else 0

        #makes the string values into floats
        start = float(dynamic_variables_dict["start"]) if dynamic_variables_dict["start"] is not None else 0
        end = float(dynamic_variables_dict["end"]) if dynamic_variables_dict["end"] is not None else 0

        step = dynamic_variables_dict["step"] if dynamic_variables_dict["step"] is not None else "0"
        step = self.dynamic_variable_formula_validation_collections.update_format(formula=step)
        dynamic_variable = Dynamic_variable(id=id, frequency=frequency, start=start, end=end, step=step, modulo_loop=modulo_loop==1)

        return dynamic_variable