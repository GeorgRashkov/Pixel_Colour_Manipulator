from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QTextEdit, QLineEdit
)
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QKeySequence
from PyQt5.QtGui import QIntValidator

from RGB_formula_checker import RGB_formula_validators
import RGB_formula_elements

class FormWindow_SwichPixelValies(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Draw mask")
        self.setMinimumSize(100, 100)
        self.resize(800, 500)             
        

        #< RGB check boxes
        self.r_check_box = QCheckBox()
        self.r_label = QLabel("red channel")
        self.r_label.setBuddy(self.r_check_box)
        self.r_check_box.setChecked(True)

        self.g_check_box = QCheckBox()
        self.g_label = QLabel("green channel")
        self.g_label.setBuddy(self.g_check_box)
        self.g_check_box.setChecked(True)

        self.b_check_box = QCheckBox()
        self.b_label = QLabel("blue channel")
        self.b_label.setBuddy(self.b_check_box)
        self.b_check_box.setChecked(True)
        #RGB check boxes>
        

        self.text_area_swap_pixel_areas = Text_area(allowed_symbols_regex="[0-9\\[\\], ]")
        self.text_area_rgb_formulas = Text_area(allowed_symbols_regex = RGB_formula_validators.rgb_formula_valid_symbols_regex)

        self.button_update_canvas = QPushButton("Update canvas")
        self.button_update_canvas_and_text_area = QPushButton("Update canvas and text")


        #<elements - size arguments for the brush in the canvas window

        validator = QIntValidator(0, 999, self)

        self.label_brush_size = QLabel("brush size| ")
        
        self.label_brush_size_min_value = QLabel("min")
        self.textBox_brush_size_min_value = QLineEdit("5")
        self.textBox_brush_size_min_value.setValidator(validator)
        self.textBox_brush_size_min_value.setMaxLength(3)
      

        self.lable_brush_size_max_value = QLabel("max")
        self.textBox_brush_size_max_value = QLineEdit("200")
        self.textBox_brush_size_max_value.setMaxLength(3)
        self.textBox_brush_size_max_value.setValidator(validator)
       


        self.lable_brush_size_delta = QLabel("increment")
        self.textBox_brush_size_delta = QLineEdit("10")
        self.textBox_brush_size_delta.setMaxLength(3)
        self.textBox_brush_size_delta.setValidator(validator)
        

        self.button_apply_brush_size_changes = QPushButton("OK")

        #elements - size arguments for the brush in the canvas window>



        #<rgb formula elements
        self.rgb_elements = RGB_formula_elements.RGB_formula_elements()
        self.rgb_labels_text = ["red channel","green channel","blue channel"]
        self.button_add_rgb_formula = QPushButton("Add RGB formulas")


        rgb_formulas_layout = QHBoxLayout()
        
        rgb_formulas_layout.addWidget(self.button_add_rgb_formula)
        rgb_formulas_layout.addWidget(QLabel("id"))
        

        for channel in self.rgb_elements.channels:

            rgb_formulas_layout.addWidget(QLabel(channel))
            rgb_formulas_layout.addWidget(self.rgb_elements.text_boxes[channel])
        
        self.label_rgb_formula_id = QLabel("RGB formula ID")
        self.label_rgb_formula_id.setMaximumWidth(80)
        int_validator = QIntValidator(0, 999_999)
        self.text_box_rgb_formula_id = QLineEdit()
        self.text_box_rgb_formula_id.setValidator(int_validator)
        self.text_box_rgb_formula_id.setMaximumWidth(50)
        self.label_rgb_formula_id.setBuddy(self.text_box_rgb_formula_id)
        
        #rgb formula elements>

        self.button_clear_canvas = QPushButton("Clear canvas")
        self.button_apply_swop_areas = QPushButton("Apply areas")
        self.button_remove_swop_areas = QPushButton("Remove areas")
        



        v_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        h_layout.addWidget(self.r_label)
        h_layout.addWidget(self.r_check_box)
        h_layout.addWidget(self.g_label)
        h_layout.addWidget(self.g_check_box)
        h_layout.addWidget(self.b_label)
        h_layout.addWidget(self.b_check_box)       
        v_layout.addLayout(h_layout)

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
        h_layout.addWidget(self.label_brush_size)
        h_layout.addWidget(self.label_brush_size_min_value)
        h_layout.addWidget(self.textBox_brush_size_min_value)
        h_layout.addWidget(self.lable_brush_size_max_value)
        h_layout.addWidget(self.textBox_brush_size_max_value)
        h_layout.addWidget(self.lable_brush_size_delta)
        h_layout.addWidget(self.textBox_brush_size_delta)
        h_layout.addWidget(self.button_apply_brush_size_changes)
        v_layout.addLayout(h_layout)
        
        v_layout.addLayout(rgb_formulas_layout)
        
        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        h_layout.addWidget(self.label_rgb_formula_id)
        h_layout.addWidget(self.text_box_rgb_formula_id)
        v_layout.addLayout(h_layout) 
       
       

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_swop_areas)
        h_layout.addWidget(self.button_remove_swop_areas)
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