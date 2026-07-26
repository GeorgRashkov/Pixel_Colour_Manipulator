from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

from Colour_slider import get_colour_slider
from Colour import Colour

class Draw_elements(QWidget):

    def __init__(self, int_validator_min_value:int=0, int_validator_max_value:int=999, text_box_max_length:int=3, text_box_max_width:int=30):
        super().__init__()

        int_validator = QIntValidator(int_validator_min_value, int_validator_max_value, self)

        self.lable_brush_size = QLabel("brush size| ")
        
        self.lable_brush_size_min_value = QLabel("min")
        self.textBox_brush_size_min_value = QLineEdit("5")
        self.textBox_brush_size_min_value.setMaxLength(text_box_max_length)
        self.textBox_brush_size_min_value.setMaximumWidth(text_box_max_width)
        self.textBox_brush_size_min_value.setValidator(int_validator)

        self.lable_brush_size_max_value = QLabel("max")
        self.textBox_brush_size_max_value = QLineEdit("200")
        self.textBox_brush_size_max_value.setMaxLength(text_box_max_length)
        self.textBox_brush_size_max_value.setMaximumWidth(text_box_max_width)
        self.textBox_brush_size_max_value.setValidator(int_validator)

        self.lable_brush_size_delta = QLabel("increment")
        self.textBox_brush_size_delta = QLineEdit("10")
        self.textBox_brush_size_delta.setMaxLength(text_box_max_length)
        self.textBox_brush_size_delta.setMaximumWidth(text_box_max_width)
        self.textBox_brush_size_delta.setValidator(int_validator)

        self.button_apply_brush_size_changes = QPushButton("OK")

        self.sliders_min_value = 0
        self.sliders_max_value = 5
        self.slider_step = 51

        self.slider_red = get_colour_slider(colour_str="red", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)
        self.slider_green = get_colour_slider(colour_str="green", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)
        self.slider_blue = get_colour_slider(colour_str="blue", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)


        self.colour = Colour(r=self.slider_red.value(),g=self.slider_green.value(),b=self.slider_blue.value())

        self.button_clear_canvas = QPushButton("Clear canvas")
        self.button_clear_canvas.setMaximumWidth(80)
        self.drawing_button = QPushButton("")
        self.set_colour_of_drawing_button()


        v_layout = QVBoxLayout()

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
        h_layout.addWidget(self.slider_red)
        h_layout.addWidget(self.slider_green)
        h_layout.addWidget(self.slider_blue)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_clear_canvas)
        h_layout.addWidget(self.drawing_button)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)


    def set_colour_of_drawing_button(self):
        self.drawing_button.setStyleSheet(f"background-color: rgb({self.colour.r},{self.colour.g},{self.colour.b})")