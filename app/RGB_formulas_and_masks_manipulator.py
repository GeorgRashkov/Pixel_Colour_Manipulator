import numpy as np

from Z_RGB_formula import RGB_formula
from Z_Pixel_areas_mask import Mask

class RGB_formulas_and_masks_manipulator():

    def __init__(self):

        self.rgb_formulas:dict[int, RGB_formula] = {}
        self.masks_ids_and_rgb_formulas_ids:dict[int, list[int]] = {}
        self.masks:dict[int, Mask] = {}
        self.masks_ids:list[int] = []

    def apply_rgb_formulas(self, rgb_formulas:dict[int, RGB_formula]):
        self.rgb_formulas = rgb_formulas

    def apply_masks_ids_and_rgb_formulas_ids(self, masks_ids_and_rgb_formulas_ids:dict[int, list[int]]):
        self.masks_ids_and_rgb_formulas_ids = masks_ids_and_rgb_formulas_ids

    def apply_masks(self, masks:dict[int, Mask]):
        self.masks= masks
        self.masks_ids = list(masks.keys())
        self.masks_ids.sort()

    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def transform_image_with_masks(self, img:np, v:np.ndarray[np.uint8]) -> np.ndarray:

        #cycle trhough all masks
        for mask_id in self.masks_ids:

            #skip masks which have no rgb formulas
            if(mask_id not in self.masks_ids_and_rgb_formulas_ids.keys()):
                continue

            rgb_formulas_ids_for_current_mask:list[int] = self.masks_ids_and_rgb_formulas_ids[mask_id]
            rgb_formulas:list[RGB_formula] = []
            for rgb_formula_id in rgb_formulas_ids_for_current_mask:
                if(rgb_formula_id in self.rgb_formulas.keys()):
                    rgb_formula = self.rgb_formulas[rgb_formula_id]
                    rgb_formulas.append(rgb_formula)

            mask = self.masks[mask_id]
            img = mask.transform_image(img=img, rgb_formulas=rgb_formulas, rgb_formulas_dynamic_variables=v)

        return img

    """
    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def transform_image_with_formulas(self, img:np, v:np.ndarray[np.uint8], rbg_formulas_ids:list[int]) -> np.ndarray:

        r = img[:,:,0]
        g = img[:,:,1]
        b = img[:,:,2]

        for rbg_formula_id in rbg_formulas_ids:
            if(rbg_formula_id in self.rgb_formulas.keys()):

                rgb_formula = self.rgb_formulas[rbg_formula_id]
                img = rgb_formula.rgb_function(r=r, g=g, b=b, v=v)

        return img
    """

    #The input must be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
    def transform_image_with_rgb_formulas(self, img:np, v:np.ndarray[np.uint8], rbg_formulas_ids:list[int]) -> np.ndarray:

        for rbg_formula_id in rbg_formulas_ids:
            if(rbg_formula_id in self.rgb_formulas.keys()):

                rgb_formula = self.rgb_formulas[rbg_formula_id]
                img = rgb_formula.rgb_function(r=img[:,:,0], g=img[:,:,1], b=img[:,:,2], v=v)

        return img

            