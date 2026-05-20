from Z_Pixel_area import Pixel_area
import ast
from Number_format_checker import check_for_positive_int_format, check_numbers_from_string, check_lists_of_numbers_from_string

class Pixel_area_initializer:

    def __init__(self):
        self.area_properties_names = ["id", "x", "y", "w", "h", "a_ids", "ag_ids", "f_id",  "f_vars_start", "f_vars_end", "f_vars_step", "f_vars_frequency", "p_ids", "p_x", "p_y", "img_in_v", "img_out_v", "img_out_stack",                                     
                                    "x_rep_start_p1", "y_rep_start_p1", "x_rep_end_p1", "y_rep_end_p1", "x_rep_step_p1","y_rep_step_p1", "x_rep_count_p1", "y_rep_count_p1", "w_rep_p1", "h_rep_p1",
                                    "x_rep_start_p2", "y_rep_start_p2", "x_rep_end_p2", "y_rep_end_p2", "x_rep_step_p2","y_rep_step_p2", "x_rep_count_p2", "y_rep_count_p2", "w_rep_p2", "h_rep_p2",
                                    "f_ids_rep", "rotations_rep"]
        
        self.area_properties_with_int_value = ["id", "x", "y", "w", "h", "f_id", "img_in_v", "img_out_v", "img_out_stack"]
        
        self.area_properties_with_non_zero_int_value = ["w", "h", "img_out_v"]
        
        self.area_properties_with_list_of_ints_value = ["a_ids", "ag_ids", "f_vars_start", "f_vars_end", "f_vars_step", "f_vars_frequency", "p_ids", "p_x", "p_y",                                     
                                    "x_rep_start_p1", "y_rep_start_p1", "x_rep_end_p1", "y_rep_end_p1", "x_rep_step_p1","y_rep_step_p1", "x_rep_count_p1", "y_rep_count_p1", "w_rep_p1", "h_rep_p1",
                                    "x_rep_start_p2", "y_rep_start_p2", "x_rep_end_p2", "y_rep_end_p2", "x_rep_step_p2","y_rep_step_p2", "x_rep_count_p2", "y_rep_count_p2", "w_rep_p2", "h_rep_p2"
                                    ]
        
        self.area_properties_with_list_of_list_of_ints_value = ["f_ids_rep", "rotations_rep"]
    
        self.id = "id"

    #the text input must contain rows of pixel area notations
    #a pixel area notation (pixel area row) looks like this:
    #{id:1; x:0; y:0; w:5; h:5; a_ids:[3,5,2]; ag_ids:[25,30]; f_id:1; p_ids:[1,2,3]; p_x:[10,20,30]; p_y:[20,30,50]; img_in_v:0; img_out_v:6; img_out_stack:2; 
    # x_rep_start_p1:[10,10,10],y_rep_start_p1:[10,10,10], x_rep_end_p1:[10,10,10], y_rep_end_p1:[10,10,10], x_rep_step_p1:[10,10,10], y_rep_step_p1:[10,10,10], x_rep_count_p1:[5,1,4], y_rep_count_p1:[3,1], w_rep_p1:[5,1,4], h_rep_p1:[3,1],
    # x_rep_start_p2:[10,10,10],y_rep_start_p1:[10,10,10], x_rep_end_p2:[10,10,10], y_rep_end_p2:[10,10,10], x_rep_step_p2:[10,10,10], y_rep_step_p2:[10,10,10], x_rep_count_p2:[5,1,4], y_rep_count_p2:[3,1], w_rep_p2:[5,1,4], h_rep_p2:[3,1],  
    # f_ids_rep:[(1,2),(3,5,6),(7,2,6,4,3)], rotations_rep:[(1,2),(3,5,6),(7,2,6,4,3)]}
    def create_pixel_areas(self, text:str) -> list[Pixel_area]:#returns a list  of objects of type `Pixel_area`

        is_format_correct = self.check_pixel_areas_str(text = text)

        if(is_format_correct == False):
            return None
        
        pixel_areas_rows = self.get_areas_rows(text=text)#this is a list of strings
        pixel_areas = []#this is a list of objects of type `Pixel_area`
        for row in pixel_areas_rows:
            pixel_area = self.create_pixel_area(text=row)
            pixel_areas.append(pixel_area)
        
        return pixel_areas


    #the text input must contain rows of pixel area notations
    #a pixel area notation (pixel area row) looks like this:
    #{id:1; x:0; y:0; w:5; h:5; a_ids:[3,5,2]; ag_ids:[25,30]; f_id:1; p_ids:[1,2,3]; p_x:[10,20,30]; p_y:[20,30,50]; img_in_v:0; img_out_v:6; img_out_stack:2; 
    # x_rep_start_p1:[10,10,10],y_rep_start_p1:[10,10,10], x_rep_end_p1:[10,10,10], y_rep_end_p1:[10,10,10], x_rep_step_p1:[10,10,10], y_rep_step_p1:[10,10,10], x_rep_count_p1:[5,1,4], y_rep_count_p1:[3,1], w_rep_p1:[5,1,4], h_rep_p1:[3,1],
    # x_rep_start_p2:[10,10,10],y_rep_start_p1:[10,10,10], x_rep_end_p2:[10,10,10], y_rep_end_p2:[10,10,10], x_rep_step_p2:[10,10,10], y_rep_step_p2:[10,10,10], x_rep_count_p2:[5,1,4], y_rep_count_p2:[3,1], w_rep_p2:[5,1,4], h_rep_p2:[3,1],  
    # f_ids_rep:[(1,2),(3,5,6),(7,2,6,4,3)], rotations_rep:[(1,2),(3,5,6),(7,2,6,4,3)]}
    def check_pixel_areas_str(self, text:str):

        pixel_areas_rows = self.get_areas_rows(text=text)
        if(pixel_areas_rows == None):
            return False
        
        row_index = 0
        for row in pixel_areas_rows:

            error_message = self.check_pixel_area_id(text=row,row_index=row_index)
            if(error_message != ""):
                print(error_message)                
                return False
            
            error_message = self.check_pixel_area_format(text=row)
            if(error_message != ""):
                pixel_area_id = self.get_pixel_area_property_value(text=row, area_property_name=self.id)
                error_message = f"error: the pixel area with id {pixel_area_id} is in wrong format; " + error_message
                print(error_message)
                return False
            
            row_index+=1
        
        return True


    #the text input must contain rows of pixel area notations
    def get_areas_rows(self, text:str):#each row contains the values of one pixel area
        start_row_symbol = "{"
        end_row_symbol = "}"

        
        start_index = 0
        index = 0
        rows = []
    
        while(True):

            row_start_index = text.find(start_row_symbol, start_index)

            if(row_start_index!=-1 and row_start_index != start_index):
                print(f"error: the area at index {index} has content between `{end_row_symbol}` and `{start_row_symbol}`")
                return None

            if(row_start_index==-1):
                break
        
            row_end_index = text.find(end_row_symbol, row_start_index+1)
            if(row_end_index==-1):
                print(f"error: the area at index {index} has no closing curly bracket")
                return None      

            row = text[row_start_index+1: row_end_index]
            rows.append(row)

            start_index = row_end_index+1       

            index+=1
        
        return rows
   
    
    #the text input must be a pixel area notation (the row content inside `{}`)
    def check_pixel_area_id(self, text:str, row_index:int) -> str:
        
        area_properties = text.split(";")
        ids_counter = 0
        error_message = ""
        
        for area_property in area_properties:
            
            if(ids_counter > 1):
                error_message = f"error: the area at row {row_index} has many ids"

            area_key_value = area_property.split(":")
            area_property_name = area_key_value[0]

            if(area_property_name == self.id):
                
                if(len(area_key_value)<2):
                    error_message = f"error: the area at row {row_index} has id with no value"
                
                if(len(area_key_value)>2):
                    error_message = f"error: the area at row {row_index} has id with many values"

                id_value = area_key_value[1]
                is_format_valid = check_for_positive_int_format(txt_value=id_value, is_zero_allowed=True)
                if(is_format_valid == False):
                    error_message = f"error: the value of the id in the area at row {row_index} is in wrong format (only numbers are allowed)"
                
                ids_counter+=1
            
            if(error_message != ""):
                break
        
        if(ids_counter < 1):
            error_message = f"error: the area at row {row_index} has no id"
        elif(ids_counter > 1):
            error_message = f"error: the area at row {row_index} has many ids"

        return error_message
    
    #the text input must be a pixel area notation (the row content inside `{}`)
    #the function get's the value of the property but it doesn't make any validation checks
    def get_pixel_area_property_value(self, text:str, area_property_name:str) -> str:

        area_properties = text.split(";")

        for area_property in area_properties:

            area_key_value = area_property.split(":")
            if(area_property_name == area_key_value[0]):
                return area_key_value[1]
        
        return ""

    #the text input must be a pixel area notation (the row content inside `{}`)
    def check_pixel_area_format(self, text:str):
        
        area_properties = text.split(";")
        area_properties_dict = {}        

        for area_property in area_properties:
            
            area_key_value = area_property.split(":")
            area_property_name = area_key_value[0]

            if(area_property_name not in self.area_properties_names):
                return f"the property `{area_property_name}` is not allowed"
            
            if(len(area_key_value) < 2):
                return f"the property `{area_property_name}` has no value"

            if(len(area_key_value) > 2):
                return f"the property `{area_property_name}` has many values"
            
            if(area_properties_dict.keys().__contains__(area_property_name)):
                return f"the property `{area_property_name}` is used many times"


            area_property_value = area_key_value[1]

            if(len(area_property_value)==0):
                return f"the property `{area_property_name}` has no value; if you don't want to use the property - delete it"

            if(area_property_name in self.area_properties_with_int_value):
                                
                if(area_property_name in self.area_properties_with_non_zero_int_value):
                    is_format_valid = check_for_positive_int_format(txt_value=area_property_value, is_zero_allowed=False)
                    if(is_format_valid == False):
                        return f"the value of the area property `{area_property_name}` is in wrong format (only numbers are allowed, the value must not be a zero)"
                else:
                    is_format_valid = check_for_positive_int_format(txt_value=area_property_value, is_zero_allowed=True)
                    if(is_format_valid == False):
                        return f"the value of the area property `{area_property_name}` is in wrong format (only numbers are allowed)"

            elif(area_property_name in self.area_properties_with_list_of_ints_value or area_property_name in self.area_properties_with_list_of_list_of_ints_value):
                
                if(area_property_value[0]!= "[" or area_property_value[-1]!="]"):
                    return f"the value of the area property `{area_property_name}` must start with `[` and end with `]`"
                elif(len(area_property_value)<3):
                    return f"the list of the area property `{area_property_name}` is empty; if you don't want to use the property - delete it"

                area_property_value = area_property_value[1:len(area_property_value)-1]
                if(area_property_name in self.area_properties_with_list_of_ints_value):
                    is_format_valid = check_numbers_from_string(txt_value=area_property_value,separator=",")
                    if(is_format_valid == False):
                        return f"the value of the area property `{area_property_name}` is in wrong format (only numbers and commas are allowed)"
                elif(area_property_name in self.area_properties_with_list_of_list_of_ints_value):
                    area_property_value = area_property_value.replace("),",");")
                    is_format_valid = check_lists_of_numbers_from_string(txt_value=area_property_value, outer_separator=";", inner_separator=",", opening_bracket_symbol="(", closing_bracket_symbol=")")
                    if(is_format_valid == False):
                        return f"the value of the area property `{area_property_name}` is in wrong format; the values inside the square brackets must be collections (each collection must start with `(` and end with `)`) of integers separated by comma"
    
        return ""
    
    #the text input must be a pixel area notation (the row content inside `{}`)
    def create_pixel_area(self, text:str):
        
        area_properties = text.split(";")        
        area_properties_dict = {property_name: None for property_name in self.area_properties_names}
         

        for area_property in area_properties:
            
            area_key_value = area_property.split(":")
            area_property_name = area_key_value[0]
            area_property_value = area_key_value[1]
            area_properties_dict[area_property_name] = area_property_value
        
        #makes the string values into ints
        id = int(area_properties_dict["id"]) if area_properties_dict["id"] is not None else 0
        x = int(area_properties_dict["x"]) if area_properties_dict["x"] is not None else 0
        y = int(area_properties_dict["y"]) if area_properties_dict["y"] is not None else 0
        w = int(area_properties_dict["w"]) if area_properties_dict["w"] is not None else 10
        h = int(area_properties_dict["h"]) if area_properties_dict["h"] is not None else 10
        f_id = int(area_properties_dict["f_id"]) if area_properties_dict["f_id"] is not None else 0

        #the default input image version is `0` which will always contain the pixel values of the original image
        img_in_v = int(area_properties_dict["img_in_v"]) if area_properties_dict["img_in_v"] is not None else 0

        #the default output image version is the input image verion; 
        #if the input image version is `0` the default output image version will be `1` (assures that image version `0` will always contain the pixel vaues of the orginal image) 
        img_out_v = int(area_properties_dict["img_out_v"]) if area_properties_dict["img_out_v"] is not None else max(1, img_in_v) 

        #the default number of stacked image versions (which will get the changes from the rgb function) is 1 (only 1 image version will get the changes from the rgb function) 
        #if the user uses the value `0` this will stack all image versions between output image version and the last image version (inclusive)
        img_out_stack = int(area_properties_dict["img_out_stack"]) if area_properties_dict["img_out_stack"] is not None else 1        
        
        #makes the string values into lists of ints
        
        a_ids = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["a_ids"])
        ag_ids = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["ag_ids"])
        f_vars_start = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["f_vars_start"])
        f_vars_end = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["f_vars_end"])
        f_vars_step = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["f_vars_step"])
        f_vars_frequency = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["f_vars_frequency"])
        p_ids = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["p_ids"])
        p_x = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["p_x"])
        p_y = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["p_y"])
        
        
        x_rep_start_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["x_rep_start_p1"], first_element=0)
        y_rep_start_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["y_rep_start_p1"], first_element=0)
        x_rep_end_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["x_rep_end_p1"], first_element=100)
        y_rep_end_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["y_rep_end_p1"], first_element=100)
        x_rep_step_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["x_rep_step_p1"], first_element=0)
        y_rep_step_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["y_rep_step_p1"], first_element=0)
        x_rep_count_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["x_rep_count_p1"], first_element=0)
        y_rep_count_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["y_rep_count_p1"], first_element=0)
        w_rep_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["w_rep_p1"], first_element=0)
        h_rep_p1 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["h_rep_p1"], first_element=0)

        x_rep_start_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["x_rep_start_p2"], first_element=0)
        y_rep_start_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["y_rep_start_p2"], first_element=0)
        x_rep_end_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["x_rep_end_p2"], first_element=100)
        y_rep_end_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["y_rep_end_p2"], first_element=100)
        x_rep_step_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["x_rep_step_p2"], first_element=0)
        y_rep_step_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["y_rep_step_p2"], first_element=0)
        x_rep_count_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["x_rep_count_p2"], first_element=0)
        y_rep_count_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["y_rep_count_p2"], first_element=0)
        w_rep_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["w_rep_p2"], first_element=0)
        h_rep_p2 = self.get__area_property_with_list_of_ints_value(str_value = area_properties_dict["h_rep_p2"], first_element=0)


        f_ids_rep = self.get__area_property_with_list_of_lists_of_ints_value(str_value = area_properties_dict["f_ids_rep"], first_element=[])
        rotations_rep = self.get__area_property_with_list_of_lists_of_ints_value(str_value = area_properties_dict["rotations_rep"], first_element=[])


        pixel_area = Pixel_area(id = id, 
        x = x, y = y, w = w, h = h,
        a_ids = a_ids, ag_ids = ag_ids, 
        f_id = f_id, f_vars_start = f_vars_start, f_vars_end = f_vars_end, f_vars_step = f_vars_step, f_vars_frequency = f_vars_frequency,
        p_ids = p_ids, p_x = p_x, p_y = p_y, 
        img_in_v = img_in_v, img_out_v = img_out_v, img_out_stack = img_out_stack,
        x_rep_start_p1=x_rep_start_p1, y_rep_start_p1=y_rep_start_p1, x_rep_end_p1=x_rep_end_p1, y_rep_end_p1=y_rep_end_p1, x_rep_step_p1=x_rep_step_p1, y_rep_step_p1=y_rep_step_p1, x_rep_count_p1=x_rep_count_p1, y_rep_count_p1=y_rep_count_p1, w_rep_p1=w_rep_p1, h_rep_p1=h_rep_p1,
        x_rep_start_p2=x_rep_start_p2, y_rep_start_p2=y_rep_start_p2, x_rep_end_p2=x_rep_end_p2, y_rep_end_p2=y_rep_end_p2, x_rep_step_p2=x_rep_step_p2, y_rep_step_p2=y_rep_step_p2, x_rep_count_p2=x_rep_count_p2, y_rep_count_p2=y_rep_count_p2, w_rep_p2=w_rep_p2, h_rep_p2=h_rep_p2,
        f_ids_rep=f_ids_rep, rotations_rep=rotations_rep)

       
        
        return pixel_area
    



    def get__area_property_with_list_of_ints_value(self, str_value:str, first_element:int=None):
        
        area_property_value = ast.literal_eval(str_value) if str_value is not None else []
        if(first_element is not None):
            area_property_value.insert(0, first_element)
        
        return area_property_value


    def get__area_property_with_list_of_lists_of_ints_value(self, str_value:str, first_element:list=None):

        main_list = []
        if str_value is not None:

            #the result is list of strings which will be something like that `["[1,2]","[]","[5,2,5,2]","[1]"]`
            collections_of_f_ids = str_value[1:-1].replace("(", "[").replace(")","]").replace("],","];").split(";")
            for collection_of_f_ids in collections_of_f_ids:
                main_list.append(ast.literal_eval(collection_of_f_ids))
        
        if(first_element is not None):
            main_list.insert(0, first_element)

        return main_list


                

            