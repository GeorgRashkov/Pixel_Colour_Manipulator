from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QButtonGroup, QRadioButton, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt

from Draw_elements import Draw_elements

from Form_elements__order_numbers import Form_elements__order_numbers

class Window_form_images(QWidget):
    def __init__(self):
        super().__init__()

        self.setMaximumWidth(300)
        self.setMaximumHeight(300)

        int_validator = QIntValidator()

        self.label_images_count = QLabel()

        self.form_elements__order_images = Form_elements__order_numbers()
        self.form_elements__order_images.set_text_for_button_order(text="order")
        self.form_elements__order_images.set_max_width_for_button_order(width=40)
        self.form_elements__order_images.remove_radio_button_ascending()
        self.form_elements__order_images.set_text_for_radio_button_descending(text="reverse")

        #<elements to add new image
        self.button_add_image = QPushButton("add image")
       
        self.radioButton_add_window_capture_input = QRadioButton("input")
        self.radioButton_add_window_capture_input.setChecked(True)
        self.radioButton_add_window_capture_output = QRadioButton("output")
        self.radioButton_add_draw_window_output = QRadioButton("drawn")

        self.checkBox_remove_last_image_before_creating_new_image = QCheckBox("remove last image")
        self.checkBox_remove_last_image_before_creating_new_image.setChecked(True)

        self.buttonGroup_add_image = QButtonGroup()
        self.buttonGroup_add_image.addButton(self.radioButton_add_window_capture_input)
        self.buttonGroup_add_image.addButton(self.radioButton_add_window_capture_output)
        self.buttonGroup_add_image.addButton(self.radioButton_add_draw_window_output)
        #elements to add new image>

        #<elements to remove images
        self.button_remove_images = QPushButton("remove images")
        self.button_remove_images.setMaximumWidth(111)
        self.label_remove_images = QLabel("range:")
        self.label_remove_images.setMaximumWidth(35)
        self.textBox_remove_images_index1 = QLineEdit("0")
        self.textBox_remove_images_index1.setMaxLength(4)
        self.textBox_remove_images_index1.setMaximumWidth(33)
        self.textBox_remove_images_index1.setValidator(int_validator)
        self.textBox_remove_images_index2 = QLineEdit("-1")
        self.textBox_remove_images_index2.setMaxLength(4)
        self.textBox_remove_images_index2.setMaximumWidth(33)
        self.textBox_remove_images_index2.setValidator(int_validator)
        #elements to remove images>

        #<elements to resize images - the selected images will be resized in percentage based on the current size of the main (capture) window
        self.button_resize_images = QPushButton("resize images")
        self.label_resize_images = QLabel("range:")
        self.textBox_resize_images_index1 = QLineEdit("0")
        self.textBox_resize_images_index1.setMaxLength(4)
        self.textBox_resize_images_index1.setMaximumWidth(33)
        self.textBox_resize_images_index1.setValidator(int_validator)
        self.textBox_resize_images_index2 = QLineEdit("-1")
        self.textBox_resize_images_index2.setMaxLength(4)
        self.textBox_resize_images_index2.setMaximumWidth(33)
        self.textBox_resize_images_index2.setValidator(int_validator)

        self.label_resize_images_height = QLabel("height:")
        self.textBox_resize_images_height = QLineEdit("100")
        self.textBox_resize_images_height.setMaxLength(4)
        self.textBox_resize_images_height.setMaximumWidth(33)
        self.textBox_resize_images_height.setValidator(int_validator)
        self.label_resize_images_width = QLabel("width:")
        self.textBox_resize_images_width = QLineEdit("100")
        self.textBox_resize_images_width.setMaxLength(4)
        self.textBox_resize_images_width.setMaximumWidth(33)
        self.textBox_resize_images_width.setValidator(int_validator)
        #elements to resize image - the selected images will be resized in percentage based on the current size of the main (capture) window>


        #<elements to show an image
        self.button_show_image = QPushButton("show image")
        self.button_show_image.setMaximumWidth(111)
        self.textBox_show_image = QLineEdit("0")
        self.textBox_show_image.setMaxLength(4)
        self.textBox_show_image.setMaximumWidth(33)
        self.textBox_show_image.setValidator(int_validator)
        #elements to show an image>

        self.button_open_image_window = QPushButton("open image window")
        self.button_open_image_window.setMaximumWidth(111)
        self.button_open_canvas_window = QPushButton("open canvas window")
        self.button_open_canvas_window.setMaximumWidth(111)

        self.draw_elements = Draw_elements()
        
        self.button_apply_images_manipulator = QPushButton("apply images")
        self.button_apply_images_manipulator.setMaximumWidth(111)
        self.label_apply_images = QLabel("range:")
        self.label_apply_images.setMaximumWidth(35)
        self.textBox_apply_images_index1 = QLineEdit("0")
        self.textBox_apply_images_index1.setMaxLength(4)
        self.textBox_apply_images_index1.setMaximumWidth(33)
        self.textBox_apply_images_index1.setValidator(int_validator)
        self.textBox_apply_images_index2 = QLineEdit("-1")
        self.textBox_apply_images_index2.setMaxLength(4)
        self.textBox_apply_images_index2.setMaximumWidth(33)
        self.textBox_apply_images_index2.setValidator(int_validator)
        

        
        v_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_images_count)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.form_elements__order_images)
        v_layout.addLayout(h_layout)
        

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_add_image)
        h_layout.addWidget(self.radioButton_add_window_capture_input)
        h_layout.addWidget(self.radioButton_add_window_capture_output)
        h_layout.addWidget(self.radioButton_add_draw_window_output)
        h_layout.addWidget(self.checkBox_remove_last_image_before_creating_new_image)
        h_layout.setAlignment(Qt.AlignLeft)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_remove_images)
        h_layout.addWidget(self.label_remove_images)
        h_layout.addWidget(self.textBox_remove_images_index1)
        h_layout.addWidget(self.textBox_remove_images_index2)
        h_layout.setAlignment(Qt.AlignLeft)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_resize_images)
        h_layout.addWidget(self.label_resize_images)
        h_layout.addWidget(self.textBox_resize_images_index1)
        h_layout.addWidget(self.textBox_resize_images_index2)

        h_layout.addWidget(self.label_resize_images_height)
        h_layout.addWidget(self.textBox_resize_images_height)
        h_layout.addWidget(self.label_resize_images_width)
        h_layout.addWidget(self.textBox_resize_images_width)
        h_layout.setAlignment(Qt.AlignLeft)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_show_image)
        h_layout.addWidget(self.textBox_show_image)
        h_layout.setAlignment(Qt.AlignLeft)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_open_image_window)
        h_layout.addWidget(self.button_open_canvas_window)
        h_layout.setAlignment(Qt.AlignLeft)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.draw_elements)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_images_manipulator)
        h_layout.addWidget(self.label_apply_images)
        h_layout.addWidget(self.textBox_apply_images_index1)
        h_layout.addWidget(self.textBox_apply_images_index2)
        h_layout.setAlignment(Qt.AlignLeft)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
        

