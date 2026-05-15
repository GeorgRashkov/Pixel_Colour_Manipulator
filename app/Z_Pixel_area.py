import numpy as np

class Pixel_area:
    
    # all input parameters must be integers or lists of integers
    def __init__(self, id:int, x:int, y:int, w:int, h:int, a_ids:list, ag_ids:list, 
                 f_id:int, f_vars_start:list, f_vars_end:list, f_vars_step:list, f_vars_frequency:list,
                 p_ids:list, p_x:list, p_y:list, img_in_v:int, img_out_v:int, img_out_stack:int,
                 x_rep_start:list, y_rep_start:list, x_rep_end:list, y_rep_end:list, x_rep_step:list,y_rep_step:list, x_rep_count:list, y_rep_count:list, f_ids_rep:list, rotations_rep:list):
        
        #area id
        self.id = id

        #area location and size
        self.x = x #top left corner horizontal position
        self.y = y #top left corner vertical position
        self.w = w #area width
        self.h = h #area height

        #animations
        self.a_ids = a_ids #list of animation ids
        self.ag_ids = ag_ids #list of the ids of groups of animations (a group of animations is an object which contains the ids of 1 or more animations)
               
        #rgb function
        self.f_id = f_id #the id of the RGB formula
        self.f_vars_max_value = 255
        self.current_f_vars = []
        self.current_f_vars_frequency = []
        self.f_vars_start = f_vars_start #the initial values of the input variables
        self.f_vars_end=f_vars_end #the ending values of the input variables
        self.f_vars_step=f_vars_step #the steps which will change the current values of the input variables (the changes will be applied the next time the rgb function is called)
        self.f_vars_frequency = f_vars_frequency
        self.make_f_vars_parameters_consistent()
               

        #pixel areas which will be used as an input for the rgb function
        self.p_ids = p_ids #contains the pixel area ids which will passed to the RGB formula
        self.p_x = p_x #this is a list which contains the horizontal position of the top left corner of not defined pixel areas which will passed to the RGB formula
        self.p_y = p_y #this is a list which contains the vertical position of the top left corner of not defined pixel areas which will passed to the RGB formula
        
        #image versions which will be used as an input and ouput of the rgb function; maximum of 10 image versions
        self.img_in_v = img_in_v #determines the version of the input image which will be passed to the RGB formula
        self.img_out_v = img_out_v #determines the version of the image to which the changed pixel values will be applied
        self.img_out_stack = img_out_stack #determines the count of image versions to which the changed pixel values will be applied; the first version is `img_out_v`, the next version is `img_out_v + 1` and so on 

        
        #<repeat areas arguments
        used_areas_count = len(self.p_ids) + min(len(self.p_x), len(self.p_y))

        #determines the place in % in the main area from where the inner areas will start being applied
        self.x_rep_start = [0]#the first value in the list corresponds to the main area
        self.y_rep_start = [0]#the first value in the list corresponds to the main area
        
        #determines the place in % in the main area from where the inner areas will end being applied
        self.x_rep_end = [100]#the first value in the list corresponds to the main area
        self.y_rep_end = [100]#the first value in the list corresponds to the main area

        #determines the amount of space in % in the main area which will be skipped when creating duplicates of the used areas
        self.x_rep_step = [0]#the first value in the list corresponds to the main area
        self.y_rep_step = [0]#the first value in the list corresponds to the main area

        #determines the max number of columns and rows of the created duplicates
        self.x_rep_count = [1]
        self.y_rep_count = [1]
                
        #determines the rgb formulas which will be applied to the duplicates; the values are collections where each collection is for specific used area while each inner element is rgb formula id which will be applied to a duplicate/s of the used area
        # Each used area can have a different collection of RGB formulas ids - the first RGB formula is applied for the first copy, the second RGB formula is applied for the second copy, etc. 
        # When the last RGB formula is applied for the current copy (of the current applied area), the next copy (of the current applied area) will use the first RGB formula, then the next copy (of the current applied area) will use the second RGB formula, etc.
        self.f_ids_rep = [[]]#the first value in the list corresponds to the main area
        """
        example:
        `
        self.f_ids_rep = [[],
                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 25, 16, 13, 19, 35, 17, 14, 18, 29, 23, 11], 
                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 25, 16, 13, 19, 35, 17, 14, 18, 29, 23, 11],
                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 25, 16, 13, 19, 35, 17, 14, 18, 29, 23, 11],
                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 25, 16, 13, 19, 35, 17, 14, 18, 29, 23, 11],
                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 25, 16, 13, 19, 35, 17, 14, 18, 29, 23, 11]]
        `
        """

        self.rotations_rep = [[]]

        for i in range(0, used_areas_count):
            
            self.x_rep_start.append(0 if i >= len(x_rep_start) else x_rep_start[i])
            self.y_rep_start.append(0 if i >= len(y_rep_start) else y_rep_start[i])

            self.x_rep_end.append(100 if i >= len(x_rep_end) else x_rep_end[i])
            self.y_rep_end.append(100 if i >= len(y_rep_end) else y_rep_end[i])

            self.x_rep_step.append(0 if i >= len(x_rep_step) else x_rep_step[i])
            self.y_rep_step.append(0 if i >= len(y_rep_step) else y_rep_step[i])

            self.x_rep_count.append(1 if i >= len(x_rep_count) else x_rep_count[i])
            self.y_rep_count.append(1 if i >= len(y_rep_count) else y_rep_count[i])

            self.f_ids_rep.append([] if i >= len(f_ids_rep) else f_ids_rep[i])
            self.rotations_rep.append([] if i >= len(rotations_rep) else rotations_rep[i])
        #repeat areas arguments>
    

    def update_dynamic_variables_for_rgb_function(self):
        
        for i in range(0, len(self.current_f_vars)):
            
            #make sure the current f_var value is changed only when the current f_var frequence is equal to or below 1
            if(self.current_f_vars_frequency[i] > 1):
                self.current_f_vars_frequency[i] -= 1
                continue
            self.current_f_vars_frequency[i] = self.f_vars_frequency[i]
            
            #get the difference between the start and the end of the current f_var
            f_var_range = self.f_vars_end[i] - self.f_vars_start[i] + 1 if(self.f_vars_end[i] >= self.f_vars_start[i]) else self.f_vars_start[i] - self.f_vars_end[i] + 1

            if(self.f_vars_end[i] >= self.f_vars_start[i]):
                
                new_value = (self.current_f_vars[i] - self.f_vars_start[i] + self.f_vars_step[i]) % f_var_range
                self.current_f_vars[i] = self.f_vars_start[i] + new_value
                
            
            else:
                
                new_value = (self.f_vars_start[i] - self.current_f_vars[i] + self.f_vars_step[i]) % f_var_range
                self.current_f_vars[i] = self.f_vars_start[i] - new_value
    
    #if any of the f_vars parameters are changed from the outside this function must also be called after that
    def make_f_vars_parameters_consistent(self):

        if(len(self.f_vars_start) == 0):
            return
        
        if(len(self.f_vars_end) == 0):
            self.f_vars_end.append(self.f_vars_max_value)
        
        if(len(self.f_vars_step) == 0):
            self.f_vars_step.append(1)
        
        if(len(self.f_vars_frequency) == 0):
            self.f_vars_frequency.append(1)

        for i in range(0, len(self.f_vars_start)):            
            
            #<make sure all collections have count of elements equal to (if above it is not an issue) `f_vars_start`
            if(i == len(self.f_vars_end)):
                self.f_vars_end.append(self.f_vars_end[len(self.f_vars_end)-1])
            
            if(i == len(self.f_vars_step)):
                self.f_vars_step.append(self.f_vars_step[len(self.f_vars_step)-1])
            
            if(i == len(self.f_vars_frequency)):
                self.f_vars_frequency.append(self.f_vars_frequency[len(self.f_vars_frequency)-1])
            
            #make sure all collections have count of elements equal to (if above it is not an issue) `f_vars_start`>
            
            #<make sure elements in collections fit in range 0-255
            if(self.f_vars_start[i] > self.f_vars_max_value):
                self.f_vars_start[i] = self.f_vars_start[i] % (self.f_vars_max_value+1)
            
            if(self.f_vars_end[i] > self.f_vars_max_value):
                self.f_vars_end[i] = self.f_vars_end[i] % (self.f_vars_max_value+1)
            #make sure elements in collections fit in range 0-255>
        

        #<make sure all collections have count of elements equal to `f_vars_start`
        self.f_vars_end = self.f_vars_end[:len(self.f_vars_start)]
        self.f_vars_step = self.f_vars_step[:len(self.f_vars_start)]
        self.f_vars_frequency = self.f_vars_frequency[:len(self.f_vars_start)]
        #make sure all collections have count of elements equal to `f_vars_start`>

        self.current_f_vars = self.f_vars_start.copy()
        self.current_f_vars_frequency = self.f_vars_frequency.copy()
        

               


            