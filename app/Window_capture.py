import ctypes
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QSlider
import win32con, win32gui
import cv2
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QCheckBox, QLabel
from PyQt5.QtCore import Qt
import RGB_formula_elements
from Z_Pixel_areas_manipulator import Pixel_areas_manipulator


class Kernel():
    def __init__(self, stride: int, holes_count: int, kernel_values: np.ndarray):
        self.stride = stride
        self.holes_count = holes_count
        self.kernel_values = kernel_values

class RGB_Kernels():
    def __init__(self, r_kernel: Kernel, g_kernel: Kernel, b_kernel: Kernel):
        self.r_kernel = r_kernel
        self.g_kernel = g_kernel
        self.b_kernel = b_kernel



class CaptureWindow(QtWidgets.QWidget):

    SLIDERS_VALUES = {"r":1, "g":1, "b":1}
    

    def __init__(self, screen_width, screen_height, camera):
        super().__init__()
        self.transformed_image = None
        self.rgb_kernels = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.mask_filters = None
        self.color_functions = [lambda r,g,b: np.stack([255-r+g*0+b*0, r*0+255-g+b*0, r*0+0*g+255-b], axis=-1)]#[{"r": lambda r,g,b:255-r+g*0+b*0, "g": lambda r,g,b:r*0+255-g+b*0, "b": lambda r,g,b:r*0+0*g+255-b}]
        self.default_color_function = lambda r,g,b: np.stack([r, g, b], axis=-1)#{"r": lambda r,g,b: r, "g": lambda r,g,b: g, "b": lambda r,g,b: b}
        
        # each element in `swap_pixel_areas` must be a rectangle pair (a numpy array of two rectangles)
        # a rectangle looks like this f"[ [{x}, {y}, {size}], [{int(use_red)}, {int(use_green)}, {int(use_blue)}], [{int(rgb_function_id)}] ]" (all elements in the rectangle must be integers) (`y` and `x` are the coordinates of the top left corner of the rectangle)
        self.swap_pixel_areas = None #when initialized it must a numpy array
        


        self.pixel_areas_manipulator:Pixel_areas_manipulator = None
        """
        #`swap_pixel_areas_rgb_formulas` is a dictionary which has numbers (RGB fomulas ids) for keys and RGB fommulas (represented as lamda functions) for values,
        # the default key is `0` while the default value is = `eval(f"lambda r,g,b: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)")`)
        self.swap_pixel_areas_rgb_formulas = None
        """        
        

        self.RGB_use_doubles = False

        self.color_methods_execution_order = [1, 2, 3, 4] #the elements in "self.color_methods_execution_order" determine the execution order of the methods in "self.color_methods"
        self.color_methods = [self.apply_color_functions_to_image, self.apply_convolution_to_image, self.apply_sliders_values_to_image, self.apply_pixel_areas_manipulator] #all the methods must: take as input an image (as type "np.ndarray"); make transformations to the image; return the tranformed image (as type "np.ndarray")

        self.setWindowTitle("Color Changer")
        self.setMinimumSize(200, 30)
        self.resize(400, 400)
             
        self.camera = camera

        # Keep a pixmap to paint
        self._pixmap = None
        
        # Timer to refresh periodically the output of the window
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(99999999)# 100 means 0.1 second #start(UPDATE_INTERVAL_MS)

        self.initialize_a_click_through_button()
        self.click_through_on_off()       

        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.button_capture_now = QPushButton('capture', QtWidgets.QWidget(self))
        self.button_capture_now.clicked.connect(self.update_capture)

        self.label_stack_output = QLabel("stack output")
        self.label_stack_output.setStyleSheet("background-color: black; color: white;")
        self.checkBox_stack_output = QCheckBox()
        self.label_stack_output.setBuddy(self.checkBox_stack_output)

        self.button_open_settings = QPushButton('settings',  QtWidgets.QWidget(self))
        self.button_open_drawMask = QPushButton('draw mask',  QtWidgets.QWidget(self))
        self.button_open_captureMask = QPushButton('capture mask',  QtWidgets.QWidget(self))
        self.button_open_convolutionalFilter = QPushButton('convolution',  QtWidgets.QWidget(self))
        self.button_open_swopAreas = QPushButton('swop areas',  QtWidgets.QWidget(self))

        #<color sliders
        
        """#not finished
        validator = QIntValidator(0, 999, self)
        textBox_colorRange = QtWidgets.QLineEdit()
        textBox_colorRange.setMaxLength(3)
        textBox_colorRange.setValidator(validator)
        """

        self.slider_red = QSlider(Qt.Horizontal)
        self.slider_red.setMinimum(0)
        self.slider_red.setMaximum(100)
        self.slider_red.setValue(100)
        self.slider_red.valueChanged.connect(lambda: self.slider_value_changed(self.slider_red.value(), 'r'))
        self.slider_red.setStyleSheet(
            """ 
            QSlider::handle:horizontal { 
            background: red; 
            }
            QSlider::sub-page:horizontal {
            background: red;
            }
        """)

        self.slider_green = QSlider(Qt.Horizontal)
        self.slider_green.setMinimum(0)
        self.slider_green.setMaximum(100)
        self.slider_green.setValue(100)
        self.slider_green.valueChanged.connect(lambda: self.slider_value_changed(self.slider_green.value(), 'g'))
        self.slider_green.setStyleSheet(
            """ 
            QSlider::handle:horizontal { 
            background: green; 
            }
            QSlider::sub-page:horizontal {
            background: green;
            }
        """)


        self.slider_blue = QSlider(Qt.Horizontal)

        self.slider_blue.setMinimum(0)
        self.slider_blue.setMaximum(100)
        self.slider_blue.setValue(100)
        self.slider_blue.valueChanged.connect(lambda: self.slider_value_changed(self.slider_blue.value(), 'b'))
        self.slider_blue.setStyleSheet(
            """ 
            QSlider::handle:horizontal { 
            background: blue; 
            }
            QSlider::sub-page:horizontal {
            background: blue;
            }
        """)

        self.setStyleSheet("""
            QSlider::groove:horizontal {
                background: black;
                height: 5px;
            }
            QSlider::handle:horizontal {
                width: 5px;
                margin: -15px 0;
            }
        """)
        #color sliders>

        #<buttons for showing and hiding widgets on the rows of the buttons
        
        self.button0_showHide_widgets = QPushButton('', QtWidgets.QWidget(self))
        self.button0_showHide_widgets.clicked.connect(lambda: self.hide_widgets(0))
        self.button0_showHide_widgets.setMaximumSize(10,10)

        self.button1_showHide_widgets = QPushButton('', QtWidgets.QWidget(self))
        self.button1_showHide_widgets.clicked.connect(lambda: self.hide_widgets(1))
        self.button1_showHide_widgets.setMaximumSize(10,10)

        self.button2_showHide_widgets = QPushButton('', QtWidgets.QWidget(self))
        self.button2_showHide_widgets.clicked.connect(lambda: self.hide_widgets(2))
        self.button2_showHide_widgets.setMaximumSize(10,10)

        self.button3_showHide_widgets = QPushButton('', QtWidgets.QWidget(self))
        self.button3_showHide_widgets.clicked.connect(lambda: self.hide_widgets(3))
        self.button3_showHide_widgets.setMaximumSize(10,10)

        self.button_showHide_all_widgets = QPushButton('', QtWidgets.QWidget(self))
        self.button_showHide_all_widgets.clicked.connect(self.show_all_widgets)
        self.button_showHide_all_widgets.setMaximumSize(10,10)
        self.are_widgets_shown = True

        #buttons for showing and hiding widgets on the rows of the buttons>
        

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0,0,0,0)
       
        h_layout = QHBoxLayout()        
        h_layout.addWidget(self.button0_showHide_widgets)
        
        h_layout.addWidget(self.button_capture_now)
        h_layout.addWidget(self.button_open_settings)
        h_layout.addWidget(self.label_stack_output)
        h_layout.addWidget(self.checkBox_stack_output)
        h_layout.setAlignment(Qt.AlignLeft)

        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()        
        h_layout.addWidget(self.button1_showHide_widgets)        
        h_layout.addWidget(self.button_open_drawMask)
        h_layout.addWidget(self.button_open_captureMask)
        h_layout.addWidget(self.button_open_convolutionalFilter)
        h_layout.addWidget(self.button_open_swopAreas)
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()        
        h_layout.addWidget(self.button2_showHide_widgets)
        h_layout.addWidget(self.slider_red)
        h_layout.addWidget(self.slider_green)
        h_layout.addWidget(self.slider_blue)
        self.v_layout.addLayout(h_layout)
        
        self.rgb_elements = RGB_formula_elements.RGB_formula_elements()
        h_layout = QHBoxLayout()
        
        h_layout.addWidget(self.button3_showHide_widgets)
        for channel in self.rgb_elements.channels:
            button_apply_formula = QPushButton("OK")
            button_apply_formula.setMaximumWidth(30)
            button_apply_formula.clicked.connect(self.set_default_color_function)
            h_layout.addWidget(button_apply_formula)
            h_layout.addWidget(self.rgb_elements.text_boxes[channel])
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_showHide_all_widgets, alignment=Qt.AlignLeft)
        
        self.v_layout.addLayout(h_layout)
       

        self.setLayout(self.v_layout)
        self.v_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Show the widget
        self.show()
    
    def on_timer(self):
        # Periodic update
        self.update_capture()

    def slider_value_changed(self, slider_value, slider_id):
        self.SLIDERS_VALUES[slider_id] = round(slider_value*0.01,2)
        #print(slider_id, self.SLIDERS_VALUES[slider_id])
    
    def show_all_widgets(self):
        rows_count = self.v_layout.layout().count()

        if(self.are_widgets_shown == False):
            self.are_widgets_shown = True
            for i in range(0, rows_count - 1):
                self.show_widgets(i)
        else:
            for i in range(0, rows_count - 1):
                self.hide_widgets(i)
    
    def show_widgets(self, row: int):
        row_layout = self.v_layout.layout().itemAt(row)
        if(row_layout == None):
            return

        for i in range(0, row_layout.count()):
                
                widget = row_layout.itemAt(i).widget()

                if(widget != None):
                    widget.show()

    def hide_widgets(self, row: int):#hides the widgets located at the row with number "row"

        row_layout = self.v_layout.layout().itemAt(row)
        self.are_widgets_shown = False
        
        if(row_layout == None):
            return
        
        for i in range(0, row_layout.count()):
                
                widget = row_layout.itemAt(i).widget()
                if(widget != None):
                    widget.hide()
       
    def set_default_color_function(self):
        self.rgb_elements.change_RGB_formula()
        self.default_color_function = self.rgb_elements.rgb_function
        print(self.rgb_elements.red_func) 
        print(self.rgb_elements.green_func) 
        print(self.rgb_elements.blue_func) 


    #creates a button which will make the set off the "click-through the window" ability
    #the button will be shown only when the window (not including the header) is pressed twice
    def initialize_a_click_through_button(self):
        self.button = QPushButton('')
        self.click_through = True
        self.button.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.button.clicked.connect(self.click_through_on_off)

        hwnd = int(self.button.winId())
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                              0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
   
    #when the window (not including the header) is pressed twice the following function will: 
    # set on the "click-through the window" ability; show a button which will be placed in the heather of the window  
    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        self.click_through_on_off()

        geo = self.geometry()# Get window geometry
        x, y, w= geo.x(), geo.y()-30, geo.width()
    
        #when the button is pressed the "click-through the window" ability will set to off
        self.button.move(x, y)
        self.button.resize(w, 30)
        self.button.show()
       


    def click_through_on_off(self):
        self.button.hide()
        hwnd = int(self.winId())
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

        if not self.click_through:
            self.click_through = True
            # Add click-through
            style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT| win32con.WS_EX_TOPMOST
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

             # Makes sure the window stays topmost in z-order (change to NOTOPMOST if desired)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                              0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
        else:
            self.click_through = False
            # Removes WS_EX_TRANSPARENT while keeping WS_EX_LAYERED
            style &= ~win32con.WS_EX_TRANSPARENT

            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
            # Makes sure the window stays topmost in z-order (change to NOTOPMOST if desired)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                              0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
   

    def showEvent(self, event):
        self.exclude_from_capture(True)
        super().showEvent(event)
        

    def exclude_from_capture(self, exclude=True):
        #Use DWM to hide window from screen capture (so it doesn't capture itself) while keeping the window visible and clickable.
        hwnd = int(self.winId())
        WDA_NONE = 0x00000000
        WDA_EXCLUDEFROMCAPTURE = 0x00000011

        mode = WDA_EXCLUDEFROMCAPTURE if exclude else WDA_NONE
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, mode)

    

    
    def get_window_coordinates(self):
        geo = self.geometry()# Get window geometry
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()#`x` and `y` are horizontal and veritcal coordinates of the top left corner of the window; `w` and `h` are the width and height of the window
            
        if(x<0):
            x=0
        if(y<0):
            y=0
        x4, y4 = (x + w), (y + h)#`x4` and `y4` are horizontal and veritcal coordinates of the bottom right corner of the window;
        if(x4 > self.screen_width):
            w = w-(x4 - self.screen_width)
        if(y4 > self.screen_height):
            h=h-(y4 - self.screen_height)
        
        return x, y, w, h
    

#<Functions for changing the RGB values of the area under the window
    
    def update_capture(self):
            
            """#this is usefull for checking the count of the mask filters and the colour functions (it is not important as it is only for testing purposes)
            if(self.mask_filters!=None):
                print(f"mask filters: {len(self.mask_filters)}, color functions: {len(self.color_functions)}, default colour function: {1}")
            """

        #try:
            x, y, w, h = self.get_window_coordinates()
            
            if(w < 1 or h < 1):#don't make tranformartions if the user places the window completly outside the screen (this check avoids errors that can crash the app when `self.camera.grab` is called)
                return

            img = None            
            if(self.checkBox_stack_output.isChecked() == True and self.transformed_image is not None):
                img = self.transformed_image 
            else:
                # Use dxcam to capture that screen rectangle
                img = self.camera.grab(region=(x, y, x + w, y + h))#The returned frame will be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
           
            if img is not None:
                
                self.transformed_image = self.transform_image(img)
               
                # Convert to QImage
                h, w = self.transformed_image.shape[:2]
                bytes_per_line = 3 * w
                qimg = QtGui.QImage(self.transformed_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                
                # make a QPixmap to draw (copy to ensure memory is owned by Qt)
                pixmap = QtGui.QPixmap.fromImage(qimg).copy()

                # Store pixmap and repaint
                self._pixmap = pixmap

            # Force a paint
            self.update() #calls the "paintEvent" function

        #except Exception as e:
          #print("Capture/update error:", e)
    
    def transform_image(self, img):
        
        #applies all methods that change that change the RGB channel values
        for method_index in self.color_methods_execution_order:
            img = self.color_methods[method_index - 1](img)
        
        if(self.RGB_use_doubles==False):
            img = img.astype(np.uint8)

        return img

   
    def apply_color_functions_to_image(self, img):#img must be a "numpy.ndarray" in the shape of (Height, Width, 3) Where 3 is for the RGB color channels
        

    #<change the color of the pixels in the image without a mask
        
        if(self.mask_filters is None):#self.default_color_function has this value `lambda r,g,b: np.stack([r, g, b], axis=-1)`
            
            transformed_image = self.default_color_function(img[:,:,0], img[:,:,1], img[:,:,2])
            return transformed_image       
        
    #change the color of the pixels in the image without a mask>
        

    #<change the color of the pixels in the image using a mask

        # Initialize output
        transformed_image = np.zeros_like(img, dtype=float)

        # Keep track of which pixels have been transformed
        processed_mask = np.zeros(self.mask_filters[0].shape, dtype=bool)

        try:        
            # Apply filters in order
            for mf, func in zip(self.mask_filters, self.color_functions):               
                
                #if the user changes the shape of the window than the code in the if statement whill be executed in order to make the size of the filters match the size of the resized image         
                if(img.shape[1] !=self.mask_filters[0].shape[0] or img.shape[0]!=self.mask_filters[0].shape[1]):
                    mf = self.resize_filter(mf, img.shape[1],img.shape[0])
                    processed_mask = self.resize_filter(processed_mask, img.shape[1],img.shape[0])
            
                apply_mask = mf & ~processed_mask
                transformed_image[apply_mask] = func(img[:,:,0], img[:,:,1], img[:,:,2])[apply_mask]
                processed_mask |= apply_mask

            # Apply default function to remaining pixels
            remaining_mask = ~processed_mask
            transformed_image[remaining_mask] = self.default_color_function(img[:,:,0], img[:,:,1], img[:,:,2])[remaining_mask]
        except:
            print("Error the mask is not compatible with the Main window. Make sure the Main window borders are inside the screen")
        return transformed_image

    
    #Resize a boolean mask to match a new image shape
    def resize_filter(self, mask, img_width, img_hight):
                
        # Convert to float for interpolation
        mask_float = mask.astype(np.float32)
        
        # Resize using nearest or bilinear interpolation
        resized = cv2.resize(mask_float, (img_width, img_hight), interpolation=cv2.INTER_LINEAR)
        
        # Convert back to boolean
        return resized > 0.5
    
    #change the color of the pixels in the image using a mask>
        
    def apply_sliders_values_to_image(self, img):
               
        image_red = img[:,:,0]
        image_green = img[:,:,1]
        image_blue = img[:,:,2]

        if(self.SLIDERS_VALUES['r']!=1):           
            image_red = image_red*self.SLIDERS_VALUES['r']
        if(self.SLIDERS_VALUES['g']!=1):
                image_green = image_green*self.SLIDERS_VALUES['g']
        if(self.SLIDERS_VALUES['b']!=1):
            image_blue = image_blue*self.SLIDERS_VALUES['b']

        transformed_image = np.dstack((image_red, image_green, image_blue))
        return transformed_image           
    
    """after you make sure that ` def apply_swop_pixel_areas` is working without issues you can delete this code
    def apply_swop_pixel_areas_v1(self, img):
        
        if(self.swap_pixel_areas is None):
            return img
        
        for rectangle_pair in self.swap_pixel_areas:
            
            first_rectangle = rectangle_pair[0]
            second_rectangle = rectangle_pair[1]

            frc = first_rectangle[0]#first rectangle coordinates (x, y, size) -> example (150, 340, 50)
            frr = first_rectangle[1]#first rectangle rgb values (use_r, use_g, use_b) -> example (1,1,0) 
            fr_rgb_formula_id = first_rectangle[2,0]#`first_rectangle[2]` has 3 values where the first value is the rgb formula id while the other values are dummy (not usable) 0 values whose purpose is to make the size of rgb formulas index compatible with the coordinates and the rgb values
            
            src = second_rectangle[0]#second rectangle coordinates (x, y, size) -> example (100, 50, 320)
            srr = second_rectangle[1]#second rectangle rgb values (use_r, use_g, use_b) -> example (0,0,0)
            sr_rgb_formula_id = second_rectangle[2,0]#`first_rectangle[2]` has 3 values where the first value is the rgb formula id while the other values are dummy (not usable) 0 values whose purpose is to make the size of rgb formulas index compatible with the coordinates and the rgb values

            #if the any of the recntangle pairs is outside the borders of the image don't apply the swap of areas
            if( (frc[0]+frc[2]>img.shape[0] or frc[1]+frc[2]>img.shape[1]) or
                (src[0]+src[2]>img.shape[0] or src[1]+src[2]>img.shape[1])
                ):
                continue
                #return img

            #<swaps the chosen rgb channels from the 2 areas (in this case rectangles)
            img_first_rectangle = np.array(img[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2]), srr==1])
            
            img[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2]), frr==1] = img[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2]), frr==1]

            img[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2]), srr==1] = img_first_rectangle
            #swaps the chosen rgb channels from the 2 areas (in this case rectangles)>

            #<apply rgb functions to swap areas
            if(fr_rgb_formula_id != 0):
                r_img_first_rectangle = img[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2]), 0]
                g_img_first_rectangle = img[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2]), 1]
                b_img_first_rectangle = img[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2]), 2]
                img[frc[0]:(frc[0]+frc[2]), frc[1]:(frc[1]+frc[2])] = self.swap_pixel_areas_rgb_formulas[fr_rgb_formula_id](r_img_first_rectangle, g_img_first_rectangle, b_img_first_rectangle)
            
            if(sr_rgb_formula_id != 0):
                r_img_second_rectangle =  img[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2]), 0]
                g_img_second_rectangle = img[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2]), 1]
                b_img_second_rectangle = img[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2]), 2]
                img[src[0]:(src[0]+src[2]), src[1]:(src[1]+src[2])] = self.swap_pixel_areas_rgb_formulas[sr_rgb_formula_id](r_img_second_rectangle, g_img_second_rectangle, b_img_second_rectangle)
            #apply rgb functions to swap areas>
        
        return img
    """
    
    def apply_pixel_areas_manipulator(self, img):

        if(self.pixel_areas_manipulator is None):
            return img
        
        transformed_image = self.pixel_areas_manipulator.transform_image(img=img)
        return transformed_image
    
    def set_pixel_areas_manipulator(self, pixel_areas_manipulator:Pixel_areas_manipulator):

        if(pixel_areas_manipulator is not None):
            self.pixel_areas_manipulator = pixel_areas_manipulator
    
    def remove_pixel_areas_manipulator(self):
        self.pixel_areas_manipulator = None
    
    """
    def apply_swop_pixel_areas(self, img):
        
        if(self.swap_pixel_areas is None):
            return img
        
        for rectangle_pair in self.swap_pixel_areas:
            
            first_rectangle = rectangle_pair[0]
            second_rectangle = rectangle_pair[1]

            frc = first_rectangle[0]#first rectangle coordinates (x, y, size) -> example (150, 340, 50)
            frr = first_rectangle[1]#first rectangle rgb values (use_r, use_g, use_b) -> example (1,1,0) 
            fr_rgb_formula_id = first_rectangle[2,0]#`first_rectangle[2]` has 3 values where the first value is the rgb formula id while the other values are dummy (not usable) 0 values whose purpose is to make the size of rgb formulas index compatible with the coordinates and the rgb values
            
            src = second_rectangle[0]#second rectangle coordinates (x, y, size) -> example (100, 50, 320)
            srr = second_rectangle[1]#second rectangle rgb values (use_r, use_g, use_b) -> example (0,0,0)
            sr_rgb_formula_id = second_rectangle[2,0]#`first_rectangle[2]` has 3 values where the first value is the rgb formula id while the other values are dummy (not usable) 0 values whose purpose is to make the size of rgb formulas index compatible with the coordinates and the rgb values
            
            

            #img coordinates
            img_height = img.shape[0]
            img_width = img.shape[1]

            #<first rectangle coordinates
            fr_x_left = frc[0]
            fr_x_left = fr_x_left if fr_x_left > 0 else 0
            
            fr_x_right = frc[0] + frc[2]
            fr_x_right = fr_x_right if fr_x_right < img_width else img_width
            
            fr_y_up = frc[1]
            fr_y_up = fr_y_up if fr_y_up > 0 else 0
            
            fr_y_down = frc[1] + frc[2]
            fr_y_down = fr_y_down if fr_y_down < img_height else img_height
            #first rectangle coordinates>
            
            #<second rectangle coordinates
            sr_x_left = src[0]
            sr_x_left = sr_x_left if sr_x_left > 0 else 0
            
            sr_x_right = src[0] + src[2]
            sr_x_right = sr_x_right if sr_x_right < img_width else img_width
            
            sr_y_up = src[1]
            sr_y_up = sr_y_up if sr_y_up > 0 else 0
            
            sr_y_down = src[1] + frc[2]
            sr_y_down = sr_y_down if sr_y_down < img_height else img_height
            #second rectangle coordinates>

            if((fr_x_left > img_width or fr_y_up > img_height) or 
               (sr_x_left > img_width or sr_y_up > img_height)):
                continue

            #<make sure the rectangles have the same size
            
            fr_width = fr_x_right - fr_x_left
            fr_height = fr_y_down - fr_y_up

            sr_width = sr_x_right - sr_x_left
            sr_height = sr_y_down - sr_y_up

            #make the width of the rectangles be the same
            if(fr_width != sr_width):    
                width_difference = fr_width - sr_width
                if(width_difference > 0):
                    fr_x_right -= width_difference
                else:
                    sr_x_right += width_difference
            
            #make the height of the rectangles be the same
            if(fr_height != sr_height):   
                height_difference = fr_height - sr_height
                if(height_difference > 0):
                    fr_y_down -= height_difference
                else:
                    sr_y_down += height_difference

            #make sure the rectangles have the same size>

            #swaps the chosen rgb channels from the 2 areas (in this case rectangles)
            if((frr==1).any() or (srr==1).any()):
                img_first_rectangle = np.array(img[fr_y_up:fr_y_down, fr_x_left:fr_x_right, srr==1 ])
                img[fr_y_up:fr_y_down, fr_x_left:fr_x_right, frr==1 ] = img[sr_y_up:sr_y_down, sr_x_left:sr_x_right, frr==1]
                img[sr_y_up:sr_y_down, sr_x_left:sr_x_right, srr==1] = img_first_rectangle
            
            if((frr==2).any() or (srr==2).any()):
                img_first_rectangle = np.array(img[fr_y_up:fr_y_down, fr_x_left:fr_x_right, srr==2 ])
                img[fr_y_up:fr_y_down, fr_x_left:fr_x_right, frr==2 ] += img[sr_y_up:sr_y_down, sr_x_left:sr_x_right, frr==2]
                img[sr_y_up:sr_y_down, sr_x_left:sr_x_right, srr==2] += img_first_rectangle


            #<apply rgb functions to swap areas
            if(fr_rgb_formula_id != 0):
                r_img_first_rectangle = img[fr_y_up:fr_y_down, fr_x_left:fr_x_right, 0]
                g_img_first_rectangle = img[fr_y_up:fr_y_down, fr_x_left:fr_x_right, 1]
                b_img_first_rectangle = img[fr_y_up:fr_y_down, fr_x_left:fr_x_right, 2]
                img[fr_y_up:fr_y_down, fr_x_left:fr_x_right] = self.swap_pixel_areas_rgb_formulas[fr_rgb_formula_id](r_img_first_rectangle, g_img_first_rectangle, b_img_first_rectangle)

            if(sr_rgb_formula_id != 0):
                r_img_second_rectangle = img[sr_y_up:sr_y_down, sr_x_left:sr_x_right, 0]
                g_img_second_rectangle = img[sr_y_up:sr_y_down, sr_x_left:sr_x_right, 1]
                b_img_second_rectangle = img[sr_y_up:sr_y_down, sr_x_left:sr_x_right, 2]
                img[sr_y_up:sr_y_down, sr_x_left:sr_x_right] = self.swap_pixel_areas_rgb_formulas[sr_rgb_formula_id](r_img_second_rectangle, g_img_second_rectangle, b_img_second_rectangle)
            #apply rgb functions to swap areas>
        
        return img

    # each element in `swap_pixel_areas` must be a rectangle pair (a numpy array of two rectangles),
    # a rectangle looks like this f"[ [{x}, {y}, {size}], [{int(use_red)}, {int(use_green)}, {int(use_blue)}], [{int(rgb_function_id)}] ]" (all elements in the rectangle must be integers) (`y` and `x` are the coordinates of the top left corner of the rectangle);
    #`swap_pixel_areas_rgb_formulas` is a dictionary which has numbers (RGB fomulas ids) for keys and RGB fommulas (represented as lamda functions) for values,
    # the default key is `0` while the default value is = `eval(f"lambda r,g,b: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)")`)
    def set_swap_pixel_areas(self, swap_pixel_areas : np.array, swap_pixel_areas_rgb_formulas:dict):
        
        if(swap_pixel_areas is None or swap_pixel_areas_rgb_formulas is None):
            self.swap_pixel_areas = None
            self.swap_pixel_areas_rgb_formulas = None
        
        elif(isinstance(swap_pixel_areas, np.ndarray) and len(swap_pixel_areas.shape) == 4 and swap_pixel_areas.shape[1:] == (2,3,3)):
            self.swap_pixel_areas = swap_pixel_areas
            self.swap_pixel_areas_rgb_formulas = swap_pixel_areas_rgb_formulas

            print("isinstance(swop_pixel_areas, np.ndarray)", isinstance(swap_pixel_areas, np.ndarray))
            print("len(swop_pixel_areas.shape) == 4", len(swap_pixel_areas.shape) == 4)
            print("swop_pixel_areas.shape[1:] == (2,2,3)", swap_pixel_areas.shape[1:] == (2,3,3))

    def apply_mask_settings(self, mask_filters, color_functions, default_color_function):#`color_functions[0]` can has this value `eval(f"lambda r,g,b: np.stack([{self.red_func},{self.green_func},{self.blue_func}], axis=-1)")`
            
        self.color_functions = None if(color_functions==None or len(color_functions)==0) else color_functions
        self.default_color_function = self.default_color_function if(default_color_function==None) else default_color_function
        self.mask_filters = None if(mask_filters==None or len(mask_filters)==0) else mask_filters

    """

    def remove_mask(self):

        self.color_functions = None
        self.mask_filters = None                            

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self._pixmap is None:
            # blank background
            painter.fillRect(self.rect(), QtCore.Qt.black)
            return
        
        # Scale pixmap to widget size while preserving aspect ratio (or not — here we fill entire widget)
        #scaled = self._pixmap.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, self._pixmap)#scaled)
        painter.end()


#<Functions for performing convolution on the image
    def apply_convolution_to_image(self, img: np.ndarray):
        
        if (self.rgb_kernels == None):
            return img

        rgb_kernels = self.rgb_kernels

        red_convolution = self.apply_convolution_to_color_channel(stride = rgb_kernels.r_kernel.stride, holes_count =rgb_kernels.r_kernel.holes_count, kernel_values = rgb_kernels.r_kernel.kernel_values, channel_values = img[:,:,0])
        green_convolution = self.apply_convolution_to_color_channel(stride = rgb_kernels.g_kernel.stride, holes_count = rgb_kernels.g_kernel.holes_count, kernel_values = rgb_kernels.g_kernel.kernel_values, channel_values = img[:,:,1])
        blue_convolution = self.apply_convolution_to_color_channel(stride = rgb_kernels.b_kernel.stride, holes_count = rgb_kernels.b_kernel.holes_count, kernel_values = rgb_kernels.b_kernel.kernel_values, channel_values = img[:,:,2])
        
        convolved_image = np.dstack((red_convolution, green_convolution, blue_convolution))
        return convolved_image

    def apply_convolution_to_color_channel(self, stride: int, holes_count: int, kernel_values: np.ndarray, channel_values: np.ndarray):
        """
        Applies a convolutional filter to a single color channel with zero-padding to keep output the same shape as input.

        Parameters:
            stride (int): Stride of the filter.
            holes_count (int): Number of holes (dilation factor - 1).
            kernel_values (list): a numpy array of float values representing the filter.
            channel_values (np.ndarray): Input channel values, shape (H, W).

        Returns:
            np.ndarray: The resulting convolved channel, same shape as input.
        """
        if(kernel_values.shape[0]==0 or kernel_values.shape[1]==0):#if the kernel has 0 columns or 0 rows - return the input channel values unchanged
            return channel_values

        img_height, img_width = channel_values.shape
        kernel_height, kernel_width = kernel_values.shape

        dilation = holes_count + 1
        eff_height = (kernel_height - 1) * dilation + 1
        eff_width = (kernel_width - 1) * dilation + 1

        # Calculate necessary padding to maintain same output size
        pad_y = ((img_height - 1) * stride + eff_height - img_height) // 2
        pad_x = ((img_width - 1) * stride + eff_width - img_width) // 2

        # Apply zero-padding
        padded = np.pad(channel_values, ((pad_y, pad_y), (pad_x, pad_x)), mode='constant', constant_values=0)

        # Output dimensions
        out_height = img_height
        out_width = img_width
        output = np.zeros((out_height, out_width))

        # Perform convolution
        for y in range(out_height):
            for x in range(out_width):
                region = padded[
                    y * stride : y * stride + eff_height : dilation,
                    x * stride : x * stride + eff_width : dilation
                ]
                # Handle edges where the region may be smaller than the kernel
                if region.shape != kernel_values.shape:
                    # Pad the region to match kernel size
                    region_padded = np.zeros_like(kernel_values)
                    region_padded[:region.shape[0], :region.shape[1]] = region
                    region = region_padded

                output[y, x] = np.sum(region * kernel_values)

        return output

    #the parameters must be dictionaries where the key (must be type "str") represents the color channel while the value (must be type "np.array") represents the kernels values
    def create_rgb_kernels(self, rgb_kernels_values: dict, rgb_kernels_strides: dict, rgb_kernels_holes_count: dict):        
        r_kernel = Kernel(stride = rgb_kernels_strides["r"], holes_count = rgb_kernels_holes_count["r"], kernel_values = rgb_kernels_values["r"])
        g_kernel = Kernel(stride = rgb_kernels_strides["g"], holes_count = rgb_kernels_holes_count["g"], kernel_values = rgb_kernels_values["g"])
        b_kernel = Kernel(stride = rgb_kernels_strides["b"], holes_count = rgb_kernels_holes_count["b"], kernel_values = rgb_kernels_values["b"])

        self.rgb_kernels = RGB_Kernels(r_kernel, g_kernel, b_kernel)

    def remove_rgb_kernels(self):
        self.rgb_kernels = None

#Functions for performing convolution on the image>

#Functions for changing the RGB values of the area under the window>

    #This function is called by the Settings window when the user clicks the button for applying the changes
    def apply_settings(self, capture_time: float, slider_min_value: float, slider_max_value: float, RGB_use_doubles:bool, color_functions_execution_order: list):
        
        capture_time = int(capture_time)
        slider_min_value = int(slider_min_value)
        slider_max_value = int(slider_max_value)

        self.timer.start(capture_time)

        self.slider_red.setMinimum(slider_min_value)
        self.slider_red.setMaximum(slider_max_value)

        self.slider_green.setMinimum(slider_min_value)
        self.slider_green.setMaximum(slider_max_value)

        self.slider_blue.setMinimum(slider_min_value)
        self.slider_blue.setMaximum(slider_max_value)

        self.RGB_use_doubles = RGB_use_doubles

        self.color_methods_execution_order = color_functions_execution_order