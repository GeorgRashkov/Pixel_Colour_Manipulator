class Pixel_area:
    
    # all input parameters must be integers or lists of integers
    def __init__(self, id:int, x:int, y:int, w:int, h:int, a_ids:list, ag_ids:list, 
                 f_id:int, p_ids:list, p_x:list, p_y:list, img_in_v:int, img_out_v:int, img_out_stack:int):
        
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

    #creates a copy of it;s self    
    def copy(self) -> "Pixel_area":
        pixel_area = Pixel_area(id = self.id, 
                                x = self.x, y = self.y, w = self.w, h = self.h,
                                a_ids=self.a_ids, ag_ids=self.ag_ids,
                                f_id = self.f_id,
                                p_ids = self.p_ids, p_x=self.p_x, p_y=self.p_y,
                                img_in_v = self.img_in_v, img_out_v=self.img_out_v, img_out_stack=self.img_out_stack)
        return pixel_area
    


    def print_size(self):
        print(f"width:{self.w}")
        print(f"height:{self.h}")