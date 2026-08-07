from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QCheckBox, QRadioButton, QPushButton, QButtonGroup, QLineEdit, QPlainTextEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

from Form_elements__order_numbers import Form_elements__order_numbers

class Window_Form_pixel_areas_masks(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        int_validator = QIntValidator(0, 999, self)

    #<elements to order masks and regions

        self.radioButton_order_masks = QRadioButton("masks")
        self.radioButton_order_masks.setMaximumWidth(60)
        self.radioButton_order_regions = QRadioButton("regions")
        self.radioButton_order_regions.setMaximumWidth(60)
        self.radioButton_order_regions.setChecked(True)

        self.form_elements__order_masks_and_regions = Form_elements__order_numbers()
        self.form_elements__order_masks_and_regions.set_text_for_button_order(text="order")
        self.form_elements__order_masks_and_regions.set_max_width_for_button_order(width=40)
        self.form_elements__order_masks_and_regions.remove_radio_button_ascending()
        self.form_elements__order_masks_and_regions.set_text_for_radio_button_descending(text="reverse")

        self.radioButtonsGroup_order_masks_or_regions = QButtonGroup()
        self.radioButtonsGroup_order_masks_or_regions.addButton(self.radioButton_order_masks)
        self.radioButtonsGroup_order_masks_or_regions.addButton(self.radioButton_order_regions)
    #elements to order masks and regions>

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
        self.textBox_mask_height = QLineEdit("0")
        self.label_mask_width = QLabel("mask width")
        self.textBox_mask_width = QLineEdit("0")

        self.checkBox_keep_ratio = QCheckBox("keep ratio")
        self.checkBox_keep_ratio.setChecked(True)
        self.checkBox_auto_remove_previous_mask_when_applying_new_mask = QCheckBox("auto remove previous mask when applying new mask")
        self.checkBox_auto_remove_previous_mask_when_applying_new_mask.setChecked(True)

    #elements to alter a mask>


    #<elements to create or delete a colour range region
        self.button_create_colour_range_region = QPushButton("create region")
        self.button_delete_colour_range_region = QPushButton("delete region")

        self.textBox_region_id = QLineEdit("1")
        self.textBox_region_id.setMaxLength(3)
        self.textBox_region_id.setMaximumWidth(30)
        self.textBox_region_id.setValidator(int_validator)
        self.label_region_id = QLabel("id")

        self.checkBox_resize_image_before_region_creation = QCheckBox("resize image before creation")
        self.checkBox_resize_image_before_region_creation.setChecked(True)
      
        #<colour range elements
        self.label_colour_range = QLabel("colour range:")


        self.textBox_r_from = QLineEdit("0")
        self.textBox_r_from.setMaxLength(3)
        self.textBox_r_from.setMaximumWidth(30)
        self.textBox_r_from.setValidator(int_validator)

        self.textBox_r_to = QLineEdit("255")
        self.textBox_r_to.setMaxLength(3)
        self.textBox_r_to.setMaximumWidth(30)
        self.textBox_r_to.setValidator(int_validator)

        self.label_r = QLabel("r|")


        self.textBox_g_from = QLineEdit("0")
        self.textBox_g_from.setMaxLength(3)
        self.textBox_g_from.setMaximumWidth(30)
        self.textBox_g_from.setValidator(int_validator)

        self.textBox_g_to = QLineEdit("255")
        self.textBox_g_to.setMaxLength(3)
        self.textBox_g_to.setMaximumWidth(30)
        self.textBox_g_to.setValidator(int_validator)

        self.label_g = QLabel("g|")


        self.textBox_b_from = QLineEdit("0")
        self.textBox_b_from.setMaxLength(3)
        self.textBox_b_from.setMaximumWidth(30)
        self.textBox_b_from.setValidator(int_validator)

        self.textBox_b_to = QLineEdit("255")
        self.textBox_b_to.setMaxLength(3)
        self.textBox_b_to.setMaximumWidth(30)
        self.textBox_b_to.setValidator(int_validator)

        self.label_b = QLabel("b|")
        #colour range elements>

        self.label_image_index = QLabel("image index")
        self.textBox_image_index = QLineEdit("-1")

        self.label_pixel_area_id = QLabel("area id")
        self.textBox_pixel_area_id = QLineEdit("0")
    #elements to create or delete a colour range region>


    #<check boxes and radio buttons for executing specific actions when appling masks

        self.checkBox_apply_already_applied_masks = QCheckBox("apply already applied masks")
        self.checkBox_apply_already_applied_masks.setChecked(True)

        self.checkBox_update_regions_when_applying_masks = QCheckBox("update regions when applying masks")
        self.checkBox_update_regions_when_applying_masks.setChecked(True)

        self.checkBox_update_last_image_when_applying_masks = QCheckBox("update last image when applying masks")
        self.checkBox_update_last_image_when_applying_masks.setChecked(True)

        self.radioButton_take_image_under_capture_window = QRadioButton("original")
        self.radioButton_take_image_under_capture_window.setChecked(True)
        self.radioButton_take_transformed_image_from_capture_window = QRadioButton("transformed")
        

        self.radioButtonsGroup_take_image = QButtonGroup()
        self.radioButtonsGroup_take_image.addButton(self.radioButton_take_image_under_capture_window)
        self.radioButtonsGroup_take_image.addButton(self.radioButton_take_transformed_image_from_capture_window)
    #check boxes and radio buttons for executing specific actions when appling masks>

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



        v_main_layout = QVBoxLayout()
        h_heather_layout = QHBoxLayout()
        h_main_layout = QHBoxLayout()

        container = QWidget()
        container.setMaximumWidth(400)
        h_heather_layout.addWidget(self.radioButton_order_masks)
        h_heather_layout.addWidget(self.radioButton_order_regions)
        h_heather_layout.addWidget(self.form_elements__order_masks_and_regions, alignment=Qt.AlignLeft)

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
        h_layout.addWidget(self.checkBox_resize_image_before_region_creation)
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
        h_layout.addWidget(self.checkBox_apply_already_applied_masks)
        h_layout.addWidget(self.checkBox_update_regions_when_applying_masks)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_update_last_image_when_applying_masks)
        h_layout.addWidget(self.radioButton_take_image_under_capture_window)
        h_layout.addWidget(self.radioButton_take_transformed_image_from_capture_window)
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

        v_main_layout.addLayout(h_heather_layout)
        v_main_layout.addLayout(h_main_layout)

        self.setLayout(v_main_layout)
   
