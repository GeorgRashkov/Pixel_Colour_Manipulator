from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QCheckBox, QRadioButton, QButtonGroup
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtGui import QIntValidator

import RGB_formula_elements

from Form_elements__order_numbers import Form_elements__order_numbers

class FormWindow_SwapPixelValues(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Pixel areas")
        self.setMinimumSize(100, 100)
        self.resize(800, 500)             
        
        self.lable_for__text_area_swap_pixel_areas = QLabel("pixel areas")
        self.text_area_swap_pixel_areas = QTextEdit()
        self.lable_for__text_area_rgb_formulas = QLabel("rgb formulas")
        self.text_area_rgb_formulas = Text_area()

        positive_int_validator = QIntValidator(0, 999_999)
        int_validator = QIntValidator(-999_999, 999_999)
        

        #<pixel areas behaviour when resizing main window
        self.label_areas_behaviour_when_resizing_main_window = QLabel("resizing behaviour:")

        self.radioButton_areas_resize = QRadioButton("resize")
        self.radioButton_areas_move = QRadioButton("move")
        self.radioButton_areas_keep_aspect_ratio = QRadioButton("keep ratio")
        self.radioButton_areas_keep_aspect_ratio.setChecked(True)

        self.radioButtonGroup_resize_behaviour = QButtonGroup()
        self.radioButtonGroup_resize_behaviour.addButton(self.radioButton_areas_resize)
        self.radioButtonGroup_resize_behaviour.addButton(self.radioButton_areas_move)
        self.radioButtonGroup_resize_behaviour.addButton(self.radioButton_areas_keep_aspect_ratio)

        self.checkBox_fast_area_creation = QCheckBox("use smallest area size")
        #pixel areas behaviour when resizing main window>

        #<pixel areas elements to order ids
        self.form_elements__order_ids = Form_elements__order_numbers()
        #pixel areas elements to order ids>



        self.checkBox_use_copy_for_replicas = QCheckBox("use copy for replicas")
        self.checkBox_use_copy_for_replicas.setChecked(True)

        self.checkBox_use_copy_for_images = QCheckBox("use copy for images")
        self.checkBox_use_copy_for_images.setChecked(True)

        #<settings for output image versions        
        
        self.label_image_version = QLabel("image versions: |")

        self.label_image_version_start_index = QLabel("start| ")
        self.textBox_image_version_start_index = QLineEdit()
        self.textBox_image_version_start_index.setValidator(int_validator)
        self.textBox_image_version_start_index.setMaxLength(3)
        self.textBox_image_version_start_index.setMaximumWidth(30)

        self.label_image_version_end_index = QLabel("end| ")
        self.textBox_image_version_end_index = QLineEdit()
        self.textBox_image_version_end_index.setValidator(int_validator)
        self.textBox_image_version_end_index.setMaxLength(3)
        self.textBox_image_version_end_index.setMaximumWidth(30)

        self.label_image_version_increment = QLabel("step| ")
        self.textBox_image_version_increment = QLineEdit()
        self.textBox_image_version_increment.setValidator(positive_int_validator)
        self.textBox_image_version_increment.setMaxLength(3)
        self.textBox_image_version_increment.setMaximumWidth(30)

        self.label_image_version_swap_frequency = QLabel("swap frequency| ")
        self.textBox_image_version_swap_frequency = QLineEdit()
        self.textBox_image_version_swap_frequency.setValidator(positive_int_validator)
        self.textBox_image_version_swap_frequency.setMaxLength(3)
        self.textBox_image_version_swap_frequency.setMaximumWidth(30)

        self.label_image_version_count = QLabel("count| ")
        self.textBox_image_version_count = QLineEdit()
        self.textBox_image_version_count.setValidator(positive_int_validator)
        self.textBox_image_version_count.setMaxLength(3)
        self.textBox_image_version_count.setMaximumWidth(30)

        self.checkBox_use_special_image_version = QCheckBox("use special")
        self.checkBox_use_special_image_version.setChecked(True)
        
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
        

        self.button_open_window__swap_areas_animations = QPushButton("Show animations")
        self.button_open_window__swap_areas_masks = QPushButton("Show masks")
        self.button_open_window__swap_areas_convolutional_kernels = QPushButton("Show convolutions")
        self.button_clear_canvas = QPushButton("Clear canvas") 

        self.button_apply_elements_to_pixel_areas_manipulator = QPushButton("Apply")
        self.button_remove_elements_from_pixel_areas_manipulator = QPushButton("Remove")

        self.check_box_pixel_areas = QCheckBox("pixel areas")
        self.check_box_rgb_formulas = QCheckBox("rgb formulas")
        self.check_box_animations = QCheckBox("animations")
        self.check_box_masks = QCheckBox("masks")
        self.check_box_convolutional_kernels = QCheckBox("convolutions")
        self.check_box_image_versions = QCheckBox("image versions")
        self.check_box_images = QCheckBox("images")



        v_layout = QVBoxLayout()


        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        h_layout.addWidget(self.label_areas_behaviour_when_resizing_main_window)
        h_layout.addWidget(self.radioButton_areas_resize)
        h_layout.addWidget(self.radioButton_areas_move)
        h_layout.addWidget(self.radioButton_areas_keep_aspect_ratio)
        h_layout.addWidget(self.checkBox_fast_area_creation)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.form_elements__order_ids, alignment=Qt.AlignLeft)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_use_copy_for_replicas)
        h_layout.addWidget(self.checkBox_use_copy_for_images)
        v_layout.addLayout(h_layout)

       
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_image_version)

        h_layout.addWidget(self.textBox_image_version_start_index)
        h_layout.addWidget(self.label_image_version_start_index)

        h_layout.addWidget(self.textBox_image_version_end_index)
        h_layout.addWidget(self.label_image_version_end_index)
        
        h_layout.addWidget(self.textBox_image_version_increment)
        h_layout.addWidget(self.label_image_version_increment)
        
        h_layout.addWidget(self.textBox_image_version_swap_frequency)
        h_layout.addWidget(self.label_image_version_swap_frequency)
        
        h_layout.addWidget(self.textBox_image_version_count)
        h_layout.addWidget(self.label_image_version_count)
        
        h_layout.addWidget(self.checkBox_use_special_image_version)

        h_layout.addStretch()
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.lable_for__text_area_swap_pixel_areas)
        h_layout.addWidget(self.lable_for__text_area_rgb_formulas)
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
        h_layout.addWidget(self.button_open_window__swap_areas_animations)
        h_layout.addWidget(self.button_open_window__swap_areas_masks)
        h_layout.addWidget(self.button_open_window__swap_areas_convolutional_kernels )
        h_layout.addWidget(self.button_clear_canvas)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_elements_to_pixel_areas_manipulator)
        h_layout.addWidget(self.button_remove_elements_from_pixel_areas_manipulator)
        h_layout.addWidget(self.check_box_pixel_areas)
        h_layout.addWidget(self.check_box_rgb_formulas)
        h_layout.addWidget(self.check_box_animations)
        h_layout.addWidget(self.check_box_masks)
        h_layout.addWidget(self.check_box_image_versions)
        h_layout.addWidget(self.check_box_images)
        h_layout.addWidget(self.check_box_convolutional_kernels)
        v_layout.addLayout(h_layout)


        self.setLayout(v_layout)



class Text_area(QTextEdit):

    def __init__(self):
        super().__init__()

    def append_on_same_line(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)       