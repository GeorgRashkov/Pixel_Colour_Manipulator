from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt

from Convolutional_kernels_initializer import Convolutional_kernels_initializer
from Formula_validation_collections import Convolutional_kernel_lambda_parameters_validation_collections

from Form_elements__order_numbers import Form_elements__order_numbers

class Window_form_convolutional_kernels(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Convolutional kernels")
        self.setMinimumSize(200, 30)


        self.button_apply_cks = QPushButton("Apply")
        self.button_remove_cks = QPushButton("Remove")
        self.button_show_dynamic_variables = QPushButton("Dynamic variables:")
        self.button_show_info = QPushButton("Info")


        #<pixel areas elements to order ids
        self.form_elements__order_ids = Form_elements__order_numbers()
        #pixel areas elements to order ids>

        
        self.label_cks_for_rgb_channel = QLabel("convolutional kernels for rgb channels:")
        self.textArea_cks_for_rgb_channel = QTextEdit()

        self.label_cks_for_image = QLabel("convolutional kernels for image:")
        self.textArea_cks_for_image = QTextEdit()

        self.label_additional_value_formula = QLabel("additional value formula:")
        self.textBox_additional_value_formula = QLineEdit()



        #adding the elements to the window
        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.button_apply_cks)
        h_layout.addWidget(self.button_remove_cks)
        h_layout.addWidget(self.button_show_dynamic_variables)
        h_layout.addWidget(self.button_show_info)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.form_elements__order_ids, alignment=Qt.AlignLeft)
        v_layout.addLayout(h_layout)



        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_cks_for_rgb_channel)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.textArea_cks_for_rgb_channel)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_cks_for_image)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.textArea_cks_for_image)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_additional_value_formula)
        h_layout.addWidget(self.textBox_additional_value_formula)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)


class Window_info_convolutional_kernels(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Convolutional kernels info")
        self.setMinimumSize(200, 30)

        
        self.label_formula = QLabel("formula symbols:")
        self.textArea_formula = QTextEdit()
        self.textArea_formula.setReadOnly(True)

        self.label_cks_for_rgb_channel = QLabel("convolutional kernels for rgb channels:")
        self.textArea_cks_for_rgb_channel = QTextEdit()
        self.textArea_cks_for_rgb_channel.setReadOnly(True)

        self.label_cks_for_image = QLabel("convolutional kernels for image:")
        self.textArea_cks_for_image = QTextEdit()
        self.textArea_cks_for_image.setReadOnly(True)

        self.label_additional_value_formula = QLabel("additional value formula:")
        self.textBox_additional_value_formula = QLineEdit()
        self.textBox_additional_value_formula.setReadOnly(True)

        self.set_text()

        #adding the elements to the window
        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_formula)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.textArea_formula)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_cks_for_rgb_channel)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.textArea_cks_for_rgb_channel)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_cks_for_image)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.textArea_cks_for_image)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_additional_value_formula)
        h_layout.addWidget(self.textBox_additional_value_formula)
        v_layout.addLayout(h_layout)


        self.setLayout(v_layout)


    def set_text(self):
        
        convolutional_kernel_lambda_parameters_validation_collections = Convolutional_kernel_lambda_parameters_validation_collections()
        convolutional_kernels_initializer = Convolutional_kernels_initializer()
        
        text_for__ck_formula = ""
        text_for__ck_formula += f"all characters: {self.get_line(strings = convolutional_kernel_lambda_parameters_validation_collections.allowed_chars)}"
        text_for__ck_formula += f"special characters: {self.get_line(convolutional_kernel_lambda_parameters_validation_collections.allowed_special_chars)}"
        text_for__ck_formula += f"collection variable characters: {self.get_line(convolutional_kernel_lambda_parameters_validation_collections.allowed_variable_collection_chars)}"
        text_for__ck_formula += f"operator characters: {self.get_line(convolutional_kernel_lambda_parameters_validation_collections.allowed_operator_chars)}"
        text_for__ck_formula += f"number characters: {self.get_line(convolutional_kernel_lambda_parameters_validation_collections.allowed_num_chars)}"
        text_for__ck_formula += f"formula names: {self.get_line(convolutional_kernel_lambda_parameters_validation_collections.allowed_special_formulas)}"
        self.textArea_formula.setText(text_for__ck_formula)

        text_for__ck_for_rgb_channel = ""
        text_for__ck_for_rgb_channel += f"all parameters: {self.get_line(convolutional_kernels_initializer.ck_for_rgb_channel_valid_parameters)}"
        text_for__ck_for_rgb_channel += f"required parameters: {self.get_line(convolutional_kernels_initializer.ck_for_rgb_channel_required_parameters)}"
        text_for__ck_for_rgb_channel += f"formula parameters: {self.get_line(convolutional_kernels_initializer.ck_for_rgb_channel_lambda_parameters)}"
        text_for__ck_for_rgb_channel += f"positive int parameters: {self.get_line(convolutional_kernels_initializer.ck_for_rgb_channel_positive_int_parameters)}"
        text_for__ck_for_rgb_channel += f"positive int parameters in range: {self.get_line(convolutional_kernels_initializer.ck_for_rgb_channel_positive_int_in_range_parameters)}"
        self.textArea_cks_for_rgb_channel.setText(text_for__ck_for_rgb_channel)

        text_for__ck_for_image = ""
        text_for__ck_for_image += f"all parameters: {self.get_line(convolutional_kernels_initializer.ck_for_image_valid_parameters)}"
        text_for__ck_for_image += f"required parameters: {self.get_line(convolutional_kernels_initializer.ck_for_image_required_parameters)}"
        text_for__ck_for_image += f"positive int parameters: {self.get_line(convolutional_kernels_initializer.ck_for_image_positive_int_parameters)}"
        text_for__ck_for_image += f"formula colletion parameters: {self.get_line(convolutional_kernels_initializer.ck_for_image_lambda_collection_parameters)}"
        self.textArea_cks_for_image.setText(text_for__ck_for_image)

        text_for__additional_value_formula = "formula without parameters"
        self.textBox_additional_value_formula.setText(text_for__additional_value_formula)
    
    def get_line(self, strings:list[str]):
        
        str_line = f"[ {"; ".join(strings)} ]\n\n" 
        return str_line