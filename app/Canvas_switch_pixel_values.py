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
        self.rectangles  = []  # each item has (x, y, size, color)
        
        self.brush_color = QColor(255, 255, 255)
        self.brush_size = 5 #initial brush size
        self.brush_min_size = 5
        self.brush_max_size = 200
        self.brush_delta = 10 #the value which will be use to increase or decrease the brush size

        self.is_first_half = True #the first half and the second half will be the pixel values to switch (the variable is controlled form the outside)
        
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
        painter.drawRect(self.brush_size//2, self.brush_size//2, self.brush_size, self.brush_size)  # (x, y, w, h)
        painter.end()

        # Create a cursor from this pixmap
        circle_cursor = QCursor(pixmap, self.brush_size, self.brush_size)  # hotspot at center

        # Apply the created cursor to the whole window
        self.setCursor(circle_cursor)

    def wheelEvent(self, event):#Scroll up/down to change brush size.
        
        if(self.is_first_half==True):

            delta = self.brush_delta if(event.angleDelta().y()> 0) else - self.brush_delta #"event.angleDelta().y()" get's the y deriction of the scroll movement
            self.brush_size = max(self.brush_min_size, min(self.brush_max_size, self.brush_size + int(delta)))
            self.parent().setWindowTitle(self.get_window_title())
            self.set_cursor()
            self.update()#calls `paintEvent` indirectly
    
    def mousePressEvent(self, event):
        self.mousePressed.emit(event.pos(), event.button())#emiting the signal will call a function specified from outside the class
   

    #this function decides where to drawn the rectangle and determines its size
    def left_mouse_button_pressed(self, x: int, y: int, r_channel:bool, g_channel:bool, b_channel:bool):#this is called from the outside the class
        
        x, y, size = self.set_and_get_coordinates_and_size_of_drawn_rectangle(x, y)
        self.set_colour_of_drawn_rectangle(r_channel, g_channel, b_channel)
        self.set_cursor()

        self.rectangles.append((x, y, size, QColor(self.brush_color)))
        self.update()#calls `paintEvent` indirectly

        return x, y, size

    def set_and_get_coordinates_and_size_of_drawn_rectangle(self, x:int, y:int):

        size = self.brush_size
        x = x - size // 2
        y = y - size // 2

        #< this code makes sure that the values of x, y and the size of the rectangle will always be inside the canvas    
        x = max(0, min(x, self.width() - size))#this is the horizontal position of the top left corner of the drawn rectangle
        y = max(0, min(y, self.height() - size))#this is the vertical position of the top left corner of the drawn rectangle

        w = self.width()#cavas width
        h = self.height()#canvas height
        size =  min(size, min(w,h))#this is the size of the rectangle
        #< this code makes sure that the values of x, y and the size of the rectangle will always be inside the canvas>
        
        return x, y, size

    def set_colour_of_drawn_rectangle(self, r_channel:bool, g_channel:bool, b_channel:bool):
        
        red = 255 if r_channel==True else 0
        green = 255 if g_channel==True else 0
        blue = 255 if b_channel==True else 0
        
        self.brush_color = QColor(red, green, blue)

        
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for x, y, size, color in self.rectangles:
            pen = QPen(color)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(x, y, size, size)

        painter.end()
    
    def clear(self):
        self.rectangles.clear()
        self.update()#calls `paintEvent` indirectly

    def set_color(self, color: QColor):
        self.brush_color = color #changes the color of the drawing line
        self.set_cursor() #makes the color of the cursor to correspond to the drawing line

    def set_brush_size_arguments(self, brush_min_size: int, brush_max_size: int, brush_delta: int):
        self.brush_min_size = brush_min_size
        self.brush_max_size = brush_max_size
        self.brush_delta = brush_delta
    
    # each element in `rectangle_pairs` must be a list of two rectangles
    # a rectangle looks like this f"[ [{x}, {y}, {size}], [{int(use_red)}, {int(use_green)}, {int(use_blue)}] ]" (all elements in the rectangle must be integers)
    def insert_rectangle_pairs(self, rectangle_pairs: list):
        
        for i in range(0, len(rectangle_pairs)):
            for j in range(0, len(rectangle_pairs[i])):

                rectangle = rectangle_pairs[i][j]
                coordinates = rectangle[0]
                rgb_values = rectangle[1]

                x = coordinates[0]
                y = coordinates[1]
                size = coordinates[2]

                r = rgb_values[0]
                g = rgb_values[1]
                b = rgb_values[2]
        
                self.rectangles.append((x, y, size, QColor(r*255, g*255, b*255)))
        
   