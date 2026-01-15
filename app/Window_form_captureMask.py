from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout
)
import GroupBox_configureColorVariables_2

class FormWindow_CaptureMask(QWidget):
    def __init__(self, columns_count, draw_colors):
        super().__init__()
        
        self.setWindowTitle("Capture mask")
        self.setMinimumSize(100, 100)
        self.resize(800, 500)

        v_layout = QVBoxLayout()#vertical layot
        h_layout = QHBoxLayout()#horizontal layot

      
        v_layout.addLayout(h_layout)

        self.forms = []
        
        h_layout = QHBoxLayout()

        for i in range(1,len(draw_colors)+1):

            form = GroupBox_configureColorVariables_2.ConfigureColorVariablesGroupBox2()
            self.forms.append(form)
            h_layout.addWidget(form)

            if(i%columns_count==0):
                v_layout.addLayout(h_layout)
                h_layout = QHBoxLayout()
        
        self.setLayout(v_layout)