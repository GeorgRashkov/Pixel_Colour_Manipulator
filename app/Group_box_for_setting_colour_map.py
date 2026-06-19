from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QLabel
from RGB_formula_elements import RGB_formula_elements
from PyQt5.QtGui import QIntValidator

class Group_box_for_setting_colour_map(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Configure color variables")
        
        
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()


        self.rgb_elements = RGB_formula_elements()

        for channel in self.rgb_elements.channels:
            
            h_layout = QHBoxLayout()
            h_layout.addWidget(self.rgb_elements.labels[channel])
            h_layout.addWidget(self.rgb_elements.text_boxes[channel])
            v_layout.addLayout(h_layout)
        
        self.rgb_formula_label = QLabel("rgb formulas")
        self.button_add_rgb_formula = QPushButton("add")#adds the rgb formula
        self.button_show_rgb_formula = QPushButton("show")#shows the RGB formula based on the id
        self.button_remove_rgb_formula = QPushButton("remove")#shows the RGB formula based on the id
        
        self.label_rgb_formula_id = QLabel("id")
        self.text_box_rgb_formula_id = QLineEdit()
        self.text_box_rgb_formula_id.setMaxLength(3)
        self.text_box_rgb_formula_id.setMaximumWidth(30)
        self.text_box_rgb_formula_id.setValidator(QIntValidator(1, 999))

        h_layout = QHBoxLayout()      
        
        h_layout.addWidget(self.rgb_formula_label)
        h_layout.addWidget(self.button_add_rgb_formula)
        h_layout.addWidget(self.button_show_rgb_formula)
        h_layout.addWidget(self.button_remove_rgb_formula)
        
        h_layout.addWidget(self.text_box_rgb_formula_id)
        h_layout.addWidget(self.label_rgb_formula_id)


        v_layout.addLayout(h_layout)

        # Apply layout to window
        self.setLayout(v_layout)
