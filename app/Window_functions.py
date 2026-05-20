from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
import numpy as np


#The returned numpy array has shape (Height, Width, 3[RGB])
def get_rgb_pixel_values_from_window(window:QWidget) -> np.ndarray[np.uint8]:
    #Return the current canvas as a NumPy array (H x W x 4, RGBA).
    # Grab the widget’s current visual state as a QImage
    qimage = window.grab().toImage()

    # Ensure format is RGBA8888 for consistent bytes layout
    qimage = qimage.convertToFormat(QImage.Format_RGBA8888)

    width = qimage.width()
    height = qimage.height()
                
    # Get the raw pointer to the image data
    ptr = qimage.bits()
    ptr.setsize(qimage.byteCount())

    rgba_values_from_window:np.ndarray = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))# Create a NumPy array (height, width, 4)
    rgb_values_from_window = rgba_values_from_window[:,:,:3].copy()# a  NumPy array (height, width, 3); each value in the most inner arrays will contain 3 elements and 2 of them will be always 0

    return rgb_values_from_window