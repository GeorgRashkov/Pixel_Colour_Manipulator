from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QCheckBox, QLabel, QLineEdit, QPlainTextEdit
from PyQt5.QtCore import Qt
from Colour import Colour
from Colour_slider import get_colour_slider

class Window_Form_pixel_areas_masks(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        int_validator = QIntValidator(0, 999, self)


        self.button_create_mask = QPushButton("create mask")
        self.button_create_mask.setMaximumWidth(80)
        self.button_delete_mask = QPushButton("delete mask")
        self.button_delete_mask.setMaximumWidth(80)

        self.label_mask_id = QLabel("id")
        self.textBox_mask_id = QLineEdit("1")
        self.textBox_mask_id.setMaxLength(3)
        self.textBox_mask_id.setMaximumWidth(30)
        self.textBox_mask_id.setValidator(int_validator)

        self.button_alter_pixel_area_id = QPushButton("alter pixel area")
        self.button_alter_pixel_area_id.setMaximumWidth(150)
        self.label_pixel_area_id = QLabel("id")
        self.textBox_pixel_area_id = QLineEdit("1")
        self.textBox_pixel_area_id.setMaxLength(3)
        self.textBox_pixel_area_id.setMaximumWidth(30)
        self.textBox_pixel_area_id.setValidator(int_validator)


        self.button_create_colour_region = QPushButton("create colour region")
        self.button_create_colour_range_region = QPushButton("create colour range region")
        self.button_delete_region = QPushButton("delete region")

        self.label_region_id = QLabel("id")
        self.textBox_region_id = QLineEdit("1")
        self.textBox_region_id.setMaxLength(3)
        self.textBox_region_id.setMaximumWidth(30)
        self.textBox_region_id.setValidator(int_validator)
      



        self.lable_brush_size = QLabel("brush size| ")
        
        self.lable_brush_size_min_value = QLabel("min")
        self.textBox_brush_size_min_value = QLineEdit("5")
        self.textBox_brush_size_min_value.setMaxLength(3)
        self.textBox_brush_size_min_value.setMaximumWidth(30)
        self.textBox_brush_size_min_value.setValidator(int_validator)

        self.lable_brush_size_max_value = QLabel("max")
        self.textBox_brush_size_max_value = QLineEdit("200")
        self.textBox_brush_size_max_value.setMaxLength(3)
        self.textBox_brush_size_max_value.setMaximumWidth(30)
        self.textBox_brush_size_max_value.setValidator(int_validator)

        self.lable_brush_size_delta = QLabel("increment")
        self.textBox_brush_size_delta = QLineEdit("10")
        self.textBox_brush_size_delta.setMaxLength(3)
        self.textBox_brush_size_delta.setMaximumWidth(30)
        self.textBox_brush_size_delta.setValidator(int_validator)

        self.button_apply_brush_size_changes = QPushButton("OK")


        self.sliders_min_value = 0
        self.sliders_max_value = 5
        self.slider_step = 51

        self.slider_red = get_colour_slider(colour_str="red", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)
        self.slider_green = get_colour_slider(colour_str="green", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)
        self.slider_blue = get_colour_slider(colour_str="blue", min_value=self.sliders_min_value, max_value=self.sliders_max_value, initial_value=self.sliders_min_value)


        self.colour = Colour(r=self.slider_red.value(),g=self.slider_green.value(),b=self.slider_blue.value())

        self.drawing_button = QPushButton("")
        self.button_clear_canvas = QPushButton("Clear canvas")
        self.button_clear_canvas.setMaximumWidth(80)
        self.set_colour_of_drawing_button()

        self.checkBox_auto_remove_previous_masks_when_applying_new_masks = QCheckBox("auto remove previous masks when applying new masks")
        self.checkBox_auto_remove_previous_masks_when_applying_new_masks.setChecked(True)

        self.checkBox_keep_ratio = QCheckBox("keep ratio")
        self.checkBox_keep_ratio.setChecked(True)

        self.button_apply_masks = QPushButton("Apply masks")
        self.button_remove_masks = QPushButton("Remove masks")



        self.text_area = QPlainTextEdit()
        self.text_area.setReadOnly(True)


        container = QWidget()
        container.setMaximumWidth(400)

        h_main_layout = QHBoxLayout()
        v_layout = QVBoxLayout(container)
        v_layout.setAlignment(Qt.AlignTop)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_create_mask)
        h_layout.addWidget(self.button_delete_mask)
        h_layout.addWidget(self.textBox_mask_id)
        h_layout.addWidget(self.label_mask_id)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_alter_pixel_area_id)
        h_layout.addWidget(self.textBox_pixel_area_id)
        h_layout.addWidget(self.label_pixel_area_id)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_create_colour_region)
        h_layout.addWidget(self.button_create_colour_range_region)
        h_layout.addWidget(self.button_delete_region)
        h_layout.addWidget(self.textBox_region_id)
        h_layout.addWidget(self.label_region_id)
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
        h_layout.addWidget(self.slider_red)
        h_layout.addWidget(self.slider_green)
        h_layout.addWidget(self.slider_blue)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_clear_canvas)
        h_layout.addWidget(self.drawing_button)
        v_layout.addLayout(h_layout)



        rgb_labels = ["r","g","b"]

        self.textBox_colorRange_list:list[list[QLineEdit]] = []

        validator = QIntValidator(0, 999, self)
        h_layout = QHBoxLayout()

        self.label_colour_range = QLabel("colour range:")
        h_layout.addWidget( self.label_colour_range)

        for i in range (0,3):
            
            self.textBox_colorRange_list.append([])

            for j in range (0,2):
                
                txt = "0" if(j==0) else "255"

                textBox_colorRange = QLineEdit(txt)
                textBox_colorRange.setMaxLength(3)
                textBox_colorRange.setMaximumWidth(30)
                textBox_colorRange.setValidator(validator)
                self.textBox_colorRange_list[i].append(textBox_colorRange)
                h_layout.addWidget(self.textBox_colorRange_list[i][j])

            label = QLabel(f"{rgb_labels[i]}|")
            h_layout.addWidget(label)
        
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_auto_remove_previous_masks_when_applying_new_masks)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_keep_ratio)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_masks)
        h_layout.addWidget(self.button_remove_masks)
        v_layout.addLayout(h_layout)

        h_main_layout.addWidget(container)
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_area)
        h_main_layout.addLayout(h_layout)

        self.setLayout(h_main_layout)



    def set_colour_of_drawing_button(self):
        self.drawing_button.setStyleSheet(f"background-color: rgb({self.colour.r},{self.colour.g},{self.colour.b})")
