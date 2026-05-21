from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, QCheckBox
)
from PyQt5.QtGui import QIntValidator
from Group_box_for_setting_colour_map import Group_box_for_setting_colour_map


class Window_Form_capture_mask(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Capture mask")
        self.setMinimumSize(100, 100)

        v_layout = QVBoxLayout()
        

        self.button_apply_mask = QPushButton("Apply mask")
        self.button_remove_mask = QPushButton("Remove mask")

        self.checkBox_auto_remove_previous_mask_when_applying_new_mask = QCheckBox("auto remove previous mask when applying new mask")
        self.checkBox_auto_remove_previous_mask_when_applying_new_mask.setChecked(True)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_mask)
        h_layout.addWidget(self.button_remove_mask)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.checkBox_auto_remove_previous_mask_when_applying_new_mask)
        v_layout.addLayout(h_layout)

        labels = ["r","g","b"]

        self.textBox_colorRange_list:list[list[QLineEdit]] = []

        validator = QIntValidator(0, 999, self)
        h_layout = QHBoxLayout()

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

            label = QLabel(f"{labels[i]}|")
            h_layout.addWidget(label)


        v_layout.addLayout(h_layout)

        self.colour_variables_group_box = Group_box_for_setting_colour_map()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.colour_variables_group_box)

        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
