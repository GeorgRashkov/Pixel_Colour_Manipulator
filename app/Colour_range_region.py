import numpy as np

from Colour import Colour_range
from Z_Pixel_area import Rectangle
from Number_operatios import get_proper_positive_index


class Colour_range_region:

    """
    def __init__(self, id:int, image_index:int, rectangle_id:int, colour_range:Colour_range):
    """
    def __init__(self, id:int, image_index:int, rectangle_id:int, colour_range:Colour_range, resize_image_before_creation:bool):

        self.id = id
        self.image_index = image_index
        self.rectangle_id = rectangle_id
        self.colour_range = colour_range
        self.resize_image_before_creation = resize_image_before_creation

    def get_image_used_by_region(self, images:list[np.ndarray[np.uint8]], rectangles_with_ids:dict[int, Rectangle]) -> np.ndarray[np.uint8]:
        
        image_index = get_proper_positive_index(index=self.image_index, elements_count=len(images))
        image_for_current_region =  images[image_index]
            
        if(self.rectangle_id in rectangles_with_ids.keys()):
            rec = rectangles_with_ids[self.rectangle_id]
            image_for_current_region = image_for_current_region[rec.y:rec.y+rec.h, rec.x:rec.x+rec.w, :]

        return image_for_current_region

    def copy(self):
        """
        self_copy = Colour_range_region(id=self.id, image_index=self.image_index, rectangle_id=self.rectangle_id, colour_range=self.colour_range)
        """
        self_copy = Colour_range_region(id=self.id, image_index=self.image_index, rectangle_id=self.rectangle_id, colour_range=self.colour_range, resize_image_before_creation=self.resize_image_before_creation)
        return self_copy