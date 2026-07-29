import numpy as np
import cv2

from Number_operatios import get_proper_positive_index, get_proper_positive_indexes

class Images_manipulator:

    def __init__(self):

        self.images:list[np.ndarray[np.uint8]] = []


    #<functions for altering the collection of images

    def add_image(self, img:np.ndarray[np.uint8]):
        self.images.append(img)

    def set_main_image(self, new_image:np.ndarray[np.uint8]):

        if(len(self.images) == 0):
            self.images.append(new_image)
        else:
            self.images[0] = new_image

    def remove_images_in_range(self, index1:int, index2:int):

        if(len(self.images) == 0):
            return

        index1, index2 = get_proper_positive_indexes(index1=index1, index2=index2, elements_count=len(self.images))
        del self.images[index1 : index2+1]

    def remove_image(self, index:int):

        if(len(self.images) == 0):
            return

        index = get_proper_positive_index(index=index, elements_count=len(self.images))
        del self.images[index]

    def resize_images_in_range(self, new_height:int, new_width:int, index1:int, index2:int):

        if(len(self.images) == 0):
            return
        
        index1, index2 = get_proper_positive_indexes(index1=index1, index2=index2, elements_count=len(self.images))
        images = []

        for i in range(index1, index2+1):
            if(i >= len(self.images)):
                break
            images.append(self.images[i])

        img_index = index1
        for image in images:
            self.images[img_index] = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

            img_index+=1
            if(img_index > index2):
                break

    def resize_image(self, images_new_percentage_height:int, images_new_percentage_width:int, index:int):

        if(len(self.images) == 0):
            return
        
        index = get_proper_positive_index(index=index, elements_count=len(self.images))
        image = self.images[index]
        self.images[index] = cv2.resize(image, (images_new_percentage_width, images_new_percentage_height), interpolation=cv2.INTER_NEAREST)

    #functions for altering the collection of images>



    #<functions for getting images from the collection of images

    def get_images_in_range(self, index1:int, index2:int) -> list[np.ndarray[np.uint8]]:

        if(len(self.images) == 0):
            return []

        index1, index2 = get_proper_positive_indexes(index1=index1, index2=index2, elements_count=len(self.images))
        return self.images[index1 : index2+1]
    
    def get_image(self, index:int) -> np.ndarray[np.uint8] | None:

        if(len(self.images) == 0):
            return None
        
        index = get_proper_positive_index(index=index, elements_count=len(self.images))
        return self.images[index]

    def get_main_image(self) -> np.ndarray[np.uint8] | None:

        if(len(self.images) == 0):
            return None
        
        return self.images[0]
    

    def get_resized_images(self, indexes:list[int], new_width:int, new_height:int, get_copies:bool=False) -> dict[np.ndarray[np.uint8]]:

        if(new_width <= 0 or new_height <= 0):
            raise Exception("the new width and height of the resized image must be positive values above 0")

        if(len(self.images) == 0 or len(indexes) == 0):
            return {}

        resized_images:dict[np.ndarray[np.uint8]] = {}

        for i in range(0, len(indexes)):

            index = get_proper_positive_index(index=indexes[i], elements_count=len(self.images))
            if(index in resized_images.keys()): #ignore already added images
                continue
            
            image = self.images[index] #get the image

            #resize the image when necessary
            if(new_width != self.images[index].shape[1] or new_height != self.images[index].shape[0]):
                
                image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

            resized_images[index] = image #add the image to the collection of images

            if(get_copies == False):
                self.images[index] = image

        return resized_images
    
    #functions for getting images from the collection of images>



    def get_image_count(self) -> int:
        return len(self.images)

    """
    def copy(self):

        images_manipulator = Images_manipulator()
        images_manipulator.images = self.images.copy()
        return images_manipulator
    """
        
    