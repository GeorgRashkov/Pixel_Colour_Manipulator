import numpy as np
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel
import RGB_formula_elements

class ConfigureColorVariablesGroupBox1(QWidget):
    def __init__(self, button_for_drawing):
        super().__init__()

        self.setWindowTitle("Configure color variables")
        self.setGeometry(100, 100, 400, 150)
        
        # --- Main vertical layout ---
        self.main_layout = QVBoxLayout()

        if(button_for_drawing!=None):
            
            self.drawing_btn = QPushButton("")
            self.drawing_btn.setStyleSheet(f"background-color: rgb({button_for_drawing.red()},{button_for_drawing.green()},{button_for_drawing.blue()})")
            
            row0_layout = QHBoxLayout()
            row0_layout.addWidget(self.drawing_btn)
            self.main_layout.addLayout(row0_layout)

        self.rgb_elements = RGB_formula_elements.RGB_formula_elements()

        for channel in self.rgb_elements.channels:
            
            row_layout = QHBoxLayout()
            row_layout.addWidget(self.rgb_elements.labels[channel])
            row_layout.addWidget(self.rgb_elements.text_boxes[channel])
            self.main_layout.addLayout(row_layout)
            
        # --- Forth row ---
        row_layout = QHBoxLayout()
        self.button_for_seting_color_variables = QPushButton("apply")#applies colour variables
        #self.button_for_seting_color_variables.clicked.connect(self.change_RGB_formula)
        self.button_for_showing_RGB_formulas = QPushButton("show")#show the current RGB formula
        self.button_for_showing_RGB_formulas.clicked.connect(self.rgb_elements.show_current_RGB_formulas)
        row_layout.addWidget(self.button_for_seting_color_variables)
        row_layout.addWidget(self.button_for_showing_RGB_formulas)

        #for testing purposes
        self.test_button = QPushButton("test")
        self.test_button.clicked.connect(self.rgb_elements.test_method)
        row_layout.addWidget(self.test_button)

        self.main_layout.addLayout(row_layout)

        # Apply layout to window
        self.setLayout(self.main_layout)
