from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


    
#most of the time `colour_str` will be either "red" or "green" or "blue"
def get_colour_slider(colour_str:str, min_value, max_value, initial_value) -> QSlider:
    
    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(min_value)
    slider.setMaximum(max_value)
    slider.setValue(initial_value)
    
    slider.setStyleSheet(
        f""" 
        QSlider::handle:horizontal {{ 
        background: {colour_str}; 
        }}
        QSlider::sub-page:horizontal {{
        background: {colour_str};
        }}
        QSlider::groove:horizontal {{
            background: black;
            height: 5px;
        }}
        QSlider::handle:horizontal {{
            width: 5px;
            margin: -15px 0;
        }}
        """)

    return slider