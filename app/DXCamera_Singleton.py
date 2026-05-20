import dxcam
from dxcam import DXCamera

class DXCamera_Singleton:
    instance = None

    def __new__(self):
        
        if self.instance is None:
            self.instance = super().__new__(self)
            self.__camera:DXCamera = dxcam.create()

        return self.instance
    
    def get_DXCamera(self):
        return self.__camera
