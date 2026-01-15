#This file is for testing purposes only (it can deleted safely as no files rely on it)

import numpy as np


def set_color_variables( r_formula, g_formula, b_formula):
    rgb_function = eval(f"lambda r,g,b: np.stack([{r_formula},{g_formula},{b_formula}], axis=-1)")
    return rgb_function

rgb_function = lambda r,g,b: np.stack([r,g,b], axis=-1)

rgb_function = set_color_variables("200+200+r", "g", "b")

img = np.array([ 
  [[10,20,30],[35,40,45]], 
  [[50,60,70],[75,85,95]], 
  [[100,120,240],[150,200,250]] 
])

transformed_img = rgb_function(img[:,:,0], img[:,:,1], img[:,:,2])
print("success:")
print(transformed_img)


"""
import dxcam
print("\ndxcam result:\n")
camera = dxcam.create()
x = 2
y = 2
w = 2
h = 2
img = camera.grab(region=(x, y, x + w, y + h))
transformed_img = rgb_function(img[:,:,0], img[:,:,1], img[:,:,2])
print("success!")
"""


import numpy as np

uint8_numpy_array = np.array([[[1,2,3],[10,20,30]],[[5,7,9],[50,70,90]]], dtype=np.uint8)
img = uint8_numpy_array
transformed_img = rgb_function(img[:,:,0], img[:,:,1], img[:,:,2])
print(transformed_img)