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