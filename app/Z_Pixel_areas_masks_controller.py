import numpy as np

from Number_format_checker import check_for_int_format, check_for_positive_int_format, check_numbers_from_string, is_number_in_range
from Colour import Colour_range
from Colour_range_region import Colour_range_region

from Z_Pixel_areas_masks_manipulator import Pixel_areas_masks_manipulator
from Z_Window_Form_pixel_areas_masks import Window_Form_pixel_areas_masks
from Z_Pixel_areas_mask import Mask

from Z_Pixel_area import Rectangle
   
class Pixel_areas_masks_controller:

    def __init__(self):

        self.uint_max_value = 255
        self.mask_max_size = 3000

        self.form_window_draw_mask = Window_Form_pixel_areas_masks()

        self.form_window_draw_mask.button_create_mask.clicked.connect(self.create_mask)
        self.form_window_draw_mask.button_delete_mask.clicked.connect(self.delete_mask)
        self.form_window_draw_mask.button_alter_mask.clicked.connect(self.alter_mask)
        
        self.form_window_draw_mask.button_create_colour_range_region.clicked.connect(self.create_colour_range_region)
        self.form_window_draw_mask.button_delete_colour_range_region.clicked.connect(self.delete_colour_range_region)

        """
        self.masks:dict[int,Mask] = {}
        self.applied_masks:dict[int,Mask] = {}
        """
        self.masks_manipulator = Pixel_areas_masks_manipulator()


#<functions for getting user input

    def get_mask_id_from_user_input(self) -> int|None:
        mask_id_txt = self.form_window_draw_mask.textBox_mask_id.text()

        if(check_for_positive_int_format(txt_value=mask_id_txt, is_zero_allowed=False) == False or mask_id_txt == ""):
            print("error: the mask id must be a positive integer above 0")
            return None
        
        mask_id = int(mask_id_txt)
        return mask_id
   
    def get_region_id_from_user_input(self) -> np.uint8|None:
        
        region_id_txt = self.form_window_draw_mask.textBox_region_id.text()

        if(check_for_positive_int_format(txt_value=region_id_txt, is_zero_allowed=False) == False or region_id_txt == ""):
            print("error: the region id must be a positive integer above 0")
            return None
        
        if(is_number_in_range(num_as_str=region_id_txt, min=1, max=self.uint_max_value) == False):
            print(f"error: the region id must be equal to or lower than {self.uint_max_value}")
            return None
    
        return np.uint8(region_id_txt)
    

    def get_mask_height_and_width(self) -> tuple[int,int]|tuple[None, None]:

        mask_height_txt = self.form_window_draw_mask.textBox_mask_height.text()
        mask_width_txt = self.form_window_draw_mask.textBox_mask_width.text()

        if(check_for_positive_int_format(txt_value=mask_height_txt) == False or mask_height_txt == "" or
            check_for_positive_int_format(txt_value=mask_width_txt) == False or mask_width_txt == ""):
            print("error: the height and width of the mask must be positive integers")
            return (None, None)
                
        if(is_number_in_range(num_as_str=mask_height_txt, min=0, max=self.mask_max_size) == False or
           is_number_in_range(num_as_str=mask_width_txt, min=0, max=self.mask_max_size) == False):
            print(f"error: the height and width of the mask must be equal to or lower than {self.mask_max_size}")
            return (None, None)

        return ( int(mask_height_txt), int(mask_width_txt) )

    
    def get_colour_range_from_user_input(self) -> Colour_range|None:

        r_from_txt, r_to_txt = self.form_window_draw_mask.textBox_r_from.text(), self.form_window_draw_mask.textBox_r_to.text()
        g_from_txt, g_to_txt = self.form_window_draw_mask.textBox_g_from.text(), self.form_window_draw_mask.textBox_g_to.text()
        b_from_txt, b_to_txt = self.form_window_draw_mask.textBox_b_from.text(), self.form_window_draw_mask.textBox_b_to.text()

        if( (r_from_txt == "" and r_to_txt == "") or (g_from_txt == "" and g_to_txt == "") or (b_from_txt == "" and b_to_txt == "")):
            print(f"error: the colour ranges for the RGB channels cannot be emtpy")
            return None
        
        r_from_txt = r_to_txt if r_from_txt=="" else r_from_txt
        r_to_txt = r_from_txt if r_to_txt=="" else r_to_txt
        g_from_txt = g_to_txt if g_from_txt=="" else g_from_txt
        g_to_txt = g_from_txt if g_to_txt=="" else g_to_txt
        b_from_txt = b_to_txt if b_from_txt=="" else b_from_txt
        b_to_txt = b_from_txt if b_to_txt=="" else b_to_txt

        if(check_for_positive_int_format(txt_value=r_from_txt) == False or check_for_positive_int_format(txt_value=r_to_txt) == False or
           check_for_positive_int_format(txt_value=g_from_txt) == False or check_for_positive_int_format(txt_value=g_to_txt) == False or
           check_for_positive_int_format(txt_value=b_from_txt) == False or check_for_positive_int_format(txt_value=b_to_txt) == False):
            print(f"error: the colour ranges for the RGB channels must be positive integers")
            return None

        if(is_number_in_range(num_as_str=r_from_txt, min=0, max=self.uint_max_value) == False or is_number_in_range(num_as_str=r_to_txt, min=0, max=self.uint_max_value) == False or
           is_number_in_range(num_as_str=g_from_txt, min=0, max=self.uint_max_value) == False or is_number_in_range(num_as_str=g_to_txt, min=0, max=self.uint_max_value) == False or
           is_number_in_range(num_as_str=b_from_txt, min=0, max=self.uint_max_value) == False or is_number_in_range(num_as_str=b_to_txt, min=0, max=self.uint_max_value) == False):
            print(f"error: the colour ranges for the RGB channels must be equal to or lower than {self.uint_max_value}")
            return None
        
        r_from, r_to = np.uint8(r_from_txt), np.uint8(r_to_txt)
        g_from, g_to = np.uint8(g_from_txt), np.uint8(g_to_txt)
        b_from, b_to = np.uint8(b_from_txt), np.uint8(b_to_txt)

        r_from, r_to = min(r_from, r_to), max(r_from, r_to)
        g_from, g_to = min(g_from, g_to), max(g_from, g_to)
        b_from, b_to = min(b_from, b_to), max(b_from, b_to)
        

        colour_range = Colour_range(r_from=r_from, r_to=r_to, g_from=g_from, g_to=g_to, b_from=b_from, b_to=b_to)
        return colour_range

    def get_image_index_from_user_input (self) -> int|None:
        image_index_txt = self.form_window_draw_mask.textBox_image_index.text()

        if(check_for_int_format(txt_value=image_index_txt) == False or image_index_txt == ""):
            print("error: the image index must be a positive integer")
            return None
        
        image_index = int(image_index_txt)
        return image_index

    def get_area_id_from_user_input (self) -> int|None:
        pixel_area_id_txt = self.form_window_draw_mask.textBox_pixel_area_id.text()

        if(check_for_positive_int_format(txt_value=pixel_area_id_txt, is_zero_allowed=True) == False or pixel_area_id_txt == ""):
            print("error: the pixel area id must be a positive integer")
            return None
        
        pixel_area_id = int(pixel_area_id_txt)
        return pixel_area_id

    def get_colour_range_region_from_user_input(self) -> Colour_range_region|None:

        region_id = self.get_region_id_from_user_input()
        image_index = self.get_image_index_from_user_input()
        area_id = self.get_area_id_from_user_input()
        colour_range = self.get_colour_range_from_user_input()
        resize_image_before_region_creation = self.form_window_draw_mask.checkBox_resize_image_before_region_creation.isChecked()

        if(region_id is None or image_index is None or area_id is None or colour_range is None):
            print("the region could not be created due to the previous error")
            return None

        colour_range_region = Colour_range_region(id=int(str(region_id)), image_index=image_index, rectangle_id=area_id, colour_range=colour_range, resize_image_before_creation=resize_image_before_region_creation)
        return colour_range_region

    """
    def get_selected_masks_ids(self, matching_masks_ids:list[int] = None) -> list[int]|None:
    
        masks_ids_str = self.form_window_draw_mask.textBox_apply_masks.text().replace(" ", "").replace("\n", "")
        is_masks_ids_str_valid = check_numbers_from_string(txt_value=masks_ids_str, separator=",", search_for_floats=False, search_for_positives_only=True)
        if(is_masks_ids_str_valid == False):
            print("error: the selected mask ids were in wrong format - make sure you use only positive integers separated by comma")
            return None
    
        masks_ids:list[int] = list(map(int, masks_ids_str.split(",")))
        if(matching_masks_ids is None):
            return masks_ids

        found_masks_ids:list[int] = []
    
        for mask_id in masks_ids:
            if(mask_id in matching_masks_ids):
                found_masks_ids.append(mask_id)
    
        return found_masks_ids
    """

    def get_selected_masks_ids(self) -> list[int]|None:
    
        masks_ids_str = self.form_window_draw_mask.textBox_apply_masks.text().replace(" ", "").replace("\n", "")
        is_masks_ids_str_valid = check_numbers_from_string(txt_value=masks_ids_str, separator=",", search_for_floats=False, search_for_positives_only=True)
        if(is_masks_ids_str_valid == False):
            print("error: the selected mask ids were in wrong format - make sure you use only positive integers separated by comma")
            return None
    
        masks_ids:list[int] = list(map(int, masks_ids_str.split(",")))
        return masks_ids

    
#functions for getting user input>



#<functions which are called when the user presses a button


    #<mask functions

    def create_mask(self):

        mask_id = self.get_mask_id_from_user_input()
        mask_height, mask_width = self.get_mask_height_and_width()
        mask_keep_ratio = self.form_window_draw_mask.checkBox_keep_ratio.isChecked()
        mask_remove_previous_mask_when_applying_mask = self.form_window_draw_mask.checkBox_auto_remove_previous_mask_when_applying_new_mask.isChecked()

        if(mask_id is None or mask_height is None or mask_width is None):
            return  

        error_message = self.masks_manipulator.create_mask(id=mask_id, height=mask_height, width=mask_width, keep_ratio=mask_keep_ratio, remove_previous_mask_when_applying_mask=mask_remove_previous_mask_when_applying_mask)
        self.print_error_message_or_display_masks(error_message=error_message)
        """

        if(mask_id in self.masks.keys()):
            print("Warning: the mask was not created because the mask id is used by another mask")
        else:
            mask = Mask(id=mask_id, height=mask_height, width=mask_width)
            mask.set_value_for__keep_ratio(self.form_window_draw_mask.checkBox_keep_ratio.isChecked())
            mask.set_value_for__auto_remove_previous_masks_when_applying_new_masks(self.form_window_draw_mask.checkBox_auto_remove_previous_mask_when_applying_new_mask.isChecked())
            self.masks[mask_id] = mask
            self.display_masks_as_text()
        """
    

    def delete_mask(self):

        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            return

        error_message = self.masks_manipulator.delete_mask(id=mask_id)
        self.print_error_message_or_display_masks(error_message=error_message)
        """
        if(mask_id not in self.masks.keys()):
            print("Error: the mask could not be deleted because the id was not found")
        else:
            self.masks.pop(mask_id)
            self.display_masks_as_text()
        """


    def alter_mask(self):

        mask_id = self.get_mask_id_from_user_input()
        mask_height, mask_width = self.get_mask_height_and_width()
        mask_keep_ratio = self.form_window_draw_mask.checkBox_keep_ratio.isChecked()
        mask_remove_previous_mask_when_applying_mask = self.form_window_draw_mask.checkBox_auto_remove_previous_mask_when_applying_new_mask.isChecked()

        if(mask_id is None or mask_height is None or mask_width is None):
            return

        error_message = self.masks_manipulator.alter_mask(id=mask_id, height=mask_height, width=mask_width, keep_ratio=mask_keep_ratio, remove_previous_mask_when_applying_mask=mask_remove_previous_mask_when_applying_mask)
        self.print_error_message_or_display_masks(error_message=error_message)
        """
        if(mask_id not in self.masks.keys()):
            print("Error: the mask could not be altered because the id was not found")
        else:
            mask = self.masks[mask_id]
            mask.alter_height(new_height=mask_height)
            mask.alter_width(new_width=mask_width)
            mask.set_value_for__keep_ratio(self.form_window_draw_mask.checkBox_keep_ratio.isChecked())
            mask.set_value_for__auto_remove_previous_masks_when_applying_new_masks(self.form_window_draw_mask.checkBox_auto_remove_previous_mask_when_applying_new_mask.isChecked())
            self.display_masks_as_text()
        """

    def order_masks(self):
        pass

    #mask functions>


    #<region functions

    def create_colour_range_region(self):
        
        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            return
        """
        elif(mask_id not in self.masks.keys()):
            print("Warning: the region cannot be created because the mask id was not found")
            return
        """

        colour_range_region = self.get_colour_range_region_from_user_input()
        if(colour_range_region is None):
            return
        
        error_message = self.masks_manipulator.create_colour_range_region(mask_id=mask_id, colour_range_region=colour_range_region)
        self.print_error_message_or_display_masks(error_message=error_message)
        """
        mask = self.masks[mask_id]
        was_region_added =  mask.add_colour_range_region(colour_range_region=colour_range_region)

        if(was_region_added == False):
            print(f"Warning: the region was not created because the mask with id {mask_id} already had an existing region with id {colour_range_region.id}")
        else:
            self.display_masks_as_text()
        """

    

    def delete_colour_range_region(self):
        
        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            return
        """
        if(mask_id not in self.masks.keys()):
            print("Warning: the region cannot be deleted because the mask id was not found")
            return
        """

        region_id = self.get_region_id_from_user_input()

        if(region_id is None):
            return

        error_message = self.masks_manipulator.delete_colour_range_region(mask_id=mask_id, region_id=region_id)
        self.print_error_message_or_display_masks(error_message=error_message)
        """
        mask = self.masks[mask_id]
        was_region_removed = mask.remove_colour_range_region(region_id=region_id)

        if(was_region_removed == False):
            print(f"Warning: the region was not deleted because the mask with id {mask_id} does not have a region with id {region_id}")
        else:
            self.display_masks_as_text()
        """

    def order_regions(self):
        pass

    #region functions>


    #<applied masks functions

    #the function: updates the masks; adds the masks to the applied masks; returns the applied masks
    def apply_masks(self, rectangles_with_ids:dict[int, Rectangle], images_for_masks:list[np.ndarray[np.uint8]], all_masks:bool) -> dict[int,Mask]|None:

        masks_ids = None 
        if(all_masks == False):
            masks_ids = self.get_selected_masks_ids()
            if(masks_ids is None):
                return None

        apply_already_applied_masks = self.form_window_draw_mask.checkBox_apply_already_applied_masks.isChecked()
        update_regions_when_applying_masks = self.form_window_draw_mask.checkBox_update_regions_when_applying_masks.isChecked()

        error_message = self.masks_manipulator.update_applied_masks(masks_ids=masks_ids, rectangles_with_ids=rectangles_with_ids, images_for_masks=images_for_masks, apply_already_applied_masks=apply_already_applied_masks, update_regions_when_applying_masks=update_regions_when_applying_masks)
        self.print_error_message_or_display_masks(error_message=error_message, always_display_masks=True)

        applied_masks = self.masks_manipulator.get_applied_masks()
        return applied_masks

    #the function: removes the selected masks from the applied masks; returns the remaining elements from the applied masks
    def remove_applied_masks(self, all_masks:bool) -> dict[int,Mask]|None:

        masks_ids = None 
        if(all_masks == False):
            masks_ids = self.get_selected_masks_ids()
            if(masks_ids is None):
                return None

        error_message = self.masks_manipulator.remove_applied_masks(masks_ids=masks_ids)
        self.print_error_message_or_display_masks(error_message=error_message, always_display_masks=True)

        remaining_applied_masks = self.masks_manipulator.get_applied_masks()
        return remaining_applied_masks

    #applied masks functions>

    """


    #<functions for applying masks
    
    #the function: updates the selected masks; adds the selected masks to the applied masks; returns the applied masks
    def apply_selected_masks(self, rectangles_with_ids:dict[int, Rectangle], images_for_masks:list[np.ndarray[np.uint8]]) -> dict[int,Mask]|None:

        masks_ids = self.get_selected_masks_ids(matching_masks_ids=list(self.masks.keys()))
        if(masks_ids is None):
            return None

        masks = self.apply_masks(masks_ids = masks_ids, rectangles_with_ids=rectangles_with_ids, images_for_masks=images_for_masks)
        return masks

    #the function: updates all masks; adds all masks to the applied masks; returns the applied masks
    def apply_all_masks(self, rectangles_with_ids:dict[int, Rectangle], images_for_masks:list[np.ndarray[np.uint8]]) -> dict[int,Mask]|None:

        masks_ids = list(self.masks.keys())
        masks = self.apply_masks(masks_ids = masks_ids, rectangles_with_ids=rectangles_with_ids, images_for_masks=images_for_masks)
        return masks

    def apply_masks(self, masks_ids:list[int], rectangles_with_ids:dict[int, Rectangle], images_for_masks:list[np.ndarray[np.uint8]]) -> dict[int,Mask]|None:

        are_masks_updated = self.update_applied_masks(masks_ids=masks_ids, rectangles_with_ids=rectangles_with_ids, images_for_masks=images_for_masks)
        if(are_masks_updated == False):
            print("warning: the masks could not be applied")
            return None
        else:
            self.display_masks_as_text()
            return self.applied_masks

    #functions for applying masks>


    #<functions for removing applied masks

    #the function: removes the selected masks from the applied masks; returns the remaining elements from the applied masks
    def remove_selected_applied_masks(self) -> dict[int,Mask]:

        masks_ids = self.get_selected_masks_ids(matching_masks_ids=list(self.applied_masks.keys()))
        if(masks_ids is None):
            return None

        #remove selected masks from applied masks
        for mask_id in masks_ids:
            self.applied_masks.pop(mask_id)

        self.display_masks_as_text()
        return self.applied_masks

    #the function: removes all masks from the applied masks
    def remove_all_applied_masks(self):
        self.applied_masks = {}
        self.display_masks_as_text()
        
    
    #functions for removing applied masks>
    """

#functions which are called when the user presses a button>



#<functions for showing info about the masks

    def print_error_message_or_display_masks(self, error_message:str, always_display_masks:bool=False):

        if(error_message != ""):
            print(error_message)

        if(error_message == "" or always_display_masks == True):
            self.display_masks_as_text()


    def display_masks_as_text(self):

        self.form_window_draw_mask.text_area.clear()
        """
        txt = self.to_string()
        """
        txt = self.masks_manipulator.to_string()
        self.form_window_draw_mask.text_area.setPlainText(txt)


    """
    def to_string(self):

        txt = "applied masks ids: {" + str.join(", ", list(map(str, self.applied_masks.keys()))) + "}\n\n"
        for mask_id in self.masks.keys():
            txt += "{ " + f"{self.masks[mask_id].to_string()}" + "\n}\n"
        return txt
    """

#functions for showing info about the masks>

    """

#<functions for updating applied masks

    def update_applied_masks(self, masks_ids:list[int], rectangles_with_ids:dict[int, Rectangle], images_for_masks:list[np.ndarray[np.uint8]]) -> bool:

        if(len(images_for_masks) == 0):
            print("error: the masks could not be applied because the image collection for colour range masks was empty")
            return False
    
        #apply colour range regions to each mask
        for mask_id in masks_ids:
    
            if(mask_id in self.applied_masks.keys() and self.form_window_draw_mask.checkBox_apply_already_applied_masks.isChecked() == False):
                print(f"warning: the mask with id {mask_id} could not be applied because it is already applied")
            else:
                mask = self.masks[mask_id]
                if(self.form_window_draw_mask.checkBox_update_regions_when_applying_masks.isChecked() == True):
                    mask.apply_regions(rectangles_with_ids=rectangles_with_ids, images_for_creating_a_mask=images_for_masks)
                
                self.applied_masks[mask_id] = mask.copy()
    
        return True
#functions for updating applied masks>

    """
