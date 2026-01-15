from PyQt5.QtWidgets import QWidget, QVBoxLayout
import Canvas    


class CanvasWindow(QWidget):
    def __init__(self):
        super().__init__()

        
        self.setMinimumSize(100, 30)
        self.resize(400, 400)
        
        self.canvas = Canvas.DrawingWidget()
        self.setWindowTitle(self.canvas.get_window_title())
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)