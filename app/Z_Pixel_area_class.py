class Pixel_area:
    
    def __init__(self, id:int, x:int, y:int, width:int, height:int, pixel_areas_ids:list, rgb_function_str:str, rgb_function_lambda):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pixel_areas_ids = pixel_areas_ids
               

        self.rgb_function_str = rgb_function_str
        self.rgb_function = rgb_function_lambda

        self.move_class_instance = None
        self.resize_class_instance = None