import numpy as np

from Z_Pixel_areas_mask import Mask
from Colour_range_region import Colour_range_region
from Z_Pixel_area import Rectangle
from Order_obj import Order_obj
from Number_operatios import order_numbers

class Pixel_areas_masks_manipulator:

    def __init__(self):

        self.masks:dict[int,Mask] = {}
        self.applied_masks:dict[int,Mask] = {}

#<mask functions

    def get_min_not_used_mask_id(self) -> int:
        
        num = 1
        if(len(self.masks) == 0):            
            return num

        while(num in self.masks.keys()):
            num+=1

        return num
    
    def create_mask(self, id:int, height:int, width:int, keep_ratio:bool, remove_previous_mask_when_applying_mask:bool) -> str:

        if(id in self.masks.keys()):
            return "error: the mask was not created because the mask id is used by another mask"
        
        mask = Mask(id=id, height=height, width=width)
        mask.set_value_for__keep_ratio(new_value=keep_ratio)
        mask.set_value_for__auto_remove_previous_masks_when_applying_new_masks(new_value=remove_previous_mask_when_applying_mask)
        self.masks[id] = mask

        return ""


    def delete_mask(self, id:int) -> str:

        if(id not in self.masks.keys()):
            return "error: the mask could not be deleted because the id was not found"

        self.masks.pop(id)

        return ""


    def alter_mask(self, id:int, height:int, width:int, keep_ratio:bool, remove_previous_mask_when_applying_mask:bool) -> str:

        if(id not in self.masks.keys()):
            return "error: the mask could not be altered because the mask id was not found"
        
        mask = self.masks[id]
        mask.alter_height(new_height=height)
        mask.alter_width(new_width=width)
        mask.set_value_for__keep_ratio(new_value=keep_ratio)
        mask.set_value_for__auto_remove_previous_masks_when_applying_new_masks(new_value=remove_previous_mask_when_applying_mask)

        return ""


    def order_masks(self, order_obj: Order_obj):

        masks_ids = list(self.masks.keys())
        masks_ids.sort()

        ordered_masks_ids = order_numbers(nums=masks_ids.copy(), order_type=order_obj.order_type, start=order_obj.start, end=order_obj.end, step=order_obj.step)
        ordered_masks:dict[int,Mask] = {}

        for i in range(0, len(masks_ids)):

            mask = self.masks[ordered_masks_ids[i]]
            ordered_masks[masks_ids[i]] = mask
            mask.alter_id(new_id=masks_ids[i])

        self.masks = ordered_masks

    def order_regions(self, mask_id:int, order_obj: Order_obj) -> str:

        if(mask_id not in self.masks.keys()):
            return "error: the regions could not be ordered because the mask id was not found"

        mask = self.masks[mask_id]
        mask.order_regions(order_obj=order_obj)

        return ""

#mask functions>


#<region functions

    def get_min_not_used_region_id(self, mask_id:int) -> np.uint8|None:

        if(mask_id not in self.masks.keys()):
            print("error: the region id cannot be created because the mask id was not found")
            return None

        mask = self.masks[mask_id]
        region_id = mask.get_min_not_used_region_id()
        return region_id


    def create_colour_range_region(self, mask_id:int, colour_range_region:Colour_range_region) -> str:

        if(mask_id not in self.masks.keys()):
            return "error: the region cannot be created because the mask id was not found"
        
        mask = self.masks[mask_id]
        was_region_added =  mask.add_colour_range_region(colour_range_region=colour_range_region)

        if(was_region_added == False):
            return f"error: the region was not created because the mask with id {mask_id} already had an existing region with id {colour_range_region.id}"

        return ""


    def delete_colour_range_region(self, mask_id:int, region_id:int) -> str:

        if(mask_id not in self.masks.keys()):
            return "error: the region cannot be deleted because the mask id was not found"

        mask = self.masks[mask_id]
        was_region_removed = mask.remove_colour_range_region(region_id=region_id)

        if(was_region_removed == False):
            return f"error: the region was not deleted because the mask with id {mask_id} does not have a region with id {region_id}"

        return ""

#region functions>



#<applied masks functions

    #if `masks_ids` is `None` then all applied masks will be updated
    def update_applied_masks(self, masks_ids:list[int]|None, rectangles_with_ids:dict[int, Rectangle]|None, images_for_masks:list[np.ndarray[np.uint8]], apply_already_applied_masks:bool, update_regions_when_applying_masks:bool) -> str:

        if(len(images_for_masks) == 0):
            return "error: the masks could not be applied because the image collection for colour range masks was empty"
    
        if(masks_ids is None):
            masks_ids = list(self.masks.keys())

        error_message = ""

        #apply colour range regions to each mask
        for mask_id in masks_ids:

            if(mask_id not in self.masks.keys()):
                error_message += f"\nwarning: the mask with id {mask_id} could not be applied because the id was not found"
            elif(mask_id in self.applied_masks.keys() and apply_already_applied_masks == False):
                error_message += f"\nwarning: the mask with id {mask_id} could not be applied because it is already applied"
            else:
                mask = self.masks[mask_id]
                if(update_regions_when_applying_masks == True):
                    mask.apply_regions(rectangles_with_ids=rectangles_with_ids, images_for_creating_a_mask=images_for_masks)
                
                self.applied_masks[mask_id] = mask.copy()
    
        return error_message


    #if `masks_ids` is `None` then all applied masks will be removed
    def remove_applied_masks(self, masks_ids:list[int]|None) -> str:

        if(masks_ids is None):
            self.applied_masks = {}
            return ""

        error_message = ""

        #remove selected masks from applied masks
        for mask_id in masks_ids:
            if(mask_id not in self.applied_masks.keys()):
                error_message += f"\nwarning: the applied mask with id {mask_id} could not be removed because the id was not found"
            else:
                self.applied_masks.pop(mask_id)

        return error_message

    def get_applied_masks(self):
        return self.applied_masks
        

#applied masks functions>


    def to_string(self):

        applied_masks_sorted_ids = list(self.applied_masks.keys())
        applied_masks_sorted_ids.sort()
        txt = "applied masks ids: {" + str.join(", ", list(map(str, applied_masks_sorted_ids))) + "}\n\n"
        for mask_id in self.masks.keys():
            txt += "{ " + f"{self.masks[mask_id].to_string()}" + "\n}\n"
        return txt
