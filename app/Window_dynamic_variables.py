from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QPlainTextEdit

from Dynamic_variable import Dynamic_variable
from Dynamic_variable_initializer import Dynamic_variable_initializer

class Window_dynamic_variables(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        self.text_area = QPlainTextEdit()
        self.button_apply_dynamic_variables = QPushButton("Apply")
        self.button_remove_dynamic_variables = QPushButton("Remove")

        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_area)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_dynamic_variables)
        h_layout.addWidget(self.button_remove_dynamic_variables)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
    

    def get_dynamic_variables(self) -> list[Dynamic_variable]:
        
        text = self.text_area.toPlainText().replace(' ', '').replace('\n', '')

        dynamic_variable_initializer = Dynamic_variable_initializer()
        dynamic_variables = dynamic_variable_initializer.create_dynamic_variables(text=text)
        if(dynamic_variables != None):
            return dynamic_variables