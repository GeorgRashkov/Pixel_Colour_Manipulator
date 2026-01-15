from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QMouseEvent, QColor, QImage, QCursor, QPixmap
from PyQt5.QtCore import Qt, QPointF
import numpy as np


class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: white;")
        self.drawing = False
        self.last_point = QPointF()
        self.lines = []  # (start_norm, end_norm, color, size)
        
        self.brush_color = QColor(0, 0, 0)
        self.brush_size = 5 #initial brush size
        self.brush_min_size = 5
        self.brush_max_size = 200
        self.brush_delta = 10 #the value which will be use to increase or decrease the brush size

        #self.setCursor(Qt.CrossCursor)
        self.set_cursor()

    def get_window_title(self):
        return f"Brush size: {self.brush_size}"
    
    def set_cursor(self):

        # Create a transparent pixmap with size width,height
        pixmap = QPixmap(self.brush_size*2, self.brush_size*2)
        pixmap.fill(Qt.transparent)

        # Draw a circle on the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.brush_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawEllipse(self.brush_size//2, self.brush_size//2, self.brush_size, self.brush_size)  # (x, y, w, h)
        painter.end()

        # Create a cursor from this pixmap
        circle_cursor = QCursor(pixmap, self.brush_size, self.brush_size)  # hotspot at center

        # Apply the created cursor to the whole window
        self.setCursor(circle_cursor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.last_point = self._normalize_point(event.pos())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing and event.buttons() & Qt.LeftButton:
            current = self._normalize_point(event.pos())
            line = (self.last_point, current, self.brush_color, self.brush_size)
            self.lines.append(line)
            self.last_point = current
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def wheelEvent(self, event):
        """Scroll up/down to change brush size."""
        delta = self.brush_delta if(event.angleDelta().y()> 0) else - self.brush_delta #"event.angleDelta().y()" get's the y deriction of the scroll movement
        self.brush_size = max(self.brush_min_size, min(self.brush_max_size, self.brush_size + int(delta)))
        self.parent().setWindowTitle(self.get_window_title())
        self.set_cursor()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        width, height = self.width(), self.height()
        for line in self.lines:
            start_norm, end_norm, color, size = line
            start = QPointF(start_norm.x() * width, start_norm.y() * height)
            end = QPointF(end_norm.x() * width, end_norm.y() * height)
            pen = QPen(color, size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(start, end)

    def clear(self):
        self.lines = []
        self.update()

    def set_color(self, color: QColor):
        self.brush_color = color #changes the color of the drawing line
        self.set_cursor() #makes the color of the cursor to correspond to the drawing line

    def set_brush_size_arguments(self, brush_min_size: int, brush_max_size: int, brush_delta: int):
        self.brush_min_size = brush_min_size
        self.brush_max_size = brush_max_size
        self.brush_delta = brush_delta


    def _normalize_point(self, point):
        """Convert pixel point → normalized (0–1) coordinates."""
        return QPointF(point.x() / self.width(), point.y() / self.height())
    
    def get_pixel_data(self):
        """Return the current canvas as a NumPy array (H x W x 4, RGBA)."""
        # Grab the widget’s current visual state as a QImage
        qimage = self.grab().toImage()

        # Ensure format is RGBA8888 for consistent bytes layout
        qimage = qimage.convertToFormat(QImage.Format_RGBA8888)

        width = qimage.width()
        height = qimage.height()

        # Get the raw pointer to the image data
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())

        # Create a NumPy array (height, width, 4)
        arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))