# **What is an RGB formula?**

An RGB formula is a user defined formula which is applied to input RGB values. The RGB formulas are used to determine the return value from a lambda function. The lambda function has 3 RGB formulas for each of the output RGB channels.

The lambda function looks like this
`eval(f"lambda r,g,b: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)")`
where: 
1) `r` contains the input values of the red channel; `g` contains the input values of the green channel; `b` contains the input values of the blue channel;
2) `self.red_func` is the RGB formula of the red output channel; `self.green_func` is the RGB formula of the green output channel; `self.blue_func` is the RGB formula of the blue output channel

Each input parameter of the lambda function is a `numpy` array of type `numpy.uint8`. <br>
The allowed symbols are \[`.` `(` `)` `r` `g` `b` `+` `-` `*` `/` `^` `%` `<` `>` `=` `0` `1` `2` `3` `4` `5` `6` `7` `8` `9`]<br>
The app will remove all spaces from the user defined formula and will replace `^` with `**` and `=` with `==`.<br><br>
The following explanations are focused on performing operations with `numpy` arrays so if you know how `numpy` arrays work you can stop reading the document. 

##

## Examples

Consider the following example - the Main window is placed on top 4 pixels, where:<br>
row 1 and column 1 has RGB val -> `(50,0,0)`; row 1 and column 2 has RGB val -> `(100,10,0)`;<br>
row 2 and column 1 has RGB val -> `(150,20,3)`; row 2 and column 2 has RGB val -> `(200,30,3)`;

This means the input of the lambda function will look like this `(r:[[50,100],[150,200]], g:[[0,10],[20,30]], b:[[0,0],[3,3]])`

<br>

### Arithmetic operators

The arithmetic operators can work with 2 different elements:
1) the array of any of the RGB channels (which has one dimensional arrays containing np.uint8 values)
2) a float or int number

When the arithmetic operator is used by an array and a number, the operation and the number will be applied separately to each np.uint8 value in the array.<br>
When the arithmetic operator is used by two arrays, the operation will be applied to those elements which have the same index.<br>
If the result of the operation is below 0 or above 255 the value will be wrapped (this is a normal numpy behaviour)

Examples based on the above RGB formula input:

RGB formula body => `r+60`<br>
RGB formula result => `r+60` -> `[[50,100],[150,200]] + 60` -> `[[110,160],[210,4]]`

RGB formula body => `r+30+50`<br>
RGB formula result => `r+30+50` -> `[[50,100],[150,200]] + 30 + 50` -> `[[80,130],[180,230]] + 50` -> `[[120,180],[230,24]]`

RGB formula body => `r-g`<br>
RGB formula result => `r-g` -> `[[50,100],[150,200]] - [[0,10],[20,30]]` -> `[[50,90],[130,170]]`

RGB formula body => `b^2`<br>
RGB formula result => `b^2` -> `b**2` -> `[[0,0],[3,3]]**2` -> `[[0,0],[9,9]]`

<br>

### Comparison operators

The comparison operators can work with 2 different elements:
1) the array of any of the RGB channels (which has one dimensional arrays containing np.uint8 values)
2) a float or int number

When the comparison operator is used by an array and a number, the operation and the number will be applied separately to each np.uint8 value in the array.<br>
When the comparison operator is used by two arrays, the operation will be applied to those elements which have the same index.<br>
The result of the comparison operator is either `False` (`0`) or `True` (`1`)

Examples based on the above RGB formula input:

RGB formula body => `r < 150`<br>
RGB formula result => `r < 150` -> `[[50,100],[150,200]] < 150` -> `[[True, True],[False, False]]` -> `[[1,1],[0,0]]`

RGB formula body => `g > b`<br>
RGB formula result => `g > b` -> `[[0,10],[20,30]]` > `[[0,0],[3,3]]` -> `[[False, True],[True, True]]` -> `[[0,1],[1,1]]`

RGB formula body => `(r = 100) * 20`<br>
RGB formula result => `(r = 100) * 20` -> `(r == 100) * 20` -> `([[50,100],[150,200]] == 100) * 20` -> `[[False, True],[False, False]] * 20` -> `[[0,1],[0,0]] * 20` -> `[[0,20],[0,0]]`

##

## How to experiment?

To get familiar with the behaviour of the RGB functions you can use the following python code:

`<br>
import numpy as np

r = np.array([[50,100],[150,200]]).astype(np.uint8)<br>
g = np.array([[0,10],[20,30]]).astype(np.uint8)<br>
b = np.array([[0,0],[3,3]]).astype(np.uint8)

RGB_formula = (r==100)*20

print(RGB_formula)
<br>`

In the above code the `r g b` variables act like the input parameters of the lambda function while `RGB_formula` acts like the user defined RGB formula which can be any of those `self.red_func`, `self.green_func`, `self.blue_func` in the lambda function. When experimenting with the above code all you have to do is choose your own values for the `r g b` and `RGB_formula`. When giving values to  `r g b` consider using this template `np.array([]).astype(np.uint8)` and inside the square brackets you can place any number of one dimensional arrays where each array contains uit8 values (range 0-255). Each array will act like a row while the values inside of it will act like cells so make sure all arrays have the same number of elements. The variables `r g b` must have the same number of arrays and the number of elements in each array must be the same. When giving values to  `RGB_formula` use any of the following elements `. ( ) r g b + - ** * / % < > == 0 1 2 3 4 5 6 7 8 9`. 





