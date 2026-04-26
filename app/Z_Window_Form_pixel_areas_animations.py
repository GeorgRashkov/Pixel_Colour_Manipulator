from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout
)


class FormWindow_PixelAreasAnimations(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Pixel areas animations")
        self.setMinimumSize(100, 100)
        self.resize(800, 500)             
        
        self.lable_for__text_area_pixel_areas_animations = QLabel("animations")
        self.text_area_pixel_areas_animations = QTextEdit() 
        self.lable_for__text_area_pixel_areas_animations_groups = QLabel("animation groups")
        self.text_area_pixel_areas_animations_groups = QTextEdit() 

        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.lable_for__text_area_pixel_areas_animations, 3)
        h_layout.addWidget(self.lable_for__text_area_pixel_areas_animations_groups, 1)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_area_pixel_areas_animations, 3)
        h_layout.addWidget(self.text_area_pixel_areas_animations_groups, 1)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

