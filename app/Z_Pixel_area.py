import numpy as np

class Pixel_area:
    
    # all input parameters must be integers or lists of integers
    def __init__(self, id:int, x:int, y:int, w:int, h:int, a_ids:list, ag_ids:list, 
                 f_id:int, p_ids:list, p_x:list, p_y:list, img_in_v:int, img_out_v:int, img_out_stack:int,
                 x_rep_start:list, y_rep_start:list, x_rep_end:list, y_rep_end:list, x_rep_step:list,y_rep_step:list, x_rep_count:list, y_rep_count:list, f_ids_rep:list):
        
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

        #pixel areas which will be used as an input for the rgb function
        self.p_ids = p_ids #contains the pixel area ids which will passed to the RGB formula
        self.p_x = p_x #this is a list which contains the horizontal position of the top left corner of not defined pixel areas which will passed to the RGB formula
        self.p_y = p_y #this is a list which contains the vertical position of the top left corner of not defined pixel areas which will passed to the RGB formula
        
        #image versions which will be used as an input and ouput of the rgb function; maximum of 10 image versions
        self.img_in_v = img_in_v #determines the version of the input image which will be passed to the RGB formula
        self.img_out_v = img_out_v #determines the version of the image to which the changed pixel values will be applied
        self.img_out_stack = img_out_stack #determines the count of image versions to which the changed pixel values will be applied; the first version is `img_out_v`, the next version is `img_out_v + 1` and so on 

        self.area_zeros = None
        self.set_area_zeros(height = self.h, width = self.w)

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
        #repeat areas arguments>

    def set_area_zeros(self, height, width):
        self.area_zeros = np.zeros(shape=(height, width, 3), dtype=np.uint8)
    
    def get_area_zeros(self):
        return self.area_zeros.copy()