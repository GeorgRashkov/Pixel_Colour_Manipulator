from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QTextEdit
)
import re
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QKeySequence

class FormWindow_SwichPixelValies(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Draw mask")
        self.setMinimumSize(100, 100)
        self.resize(800, 500)             
        
        #< RGB check boxes
        self.r_check_box = QCheckBox()
        self.r_label = QLabel("red channel")
        self.r_label.setBuddy(self.r_check_box)

        self.g_check_box = QCheckBox()
        self.g_label = QLabel("green channel")
        self.g_label.setBuddy(self.g_check_box)

        self.b_check_box = QCheckBox()
        self.b_label = QLabel("blue channel")
        self.b_label.setBuddy(self.b_check_box)
        #RGB check boxes>

        self.text_area = Text_area()

        self.button_update_canvas = QPushButton("Update canvas")
        self.button_update_canvas_and_text_area = QPushButton("Update canvas and text")
        self.button_clear_canvas = QPushButton("Clear canvas")
        self.button_apply = QPushButton("Apply")
        



        v_layout = QVBoxLayout()
        
        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        h_layout.addWidget(self.r_label)
        h_layout.addWidget(self.r_check_box)
        h_layout.addWidget(self.g_label)
        h_layout.addWidget(self.g_check_box)
        h_layout.addWidget(self.b_label)
        h_layout.addWidget(self.b_check_box)       
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_area)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_update_canvas)
        h_layout.addWidget(self.button_update_canvas_and_text_area)
        h_layout.addWidget(self.button_clear_canvas)
        h_layout.addWidget(self.button_apply)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)



class Text_area(QTextEdit):

    regex = re.compile("[0-9\[\], ]")
    
    def keyPressEvent(self, event):
        
        # Allow standard shortcuts (Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+A, etc.)
        if event.matches(QKeySequence.Copy) or \
            event.matches(QKeySequence.Paste) or \
            event.matches(QKeySequence.Cut) or \
            event.matches(QKeySequence.SelectAll) or \
            event.matches (QKeySequence.Redo) or \
            event.matches (QKeySequence.Undo):
            super().keyPressEvent(event)
            return
        
        # Allow only specific symbols to be used in the text area
        text = event.text()
        if self.regex.fullmatch(text) or event.key() in (
            Qt.Key_Backspace, Qt.Key_Delete,#delete options 
            Qt.Key_Return, Qt.Key_Enter,#new line option
            Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down#move options        
        ):
            super().keyPressEvent(event)
    
    def append_on_same_line(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)       