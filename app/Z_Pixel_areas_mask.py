import numpy as np

from Z_RGB_formula import RGB_formula
from Z_Pixel_areas_RGB_formulas_mask import RGB_formulas_mask
from Colour_range_region import Colour_range_region

from Z_Pixel_area import Rectangle

from Order_obj import Order_obj
from Number_operatios import order_numbers

class Mask():
    
    def __init__(self, id:int, height:int, width:int):
        
        self.id = id
        self.height = height
        self.width = width

        self.rgb_formulas_mask = RGB_formulas_mask()
        
        #the keys are the ids of the regions while the values are objects of type `Colour_range_region`
        self.colour_range_regions:dict[np.uint8, Colour_range_region] = {}

        self.remove_previous_mask_when_applying_mask = True
        self.keep_ratio = True

    def get_min_not_used_region_id(self) -> np.uint8|None:
        region_id = self.rgb_formulas_mask.get_min_not_used_region_id()
        return region_id

    def alter_id(self, new_id:int):
        self.id = new_id

    def alter_height(self, new_height:int):
        self.height = new_height

    def alter_width(self, new_width:int):
        self.width = new_width
    
    def add_colour_range_region(self, colour_range_region:Colour_range_region) -> bool:

        region_id = colour_range_region.id
        if(region_id in self.colour_range_regions.keys()):
            return False
        
        self.colour_range_regions[region_id] = colour_range_region
        self.rgb_formulas_mask.add_region(region_id=region_id)
        return True

    def remove_colour_range_region(self, region_id:np.uint8):

        if(region_id not in self.colour_range_regions.keys()):
            return False

        self.colour_range_regions.pop(region_id)
        self.rgb_formulas_mask.remove_region(region_id=region_id)
        return True
    
    
    def set_value_for__auto_remove_previous_masks_when_applying_new_masks(self, new_value:bool):
        self.remove_previous_mask_when_applying_mask = new_value
    
    def set_value_for__keep_ratio(self, new_value:bool):
        self.keep_ratio = new_value

    def order_regions(self, order_obj: Order_obj):

        colour_range_regions_ids:list[int] = []
        for colour_range_region_id in self.colour_range_regions.keys():
            colour_range_regions_ids.append(int(colour_range_region_id))
        colour_range_regions_ids.sort()

        ordered_colour_range_regions_ids = order_numbers(nums=colour_range_regions_ids.copy(), order_type=order_obj.order_type, start=order_obj.start, end=order_obj.end, step=order_obj.step)
        ordered_colour_range_regions:dict[np.uint8, Colour_range_region] = {}

        for i in range(0, len(colour_range_regions_ids)):

            colour_range_region = self.colour_range_regions[np.uint8(ordered_colour_range_regions_ids[i])]
            ordered_colour_range_regions[np.uint8(colour_range_regions_ids[i])] = colour_range_region
            colour_range_region.alter_id(new_id=colour_range_regions_ids[i])

        self.colour_range_regions = ordered_colour_range_regions

    def apply_regions(self, rectangles_with_ids:dict[int, Rectangle]|None, images_for_creating_a_mask:list[np.ndarray[np.uint8]]):

        if(len(images_for_creating_a_mask) > 0):
            mask_height = self.height if self.height>0 else images_for_creating_a_mask[-1].shape[0]
            mask_width = self.width if self.width>0 else images_for_creating_a_mask[-1].shape[1]
            self.rgb_formulas_mask.create_colour_range_regions(mask_height=mask_height, mask_width=mask_width, images_for_creating_a_mask=images_for_creating_a_mask, rectangles_with_ids=rectangles_with_ids, colour_range_regions=self.colour_range_regions, remove_previous_mask=self.remove_previous_mask_when_applying_mask)

    
    #`img` must be a "numpy.ndarray" in the shape of (Areas, Height, Width, 3) or (Height, Width, 3) Where 3 is for the RGB color channels
    #`rgb_formulas` must be a list which contains objects of type `RGB_formula`
    #the first rgb formula will be applied to the first region, the second rgb formula will be applied to the second region and so on
    def transform_image(self, img:np.ndarray[np.uint8], rgb_formulas:list[RGB_formula], rgb_formulas_dynamic_variables:np.ndarray[np.uint8]) -> np.ndarray[np.uint8]:
        transformed_img = self.rgb_formulas_mask.transform_image(img=img, rgb_formulas=rgb_formulas, rgb_formulas_dynamic_variables=rgb_formulas_dynamic_variables, keep_ratio=self.keep_ratio)
        return transformed_img
    

    #`img` must be a "numpy.ndarray" in the shape of (Areas, Height, Width, 3) Where 3 is for the RGB color channels
    #`region_images` must be a list which contains elements of type "numpy.ndarray" in the shape of (Height, Width, 3) Where 3 is for the RGB color channels
    #the first region image will be applied to the first region, the second region image will be applied to the second region and so on
    def transform_image_using_other_images(self, img:np.ndarray[np.uint8], region_images:list[np.ndarray[np.uint8]]) -> np.ndarray[np.uint8]:
        transformed_img = self.rgb_formulas_mask.transform_image_using_other_images(img=img, region_images=region_images, keep_ratio=self.keep_ratio)
        return transformed_img

    
    
    def copy(self):
        
        self_copy = Mask(id=self.id, height=self.height, width=self.width)
        self_copy.rgb_formulas_mask = self.rgb_formulas_mask.copy()

        colour_ranges: dict[np.uint8, Colour_range_region] = {}
        for region_id in self.colour_range_regions.keys():
            region = self.colour_range_regions[region_id]
            colour_ranges[region_id] = region.copy()
        self_copy.colour_range_regions = colour_ranges

            
        self_copy.remove_previous_mask_when_applying_mask = self.remove_previous_mask_when_applying_mask
        self_copy.keep_ratio = self.keep_ratio

        return self_copy

    def to_string(self):
        
        txt = f"mask -> id: {self.id}; height: {self.height};  width: {self.width}; keep ratio: {self.keep_ratio}; remove previous mask when applying new mask: {self.remove_previous_mask_when_applying_mask};;"
        regions_ids = self.rgb_formulas_mask.get_regions_ids()

        for region_id in regions_ids:
            
            helper_str = f"\n region id: {region_id}"

            if(region_id in self.colour_range_regions.keys()):
                region  = self.colour_range_regions[region_id]
                r_range = f"{region.colour_range.r_from}-{region.colour_range.r_to}" if region.colour_range.r_from != region.colour_range.r_to else f"{region.colour_range.r_from}"
                g_range = f"{region.colour_range.g_from}-{region.colour_range.g_to}" if region.colour_range.g_from != region.colour_range.g_to else f"{region.colour_range.g_from}"
                b_range = f"{region.colour_range.b_from}-{region.colour_range.b_to}" if region.colour_range.b_from != region.colour_range.b_to else f"{region.colour_range.b_from}"
                
                txt += f"{helper_str} -> colour range: [r:{r_range}, g:{g_range}, b:{b_range}]; image index:{region.image_index}; area id:{region.rectangle_id}; resize before creation:{region.resize_image_before_creation}"
            else:
                txt+= helper_str
        
        return txt