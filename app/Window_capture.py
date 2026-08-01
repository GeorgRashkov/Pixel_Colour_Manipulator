import ctypes
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QSlider
import win32con, win32gui
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QCheckBox, QLabel
from PyQt5.QtCore import Qt
import RGB_formula_elements
from Z_Pixel_areas_manipulator import Pixel_areas_manipulator
from Z_RGB_formulas_mask import RGB_formulas_mask
from PyQt5.QtWidgets import QApplication
from dxcam import DXCamera

from Dynamic_variable import Dynamic_variable

from Convolutional_kernels_manipulator import Convolutional_kernels_manipulator

from DXCamera_Singleton import DXCamera_Singleton

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
    
   
    def __init__(self):
        super().__init__()

        

        self.transformed_image = None
        
        self.convolutional_kernels_manipulator:Convolutional_kernels_manipulator = Convolutional_kernels_manipulator()
        self.screen_width = QApplication.primaryScreen().geometry().width()
        self.screen_height = QApplication.primaryScreen().geometry().height()
        
        self.dynamic_variables:list[Dynamic_variable] = []
        self.dynamic_variables_values:np.ndarray[np.uint8] = np.array([0], dtype=np.uint8)
        self.dynamic_variables_float_values:list[float] = [0]

        self.default_color_function = lambda r,g,b, areas_count=1, v=np.array([0], dtype=np.uint8) : np.stack([r, g, b], axis=-1)
        
        

        self.rgb_mask:RGB_formulas_mask = None

        self.pixel_areas_manipulator:Pixel_areas_manipulator = None
        
        

        self.RGB_use_doubles = False

        self.color_methods_execution_order = [1, 2, 3, 4, 5] #the elements in "self.color_methods_execution_order" determine the execution order of the methods in "self.color_methods"
       
        self.color_methods = [self.apply_default_color_function, self.apply_rgb_mask, self.apply_convolution_to_image, self.apply_sliders_values_to_image, self.apply_pixel_areas_manipulator] #all the methods must: take as input an image (as type "np.ndarray"); make transformations to the image; return the tranformed image (as type "np.ndarray")

        self.setWindowTitle("Colour Changer")
        self.setMinimumSize(200, 30)
        self.resize(400, 400)
             
        self.camera:DXCamera = DXCamera_Singleton().get_DXCamera()

        # Keep a pixmap to paint
        self._pixmap = None
        
        # Timer to refresh periodically the output of the window
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(100)# 100 means 0.1 second #start(UPDATE_INTERVAL_MS)

        self._button_click_trough = self.initialize_special_button()
        self._button_click_trough.clicked.connect(self.click_through_on_off)

        self._button_pseudo_maximize = self.initialize_special_button()
        self._button_pseudo_maximize.clicked.connect(self.pseudo_maximize)

        self.last_geometry_before_pseudo_maximize = self.geometry()
        self.is_pseudo_maximized = False
        self.is_pseudo_maximized_cover_task = False
                

        self.click_through = True
        self.click_through_on_off()       

        
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.button_capture_now = QPushButton('capture', QtWidgets.QWidget(self))
        self.button_capture_now.clicked.connect(self.update_capture)

        self.label_stack_output = QLabel("stack output")
        self.label_stack_output.setStyleSheet("background-color: black; color: white;")
        self.checkBox_stack_output = QCheckBox()
        self.label_stack_output.setBuddy(self.checkBox_stack_output)

        self.label_auto_capture = QLabel("auto capture")
        self.label_auto_capture.setStyleSheet("background-color: black; color: white;")
        self.checkBox_auto_capture = QCheckBox()
        self.label_auto_capture.setBuddy(self.checkBox_auto_capture)

        self.button_open_settings = QPushButton('settings',  QtWidgets.QWidget(self))
        self.button_open_drawMask = QPushButton('draw mask',  QtWidgets.QWidget(self))
        self.button_open_captureMask = QPushButton('capture mask',  QtWidgets.QWidget(self))
        self.button_open_convolutionalFilter = QPushButton('convolution',  QtWidgets.QWidget(self))
        self.button_open_swapAreas = QPushButton('swap areas',  QtWidgets.QWidget(self))

        self.button_open_drawFormula = QPushButton('draw formula',  QtWidgets.QWidget(self))
        self.button_open_dynamic_variables = QPushButton('dynamic variables',  QtWidgets.QWidget(self))
        self.button_open_images = QPushButton('images',  QtWidgets.QWidget(self))

        #<color sliders
               

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

        self.button4_showHide_widgets = QPushButton('', QtWidgets.QWidget(self))
        self.button4_showHide_widgets.clicked.connect(lambda: self.hide_widgets(4))
        self.button4_showHide_widgets.setMaximumSize(10,10)

        self.button_showHide_all_widgets = QPushButton('', QtWidgets.QWidget(self))
        self.button_showHide_all_widgets.clicked.connect(self.show_or_hide_all_widgets)
        self.button_showHide_all_widgets.setMaximumSize(10,10)
        self.are_widgets_shown = True

        #buttons for showing and hiding widgets on the rows of the buttons>
        

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0,0,0,0)
       
        h_layout = QHBoxLayout()        
        h_layout.addWidget(self.button0_showHide_widgets)
        h_layout.addWidget(self.label_auto_capture)
        h_layout.addWidget(self.checkBox_auto_capture)
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
        h_layout.addWidget(self.button_open_swapAreas)
        h_layout.setAlignment(Qt.AlignLeft)
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button2_showHide_widgets)
        h_layout.addWidget(self.button_open_drawFormula)
        h_layout.addWidget(self.button_open_dynamic_variables)
        h_layout.addWidget(self.button_open_images)
        h_layout.setAlignment(Qt.AlignLeft)
        self.v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()        
        h_layout.addWidget(self.button3_showHide_widgets)
        h_layout.addWidget(self.slider_red)
        h_layout.addWidget(self.slider_green)
        h_layout.addWidget(self.slider_blue)
        self.v_layout.addLayout(h_layout)
        
        self.rgb_elements = RGB_formula_elements.RGB_formula_elements()
        h_layout = QHBoxLayout()
        
        h_layout.addWidget(self.button4_showHide_widgets)
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
        if(self.checkBox_auto_capture.isChecked() == True):
            self.update_capture()
        
    """
    def get_transformed_img(self) -> np:
        self.update_capture()
        return self.transformed_image
    """
    def get_transformed_img(self) -> np.ndarray[np.uint8]:

        img = np.zeros(shape=[1,1,3], dtype=np.uint8)
        if(self.transformed_image is not None):
            img = self.transformed_image.copy()
        return img
        
    """
    #this function is causing issues !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def get_original_img(self) -> np.ndarray[np.uint8]:

        img = np.zeros(shape=[1,1,3], dtype=np.uint8)
        x, y, w, h = self.get_window_coordinates()
        if(w > 0 and h > 0):
            # Use dxcam to capture pixel values under the window
            img = self.camera.grab(region=(x, y, x + w, y + h))#The returned frame will be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB])
            img = np.ascontiguousarray(img) # copy DXCamera view into a contiguous NumPy array
        return img
    """

    def get_original_img(self) -> np.ndarray[np.uint8]:

        img = np.zeros(shape=[1,1,3], dtype=np.uint8)
        x, y, w, h = self.get_window_coordinates()
        if(w > 0 and h > 0):

            should_enable_auto_capture = False
            if(self.checkBox_auto_capture.isChecked() == True): 
                should_enable_auto_capture = True
                self.checkBox_auto_capture.setChecked(False)
            
            img = np.array([1])
            while(img is None or len(img.shape)!=3):

                # Use dxcam to capture pixel values under the window
                img = self.camera.grab(region=(x, y, x + w, y + h))#The returned frame will be a "numpy.ndarray" in the shape of (Height, Width, 3[RGB]); warning: the result might sometimes be a "numpy.ndarray" with shape (1,) containing one `None` object (if the dxcam version get's updated the result might be `None`)
                img = np.ascontiguousarray(img) # copy DXCamera view into a contiguous NumPy array
                    
            if(should_enable_auto_capture == True):
                self.checkBox_auto_capture.setChecked(True)

        return img
   

    def slider_value_changed(self, slider_value, slider_id):
        self.SLIDERS_VALUES[slider_id] = round(slider_value*0.01,2)
    
    def show_or_hide_all_widgets(self):
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


    #creates a button which will remain clickable even when the window is click-trough
    #the button will be shown only when the window (not including the header) is pressed twice
    def initialize_special_button(self) -> QPushButton:
        
        overlay = QtWidgets.QWidget(self)  # top-level window
        overlay.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        overlay.setAttribute(Qt.WA_TranslucentBackground)
        
        special_button = QPushButton('', overlay)
        special_button.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)

        hwnd = int(special_button.winId())
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                              0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
        
        return special_button
   
    #when the window (not including the header) is pressed twice the following function will: 
    # set on the "click-through the window" ability; show a button which will be placed in the heather of the window  
    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        
        self.click_through_on_off()

        self.are_widgets_shown = True
        self.show_or_hide_all_widgets()

       
        self.place_special_buttons()
    
    def place_special_buttons(self):

        geo = self.geometry()# Get window geometry
        x, y, x2, y2 = max(geo.x(),0), max(geo.y(),0), min(geo.x()+geo.width(), self.screen_width), min(geo.y()+geo.height(), self.screen_height)

        btn_size = 10

        #when the button is pressed the window will become clickable again
        self._button_click_trough.move(x, y)
        self._button_click_trough.setMaximumSize(btn_size, btn_size)
        self._button_click_trough.show()

        #when the button is pressed the window will cover the entire screen without the taskbar
        self._button_pseudo_maximize.move(x2-btn_size, y)
        self._button_pseudo_maximize.setMaximumSize(btn_size,btn_size)
        self._button_pseudo_maximize.show()

       
       


    def click_through_on_off(self):
        
        self._button_click_trough.hide()
        self._button_pseudo_maximize.hide()
        
        hwnd = int(self.winId())
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)

        if self.click_through == True:

            self.click_through = False
            # Removes WS_EX_TRANSPARENT while keeping WS_EX_LAYERED
            style &= ~win32con.WS_EX_TRANSPARENT

            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
            # Makes sure the window stays topmost in z-order (change to NOTOPMOST if desired)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                              0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)

        else:
            
            self.click_through = True
            # Add click-through
            style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT| win32con.WS_EX_TOPMOST
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

             # Makes sure the window stays topmost in z-order (change to NOTOPMOST if desired)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                              0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
            

    def pseudo_maximize(self):
        
        if(self.is_pseudo_maximized == True):
            self.setWindowState(Qt.WindowNoState)
            self.setGeometry(self.last_geometry_before_pseudo_maximize)
            self.is_pseudo_maximized = False
            
                
        else:
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()  #get's the screen size without the taskbar            
            
            self.last_geometry_before_pseudo_maximize = self.geometry()
            self.setWindowState(Qt.WindowNoState)
            self.setGeometry(screen_geometry)
            self.is_pseudo_maximized = True
        
        self.place_special_buttons()
    
        



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
            
       
        if(x+w > self.screen_width):
            w = self.screen_width-x
        if(y+h > self.screen_height):
            h=self.screen_height - y
        
        return x, y, w, h
    

#<Functions for changing the RGB values of the area under the window
    
    def update_capture(self):
            
          

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
                
                try:
                    self.transformed_image = self.transform_image(img)
                except ZeroDivisionError:
                    print("division by zero detected in image transform formula")
                    self.checkBox_auto_capture.setChecked(False)#disable autocapture when division by zero occurs
                    self.transformed_image = np.zeros(shape=img.shape, dtype=np.uint8)#make sure the tranformed image is not `None` when division by zero occurs
               
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
    
    def transform_image(self, img:np.ndarray):

        self.update_dynamic_variables_values()

        #applies all methods that change that change the RGB channel values
        for method_index in self.color_methods_execution_order:
            img = self.color_methods[method_index - 1](img)
        
        if(self.RGB_use_doubles==False):
            img = img.astype(np.uint8)

        self.update_dynamic_variables_frequences()
        
        return img

    

    def apply_sliders_values_to_image(self, img:np.ndarray):
               
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
    
    
    def apply_rgb_mask(self, img:np.ndarray):

        if(self.rgb_mask is None):
            return img
        
        transformed_image = self.rgb_mask.apply_mask_to_image(img=img, v=self.dynamic_variables_values)
        return transformed_image
    
    def set_rgb_mask(self, rgb_mask:RGB_formulas_mask):

        if(rgb_mask is not None):
            self.rgb_mask = rgb_mask
    
    def remove_rgb_mask(self):
        self.rgb_mask = None


    def apply_default_color_function(self, img:np.ndarray):#img must be a "numpy.ndarray" in the shape of (Height, Width, 3) Where 3 is for the RGB color channels
        transformed_image = self.default_color_function(img[:,:,0], img[:,:,1], img[:,:,2], v=self.dynamic_variables_values)
        return transformed_image

    def apply_pixel_areas_manipulator(self, img:np.ndarray):

        if(self.pixel_areas_manipulator is None):
            return img
        
        transformed_image = self.pixel_areas_manipulator.transform_image(img=img, v=self.dynamic_variables_values)
        return transformed_image
    

    #the input must be a pixel areas manipulator or None
    def set_pixel_areas_manipulator(self, pixel_areas_manipulator:Pixel_areas_manipulator):
        self.pixel_areas_manipulator = pixel_areas_manipulator
    
   


    def set_dynamic_variables(self, dynamic_variables:list[Dynamic_variable]):
        
        if(len(dynamic_variables) == 0):
            self.dynamic_variables = []
            self.dynamic_variables_values = np.array([0], dtype=np.uint8)
            self.dynamic_variables_float_values = [0]

        else:
            self.dynamic_variables = dynamic_variables
            updated_values_for_dynamic_variables = []
            updated_float_values_for_dynamic_variables = []

            for dynamic_variable in dynamic_variables:
                
                dynamic_variable_current_value = dynamic_variable.get_current_value()
                updated_float_values_for_dynamic_variables.append(dynamic_variable_current_value)
                
                dynamic_variable_current_value = dynamic_variable_current_value%256
                updated_values_for_dynamic_variables.append(np.uint8(dynamic_variable_current_value))
            
            self.dynamic_variables_values = np.array(updated_values_for_dynamic_variables, dtype=np.uint8)
            self.dynamic_variables_float_values = updated_float_values_for_dynamic_variables

    
    def update_dynamic_variables_values(self):

        updated_values_for_dynamic_variables = []
        updated_float_values_for_dynamic_variables = []

        for dynamic_variable in self.dynamic_variables:
            
            dynamic_variable_updated_value = dynamic_variable.get_value(v=self.dynamic_variables_float_values)
            updated_float_values_for_dynamic_variables.append(dynamic_variable_updated_value)

            dynamic_variable_updated_value = dynamic_variable_updated_value%256
            updated_values_for_dynamic_variables.append(np.uint8(dynamic_variable_updated_value))
        
        if(len(updated_values_for_dynamic_variables)>0):
            self.dynamic_variables_values = np.array(updated_values_for_dynamic_variables, dtype=np.uint8)
            self.dynamic_variables_float_values = updated_float_values_for_dynamic_variables
        else:
            self.dynamic_variables_values = np.array([0], dtype=np.uint8)
            self.dynamic_variables_float_values = [0]

    def update_dynamic_variables_frequences(self):

        for dynamic_variable in self.dynamic_variables:
            dynamic_variable.update_frequency()


    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self._pixmap is None:
            # blank background
            painter.fillRect(self.rect(), QtCore.Qt.black)
            return
        
        # Scale pixmap to widget size while preserving aspect ratio (or not — here we fill entire widget)
        #scaled = self._pixmap.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        x = 0
        if(self.geometry().x() < 0):
            x = (-1)*self.geometry().x()
        y = 0
        if(self.geometry().y() < 0):
            y = (-1)*self.geometry().y()
        painter.drawPixmap(x, y, self._pixmap)
        painter.end()


#<Functions for performing convolution on the image
   
    def apply_convolution_to_image(self, img: np.ndarray):
        img = self.convolutional_kernels_manipulator.transform_image_0(img=img)
        return img

    def set_convolutional_kernels(self, cks_manipulator:Convolutional_kernels_manipulator):
        self.convolutional_kernels_manipulator = cks_manipulator

    def remove_convolutional_kernels(self):
        self.convolutional_kernels_manipulator = Convolutional_kernels_manipulator()
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
    