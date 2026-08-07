from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIntValidator

from Number_format_checker import check_for_int_format
from Enums import Enum_order
from Order_obj import Order_obj


class Form_elements__order_numbers(QWidget):
    def __init__(self):
        super().__init__()

        int_validator = QIntValidator()
        
        self.button_order_nums = QPushButton("order ids: ")
        self.button_order_nums.setMaximumWidth(70)

        self.label_order_nums__start = QLabel("start| ")
        self.textBox_order_nums__start = QLineEdit()
        self.textBox_order_nums__start.setMaximumWidth(30)
        self.textBox_order_nums__start.setMaxLength(3)
        self.textBox_order_nums__start.setValidator(int_validator)

        self.label_order_nums__end = QLabel("end| ")
        self.textBox_order_nums__end = QLineEdit()
        self.textBox_order_nums__end.setMaximumWidth(30)
        self.textBox_order_nums__end.setMaxLength(3)
        self.textBox_order_nums__end.setValidator(int_validator)

        self.label_order_nums__step = QLabel("step| ")
        self.textBox_order_nums__step = QLineEdit()
        self.textBox_order_nums__step.setMaximumWidth(30)
        self.textBox_order_nums__step.setMaxLength(3)
        self.textBox_order_nums__step.setValidator(int_validator)

        self.radioButton_ascending = QRadioButton("ascending")
        self.radioButton_descending = QRadioButton("descending")
        self.radioButton_random = QRadioButton("random")
        self.radioButtons_group_order = QButtonGroup()
        self.radioButtons_group_order.addButton(self.radioButton_ascending)
        self.radioButtons_group_order.addButton(self.radioButton_descending)
        self.radioButtons_group_order.addButton(self.radioButton_random)
        self.radioButton_ascending.setChecked(True)



        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_order_nums)
        h_layout.addWidget(self.textBox_order_nums__start)
        h_layout.addWidget(self.label_order_nums__start)
        h_layout.addWidget(self.textBox_order_nums__end)
        h_layout.addWidget(self.label_order_nums__end)
        h_layout.addWidget(self.textBox_order_nums__step)
        h_layout.addWidget(self.label_order_nums__step)
        h_layout.addWidget(self.radioButton_ascending)
        h_layout.addWidget(self.radioButton_descending)
        h_layout.addWidget(self.radioButton_random)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)
    
    
    #<set text for different elements
    def set_text_for_button_order(self, text:str):
        self.button_order_nums.setText(text)

    def set_text_for_radio_button_ascending(self, text:str):
        self.radioButton_ascending.setText(text)

    def set_text_for_radio_button_descending(self, text:str):
        self.radioButton_descending.setText(text)

    def set_text_for_radio_button_random(self, text:str):
        self.radioButton_random.setText(text)
    #set text for different elements>


    #<set max width for different elements
    def set_max_width_for_button_order(self, width:int):
        self.button_order_nums.setMaximumWidth(width)

    def set_max_width_for_text_boxes(self, width:int):
        self.textBox_order_nums__start.setMaximumWidth(width)
        self.textBox_order_nums__end.setMaximumWidth(width)
        self.textBox_order_nums__step.setMaximumWidth(width)
    #set max width for different elements>


    #set max number af characters for each text
    def set_max_length_for_text_boxes(self, width:int):
        self.textBox_order_nums__start.setMaxLength(width)
        self.textBox_order_nums__end.setMaxLength(width)
        self.textBox_order_nums__step.setMaxLength(width)


    #remove the radio button which sorts the elements in ascending order
    def remove_radio_button_ascending(self):
        self.radioButton_ascending.setChecked(False)
        self.radioButton_descending.setChecked(True)
        self.layout().removeWidget(self.radioButton_ascending)
        self.radioButton_ascending.deleteLater()
        self.radioButton_ascending = None


    def get__order_obj(self) -> Order_obj:

        start_txt = self.textBox_order_nums__start.text()
        end_txt = self.textBox_order_nums__end.text()
        step_txt = self.textBox_order_nums__step.text()

        is_start_txt_valid = check_for_int_format(txt_value=start_txt)
        is_end_txt_valid = check_for_int_format(txt_value=end_txt)
        is_step_txt_valid = check_for_int_format(txt_value=step_txt)

        if(is_start_txt_valid == False):
            print("error: the start index was in wrong format, only integers are allowed")
            return None
        if(is_end_txt_valid == False):
            print("error: the end index was in wrong format, only integers are allowed")
            return None
        if(is_step_txt_valid == False):
            print("error: the step index was in wrong format, only integers are allowed")
            return None
            
        start = int(start_txt) if start_txt!="" else None
        end = int(end_txt) if end_txt!="" else None
        step = int(step_txt) if step_txt!="" else None

        order_type = Enum_order.ascending
        if(self.radioButton_descending.isChecked() == True):
            order_type = Enum_order.descending
        elif(self.radioButton_random.isChecked() == True):
            order_type = Enum_order.random

        order_obj = Order_obj(order_type=order_type, start=start, end=end, step=step)
        return order_obj

