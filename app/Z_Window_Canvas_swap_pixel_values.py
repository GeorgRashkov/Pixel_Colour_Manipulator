from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QCursor, QPixmap
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtCore import pyqtSignal, QPoint


class DrawingWidget(QWidget):
    
    mousePressed = pyqtSignal(QPoint, Qt.MouseButton) #this is a mouse button signal which will be used from outside the class to determine which outside function to call

    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")
        self.last_point = QPointF()
        self.rectangles  = []  # each item has (x, y, width, height, color)
        
        self.brush_color = QColor(0, 0, 0)
        self.brush_width = 101 #initial brush width
        self.brush_height = 101 #initial brush height
        self.brush_min_width = 1
        self.brush_max_width = 999
        self.brush_min_height = 1
        self.brush_max_height = 999
        #self.width_height_percentage_difference = self.brush_width/self.brush_height
        self.brush_delta_width = 50 #the value which will be use to increase or decrease the brush width
        self.brush_delta_height = 50 #the value which will be use to increase or decrease the brush height
        
        self.set_cursor()
      

    def get_window_title(self):
        return f"Brush width: {self.brush_width} | Brush_height: {self.brush_height}"
    
    def set_cursor(self):

        # Create a transparent pixmap with size width,height
        pixmap = QPixmap(self.brush_width*2, self.brush_height*2)
        pixmap.fill(Qt.transparent)

        # Draw a circle on the pixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.brush_color)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawRect(self.brush_width//2, self.brush_height//2, self.brush_width, self.brush_height)  # (x, y, w, h)
        painter.end()

        # Create a cursor from this pixmap
        square_cursor = QCursor(pixmap, self.brush_width, self.brush_height)  # hotspot at center

        # Apply the created cursor to the whole window
        self.setCursor(square_cursor)

    def wheelEvent(self, event):#Scroll up/down to change brush size.

            delta_width = self.brush_delta_width if(event.angleDelta().y()> 0) else - self.brush_delta_width #"event.angleDelta().y()" get's the y deriction of the scroll movement
            delta_height = self.brush_delta_height if(event.angleDelta().y()> 0) else - self.brush_delta_height #"event.angleDelta().y()" get's the y deriction of the scroll movement

            new_brush_width = int(self.brush_width + delta_width)
            new_brush_height = int(self.brush_height + delta_height)
            
            if(new_brush_width >= self.brush_min_width and new_brush_width <= self.brush_max_width and
               new_brush_height >= self.brush_min_height and new_brush_height <= self.brush_max_height):
                
                self.brush_width = new_brush_width
                self.brush_height = new_brush_height
            
                self.parent().setWindowTitle(self.get_window_title())
                self.set_cursor()
                self.update()#calls `paintEvent` indirectly
    
    def mousePressEvent(self, event):
        self.mousePressed.emit(event.pos(), event.button())#emiting the signal will call a function specified from outside the class
   

    #this function decides where to drawn the rectangle and determines its size
    def left_mouse_button_pressed(self, x: int, y: int):#this is called from outside the class
        
        x, y, width, height = self.set_and_get_coordinates_of_drawn_rectangle(x, y)
        self.set_cursor()

        self.rectangles.append((x, y, width, height, QColor(self.brush_color)))
        self.update()#calls `paintEvent` indirectly

        return x, y, width, height

    def set_and_get_coordinates_of_drawn_rectangle(self, x:int, y:int):

        width = self.brush_width
        height = self.brush_height
        x = x - width // 2
        y = y - height // 2

        #< this code makes sure that the values of width, height, x, y of the rectangle will always be inside the canvas    
        x = max(0, min(x, self.width() - width))#this is the horizontal position of the top left corner of the drawn rectangle
        y = max(0, min(y, self.height() - height))#this is the vertical position of the top left corner of the drawn rectangle

        w = self.width()#cavas width
        h = self.height()#canvas height
        width =  min(width, min(w,h))#this is the width of the rectangle
        height =  min(height, min(w,h))#this is the height of the rectangle
        # this code makes sure that the values of width, height, x, y of the rectangle will always be inside the canvas  >
        
        return x, y, width, height

    def set_colour_of_drawn_rectangle(self, r_channel:bool, g_channel:bool, b_channel:bool):
        
        red = 255 if r_channel==True else 0
        green = 255 if g_channel==True else 0
        blue = 255 if b_channel==True else 0
        
        self.brush_color = QColor(red, green, blue)

        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for x, y, width, height, color in self.rectangles:
            pen = QPen(color)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(x, y, width, height)

        painter.end()
    
    def clear(self):
        self.rectangles.clear()
        self.update()#calls `paintEvent` indirectly

    def set_brush_width_arguments(self, brush_min_width: int, brush_max_width: int, brush_delta_width: int):
        self.brush_min_width = brush_min_width
        self.brush_max_width = brush_max_width
        self.brush_delta_width = brush_delta_width
    
    def set_brush_height_arguments(self, brush_min_height: int, brush_max_height: int, brush_delta_height: int):
        self.brush_min_height = brush_min_height
        self.brush_max_height = brush_max_height
        self.brush_delta_height = brush_delta_height
    
    def set_brush_size(self, brush_width, brush_height):
        self.brush_width = brush_width
        self.brush_height = brush_height
        self.set_cursor()

    
    def insert_rectangle(self, x: int, y: int, width: int, height: int):
        self.rectangles.append((x, y, width, height, QColor(0, 0, 0)))
        
   