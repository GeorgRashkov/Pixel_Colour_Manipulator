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









"""

"""
import numpy as np

img = np.array([[[1,2,3],[10,20,30]],[[5,7,9],[50,70,90]]])
img1 = np.array([[[11,12,13],[110,120,130]],[[5,7,9],[50,70,90]]])
img2 = np.array([[[21,22,23],[210,220,230]],[[5,7,9],[50,70,90]]])
img3 = np.array([[[31,32,33],[310,320,330]],[[5,7,9],[50,70,90]]])

img_list = [img, img1, img2, img3]

img_areas = np.array([])

print(img_areas.shape)
print(img_areas.shape[0])
"""



"""
import numpy as np

img = np.array([ [[[1,2,3],[10,20,30]],[[5,7,9],[50,70,90]]], [[[11,22,33],[110,220,35]],[[55,77,99],[150,170,190]]] ], dtype=np.uint8)

rgb_formula1 = "np.stack([ r[0 if 0<areas_count else 0]+g, g, b ], axis=-1)"
rgb_function1 = eval(f"lambda r,g,b,areas_count: {rgb_formula1}")

transformed_img1 = rgb_function1(img[:,:,:,0], img[:,:,:,1], img[:,:,:,2], img.shape[0])



rgb_formula2 = "np.stack([ r+g, g, b ], axis=-1)"
rgb_function2 = eval(f"lambda r,g,b,areas_count: {rgb_formula2}")

transformed_img2 = rgb_function2(img[:,:,:,0], img[:,:,:,1], img[:,:,:,2], img.shape[0])


print("transformed_img1:red") 
print(transformed_img1[:,:,:,0])
print("-------------------------------------")
print("transformed_img2:red") 
print(transformed_img2[:,:,:,0])
print("-------------------------------------")

print("transformed_img1.shape") 
print(transformed_img1.shape)
print("transformed_img2.shape") 
print(transformed_img2.shape)
    

print("-------------------------------------")
print("-------------------------------------")
print("-------------------------------------")


img = np.array([   [ [[1,2,3],[10,20,30]], [[1,2,3],[10,20,30]], [[5,7,9],[50,70,90]]],   [ [[11,22,33],[110,220,35]], [[55,77,99],[150,170,190]], [[1,2,3],[10,20,30]]  ] ], dtype=np.uint8)
print("img[:,:,:,1]")
print(img[:,:,:,1])
print("-------------------------------------")
print("img[:,:,:,0]")
print(img[:,:,:,0])
print("-------------------------------------")
print("img[:,:,:,0]+img[:,:,:,1]")
print(img[:,:,:,0]+img[:,:,:,1])
print("-------------------------------------")
print("img[:,:,:,0][0]")
print(img[:,:,:,0][0])
print("-------------------------------------")
print("img[:,:,:,0][0]+img[:,:,:,1][0]")
print(img[:,:,:,0][0]+img[:,:,:,1][0])
print("-------------------------------------")
print("-------------------------------------")
print("-------------------------------------")
print("-------------------------------------")


print("img[:,:,:,0][0]")
print(img[:,:,:,0][0])
print("-------------------------------------")
print("img[:,:,0,1][0]")
print(img[:,:,0,1][0])
print("-------------------------------------")
print("img[:,:,:,0][0] + img[:,:,0,1][0]")
print(img[:,:,:,0][0] + img[:,:,0,1][0])

"""





for i in range(0, 34):

  current = 189
  start = 59
  end = 47
  step = i
  range_ = end-start+1 if(end>=start) else start-end+1

  new_value = 0

  if(range_ == 0):
    continue

  if(end >= start):
    new_value = (current-start+step) % range_
    current = start + new_value

    if(current > end):
      print("wtf")
      #current = start + current%(end+1)

  else:
    new_value = (start-current+step) % range_
    current = start - new_value

    if(current < end):
      print("wtf")
      #current = start - current%(end+1)


    
  print("current:", current, "step:", step)