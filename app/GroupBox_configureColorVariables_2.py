import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIntValidator
from PyQt5 import QtWidgets
import GroupBox_configureColorVariables_1

class ConfigureColorVariablesGroupBox2(GroupBox_configureColorVariables_1.ConfigureColorVariablesGroupBox1):

    def __init__(self):
        super().__init__(None)

        self.h_layout = QHBoxLayout()
        labels = ["r","g","b"]

        self.textBox_colorRange_list = {}

        validator = QIntValidator(0, 999, self)
        
        for i in range (0,3):

            label = QLabel(f"| {labels[i]}")
            self.h_layout.addWidget(label)

            for j in range (0,2):
                
                txt = "0" if(j==0) else "255"

                textBox_colorRange = QtWidgets.QLineEdit(txt)
                textBox_colorRange.setMaxLength(3)
                textBox_colorRange.setValidator(validator)
                self.textBox_colorRange_list[f"{labels[i]}{j}"] = textBox_colorRange
                self.h_layout.addWidget(self.textBox_colorRange_list[f"{labels[i]}{j}"])

        self.main_layout.addLayout(self.h_layout)