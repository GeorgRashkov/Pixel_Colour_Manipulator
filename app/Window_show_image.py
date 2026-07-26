import numpy as np

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget

class Window_show_image(QWidget):

    def __init__(self):

        super().__init__()
        # Keep a pixmap to paint
        self._pixmap = None

    def show_image(self, img:np.ndarray[np.uint8]):

        # Convert the numpy array to QImage
        h, w = img.shape[0], img.shape[1]
        bytes_per_line = 3 * w
        qimg = QtGui.QImage(img.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                
        # make a QPixmap to draw (copy to ensure memory is owned by Qt)
        pixmap = QtGui.QPixmap.fromImage(qimg).copy()
    
        # Store pixmap
        self._pixmap = pixmap

        # Force a paint
        self.update() #calls the "paintEvent" function

    def paintEvent(self, event):
        
        painter = QtGui.QPainter(self)
        if self._pixmap is None:
            # blank background
            painter.fillRect(self.rect(), QtCore.Qt.black)
            return
        
        """
        # Scale pixmap to widget size while preserving aspect ratio (fill the entire widget)
        scaled = self._pixmap.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        """
        x = 0
        if(self.geometry().x() < 0):
            x = (-1)*self.geometry().x()
        y = 0
        if(self.geometry().y() < 0):
            y = (-1)*self.geometry().y()
        painter.drawPixmap(x, y, self._pixmap)
        painter.end()