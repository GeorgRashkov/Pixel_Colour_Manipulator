import numpy as np

from Z_RGB_formula import RGB_formula
from Z2_RGB_formulas_mask import RGB_formulas_mask
from Colour import Colour, Colour_range

class Mask():

    def __init__(self, mask_id:int, pixel_area_id:int):
        
        self.id = mask_id
        self.pixel_area_id = pixel_area_id

        self.rgb_formulas_mask = RGB_formulas_mask()
        self.colours:dict[np.uint8,Colour] = {}
        self.colour_ranges:dict[np.uint8,Colour_range] = {}

        self.img_from_canvas:np.ndarray[np.uint8] = None
        self.remove_previous_mask_when_applying_mask = True
        self.keep_ratio = True

    
    def add_or_alter_colour(self, region_id:np.uint8, colour:Colour):
        self.colours[region_id] = colour
    
    def add_or_alter_colour_range(self, region_id:np.uint8, colour_range:Colour_range):
        self.colour_ranges[region_id] = colour_range

    def alter_pixel_area_id(self, new_pixel_area_id:int):
        self.pixel_area_id = new_pixel_area_id
    
    def remove_colour_or_colour_range(self, region_id:np.uint8):
        
        if(region_id in self.colours):
            del self.colours[region_id]
        elif(region_id in self.colour_ranges):
            del self.colour_ranges[region_id]
    
    def update_img_from_canvas(self, new_img_from_canvas):
        self.img_from_canvas = new_img_from_canvas
    
    def set_value_for__auto_remove_previous_masks_when_applying_new_masks(self, new_value:bool):
        self.remove_previous_mask_when_applying_mask = new_value
    
    def set_value_for__keep_ratio(self, new_value:bool):
        self.keep_ratio = new_value

    def apply_regions(self, img_for_colour_ranges:np.ndarray[np.uint8]):
        
        if(self.img_from_canvas is not None):
            self.rgb_formulas_mask.create_colour_regions(img_for_creating_a_mask=self.img_from_canvas, colours=self.colours, remove_previous_mask=self.remove_previous_mask_when_applying_mask)
            if(img_for_colour_ranges.shape[0] > 0 and img_for_colour_ranges.shape[1] > 0):
                self.rgb_formulas_mask.create_colour_range_regions(img_for_creating_a_mask=img_for_colour_ranges, colour_ranges=self.colour_ranges, remove_previous_mask=False)
        elif(img_for_colour_ranges.shape[0] > 0 and img_for_colour_ranges.shape[1] > 0):
            self.rgb_formulas_mask.create_colour_range_regions(img_for_creating_a_mask=img_for_colour_ranges, colour_ranges=self.colour_ranges, remove_previous_mask=self.remove_previous_mask_when_applying_mask)


    
    #`img` must be a "numpy.ndarray" in the shape of (Areas, Height, Width, 3) Where 3 is for the RGB color channels
    #`rgb_formulas` must be a list which contains objects of type `RGB_formula`
    #the first rgb formula will be applied to the first region, the second rgb formula will be applied to the second region and so on
    def transform_image(self, img:np.ndarray[np.uint8], rgb_formulas:list[RGB_formula], rgb_formulas_dynamic_variables:np.ndarray[np.uint8]) -> np.ndarray[np.uint8]:
        transformed_img = self.rgb_formulas_mask.transform_image(img=img, rgb_formulas=rgb_formulas, rgb_formulas_dynamic_variables=rgb_formulas_dynamic_variables, keep_ratio=self.keep_ratio)
        return transformed_img

    
    
    def copy(self):

        self_copy = Mask(mask_id=self.id,pixel_area_id=self.pixel_area_id)
        self_copy.rgb_formulas_mask = self.rgb_formulas_mask.copy()

        colours = {}
        for colour_id in self.colours.keys():
            colours[colour_id] = self.colours[colour_id].copy()
        self_copy.colours = colours

        colour_ranges = {}
        for colour_range_id in self.colour_ranges.keys():
            colour_ranges[colour_range_id] = self.colour_ranges[colour_range_id].copy()
        self_copy.colour_ranges = colour_ranges

        if(self.img_from_canvas is not None):
            self_copy.img_from_canvas = self.img_from_canvas.copy()
            
        self_copy.remove_previous_mask_when_applying_mask = self.remove_previous_mask_when_applying_mask
        self_copy.keep_ratio = self.keep_ratio

        return self_copy

    def to_string(self):
        
        txt = f"pixel area id: {self.pixel_area_id}; keep ratio: {self.keep_ratio}; remove previous mask when applying new mask: {self.remove_previous_mask_when_applying_mask}"
        regions_ids = self.rgb_formulas_mask.get_regions_ids()

        for region_id in regions_ids:
            
            helper_str = f"\n region id: {region_id}"

            if(region_id in self.colours.keys()):
                txt += f"{helper_str} -> colour: r:{self.colours[region_id].r}, g:{self.colours[region_id].g}, b:{self.colours[region_id].b}"
            elif(region_id in self.colour_ranges.keys()):
                txt += f"{helper_str} -> colour range: r:{self.colour_ranges[region_id].r_from}-{self.colour_ranges[region_id].r_to}, g:{self.colour_ranges[region_id].g_from}-{self.colour_ranges[region_id].g_to}, b:{self.colour_ranges[region_id].b_from}-{self.colour_ranges[region_id].b_to}"
            else:
                txt+= helper_str
        
        return txt