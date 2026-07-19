"""
class Image_version_controller():
    def __init__(self, image_version_start_index:int, image_version_increment:int, image_version_swap_frequency:int, image_versions_count:int):
        
        self.current_image_version_index = image_version_start_index
        self.image_version_increment = image_version_increment
        self.image_version_swap_frequency = image_version_swap_frequency
        self.calls_counter = image_version_swap_frequency
        
        self.image_versions_count = image_versions_count
        self.current_image_version_index %= image_versions_count
        self.image_version_increment %= image_versions_count
        
        
    
    def update_parameters(self):
        
        self.calls_counter-=1
        if(self.calls_counter > 0):
            return
        
        self.calls_counter = self.image_version_swap_frequency
        self.current_image_version_index = (self.current_image_version_index + self.image_version_increment) % self.image_versions_count
    
    def get_next_image_version_index(self) -> int:

        self.update_parameters()
        return self.current_image_version_index
"""



class Image_version_controller():
    def __init__(self, start:int, end:int, step:int, swap_frequency:int, image_versions_count:int):
        
        if(swap_frequency < 0):
            raise Exception("the swap frequency of the image versions cannot be negative")

        if(image_versions_count < 1):
            raise Exception("the count of the image versions cannot be below 1")

        self.start = start % image_versions_count
        self.end = end % image_versions_count
        self.step = step % image_versions_count

        self.current_index = 0

        self.image_versions_count = abs(self.end - self.start) + 1
        self.swap_frequency = swap_frequency
        self.calls_counter = swap_frequency
    
    def get_next_image_version_index(self) -> int:

        if(self.step!=0 and self.image_versions_count!=0):
            self.calls_counter-=1
            if(self.calls_counter <= 0):
                self.calls_counter = self.swap_frequency
                self.current_index = (self.current_index + self.step) % self.image_versions_count
        
        current_index = self.start + self.current_index if(self.start < self.end) else self.start - self.current_index

        return current_index