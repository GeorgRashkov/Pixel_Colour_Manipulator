from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QCheckBox
)
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QKeySequence
from PyQt5.QtGui import QIntValidator

from Z_RGB_formula_checker import RGB_formula_validators
import RGB_formula_elements

class FormWindow_SwapPixelValues(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Draw mask")
        self.setMinimumSize(100, 100)
        self.resize(800, 500)             
        
        self.text_area_swap_pixel_areas = QTextEdit() #Text_area(allowed_symbols_regex="[0-9\\[\\], ]")
        self.text_area_rgb_formulas = Text_area(allowed_symbols_regex = RGB_formula_validators.rgb_formula_valid_symbols_for_swap_areas_regex)

        positive_int_validator = QIntValidator(0, 999_999)
        int_validator = QIntValidator(-999_999, 999_999)
        

        #<settings for pixel areas
        self.label_movable_areas = QLabel("movable areas")
        self.checkBox_movable_areas = QCheckBox()
        self.label_movable_areas.setBuddy(self.checkBox_movable_areas)
        #settings for pixel areas>

        #<settings for output image versions        
        
        self.label_image_version_start_index = QLabel("image version start index")
        self.textBox_image_version_start_index = QLineEdit()
        self.textBox_image_version_start_index.setValidator(int_validator)
        self.textBox_image_version_start_index.setMaxLength(3)
        self.label_image_version_start_index.setBuddy(self.textBox_image_version_start_index)

        self.label_image_version_increment = QLabel("image version increment")
        self.textBox_image_version_increment = QLineEdit()
        self.textBox_image_version_increment.setValidator(int_validator)
        self.textBox_image_version_increment.setMaxLength(3)
        self.label_image_version_increment.setBuddy(self.textBox_image_version_increment)

        self.label_image_version_swap_frequency = QLabel("image version swap frequency")
        self.textBox_image_version_swap_frequency = QLineEdit()
        self.textBox_image_version_swap_frequency.setValidator(positive_int_validator)
        self.textBox_image_version_swap_frequency.setMaxLength(3)
        self.label_image_version_swap_frequency.setBuddy(self.textBox_image_version_swap_frequency)
        
        #settings for output image versions>

        #<elements - size arguments for the brush in the canvas window

        #<brush width
        self.label_brush_width = QLabel("brush width| ")
        
        self.label_brush_width_min_value = QLabel("min")
        self.textBox_brush_width_min_value = QLineEdit("1")
        self.textBox_brush_width_min_value.setValidator(positive_int_validator)
        self.textBox_brush_width_min_value.setMaxLength(3)

        self.lable_brush_width_max_value = QLabel("max")
        self.textBox_brush_width_max_value = QLineEdit("999")
        self.textBox_brush_width_max_value.setMaxLength(3)
        self.textBox_brush_width_max_value.setValidator(positive_int_validator)

        self.lable_brush_width_delta = QLabel("increment")
        self.textBox_brush_width_delta = QLineEdit("50")
        self.textBox_brush_width_delta.setMaxLength(3)
        self.textBox_brush_width_delta.setValidator(positive_int_validator)
       

        self.button_apply_brush_width_changes = QPushButton("OK")
        #brush width>

        #<brush height
        self.label_brush_height = QLabel("brush height| ")
        
        self.label_brush_height_min_value = QLabel("min")
        self.textBox_brush_height_min_value = QLineEdit("1")
        self.textBox_brush_height_min_value.setValidator(positive_int_validator)
        self.textBox_brush_height_min_value.setMaxLength(3)
      

        self.lable_brush_height_max_value = QLabel("max")
        self.textBox_brush_height_max_value = QLineEdit("999")
        self.textBox_brush_height_max_value.setMaxLength(3)
        self.textBox_brush_height_max_value.setValidator(positive_int_validator)

        self.lable_brush_height_delta = QLabel("increment")
        self.textBox_brush_height_delta = QLineEdit("50")
        self.textBox_brush_height_delta.setMaxLength(3)
        self.textBox_brush_height_delta.setValidator(positive_int_validator)
       

        self.button_apply_brush_height_changes = QPushButton("OK")
        #brush height>
       
        #<brush size
        self.label_brush_size_set = QLabel("Set brush size| ")
        
        self.label_brush_width_set = QLabel("width")
        self.textBox_brush_width_set = QLineEdit("100")
        self.textBox_brush_width_set.setValidator(positive_int_validator)
        self.textBox_brush_width_set.setMaxLength(3)

        self.label_brush_height_set = QLabel("height")
        self.textBox_brush_height_set = QLineEdit("100")
        self.textBox_brush_height_set.setMaxLength(3)
        self.textBox_brush_height_set.setValidator(positive_int_validator)

        self.button_set_brush_size = QPushButton("OK")

        #brush size>

        #elements - size arguments for the brush in the canvas window>



        #<rgb formula elements
        self.rgb_elements = RGB_formula_elements.RGB_formula_elements(use_areas=True)
        self.rgb_labels_text = ["red channel","green channel","blue channel"]
        self.label_rgb_formula = QLabel("RGB formulas| ")
        self.button_add_rgb_formula = QPushButton("Add")


        rgb_formulas_layout = QHBoxLayout()
        
        rgb_formulas_layout.addWidget(self.label_rgb_formula)        

        for channel in self.rgb_elements.channels:

            rgb_formulas_layout.addWidget(QLabel(channel))
            rgb_formulas_layout.addWidget(self.rgb_elements.text_boxes[channel])
        
        rgb_formulas_layout.addWidget(self.button_add_rgb_formula)
        
                
        #rgb formula elements>
        
        #<values to insert in the text area (the one containing the swap pixel areas) when clicking the canvas

        #list of animation ids
        self.label_animation_ids = QLabel("a_ids")
        self.text_box_animation_ids = QLineEdit()        
        self.label_animation_ids.setBuddy(self.text_box_animation_ids)

        #list of the ids of groups of animations (a group of animations is an object which contains the ids of 1 or more animations)
        self.label_animations_group_ids = QLabel("ag_ids")
        self.text_box_animations_group_ids = QLineEdit()        
        self.label_animations_group_ids.setBuddy(self.text_box_animations_group_ids)


        #the id of the RGB formula
        self.label_rgb_formula_id = QLabel("f_id")
        self.text_box_rgb_formula_id = QLineEdit()
        self.text_box_rgb_formula_id.setValidator(positive_int_validator)
        self.label_rgb_formula_id.setBuddy(self.text_box_rgb_formula_id)

        #contains the pixel area ids which will passed to the RGB formula
        self.label_pixel_area_ids_as_input_for_rgb_func = QLabel("p_ids")
        self.text_box_pixel_area_ids_as_input_for_rgb_func = QLineEdit()
        self.label_pixel_area_ids_as_input_for_rgb_func.setBuddy(self.text_box_pixel_area_ids_as_input_for_rgb_func)

        #this is a list which contains the horizontal position of the top left corner of not defined pixel areas which will passed to the RGB formula
        self.label_pixel_area_x_locations_as_input_for_rgb_func = QLabel("p_x")
        self.text_box_pixel_area_x_locations_as_input_for_rgb_func = QLineEdit()
        self.label_pixel_area_x_locations_as_input_for_rgb_func.setBuddy(self.text_box_pixel_area_x_locations_as_input_for_rgb_func)

        #this is a list which contains the vertical position of the top left corner of not defined pixel areas which will passed to the RGB formula
        self.label_pixel_area_y_locations_as_input_for_rgb_func = QLabel("p_y")
        self.text_box_pixel_area_y_locations_as_input_for_rgb_func = QLineEdit()
        self.label_pixel_area_y_locations_as_input_for_rgb_func.setBuddy(self.text_box_pixel_area_y_locations_as_input_for_rgb_func)
        
        #determines the version of the input image which will be passed to the RGB formula
        self.label_image_version_as_input_for_rgb_func = QLabel("img_in_v")
        self.text_box_image_version_as_input_for_rgb_func = QLineEdit()
        self.text_box_image_version_as_input_for_rgb_func.setValidator(positive_int_validator)
        self.label_image_version_as_input_for_rgb_func.setBuddy(self.text_box_image_version_as_input_for_rgb_func)

        #determines the version of the image to which the changed pixel values will be applied
        self.label_image_version_as_output_from_rgb_func = QLabel("img_out_v")
        self.text_box_image_version_as_output_from_rgb_func = QLineEdit()
        self.text_box_image_version_as_output_from_rgb_func.setValidator(positive_int_validator)
        self.label_image_version_as_output_from_rgb_func.setBuddy(self.text_box_image_version_as_output_from_rgb_func)

        #determines the count of image versions to which the changed pixel values will be applied; the first version is `img_out_v`, the next version is `img_out_v + 1` and so on
        self.label_image_version_as_output_from_rgb_func_stack = QLabel("img_out_v")
        self.text_box_image_version_as_output_from_rgb_func_stack = QLineEdit()
        self.text_box_image_version_as_output_from_rgb_func_stack.setValidator(positive_int_validator)
        self.label_image_version_as_output_from_rgb_func_stack.setBuddy(self.text_box_image_version_as_output_from_rgb_func_stack)


        #values to insert in the text area (the one containing the swap pixel areas) when clicking the canvas>



        
        self.button_apply_swap_areas = QPushButton("Apply areas")
        self.button_remove_swap_areas = QPushButton("Remove areas")
        self.button_clear_canvas = QPushButton("Clear canvas")
        



        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        h_layout.addWidget(self.label_movable_areas)
        h_layout.addWidget(self.checkBox_movable_areas)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        h_layout.addWidget(self.label_image_version_start_index)
        h_layout.addWidget(self.textBox_image_version_start_index)
        h_layout.addWidget(self.label_image_version_increment)
        h_layout.addWidget(self.textBox_image_version_increment)
        h_layout.addWidget(self.label_image_version_swap_frequency)
        h_layout.addWidget(self.textBox_image_version_swap_frequency)
        v_layout.addLayout(h_layout)
       
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_area_swap_pixel_areas)
        h_layout.addWidget(self.text_area_rgb_formulas)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_brush_width)
        h_layout.addWidget(self.label_brush_width_min_value)
        h_layout.addWidget(self.textBox_brush_width_min_value)
        h_layout.addWidget(self.lable_brush_width_max_value)
        h_layout.addWidget(self.textBox_brush_width_max_value)
        h_layout.addWidget(self.lable_brush_width_delta)
        h_layout.addWidget(self.textBox_brush_width_delta)
        h_layout.addWidget(self.button_apply_brush_width_changes)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_brush_height)
        h_layout.addWidget(self.label_brush_height_min_value)
        h_layout.addWidget(self.textBox_brush_height_min_value)
        h_layout.addWidget(self.lable_brush_height_max_value)
        h_layout.addWidget(self.textBox_brush_height_max_value)
        h_layout.addWidget(self.lable_brush_height_delta)
        h_layout.addWidget(self.textBox_brush_height_delta)
        h_layout.addWidget(self.button_apply_brush_height_changes)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_brush_size_set)
        h_layout.addWidget(self.label_brush_width_set)
        h_layout.addWidget(self.textBox_brush_width_set)
        h_layout.addWidget(self.label_brush_height_set)
        h_layout.addWidget(self.textBox_brush_height_set)
        h_layout.addWidget(self.button_set_brush_size)
        v_layout.addLayout(h_layout)

        
        v_layout.addLayout(rgb_formulas_layout)

        
        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)

        h_layout.addWidget(self.label_animation_ids)
        h_layout.addWidget(self.text_box_animation_ids)

        h_layout.addWidget(self.label_animations_group_ids)
        h_layout.addWidget(self.text_box_animations_group_ids)

        h_layout.addWidget(self.label_rgb_formula_id)
        h_layout.addWidget(self.text_box_rgb_formula_id)

        h_layout.addWidget(self.label_pixel_area_ids_as_input_for_rgb_func)
        h_layout.addWidget(self.text_box_pixel_area_ids_as_input_for_rgb_func)

        h_layout.addWidget(self.label_pixel_area_x_locations_as_input_for_rgb_func)
        h_layout.addWidget(self.text_box_pixel_area_x_locations_as_input_for_rgb_func)

        h_layout.addWidget(self.label_pixel_area_y_locations_as_input_for_rgb_func)
        h_layout.addWidget(self.text_box_pixel_area_y_locations_as_input_for_rgb_func)

        h_layout.addWidget(self.label_image_version_as_input_for_rgb_func)
        h_layout.addWidget(self.text_box_image_version_as_input_for_rgb_func)

        h_layout.addWidget(self.label_image_version_as_output_from_rgb_func)
        h_layout.addWidget(self.text_box_image_version_as_output_from_rgb_func)

        h_layout.addWidget(self.label_image_version_as_output_from_rgb_func_stack)
        h_layout.addWidget(self.text_box_image_version_as_output_from_rgb_func_stack)
       

        v_layout.addLayout(h_layout) 
       
       

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_swap_areas)
        h_layout.addWidget(self.button_remove_swap_areas)
        h_layout.addWidget(self.button_clear_canvas)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)



class Text_area(QTextEdit):
    
    def __init__(self, allowed_symbols_regex):
        super().__init__()
        self.regex = re.compile(allowed_symbols_regex)

    def keyPressEvent(self, event):
        
        # Allow standard shortcuts (Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+A, etc.)
        if event.matches(QKeySequence.Copy) or \
            event.matches(QKeySequence.Paste) or \
            event.matches(QKeySequence.Cut) or \
            event.matches(QKeySequence.SelectAll) or \
            event.matches (QKeySequence.Redo) or \
            event.matches (QKeySequence.Undo):
            super().keyPressEvent(event)
            return
        
        # Allow only specific symbols to be used in the text area
        text = event.text()
        if self.regex.fullmatch(text) or event.key() in (
            Qt.Key_Backspace, Qt.Key_Delete,#delete options 
            Qt.Key_Return, Qt.Key_Enter,#new line option
            Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down#move options        
        ):
            super().keyPressEvent(event)
    
    def append_on_same_line(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)       