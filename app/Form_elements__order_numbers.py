from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QRadioButton, QButtonGroup, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIntValidator

from Number_format_checker import check_for_int_format
from Enums import Enum_order
from Order_obj import Order_obj


class Form_elements__order_numbers(QWidget):
    def __init__(self, text_for_button_order:str = "order ids: ", text_boxes_max_lenght: int = 3, text_boxes_max_width: int = 30):
        super().__init__()

        int_validator = QIntValidator()
        
        self.button_order_nums = QPushButton(text_for_button_order)

        self.label_order_nums__start = QLabel("start| ")
        self.textBox_order_nums__start = QLineEdit()
        self.textBox_order_nums__start.setMaximumWidth(text_boxes_max_width)
        self.textBox_order_nums__start.setMaxLength(text_boxes_max_lenght)
        self.textBox_order_nums__start.setValidator(int_validator)

        self.label_order_nums__end = QLabel("end| ")
        self.textBox_order_nums__end = QLineEdit()
        self.textBox_order_nums__end.setMaximumWidth(text_boxes_max_width)
        self.textBox_order_nums__end.setMaxLength(text_boxes_max_lenght)
        self.textBox_order_nums__end.setValidator(int_validator)

        self.label_order_nums__step = QLabel("step| ")
        self.textBox_order_nums__step = QLineEdit()
        self.textBox_order_nums__step.setMaximumWidth(text_boxes_max_width)
        self.textBox_order_nums__step.setMaxLength(text_boxes_max_lenght)
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

