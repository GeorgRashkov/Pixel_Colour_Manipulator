# **Pixel Colour Manipulator**

A colour manipulation sandbox for experimentation, learning and visual effects which ca be applied to videos, images, and screen content.
The app is a Python tool designed for Windows OS which uses a Main window that captures the RGB pixel values under it, applies custom user-defined colour functions and displays the transformed result.

<br>

**Important Note** 
This project depends on third-party packages that may have their own license agreements. Their licenses and usage terms may change over time. You can find the third-party packages in the `requirements.txt` file.

##


### **Features**

**🧮 User-defined formulas for each RGB channel**

**🌀 Near real-time pixel transformation using a configurable timer**

**🎛️ Per-channel convolutional filters**

**🎨 Drawing masks that apply separate formulas to user-painted regions**

**📸 Capture masks that apply separate formulas to different regions created with the output of the Main window and RGB thresholds defined by the user**

**🎥 Works on almost anything placed below the Main window including static content or live video behind the window**

##

### **How it works**

The Main window continuously samples the pixels under it and applies the user-defined formulas to them.

The Main window allows the user to enter formula for each of the RGB channels. Formulas entered by user are used as a return value from lambda functions. Each lambda function takes as input the parameters `(r,g,b)` where `r` contains the red channel pixel values under the window, `g` contains the green channel pixel values under the window, `b` contains the blue channel pixel values under the window. Each Main window RGB channel has its own lambda function whose return value is defined by the user. The lambda finctions look like this:
<br>
`eval(f"lambda r,g,b: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)")`

The user can use any of the following characters when writing the formula: \[`.` `(` `)` `r` `g` `b` `+` `-` `*` `/` `^` `%` `<` `>` `=` `0` `1` `2` `3` `4` `5` `6` `7` `8` `9`]. When writing the formula the user must use at least once any of the symbols \[`r` `g` `b`] so the program can have pixel values to apply transformations. 

Some symbols are transformed by the app to make them compatible with the Python syntax. The symbol `^` is transformed into `**` while `=` is transformed into `==`. The app will not allow the user to change the RGB formulas if the user uses invalid symbols (spaces are ignored but also allowed for readability) or invalid syntax. Here are a few valid formulas: `r-g+100`; `r-g-b*0.2`; `b`, `r>155`; `5^r^g`; `(r-20)*(g-150)`. Here are a few invalid formulas: `r-g+`, `100`, `200-100`, `r**2`.

##


### **Windows and tools**

###### 

#### **Main window**

* RGB text boxes - allow the user to enter formulas for R, G, B outputs
* RGB sliders - allow the user to suppress or strengthen the R, G, B outputs in a simple, fast and smooth way
* Slider value - an int value which gets divided by 100 and then it is multiplied by the RGB input values 
* Capture timer - defines how often the pixels under the window are captured and updated
* `capture` button - samples the pixels under the Main window only once allowing the user to update the output of the main window manually when the Capture timer value is high
* `settings` button - opens the Settings window
* `draw mask` button - opens the Draw masks window
* `capture mask` button - opens the Capture mask window
* `convolution` button - opens the Convolution window



#### **Settings window**

* `Update capture time` text box - allows the user to set the value for the Capture timer (in seconds) of the Main Window
* `Slider min value (in %)` text box - allows the user to set the min value (in percentage) of the RGB sliders on the Main window
* `Slider max value (in %)` text box - allows the user to set the max value (in percentage) of the RGB sliders on the Main window 
* Colour functions sequence order - allows the user to determine the execution sequence of different colour functions 
* `RGB use doubles` check box - when the check box is checked the Main window will be showing the actual result from the colour functions without transforming the values to np.uint8.



#### **Convolution window**

* allows the user to define convolutional filters for each RGB channel which the Main window will apply to the pixel values under it for obtaining the result
* the user can set the width, height, stride and dilation of the convolutional kernels
* each Main window RGB channel has its convolutional kernel
* the values of the convolutional filter are represented as text fields in which the user can enter any float numbers, including negative ones
* Useful for blur/sharpen/edge detect



#### **Draw Masks window**

* Six colour sections: red, green, blue, yellow, black, white
* Each colour section has its own RGB formulas (they are the same as those of the Main window) defined by the user
* The colour sections allow the user to draw on a canvas and apply to the Main window separate RGB formulas to user-painted regions
* The app will use as a default RGB formula the last section. The default RGB formula is applied not only to the regions with its colour but also to those regions that were not painted at all by the user.



#### **Capture Masks window**

* Six sections with min-max RGB thresholds defined by the user
* Each section has its own RGB formulas (they are the same as those of the main Window) defined by the user
* Allows the user to apply up to 6 RGB formulas in different locations of the Main window. When the user applies the capture mask, the app creates those locations (the mask) by using the min-max RGB threshold values and the output result of the Main window. The result is that the RGB formulas of any section will be applied to those locations where the pixel values of the Main window were within the RGB thresholds of the section. During the creation of the mask if a pixel appears to be within the RGB thresholds of 2 or more sections the location of that pixel will use the RGB formulas of the first matching section.
* The app will use as a default RGB formula the last section. The default RGB formula is applied not only to the regions that match its min-max RGB threshold values but also to those regions which didn't match any of the min-max RGB threshold values for the six sections.


##


### **Additional functionalities**


#### **Main window movement**

The user can freely move the Main window to any point on the screen. The user can also change the width and height of the Main window to match the size of the region on the screen which the user wants to capture.


#### **Brush size**

When using the canvas of the Draw mask window the user can change the brush size by placing the cursor on top of the canvas and move the scroll up (to increase the size) or down (to reduce the size). The user can also define min, max and increment values of the brush by using the specified text boxes on the Draw mask window.


#### **Controlling number of active sections when creating masks**

When the user creates a drawn or captured mask, the mask will have 6 sections. Since each section is processed separately on each pixel under the Main window, the app uses only the active sections to boost performance. The app activates only those sections which have different RGB formulas from the previous sections.


#### **Showing current RGB section formula**

When the user uses the Draw mask window or the Capture mask window he can check the current RGB formulas by pressing the button `show`. Both windows have this button in each of their sections. This button is useful when the user tries to apply invalid RGB formulas - the RGB text box will have the value which the user entered (which can be wrong) while the button `show` is responsible for showing the currently selected formula for the section. 


#### **Controlling colour functions**

When the user applies a colour function, the function may either overwrite other colour functions or it might be added as a separate colour function. This behaviour depends on the type of the colour function. 

The Capture mask window, the Draw mask window and the text boxes on the Main window all use RGB formulas for changing the colour of the pixels under the Main window and when the user applies a new RGB formula it can overwrite the others. Capture mask window and Draw mask window can apply different RGB formulas at specific regions and whenever the user applies a captured mask or drawn mask it will override the previous mask as well as the RGB formulas defined in the text boxes on the Main window. The RGB formulas created with the text boxes on the Main window act as default colour function which means whenever the user creates a captured mask or drawn mask he can change their default colour function by using the text boxes on the Main window. In order to remove a captured mask or drawn mask the user must use the button `Remove mask` located on the Draw mask window. When the mask is removed the current default colour function will remain.

The sliders on the Main window and the convolutional filters on the Convolution mask window use independent colour functions. This means they cannot overwrite other colour functions except their own colour function. This behaviour allows the user to define either captured mask or drawn mask which can be processed alongside the sliders' values and the convolutional filters. The processing of the colour functions happens in a sequence. The user can define the execution sequence of the colour functions in the Settings window. In order to disable the convolutional filters the user must use the button `Remove filters` in the Convolutional mask window. In order to disable the sliders the user has to set them to the value 100. As the sliders provide a little info about their exact value the user can set their min and max values from the settings window. In fact the user can automatically set the sliders to the exact value he wants by setting their max and min value to be the value he wants.


##


### **Tips**

* For fast performance - simplify RGB formulas, avoid convolution, reduce the size of the Main window, when using captured mask or drawn mask use small number of active sections
* When using convolution is advisable to disable auto update by setting timer high (e.g., 999999), as the convolutional process may take a while before completing.  
* When using the Capture mask window consider not applying the same RGB formulas in more than 1 section as the program will use only the first one of them. If you want to use the same RGB formula for 2 or more min-max colour ranges you can do that by changing the string representation of any of the RGB formulas without affecting the result. For instance the RGB formula `r` produces the same result as `r+0` however since their string representation is different when you apply the capture mask the program will create 2 separate active regions and will threat them as if they were different formulas. Consider that this will lead to extra computation in comparison to using the RGB formula in just one section. Keep in mind that the program ignores spaces (the program will threat `r + g`, `r+ g`, `r  +g` as `r+b`). 
* Do not use values in the RGB formulas outside 0-255. The app uses dxcam to get the pixel values under the Main window and dxcam produces a uint8 numpy array making the formula uncapable of handling values outside 0-255 (the app won't crash as it will use the previous working formula). Operation between 2 uint8 values which results in a value outside 0-255 (for instance `100*3`, `0-1`) will cause the same problem, however operations between uint8 value and a numpy array (which can be any of the RGB channels for the pixels under the Main window) will silently wrap the result if it is outside 0-255 without throwing errors: if you use `200+200+r` the app will not apply the formula, however if you use `r+200+200` the app will apply the formula due to the silent wraps by numpy. If you want to use negative powers on RGB channels consider writing something like `r^(r*0+1-2)` (if you try to use `r^(1-2)` the app will not apply your formula because `1-2` is outside the range 0-255).
* Keep the `RGB use doubles` check box from the Settings window unchecked as it can make the output of the Main window look very weird.
* All messages created by the app are shown in the terminal. In case you wonder why the app doesn't apply your input you can check the terminal for error messages to find out what was wrong with the input. 


##


### **Requirements**

* Windows OS - confirmed to work on Windows 11
* Python - confirmed to work with Python 3.12.5
* Virtual python env
* IDE - tested with VS Code


##


### Setup
0. Clone the repository

1. Create a virtual python environment (make sure the env's folder is inside the repo)  
   `python -m venv "path/to/new/virtual/environment"`  

2. Activate the env - if you don't know how you can check my `python_venv_activation.md` file

3. Install the required packages in the env  
   `pip install -r requirements.txt`

4. Run the `Main_app.py` file
