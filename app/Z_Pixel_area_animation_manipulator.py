import numpy as np

from Z_Pixel_area import Pixel_area
from Z_Pixel_area_animations import Pixel_area_animation_group, Pixel_area_animation

class Pixel_area_animation_manipulator():

    def __init__(self, pixel_areas_animations_dict:dict[int, Pixel_area_animation], pixel_areas_animations_groups_dict:dict[int, Pixel_area_animation_group]):
        
        #this is a dictionary which has pixel area ids for keys and inner dictonary for values;
        #the inner dictionary has 2 key value pairs where the keys are "a_ids" and "ag_ids" while the 2 values are the current index of `a_ids` and `ag_ids` used by the pixel area
        self.pixel_areas_ids_with_animation_indexes:dict[int, dict[str,int]] = {}

        #contains a pixel area animation for value and its id for key; the collection can have 0 or more key-value pairs
        self.pixel_areas_animations_dict:dict[int, Pixel_area_animation] = pixel_areas_animations_dict #must be initialized in the constructor from outside
        
        #contains a pixel area animations group for value and its id for key; the collection can have 0 or more key-value pairs
        self.pixel_areas_animations_groups_dict:dict[int, Pixel_area_animation_group] = pixel_areas_animations_groups_dict #must be initialized in the constructor from outside

        #contains the id of pixel area animations group for key and for value it has another dictionary
        #the inner dictionary for keys has the ids of the animations used by the animation group and for values it has a booleans indicating whether the animation reached the end
        #the app passess from one area animation group to the other when all animations used by the animation group reach their end
        self.pixel_areas_animations_groups__end_reached_helper:dict[int, dict[int, bool]] = {}
        for animations_group_id in  self.pixel_areas_animations_groups_dict.keys():
            self.pixel_areas_animations_groups__end_reached_helper[animations_group_id] = {}

            for animation_id in self.pixel_areas_animations_groups_dict[animations_group_id].a_ids:
                self.pixel_areas_animations_groups__end_reached_helper[animations_group_id][animation_id] = False



    
    def apply_animations(self, pixel_area:Pixel_area, img:np):
        
        #make sure the pixel area is never tracked if it doesn't have any animations
        if(len(pixel_area.a_ids)==0 and len(pixel_area.ag_ids)==0):
            return
        

        #make sure the pixel area and the indexes for `a_ids` and `ag_ids` of the pixel area are tracked
        if(pixel_area.id not in self.pixel_areas_ids_with_animation_indexes.keys()):
            self.pixel_areas_ids_with_animation_indexes[pixel_area.id] = { "a_ids":0,"ag_ids":0 }
        

        
        #apply the current animation in `a_ids` used by the pixel area
        if(len(pixel_area.a_ids) > 0):
            current_animation_index = self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["a_ids"]
            current_animation_id = pixel_area.a_ids[current_animation_index]

            if(current_animation_id in self.pixel_areas_animations_dict.keys()):
                did_animation_reached_the_end = self.pixel_areas_animations_dict[current_animation_id].apply_animation(pixel_area=pixel_area, img=img)

                if(did_animation_reached_the_end == True):
                    self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["a_ids"]+=1
                    
            else:
                self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["a_ids"]+=1
            
            if(self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["a_ids"] >= len(pixel_area.a_ids)):
                self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["a_ids"] = 0
        


        

        #apply the animations in the current animation group in `ag_ids` used by the pixel area
        if(len(pixel_area.ag_ids) > 0):
            did_animations_group_reach_the_end = False
            current_animations_group_index = self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["ag_ids"]
            current_animations_group_id = pixel_area.ag_ids[current_animations_group_index]

            if(current_animations_group_id in self.pixel_areas_animations_groups_dict.keys()):
                
                animations_ids = self.pixel_areas_animations_groups_dict[current_animations_group_id].a_ids
                for animation_id in animations_ids:
                    
                    if(animation_id in self.pixel_areas_animations_dict.keys()):
                        did_animation_reached_the_end = self.pixel_areas_animations_dict[animation_id].apply_animation(pixel_area=pixel_area, img=img)
                        if(did_animation_reached_the_end == True):
                            self.pixel_areas_animations_groups__end_reached_helper[current_animations_group_id][animation_id] = True
                            did_animations_group_reach_the_end = self.did_animations_in_group_reach_their_end(animations_group_id=current_animations_group_id)
                    else:
                        self.pixel_areas_animations_groups__end_reached_helper[current_animations_group_id][animation_id] = True
            else:
                self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["ag_ids"]+=1
               
            if(did_animations_group_reach_the_end == True):
                self.reset_end_indicator_for_animations_in_group(animations_group_id = current_animations_group_id)
                self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["ag_ids"]+=1

            if(self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["ag_ids"] >= len(pixel_area.ag_ids)):
                self.pixel_areas_ids_with_animation_indexes[pixel_area.id]["ag_ids"] = 0
    


    def did_animations_in_group_reach_their_end(self, animations_group_id):
        
        for end_reached in self.pixel_areas_animations_groups__end_reached_helper[animations_group_id].values():
            if(end_reached == False):
                return False
        
        return True
    
    def reset_end_indicator_for_animations_in_group(self, animations_group_id):
        
        pixel_areas_animations_in_group__end_reached_helper = self.pixel_areas_animations_groups__end_reached_helper[animations_group_id]

        for animation_id in pixel_areas_animations_in_group__end_reached_helper.keys():
                self.pixel_areas_animations_groups__end_reached_helper[animations_group_id][animation_id] = False

        

