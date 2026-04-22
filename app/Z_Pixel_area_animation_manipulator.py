import numpy as np

from Z_Pixel_area import Pixel_area
from Z_Pixel_area_animations import Pixel_area_animation_group, Pixel_area__move_or_resize, Pixel_area__change_used_areas, Pixel_area__change_rgbId_or_imgVersion, Pixel_area_animation

class Pixel_area_animation_manipulator():

    def __init__(self):
        
        #this is a dictionary which has pixel area ids for keys and inner dictonary for values;
        #the inner dictionary has 2 key value pairs where the keys are "a_ids" and "ag_ids" while the 2 values are the current index of `a_ids` and `ag_ids` used by the pixel area
        self.pixel_areas_ids_width_animation_indexes:dict[int, dict[str,int]] = {}

        #contains a pixel area animation for value and its id for key; the collection can have 0 or more key-value pairs
        self.pixel_areas_animations:dict[int, Pixel_area_animation] = []#must be initialized in the constructor from outside
        
        #contains a pixel area animations group for value and its id for key; the collection can have 0 or more key-value pairs
        self.pixel_areas_animations_groups:dict[int, Pixel_area_animation_group] = []#must be initialized in the constructor from outside

        #this is for testing purposes only !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pixel_areas_animations = {

            1: Pixel_area__move_or_resize(id=1, a_type="x", increment=5, frequency=5, initial_value = 20, border=95, border_exact=5_000, values=[], values_exact=[]),
            2: Pixel_area__move_or_resize(id=2, a_type="x", increment=5, frequency=5, initial_value = 20, border=110, border_exact=5_000, values=[], values_exact=[]),
            3: Pixel_area__move_or_resize(id=3, a_type="x", increment=-5, frequency=5, initial_value = 90, border=-10, border_exact=-5_000, values=[], values_exact=[]),
            
            4: Pixel_area__move_or_resize(id=4, a_type="y", increment=5, frequency=5, initial_value = 20, border=95, border_exact=5_000, values=[], values_exact=[]),
            5: Pixel_area__move_or_resize(id=5, a_type="y", increment=5, frequency=5, initial_value = 20, border=110, border_exact=5_000, values=[], values_exact=[]),
            6: Pixel_area__move_or_resize(id=6, a_type="y", increment=-5, frequency=5, initial_value = 90, border=-10, border_exact=-5_000, values=[], values_exact=[]),
            
            7: Pixel_area__move_or_resize(id=7, a_type="w", increment=2, frequency=5, initial_value = 20, border=50, border_exact=5_000, values=[], values_exact=[]),
            8: Pixel_area__move_or_resize(id=8, a_type="w", increment=-2, frequency=5, initial_value = 50, border=20, border_exact=-5_000, values=[], values_exact=[]),
            9: Pixel_area__move_or_resize(id=9, a_type="w", increment=-2, frequency=5, initial_value = 50, border=-20, border_exact=-5_000, values=[], values_exact=[]),
            
            10: Pixel_area__move_or_resize(id=10, a_type="h", increment=2, frequency=5, initial_value = 20, border=50, border_exact=5_000, values=[], values_exact=[]),
            11: Pixel_area__move_or_resize(id=11, a_type="h", increment=-2, frequency=5, initial_value = 50, border=20, border_exact=-5_000, values=[], values_exact=[]),
            12: Pixel_area__move_or_resize(id=12, a_type="h", increment=-2, frequency=5, initial_value = 50, border=-20, border_exact=-5_000, values=[], values_exact=[]),
                        
            
            
            100: Pixel_area__change_rgbId_or_imgVersion(id=100, a_type="f_id", increment=1, frequency=20, initial_value = 1, ids=[1,2,3,4,5])
        }
        self.pixel_areas_animations = pixel_areas_animations

        #this is for testing purposes only !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pixel_areas_animations_groups = {
            1: Pixel_area_animation_group(id=1, a_ids=[1,4]),
            2: Pixel_area_animation_group(id=2, a_ids=[3,6])
        }
        self.pixel_areas_animations_groups = pixel_areas_animations_groups

    
    
    def apply_animations(self, pixel_area:Pixel_area, img:np):
        
        #make sure the pixel area and the indexes for `a_ids` and `ag_ids` of the pixel area are tracked
        if(pixel_area.id not in self.pixel_areas_ids_width_animation_indexes.keys()):
            self.pixel_areas_ids_width_animation_indexes[pixel_area.id] = { "a_ids":0,"ag_ids":0 }
        

        #apply the current animation in `a_ids` used by the pixel area
        if(len(pixel_area.a_ids) > 0):
            current_animation_index = self.pixel_areas_ids_width_animation_indexes[pixel_area.id]["a_ids"]
            current_animation_id = pixel_area.a_ids[current_animation_index]

            if(current_animation_id in self.pixel_areas_animations.keys()):
                self.pixel_areas_animations[current_animation_id].apply_animation(pixel_area=pixel_area, img=img)

            self.pixel_areas_ids_width_animation_indexes[pixel_area.id]["a_ids"]+=1
            if(self.pixel_areas_ids_width_animation_indexes[pixel_area.id]["a_ids"] >= len(pixel_area.a_ids)):
                self.pixel_areas_ids_width_animation_indexes[pixel_area.id]["a_ids"] = 0
        

        #apply the animations in the current animation group in `ag_ids` used by the pixel area
        if(len(pixel_area.ag_ids) > 0):
            current_animations_group_index = self.pixel_areas_ids_width_animation_indexes[pixel_area.id]["ag_ids"]
            current_animations_group_id = pixel_area.ag_ids[current_animations_group_index]

            if(current_animations_group_id in self.pixel_areas_animations_groups.keys()):
                
                animations_ids = self.pixel_areas_animations_groups[current_animations_group_id].a_ids
                for animation_id in animations_ids:
                    if(animation_id in self.pixel_areas_animations.keys()):
                        self.pixel_areas_animations[animation_id].apply_animation(pixel_area=pixel_area, img=img)

            self.pixel_areas_ids_width_animation_indexes[pixel_area.id]["ag_ids"]+=1
            if(self.pixel_areas_ids_width_animation_indexes[pixel_area.id]["ag_ids"] >= len(pixel_area.ag_ids)):
                self.pixel_areas_ids_width_animation_indexes[pixel_area.id]["ag_ids"] = 0
        


        

