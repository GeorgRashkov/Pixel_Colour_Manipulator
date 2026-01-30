from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit
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
        
        self.text_area_swap_pixel_areas = Text_area(allowed_symbols_regex="[0-9\\[\\], ]")
        self.text_area_rgb_formulas = Text_area(allowed_symbols_regex = RGB_formula_validators.rgb_formula_valid_symbols_for_swap_areas_regex)

        self.button_update_canvas = QPushButton("Update canvas")
        self.button_update_canvas_and_text_area = QPushButton("Update canvas and text")

        int_validator = QIntValidator(0, 999_999)

        #<elements - size arguments for the brush in the canvas window

        #<brush width
        self.label_brush_width = QLabel("brush width| ")
        
        self.label_brush_width_min_value = QLabel("min")
        self.textBox_brush_width_min_value = QLineEdit("1")
        self.textBox_brush_width_min_value.setValidator(int_validator)
        self.textBox_brush_width_min_value.setMaxLength(3)

        self.lable_brush_width_max_value = QLabel("max")
        self.textBox_brush_width_max_value = QLineEdit("999")
        self.textBox_brush_width_max_value.setMaxLength(3)
        self.textBox_brush_width_max_value.setValidator(int_validator)

        self.lable_brush_width_delta = QLabel("increment")
        self.textBox_brush_width_delta = QLineEdit("50")
        self.textBox_brush_width_delta.setMaxLength(3)
        self.textBox_brush_width_delta.setValidator(int_validator)
       

        self.button_apply_brush_width_changes = QPushButton("OK")
        #brush width>

        #<brush height
        self.label_brush_height = QLabel("brush height| ")
        
        self.label_brush_height_min_value = QLabel("min")
        self.textBox_brush_height_min_value = QLineEdit("1")
        self.textBox_brush_height_min_value.setValidator(int_validator)
        self.textBox_brush_height_min_value.setMaxLength(3)
      

        self.lable_brush_height_max_value = QLabel("max")
        self.textBox_brush_height_max_value = QLineEdit("999")
        self.textBox_brush_height_max_value.setMaxLength(3)
        self.textBox_brush_height_max_value.setValidator(int_validator)

        self.lable_brush_height_delta = QLabel("increment")
        self.textBox_brush_height_delta = QLineEdit("50")
        self.textBox_brush_height_delta.setMaxLength(3)
        self.textBox_brush_height_delta.setValidator(int_validator)
       

        self.button_apply_brush_height_changes = QPushButton("OK")
        #brush height>
       
        #<brush size
        self.label_brush_size_set = QLabel("Set brush size| ")
        
        self.label_brush_width_set = QLabel("width")
        self.textBox_brush_width_set = QLineEdit("100")
        self.textBox_brush_width_set.setValidator(int_validator)
        self.textBox_brush_width_set.setMaxLength(3)

        self.label_brush_height_set = QLabel("height")
        self.textBox_brush_height_set = QLineEdit("100")
        self.textBox_brush_height_set.setMaxLength(3)
        self.textBox_brush_height_set.setValidator(int_validator)

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

        self.label_area_ids = QLabel("Area ids")
        self.text_box_area_ids = QLineEdit()        
        self.label_area_ids.setBuddy(self.text_box_area_ids)

        self.label_rgb_formula_id = QLabel("RGB formula ID")
        self.text_box_rgb_formula_id = QLineEdit()
        self.text_box_rgb_formula_id.setValidator(int_validator)
        self.label_rgb_formula_id.setBuddy(self.text_box_rgb_formula_id)

        self.label_movement_id = QLabel("Movement ID")
        self.text_box_movement_id = QLineEdit()
        self.text_box_movement_id.setValidator(int_validator)
        self.label_movement_id.setBuddy(self.text_box_movement_id)


        self.label_resize_id = QLabel("Resize ID")
        self.text_box_resize_id = QLineEdit()
        self.text_box_resize_id.setValidator(int_validator)
        self.label_resize_id.setBuddy(self.text_box_movement_id)

        #values to insert in the text area (the one containing the swap pixel areas) when clicking the canvas>



        self.button_clear_canvas = QPushButton("Clear canvas")
        self.button_apply_swap_areas = QPushButton("Apply areas")
        self.button_remove_swap_areas = QPushButton("Remove areas")
        



        v_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_area_swap_pixel_areas)
        h_layout.addWidget(self.text_area_rgb_formulas)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_update_canvas)
        h_layout.addWidget(self.button_update_canvas_and_text_area)
        h_layout.addWidget(self.button_clear_canvas)
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

        h_layout.addWidget(self.label_area_ids)
        h_layout.addWidget(self.text_box_area_ids)

        h_layout.addWidget(self.label_rgb_formula_id)
        h_layout.addWidget(self.text_box_rgb_formula_id)

        h_layout.addWidget(self.label_movement_id)
        h_layout.addWidget(self.text_box_movement_id)

        h_layout.addWidget(self.label_resize_id)
        h_layout.addWidget(self.text_box_resize_id)

        v_layout.addLayout(h_layout) 
       
       

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_swap_areas)
        h_layout.addWidget(self.button_remove_swap_areas)
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