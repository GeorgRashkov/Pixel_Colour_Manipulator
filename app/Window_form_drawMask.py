from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout
)
from PyQt5.QtGui import QIntValidator
from GroupBox_configureColorVariables_1 import ConfigureColorVariablesGroupBox1


class FormWindow_DrawMask(QWidget):
    def __init__(self, columns_count, draw_colors):
        super().__init__()
        
        self.setWindowTitle("Draw mask")
        self.setMinimumSize(100, 100)
        self.resize(800, 500)

        #<elements - size arguments for the brush in the canvas window
        validator = QIntValidator(0, 999, self)

        self.lable_brush_size = QLabel("brush size| ")
        
        self.lable_brush_size_min_value = QLabel("min")
        self.textBox_brush_size_min_value = QLineEdit("5")
        self.textBox_brush_size_min_value.setValidator(validator)
        self.textBox_brush_size_min_value.setMaxLength(3)
        #self.textBox_brush_size_min_value.setMaximumWidth(30)

        self.lable_brush_size_max_value = QLabel("max")
        self.textBox_brush_size_max_value = QLineEdit("200")
        self.textBox_brush_size_max_value.setMaxLength(3)
        self.textBox_brush_size_max_value.setValidator(validator)
        #self.textBox_brush_size_max_value.setMaximumWidth(30)


        self.lable_brush_size_delta = QLabel("increment")
        self.textBox_brush_size_delta = QLineEdit("10")
        self.textBox_brush_size_delta.setMaxLength(3)
        self.textBox_brush_size_delta.setValidator(validator)
        #self.textBox_brush_size_delta.setMaximumWidth(30)

        self.button_apply_brush_size_changes = QPushButton("OK")
        #elements - size arguments for the brush in the canvas window>

        v_layout = QVBoxLayout()#vertical layot
        h_layout = QHBoxLayout()#horizontal layot

        self.clear_btn = QPushButton("Clear canvas")
        self.apply_mask_btn = QPushButton("Apply mask")
        self.remove_mask_btn = QPushButton("Remove mask")

        h_layout.addWidget(self.clear_btn)
        h_layout.addWidget(self.apply_mask_btn)
        h_layout.addWidget(self.remove_mask_btn)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.lable_brush_size)
       
        h_layout.addWidget(self.lable_brush_size_min_value)
        h_layout.addWidget(self.textBox_brush_size_min_value)

        h_layout.addWidget(self.lable_brush_size_max_value)
        h_layout.addWidget(self.textBox_brush_size_max_value)

        h_layout.addWidget(self.lable_brush_size_delta)
        h_layout.addWidget(self.textBox_brush_size_delta)

        h_layout.addWidget(self.button_apply_brush_size_changes)

        v_layout.addLayout(h_layout)

        self.forms = []
        
        h_layout = QHBoxLayout()

        for i in range(1,len(draw_colors)+1):
            
            form = ConfigureColorVariablesGroupBox1(draw_colors[i-1]) 
            self.forms.append(form)
            h_layout.addWidget(form)

            if(i%columns_count==0):
                v_layout.addLayout(h_layout)
                h_layout = QHBoxLayout()

        self.setLayout(v_layout)
