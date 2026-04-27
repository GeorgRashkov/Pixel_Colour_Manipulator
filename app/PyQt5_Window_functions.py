from PyQt5.QtWidgets import QWidget

def open_or_minimize_window(window:QWidget):
    if(window.isVisible()==False):
        window.show()
    elif(window.isMinimized()):
        window.showNormal()
    else:
        window.showMinimized()


def open_or_minimize_windows(windows:list[QWidget]):
    
    are_all_windows_openned = True
    for window in windows:

        if(window.isVisible()==False):
            are_all_windows_openned = False
            window.show()

        elif(window.isMinimized()):
            are_all_windows_openned = False
            window.showNormal()
    
    if(are_all_windows_openned == True):
        for window in windows:
            window.showMinimized()