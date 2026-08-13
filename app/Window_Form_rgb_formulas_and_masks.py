from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout

from RGB_formula_elements import RGB_formula_elements

class Window_Form_rgb_formulas_and_masks(QtWidgets.QWidget): 
    def __init__(self):

        super().__init__()
        
        #<rgb formula elements

        self.rgb_elements = RGB_formula_elements(use_areas=False)
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

        #<elements to open/minize windows
        self.button_open_masks_window = QPushButton("open masks")
        self.button_open_masks_window.setMaximumWidth(100)
        #elements to open/minize windows>

        #<text areas
        self.label_for__text_area_rgb_formulas = QLabel("rgb formulas")
        self.text_area_rgb_formulas = QTextEdit()

        self.label_for_text_area_mask_ids_with_f_ids = QLabel("mask ids")
        self.text_area_mask_ids_with_f_ids = QTextEdit()
        #text areas>


        #<apply/remove elements
        self.button_apply_elements_to__rgb_formulas_and_masks_manipulator = QPushButton("Apply")
        self.button_apply_elements_to__rgb_formulas_and_masks_manipulator.setMaximumWidth(100)
        self.button_remove_elements_from__rgb_formulas_and_masks_manipulator = QPushButton("Remove")
        self.button_remove_elements_from__rgb_formulas_and_masks_manipulator.setMaximumWidth(100)

        self.check_box_rgb_formulas = QCheckBox("rgb formulas")
        self.check_box_rgb_formulas.setMaximumWidth(100)
        self.check_box__masks_ids_and_rgb_formulas_ids = QCheckBox("mask ids")
        self.check_box__masks_ids_and_rgb_formulas_ids.setMaximumWidth(100)
        self.check_box_masks = QCheckBox("mask")
        self.check_box_masks.setMaximumWidth(100)
        #apply/remove elements>

        v_layout = QVBoxLayout()

        v_layout.addLayout(rgb_formulas_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_for__text_area_rgb_formulas, 4)
        h_layout.addWidget(self.label_for_text_area_mask_ids_with_f_ids, 1)
        h_layout.addWidget(self.button_open_masks_window, 1)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_area_rgb_formulas, 4)
        h_layout.addWidget(self.text_area_mask_ids_with_f_ids, 2)
        v_layout.addLayout(h_layout)

        """
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_open_masks_window)
        v_layout.addLayout(h_layout)
        """

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_elements_to__rgb_formulas_and_masks_manipulator)
        h_layout.addWidget(self.button_remove_elements_from__rgb_formulas_and_masks_manipulator)
        h_layout.addWidget(self.check_box_rgb_formulas)
        h_layout.addWidget(self.check_box__masks_ids_and_rgb_formulas_ids)
        h_layout.addWidget(self.check_box_masks)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
