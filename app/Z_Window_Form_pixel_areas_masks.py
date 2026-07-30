from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QCheckBox, QLabel, QLineEdit, QPlainTextEdit
from PyQt5.QtCore import Qt

class Window_Form_pixel_areas_masks(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        int_validator = QIntValidator(0, 999, self)

    #<elements to create or delete a mask
        self.button_create_mask = QPushButton("create mask")
        self.button_create_mask.setMaximumWidth(80)
        self.button_delete_mask = QPushButton("delete mask")
        self.button_delete_mask.setMaximumWidth(80)

        self.textBox_mask_id = QLineEdit("1")
        self.textBox_mask_id.setMaxLength(3)
        self.textBox_mask_id.setMaximumWidth(30)
        self.textBox_mask_id.setValidator(int_validator)
        self.label_mask_id = QLabel("id")

    #elements to create or delete a mask>

    #<elements to alter a mask

        self.button_alter_mask = QPushButton("alter mask")
        self.label_mask_height = QLabel("mask height")
        self.textBox_mask_height = QLineEdit("100")
        self.label_mask_width = QLabel("mask width")
        self.textBox_mask_width = QLineEdit("100")

        self.checkBox_keep_ratio = QCheckBox("keep ratio")
        self.checkBox_keep_ratio.setChecked(True)
        self.checkBox_auto_remove_previous_mask_when_applying_new_mask = QCheckBox("auto remove previous mask when applying new mask")
        self.checkBox_auto_remove_previous_mask_when_applying_new_mask.setChecked(True)

    #elements to alter a mask>


    #<elements to create or delete a colour range region
        self.button_create_colour_range_region = QPushButton("create region")
        self.button_delete_colour_range_region = QPushButton("delete region")

        self.label_region_id = QLabel("id")
        self.textBox_region_id = QLineEdit("1")
        self.textBox_region_id.setMaxLength(3)
        self.textBox_region_id.setMaximumWidth(30)
        self.textBox_region_id.setValidator(int_validator)
      
        #<colour range elements
        self.label_colour_range = QLabel("colour range:")


        self.textBox_r_from = QLineEdit("0")
        self.textBox_r_from.setMaxLength(3)
        self.textBox_r_from.setMaximumWidth(30)
        self.textBox_r_from.setValidator(int_validator)

        self.textBox_r_to = QLineEdit("")
        self.textBox_r_to.setMaxLength(3)
        self.textBox_r_to.setMaximumWidth(30)
        self.textBox_r_to.setValidator(int_validator)

        self.label_r = QLabel("r|")


        self.textBox_g_from = QLineEdit("0")
        self.textBox_g_from.setMaxLength(3)
        self.textBox_g_from.setMaximumWidth(30)
        self.textBox_g_from.setValidator(int_validator)

        self.textBox_g_to = QLineEdit("")
        self.textBox_g_to.setMaxLength(3)
        self.textBox_g_to.setMaximumWidth(30)
        self.textBox_g_to.setValidator(int_validator)

        self.label_g = QLabel("g|")


        self.textBox_b_from = QLineEdit("0")
        self.textBox_b_from.setMaxLength(3)
        self.textBox_b_from.setMaximumWidth(30)
        self.textBox_b_from.setValidator(int_validator)

        self.textBox_b_to = QLineEdit("")
        self.textBox_b_to.setMaxLength(3)
        self.textBox_b_to.setMaximumWidth(30)
        self.textBox_b_to.setValidator(int_validator)

        self.label_b = QLabel("b|")
        #colour range elements>

        self.label_image_index = QLabel("image index")
        self.textBox_image_index = QLineEdit("0")

        self.label_pixel_area_id = QLabel("area id")
        self.textBox_pixel_area_id = QLineEdit("0")
    #elements to create or delete a colour range region>

    #<check boxes for executing specific actions when appling masks

        self.checkBox_auto_update_last_image_when_applying_masks = QCheckBox("auto update last image when applying masks")
        self.checkBox_auto_update_last_image_when_applying_masks.setChecked(True)
        self.checkBox_apply_already_applied_masks = QCheckBox("apply already applied masks")
        self.checkBox_apply_already_applied_masks.setChecked(True)
    #check boxes for executing specific actions when appling masks>

    #<elements for applying or removing masks
        self.button_apply_selected_masks = QPushButton("Apply masks")
        self.button_remove_selected_masks = QPushButton("Remove masks")
        self.textBox_apply_masks = QLineEdit()
        self.label_apply_masks = QLabel("ids")

        self.button_apply_all_masks = QPushButton("Apply all masks")
        self.button_remove_all_masks = QPushButton("Remove all masks")

        self.text_area = QPlainTextEdit()
        self.text_area.setReadOnly(True)
    #elements for applying or removing masks>



        h_main_layout = QHBoxLayout()

        container = QWidget()
        container.setMaximumWidth(400)
        v_layout = QVBoxLayout(container)
        v_layout.setAlignment(Qt.AlignTop)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_create_mask)
        h_layout.addWidget(self.button_delete_mask)
        h_layout.addWidget(self.textBox_mask_id)
        h_layout.addWidget(self.label_mask_id)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_alter_mask)
        h_layout.addWidget(self.label_mask_height)
        h_layout.addWidget(self.textBox_mask_height)
        h_layout.addWidget(self.label_mask_width)
        h_layout.addWidget(self.textBox_mask_width)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_keep_ratio)
        h_layout.addWidget(self.checkBox_auto_remove_previous_mask_when_applying_new_mask)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_create_colour_range_region)
        h_layout.addWidget(self.button_delete_colour_range_region)
        h_layout.addWidget(self.textBox_region_id)
        h_layout.addWidget(self.label_region_id)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_colour_range)
        h_layout.addWidget(self.textBox_r_from)
        h_layout.addWidget(self.textBox_r_to)
        h_layout.addWidget(self.label_r)
        h_layout.addWidget(self.textBox_g_from)
        h_layout.addWidget(self.textBox_g_to)
        h_layout.addWidget(self.label_g)
        h_layout.addWidget(self.textBox_b_from)
        h_layout.addWidget(self.textBox_b_to)
        h_layout.addWidget(self.label_b)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_image_index)
        h_layout.addWidget(self.textBox_image_index)
        h_layout.addWidget(self.label_pixel_area_id)
        h_layout.addWidget(self.textBox_pixel_area_id)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_auto_update_last_image_when_applying_masks)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_apply_already_applied_masks)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_selected_masks)
        h_layout.addWidget(self.button_remove_selected_masks)
        h_layout.addWidget(self.textBox_apply_masks)
        h_layout.addWidget(self.label_apply_masks)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_all_masks)
        h_layout.addWidget(self.button_remove_all_masks)
        v_layout.addLayout(h_layout)

        h_main_layout.addWidget(container)
        h_main_layout.addWidget(self.text_area)


        self.setLayout(h_main_layout)
   
