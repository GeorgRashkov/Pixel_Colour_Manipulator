import numpy as np

from Z_Pixel_area import Pixel_area

class Pixel_area_animation_group():
    
    def __init__(self, id:int, a_ids:list[int]):
        self.id = id
        self.a_ids = a_ids


# the class must not be intantiated; use its children for creating objects
class Pixel_area_animation():
    
    def __init__(self, id:int, a_type:str, step:int, step_img_s:int, step_img_w:int, step_img_h:int, frequency:int):
        
        valid_animation_types = ["x", "y", "w", "h", "a_ids", "ag_ids", "f_id",  "f_vars_start", "f_vars_end", "f_vars_step", "f_vars_frequency", "p_ids", "p_x", "p_y", "img_in_v", "img_out_v", "img_out_stack", "x_rep_start", "y_rep_start", "x_rep_end", "y_rep_end", "x_rep_step", "y_rep_step", "x_rep_count", "y_rep_count"]
        
        if(a_type not in valid_animation_types):
            raise Exception("invalid animation type")

        self.id = id #the id of the animation
        self.a_type = a_type #the animation type
        self.step = step #the size of the change (the step can be positive or negative, however if it value is zero there will be no animation)
        self.step_img_s = step_img_s #the size of the change represented as percentage relative to the image size(width or height); the step can be positive or negative, however if it value is zero there will be no animation
        self.step_img_w = step_img_w #the size of the change represented as percentage relative to the image width; the step can be positive or negative, however if it value is zero there will be no animation
        self.step_img_h = step_img_h #the size of the change represented as percentage relative to the image height; the step can be positive or negative, however if it value is zero there will be no animation
        self.frequency = frequency #the number of grabs before applying the animation
        self.calls = 1
    
    #this function must remain emtpy
    #the return value will indicate if the animation reached the end (occurs when crossing the border)
    def apply_animation(self, pixel_area:Pixel_area, img:np) -> bool:
        return False
    
    def get_animation_step(self, img:np) -> int:
        
        img_width = img.shape[1]
        img_height = img.shape[0]

        step = self.step

        if(self.step_img_w != 0):
            step += img_width/100 * self.step_img_w
        if(self.step_img_h != 0):
            step += img_height/100 * self.step_img_h

        if(self.step_img_s!=0):
            
            if(self.a_type == "x" or self.a_type=="w"):
                step += img_width/100 * self.step_img_s
            elif(self.a_type == "y" or self.a_type=="h"):
                step += img_height/100 * self.step_img_s
            else:
                step += min(img_width, img_height)/100 * self.step_img_s
        
        return int(step)


class Pixel_area_animation_xywh(Pixel_area_animation):

    def __init__(self, id:int, a_type:str, step:int, step_img_s:int, step_img_w:int, step_img_h:int, frequency:int, initial_value:int, border:int, border_exact:int, values:list[int], values_exact:list[int]):

        Pixel_area_animation.__init__(self, id=id, a_type=a_type, step=step, step_img_s=step_img_s, step_img_w=step_img_w, step_img_h=step_img_h, frequency=frequency)
        self.initial_value = initial_value
        self.border = border #set's a padding (in percentage with respect to the image size) between the area and the image; when the border is crossed then the next time the animation is apllied one of those [x,y,w,h] will be set to the initial value 
        self.border_exact = border_exact #for moving animation - set's a padding (in pixels) between the area and the image; for resizing animation - set's the minimum or maximum size which the area can have; when the border is crossed then the next time the animation is apllied one of those [x,y,w,h] will be set to the initial value  

        self.values = values #the location animation can be presented as percentage values based on the image size (if so the border parameters will be ignored)
        self.values_exact = values_exact #the location animation can be presented as exact pixel values (if so the border parameters will be ignored)
        self.current_index_for__values = 0
    
    #the return value will indicate if the animation reached the end (occurs when crossing the border)
    def apply_animation(self, pixel_area:Pixel_area, img:np) -> bool:
        
        step = self.get_animation_step(img=img)

        # the animation will never be applied 
        if(step == 0):
            return True

        if(self.calls < self.frequency):
            self.calls+=1
            return False
        
        img_width = img.shape[1]
        img_height = img.shape[0]

        did_animation_reached_the_end = False

        if(len(self.values) > 0):

            if(self.current_index_for__values + step >= len(self.values)-1):
                did_animation_reached_the_end = True

            self.current_index_for__values = (self.current_index_for__values + step) % len(self.values)

            if(self.a_type == "x"):            
                pixel_area.x = int(img_width/100 * self.values[self.current_index_for__values])
            
            elif(self.a_type == "y"):            
                pixel_area.y = int(img_height/100 * self.values[self.current_index_for__values])
            
            elif(self.a_type == "w"):            
                pixel_area.w = int(img_width/100 * self.values[self.current_index_for__values])
            
            elif(self.a_type == "h"):            
                pixel_area.h = int(img_height/100 * self.values[self.current_index_for__values])
        
        elif(len(self.values_exact) > 0):

            if(self.current_index_for__values + step >= len(self.values_exact)-1):
                did_animation_reached_the_end = True

            self.current_index_for__values = (self.current_index_for__values + step) % len(self.values_exact)

            if(self.a_type == "x"):            
                pixel_area.x = self.values_exact[self.current_index_for__values]
            
            elif(self.a_type == "y"):            
                pixel_area.y = self.values_exact[self.current_index_for__values]
            
            elif(self.a_type == "w"):            
                pixel_area.w = self.values_exact[self.current_index_for__values]
            
            elif(self.a_type == "h"):            
                pixel_area.h = self.values_exact[self.current_index_for__values]

        else:
            if(self.a_type == "x"):            
                did_animation_reached_the_end = self.change_x(pixel_area=pixel_area, img=img, step=step)
            
            elif(self.a_type == "y"):            
                did_animation_reached_the_end = self.change_y(pixel_area=pixel_area, img=img, step=step)
            
            elif(self.a_type == "w"):            
                did_animation_reached_the_end = self.change_width(pixel_area=pixel_area, img=img, step=step)
            
            elif(self.a_type == "h"):            
                did_animation_reached_the_end = self.change_height(pixel_area=pixel_area, img=img, step=step)       

        self.calls = 1

        return did_animation_reached_the_end
    


    #the return value will indicate if the animation reached the end (occurs when crossing the border)
    def change_x(self, pixel_area:Pixel_area, img:np, step:int) -> bool:
        
        did_animation_reached_the_end = False

        img_width = img.shape[1]
        
        #move the area to the left side of the image
        if(step < 0):
            
            img_left_border = int(max(img_width/100*self.border, self.border_exact, 0))

            #this occurs when the area is already at (or outside) the left border of the image
            if(pixel_area.x <= img_left_border):
                if(self.initial_value >= 0):
                    pixel_area.x = self.initial_value
                did_animation_reached_the_end = True

            else:
                new_x_value = pixel_area.x + step
                
                #make sure the animation will not make the area to appear outside the left border of the image
                if(new_x_value <= img_left_border):
                    new_x_value = img_left_border
                    did_animation_reached_the_end = True
                
                pixel_area.x = new_x_value
        
        #move the area to the right side of the image
        elif(step > 0):

            area_right_corner_location = pixel_area.x + pixel_area.w

            img_right_border = int(min(img_width/100*self.border, self.border_exact))
                        
            #this occurs when the area is already at (or outside) the right border of the image
            if(area_right_corner_location >= img_right_border):
                if(self.initial_value >= 0):
                    pixel_area.x = self.initial_value
                did_animation_reached_the_end = True
            
            else:
                new_x_value = pixel_area.x + step
                
                #make sure the animation will not make the area to appear outside the right border of the image                    
                if(new_x_value + pixel_area.w >= img_right_border):
                    new_x_value = img_right_border - pixel_area.w
                    did_animation_reached_the_end = True
                
                pixel_area.x = new_x_value
        
        pixel_area.x = int(pixel_area.x)
        return did_animation_reached_the_end


    #the return value will indicate if the animation reached the end (occurs when crossing the border)
    def change_y(self, pixel_area:Pixel_area, img:np, step:int) -> bool:
        
        did_animation_reached_the_end = False

        img_height = img.shape[0]
        
        #move the area to the top side of the image
        if(step < 0):
            
            img_top_border = int(max(img_height/100*self.border, self.border_exact, 0))

            #this occurs when the area is already at (or outside) the top border of the image
            if(pixel_area.y <= img_top_border):
                if(self.initial_value >= 0):
                    pixel_area.y = self.initial_value
                did_animation_reached_the_end = True
            
            else:
                new_y_value = pixel_area.y + step
                
                #make sure the animation will not make the area to appear outside the top border of the image
                if(new_y_value <= img_top_border):
                    new_y_value = img_top_border
                    did_animation_reached_the_end = True
                
                pixel_area.y = new_y_value
        
        #move the area to the down side of the image
        elif(step > 0):

            area_bottom_corner_location = pixel_area.y + pixel_area.h
                        
            img_bottom_border = int(min(img_height/100*self.border, self.border_exact))

            #this occurs when the area is already at (or outside) the bottom border of the image
            if(area_bottom_corner_location >= img_bottom_border):
                if(self.initial_value >= 0):
                    pixel_area.y = self.initial_value
                did_animation_reached_the_end = True
            
            else:
                new_y_value = pixel_area.y + step
                
                #make sure the animation will not make the area to appear under the bottom border of the image                   
                if(new_y_value + pixel_area.h >= img_bottom_border):
                    new_y_value = img_bottom_border - pixel_area.h
                    did_animation_reached_the_end = True
                
                pixel_area.y = new_y_value
        
        pixel_area.y = int(pixel_area.y)
        return did_animation_reached_the_end
    

    #the return value will indicate if the animation reached the end (occurs when crossing the border)
    def change_width(self, pixel_area:Pixel_area, img:np, step:int) -> bool:

        did_animation_reached_the_end = False

        img_width = img.shape[1]

        #decrease the area width
        if(step < 0):
            
            area_min_width_border = int(max(img_width/100*self.border, self.border_exact, 1))

            #this occurs when the area width is already equal to (or smaller than) the minimum width it can have
            if(pixel_area.w <= area_min_width_border):
                if(self.initial_value > 0):
                    pixel_area.w = self.initial_value
                did_animation_reached_the_end = True
            
            else:
                if(pixel_area.w + step <= area_min_width_border):
                    did_animation_reached_the_end = True 

                #make sure the animation will not make the area width smaller than the minimum width it can have; also make sure the area width is positive
                pixel_area.w = max(pixel_area.w + step, area_min_width_border, 1)

                                        
        #increase the area width
        elif(step > 0):
            
            area_max_width_border = int(min(img_width/100*self.border, self.border_exact))
            
            #this occurs when the area width is already equal to (or bigger than) the maximum width it can have
            if(pixel_area.w >= area_max_width_border):
                if(self.initial_value > 0):
                    pixel_area.w = self.initial_value
                did_animation_reached_the_end = True
            
            else:
                if(pixel_area.w + step >= area_max_width_border):
                    did_animation_reached_the_end = True 

                #make sure the animation will not make the area width bigger than the maximum width it can have; also make sure the area width is positive              
                pixel_area.w = max(min(pixel_area.w + step, area_max_width_border), 1)

        pixel_area.w = int(pixel_area.w)
        return did_animation_reached_the_end
    

    #the return value will indicate if the animation reached the end (occurs when crossing the border)
    def change_height(self, pixel_area:Pixel_area, img:np, step:int) -> bool:

        did_animation_reached_the_end = False

        img_height = img.shape[1]

        #decrease the area height
        if(step < 0):
            
            area_min_height_border = int(max(img_height/100*self.border, self.border_exact, 1))

            #this occurs when the area height is already equal to (or smaller than) the minimum height it can have
            if(pixel_area.h <= area_min_height_border):
                if(self.initial_value > 0):
                    pixel_area.h = self.initial_value
                did_animation_reached_the_end = True
            
            else:
                if(pixel_area.h + step <= area_min_height_border):
                    did_animation_reached_the_end = True 

                #make sure the animation will not make the area height smaller than the minimum height it can have; also make sure the area height is positive
                pixel_area.h = max(pixel_area.h + step, area_min_height_border, 1)

                                        
        #increase the area height
        elif(step > 0):
            
            area_max_height_border = int(min(img_height/100*self.border, self.border_exact))
            
            #this occurs when the area height is already equal to (or bigger than) the maximum height it can have
            if(pixel_area.h >= area_max_height_border):
                if(self.initial_value > 0):
                    pixel_area.h = self.initial_value
                did_animation_reached_the_end = True
            
            else:
                if(pixel_area.h + step >= area_max_height_border):
                    did_animation_reached_the_end = True

                #make sure the animation will not make the area height bigger than the maximum height it can have; also make sure the area height is positive              
                pixel_area.h = max(min(pixel_area.h + step, area_max_height_border), 1)
        
        pixel_area.h = int(pixel_area.h)
        return did_animation_reached_the_end
        
        


class Pixel_area_animation_for_list_of_ints(Pixel_area_animation):

    def __init__(self, id:int, a_type:str, step:int, step_img_s:int, step_img_w:int, step_img_h:int, frequency:int, values:list[int]):

        Pixel_area_animation.__init__(self, id=id, a_type=a_type, step=step, step_img_s=step_img_s, step_img_w=step_img_w, step_img_h=step_img_h,  frequency=frequency)
        self.values = values

        self.current_index_for__values = 0
    
    #the return value will indicate if the animation reached the end (occurs when crossing the border)
    def apply_animation(self, pixel_area:Pixel_area, img:np) -> bool:
        
        step = self.get_animation_step(img=img)

        if(len(self.values) == 0 or step == 0):
            return True

        if(self.calls < self.frequency):
            self.calls+=1
            return False
        
        did_animation_reached_the_end = False
        if(self.current_index_for__values + step >= len(self.values)-1):
                did_animation_reached_the_end = True

        self.current_index_for__values = (self.current_index_for__values + step) % len(self.values)

        if(self.a_type == "f_id"):            
           pixel_area.f_id = self.values[self.current_index_for__values]
        
        elif(self.a_type == "img_in_v"):            
           pixel_area.img_in_v = self.values[self.current_index_for__values]
        
        elif(self.a_type == "img_out_v"):            
           pixel_area.img_out_v = max(self.values[self.current_index_for__values], 1)#make sure the first image version will never be modified
        
        elif(self.a_type == "img_out_stack"):            
            pixel_area.img_out_stack = self.values[self.current_index_for__values]     

        self.calls = 1

        return did_animation_reached_the_end
    


class Pixel_area_animation_for_list_of_lists_of_ints(Pixel_area_animation):

    def __init__(self, id:int, a_type:str, step:int, step_img_s:int, step_img_w:int, step_img_h:int, frequency:int, values:list[list[int]]):

        Pixel_area_animation.__init__(self, id=id, a_type=a_type, step=step, step_img_s=step_img_s, step_img_w=step_img_w, step_img_h=step_img_h, frequency=frequency)
        self.values = values
       
        self.current_index_for__values = 0
    
    #the return value will indicate if the animation reached the end (occurs when crossing the border)
    def apply_animation(self, pixel_area:Pixel_area, img:np) -> bool:
        
        step = self.get_animation_step(img=img)

        if(len(self.values) == 0 or step==0):
            return True

        if(self.calls < self.frequency):
            self.calls+=1
            return False
        
        did_animation_reached_the_end = False
        if(self.current_index_for__values + step >= len(self.values)-1):
                did_animation_reached_the_end = True

        self.current_index_for__values = (self.current_index_for__values + step) % len(self.values)

        if(self.a_type == "a_ids"): 
            pixel_area.a_ids = self.values[self.current_index_for__values]

        elif(self.a_type == "ag_ids"): 
            pixel_area.ag_ids = self.values[self.current_index_for__values]

        elif(self.a_type == "f_vars_start"): 
            pixel_area.f_vars_start = self.values[self.current_index_for__values]
            pixel_area.make_f_vars_parameters_consistent()
                    
        elif(self.a_type == "f_vars_end"): 
            pixel_area.f_vars_end = self.values[self.current_index_for__values]
            pixel_area.make_f_vars_parameters_consistent()
                    
        elif(self.a_type == "f_vars_step"): 
            pixel_area.f_vars_step = self.values[self.current_index_for__values]
            pixel_area.make_f_vars_parameters_consistent()
                    
        elif(self.a_type == "f_vars_frequency"): 
            pixel_area.f_vars_frequency = self.values[self.current_index_for__values]
            pixel_area.make_f_vars_parameters_consistent()
            
        elif(self.a_type == "p_ids"): 
            pixel_area.p_ids = self.values[self.current_index_for__values]

        elif(self.a_type == "p_x"): 
            pixel_area.p_x = self.values[self.current_index_for__values]

        elif(self.a_type == "p_y"): 
            pixel_area.p_y = self.values[self.current_index_for__values]

        elif(self.a_type == "x_rep_start"): 
            pixel_area.x_rep_start = self.values[self.current_index_for__values]

        elif(self.a_type == "y_rep_start"): 
            pixel_area.y_rep_start = self.values[self.current_index_for__values]

        elif(self.a_type == "x_rep_end"): 
            pixel_area.x_rep_end = self.values[self.current_index_for__values]

        elif(self.a_type == "y_rep_end"): 
            pixel_area.y_rep_end = self.values[self.current_index_for__values]

        elif(self.a_type == "x_rep_step"):            
           pixel_area.x_rep_step = self.values[self.current_index_for__values]
        
        elif(self.a_type == "y_rep_step"):            
           pixel_area.y_rep_step = self.values[self.current_index_for__values]
        
        elif(self.a_type == "x_rep_count"):            
            pixel_area.x_rep_count = self.values[self.current_index_for__values] 

        elif(self.a_type == "y_rep_count"):            
            pixel_area.y_rep_count = self.values[self.current_index_for__values]      

        self.calls = 1

        return did_animation_reached_the_end