#this file should be deleted !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QCheckBox
)
from PyQt5.QtGui import QIntValidator
from Group_box_for_setting_colour_map import Group_box_for_setting_colour_map

from Colour import Colour
from Colour_slider import get_colour_slider

class Window_Form_draw_mask(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Draw mask")
        self.setMinimumSize(100, 100)

        #<elements - size arguments for the brush in the canvas window
        validator = QIntValidator(0, 999, self)

        self.lable_brush_size = QLabel("brush size| ")
        
        self.lable_brush_size_min_value = QLabel("min")
        self.textBox_brush_size_min_value = QLineEdit("5")
        self.textBox_brush_size_min_value.setMaxLength(3)
        self.textBox_brush_size_min_value.setMaximumWidth(30)
        self.textBox_brush_size_min_value.setValidator(validator)

        self.lable_brush_size_max_value = QLabel("max")
        self.textBox_brush_size_max_value = QLineEdit("200")
        self.textBox_brush_size_max_value.setMaxLength(3)
        self.textBox_brush_size_max_value.setMaximumWidth(30)
        self.textBox_brush_size_max_value.setValidator(validator)

        self.lable_brush_size_delta = QLabel("increment")
        self.textBox_brush_size_delta = QLineEdit("10")
        self.textBox_brush_size_delta.setMaxLength(3)
        self.textBox_brush_size_delta.setMaximumWidth(30)
        self.textBox_brush_size_delta.setValidator(validator)


        self.button_apply_brush_size_changes = QPushButton("OK")
        #elements - size arguments for the brush in the canvas window>


        self.button_clear_canvas = QPushButton("Clear canvas")
        self.button_apply_mask = QPushButton("Apply mask")
        self.button_remove_mask = QPushButton("Remove mask")

        self.checkBox_auto_remove_previous_mask_when_applying_new_mask = QCheckBox("auto remove previous mask when applying new mask")
        self.checkBox_auto_remove_previous_mask_when_applying_new_mask.setChecked(True)

        self.sliders_min_value = 0
        self.sliders_max_value = 5
        self.slider_step = 51

        self.slider_red = get_colour_slider(colour_str="red", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)
        self.slider_green = get_colour_slider(colour_str="green", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)
        self.slider_blue = get_colour_slider(colour_str="blue", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)

        self.colour = Colour(r=self.slider_red.value(),g=self.slider_green.value(),b=self.slider_blue.value())

        self.drawing_button = QPushButton("")
        self.set_colour_of_drawing_button()

        self.colour_variables_group_box = Group_box_for_setting_colour_map()




        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.slider_red)
        h_layout.addWidget(self.slider_green)
        h_layout.addWidget(self.slider_blue)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_clear_canvas)
        h_layout.addWidget(self.button_apply_mask)
        h_layout.addWidget(self.button_remove_mask)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_auto_remove_previous_mask_when_applying_new_mask)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.lable_brush_size)
       
        h_layout.addWidget(self.textBox_brush_size_min_value)
        h_layout.addWidget(self.lable_brush_size_min_value)

        h_layout.addWidget(self.textBox_brush_size_max_value)
        h_layout.addWidget(self.lable_brush_size_max_value)

        h_layout.addWidget(self.textBox_brush_size_delta)
        h_layout.addWidget(self.lable_brush_size_delta)

        h_layout.addWidget(self.button_apply_brush_size_changes)

        v_layout.addLayout(h_layout)

        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.drawing_button)
        v_layout.addLayout(h_layout)
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.colour_variables_group_box)

        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
    

    
    def set_colour_of_drawing_button(self):
        self.drawing_button.setStyleSheet(f"background-color: rgb({self.colour.r},{self.colour.g},{self.colour.b})")
