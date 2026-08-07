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

        self.form_window_draw_mask.form_elements__order_masks_and_regions.button_order_nums.clicked.connect(self.order_masks_or_regions)

        self.form_window_draw_mask.button_create_mask.clicked.connect(self.create_mask)
        self.form_window_draw_mask.button_delete_mask.clicked.connect(self.delete_mask)
        self.form_window_draw_mask.button_alter_mask.clicked.connect(self.alter_mask)
        
        self.form_window_draw_mask.button_create_colour_range_region.clicked.connect(self.create_colour_range_region)
        self.form_window_draw_mask.button_delete_colour_range_region.clicked.connect(self.delete_colour_range_region)

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
    

    def delete_mask(self):

        mask_id = self.get_mask_id_from_user_input()
        if(mask_id is None):
            return

        error_message = self.masks_manipulator.delete_mask(id=mask_id)
        self.print_error_message_or_display_masks(error_message=error_message)


    def alter_mask(self):

        mask_id = self.get_mask_id_from_user_input()
        mask_height, mask_width = self.get_mask_height_and_width()
        mask_keep_ratio = self.form_window_draw_mask.checkBox_keep_ratio.isChecked()
        mask_remove_previous_mask_when_applying_mask = self.form_window_draw_mask.checkBox_auto_remove_previous_mask_when_applying_new_mask.isChecked()

        if(mask_id is None or mask_height is None or mask_width is None):
            return

        error_message = self.masks_manipulator.alter_mask(id=mask_id, height=mask_height, width=mask_width, keep_ratio=mask_keep_ratio, remove_previous_mask_when_applying_mask=mask_remove_previous_mask_when_applying_mask)
        self.print_error_message_or_display_masks(error_message=error_message)


    #mask functions>


    #<region functions

    def create_colour_range_region(self):
        
        mask_id = self.get_mask_id_from_user_input()

        if(mask_id is None):
            return

        colour_range_region = self.get_colour_range_region_from_user_input()
        if(colour_range_region is None):
            return
        
        error_message = self.masks_manipulator.create_colour_range_region(mask_id=mask_id, colour_range_region=colour_range_region)
        self.print_error_message_or_display_masks(error_message=error_message)

    

    def delete_colour_range_region(self):
        
        mask_id = self.get_mask_id_from_user_input()
        if(mask_id is None):
            return

        region_id = self.get_region_id_from_user_input()
        if(region_id is None):
            return

        error_message = self.masks_manipulator.delete_colour_range_region(mask_id=mask_id, region_id=region_id)
        self.print_error_message_or_display_masks(error_message=error_message)


    #region functions>


    def order_masks_or_regions(self):

        order_obj = self.form_window_draw_mask.form_elements__order_masks_and_regions.get__order_obj()

        if(order_obj is not None):

            error_message = ""

            if(self.form_window_draw_mask.radioButton_order_masks.isChecked() == True):
                self.masks_manipulator.order_masks(order_obj=order_obj)

            elif(self.form_window_draw_mask.radioButton_order_regions.isChecked() == True):
                mask_id = self.get_mask_id_from_user_input()
                if(mask_id is not None):
                    error_message = self.masks_manipulator.order_regions(mask_id=mask_id, order_obj=order_obj)

            self.print_error_message_or_display_masks(error_message=error_message)


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


#functions which are called when the user presses a button>



#<functions for showing info about the masks

    def print_error_message_or_display_masks(self, error_message:str, always_display_masks:bool=False):

        if(error_message != ""):
            print(error_message)

        if(error_message == "" or always_display_masks == True):
            self.display_masks_as_text()


    def display_masks_as_text(self):

        self.form_window_draw_mask.text_area.clear()
        txt = self.masks_manipulator.to_string()
        self.form_window_draw_mask.text_area.setPlainText(txt)



#functions for showing info about the masks>
