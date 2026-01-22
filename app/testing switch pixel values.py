#testing ways to implement the switch pixel functionallity

"""
import numpy as np

arr_pixel_values = np.array(
[ 

[[100, 150, 200], [101, 151, 201]],
[[105, 155, 205], [107, 157, 207]],
[[100, 150, 200], [110, 160, 210]]

]
)

original_img = np.array(arr_pixel_values)


arr_rectangles_pairs = np.array(

[
[ [ [0, 2, 1], [1, 0, 0] ], [ [0, 1, 1], [0, 0, 1] ] ],
[ [ [0, 0, 2], [1, 1, 1] ], [ [0, 1, 2], [0, 0, 0] ] ]
]

)


helper = np.array(arr_rectangles_pairs[:,:,0,0])
arr_rectangles_pairs[:,:,0,0] = arr_rectangles_pairs[:,:,0,1] 
arr_rectangles_pairs[:,:,0,1] = helper

print(arr_pixel_values[2,1,0])#the result is 110






first_rectangle_pair = arr_rectangles_pairs[1]
first_rectangle = first_rectangle_pair[0]
second_rectangle = first_rectangle_pair[1]

first_rectangle_coordinates = first_rectangle[0]
first_rectangle_rgb = first_rectangle[1]
second_rectangle_coordinates = second_rectangle[0]
second_rectangle_rgb = second_rectangle[1]

frc = first_rectangle_coordinates
frr = first_rectangle_rgb
src = second_rectangle_coordinates
srr = second_rectangle_rgb


img_first_rectangle = arr_pixel_values[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2])]
helper = np.array(img_first_rectangle)

arr_pixel_values[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2])] = arr_pixel_values[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2])]
arr_pixel_values[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2])] = helper
#img_first_rectangle = img_second_rectangle
#img_second_rectangle = helper



print("---------------------------------")
print(original_img)
print("---------------------------------")
print(arr_pixel_values)
print("---------------------------------")
print(arr_rectangles_pairs)
print("---------------------------------")
#print(first_rectangle_pair)
print("---------------------------------")
#print(arr_pixel_values[2,0])
print("---------------------------------")
"""









import numpy as np

img = np.array(
[ 

[[100, 150, 200], [101, 151, 201]],
[[105, 155, 205], [107, 157, 207]],
[[100, 150, 200], [110, 160, 210]]

]
)

original_img = np.array(img)


arr_rectangles_pairs = np.array(

[
[ [ [0, 2, 1], [1, 0, 0] ], [ [0, 1, 1], [0, 0, 1] ] ],
[ [ [0, 0, 2], [1, 1, 1] ], [ [0, 1, 2], [0, 0, 0] ] ],
[ [ [0, 0, 2], [1, 1, 1] ], [ [0, 1, 2], [0, 1, 0] ] ],
[ [ [0, 0, 2], [1, 1, 1] ], [ [0, 1, 2], [0, 1, 0] ] ],
[ [ [0, 0, 2], [1, 1, 1] ], [ [0, 1, 2], [0, 1, 0] ] ]
]

)


helper = np.array(arr_rectangles_pairs[:,:,0,0])
arr_rectangles_pairs[:,:,0,0] = arr_rectangles_pairs[:,:,0,1] 
arr_rectangles_pairs[:,:,0,1] = helper







rectangle_pair = arr_rectangles_pairs[2]
first_rectangle = rectangle_pair[0]
second_rectangle = rectangle_pair[1]

first_rectangle_coordinates = first_rectangle[0]
first_rectangle_rgb = first_rectangle[1]
second_rectangle_coordinates = second_rectangle[0]
second_rectangle_rgb = second_rectangle[1]

frc = first_rectangle_coordinates
frr = first_rectangle_rgb
src = second_rectangle_coordinates
srr = second_rectangle_rgb




img_first_rectangle = img[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2]), srr==1]
helper = np.array(img_first_rectangle)

img[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2]), frr==1] = img[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2]), frr==1]

img[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2]), srr==1] = helper





print("---------------------------------")
print("original_img")
print(original_img)
print("---------------------------------")
print("img")
print(img)
print("---------------------------------")
print("arr_rectangles_pairs")
print(arr_rectangles_pairs)
print("---------------------------------")
print("rectangle_pair")
print(rectangle_pair)
print("---------------------------------")
print("img[2,1,0]")
print(img[2,1,0])#the result is 110
print("---------------------------------")
print("arr_rectangles_pairs.size")
print(arr_rectangles_pairs.size)
print("---------------------------------")
print("arr_rectangles_pairs.shape")
print(arr_rectangles_pairs.shape)
print("---------------------------------")
print("len(arr_rectangles_pairs.shape)")
print(len(arr_rectangles_pairs.shape))
print("---------------------------------")
print("arr_rectangles_pairs.shape[1:]")
print(arr_rectangles_pairs.shape[1:])
print("---------------------------------")
print("img.shape[0]")
print(img.shape[0])
print("---------------------------------")
