from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QRadioButton, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QButtonGroup
from PyQt5.QtCore import Qt

class Window_Form_draw_formula(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.label_draw_type = QLabel("draw type")
        self.radioButton_contour = QRadioButton("contour")
        self.radioButton_contour.setChecked(True)
        self.radioButton_plot = QRadioButton("plot")
        self.radioButton_scatter = QRadioButton("scatter")

        self.radioButtonGroup_draw_type = QButtonGroup()
        self.radioButtonGroup_draw_type.addButton(self.radioButton_contour)
        self.radioButtonGroup_draw_type.addButton(self.radioButton_plot)
        self.radioButtonGroup_draw_type.addButton(self.radioButton_scatter)


        self.label_resize_type = QLabel("resize type")
        self.radioButton_equal = QRadioButton("equal")
        self.radioButton_equal.setChecked(True)
        self.radioButton_tight = QRadioButton("tight")
       

        self.radioButtonGroup_resize_type = QButtonGroup()
        self.radioButtonGroup_resize_type.addButton(self.radioButton_equal)
        self.radioButtonGroup_resize_type.addButton(self.radioButton_tight)

        
        self.label_x_values = QLabel("x values| ")
        self.label_x_start_value = QLabel("start")
        self.textBox_x_start_value = QLineEdit("-10")

        self.label_x_end_value = QLabel("end")
        self.textBox_x_end_value = QLineEdit("10")

        self.label_x_values_count = QLabel("count")
        self.textBox_x_values_count = QLineEdit("1000")

        
        self.label_y_values = QLabel("y values| ")
        self.label_y_start_value = QLabel("start")
        self.textBox_y_start_value = QLineEdit("-10")

        self.label_y_end_value = QLabel("end")
        self.textBox_y_end_value = QLineEdit("10")

        self.label_y_values_count = QLabel("count")
        self.textBox_y_values_count = QLineEdit("1000")



        self.label_sub_expressions = QLabel("sub expressions")
        self.textBox_sub_expressions = QLineEdit()

        self.label_main_expressions = QLabel("main expressions")

        self.label_X = QLabel("X")
        self.textBox_X = QLineEdit()

        self.label_Y = QLabel("Y")
        self.textBox_Y = QLineEdit()

        self.label_Z = QLabel("Z")
        self.textBox_Z = QLineEdit()



        self.label_colour = QLabel("colour")
        
        self.label_red = QLabel("r")
        self.textBox_red = QLineEdit("0")

        self.label_green = QLabel("g")
        self.textBox_green = QLineEdit("0")

        self.label_blue = QLabel("b")
        self.textBox_blue = QLineEdit("0")



        self.label_line_width = QLabel("width")
        self.textBox_line_width = QLineEdit("2")

        self.label_levels = QLabel("levels")
        self.textBox_levels = QLineEdit("0")

        
        self.label_drawing_id = QLabel("drawing id")
        self.textBox_drawing_id = QLineEdit()
        self.button_add_draw_formula = QPushButton("Add")
        self.button_remove_draw_formula = QPushButton("Remove")
        self.button_show_drawing = QPushButton("Show")


        self.text_area = QPlainTextEdit()
        self.text_area.setReadOnly(True)



        container = QWidget()
        container.setMaximumWidth(400)

        h_main_layout = QHBoxLayout()
        v_layout = QVBoxLayout(container)
        v_layout.setAlignment(Qt.AlignTop)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_draw_type) 
        h_layout.addWidget(self.radioButton_contour)
        h_layout.addWidget(self.radioButton_plot)
        h_layout.addWidget(self.radioButton_scatter)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_resize_type) 
        h_layout.addWidget(self.radioButton_equal)
        h_layout.addWidget(self.radioButton_tight)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_x_values)
        h_layout.addWidget(self.label_x_start_value)
        h_layout.addWidget(self.textBox_x_start_value)
        h_layout.addWidget(self.label_x_end_value)
        h_layout.addWidget(self.textBox_x_end_value)
        h_layout.addWidget(self.label_x_values_count)
        h_layout.addWidget(self.textBox_x_values_count)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_y_values)
        h_layout.addWidget(self.label_y_start_value)
        h_layout.addWidget(self.textBox_y_start_value)
        h_layout.addWidget(self.label_y_end_value)
        h_layout.addWidget(self.textBox_y_end_value)
        h_layout.addWidget(self.label_y_values_count)
        h_layout.addWidget(self.textBox_y_values_count)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_sub_expressions)
        h_layout.addWidget(self.textBox_sub_expressions)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_main_expressions)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_X)
        h_layout.addWidget(self.textBox_X)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_Y)
        h_layout.addWidget(self.textBox_Y)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_Z)
        h_layout.addWidget(self.textBox_Z)
        v_layout.addLayout(h_layout)


        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_colour)
        h_layout.addWidget(self.label_red)
        h_layout.addWidget(self.textBox_red)
        h_layout.addWidget(self.label_green)
        h_layout.addWidget(self.textBox_green)
        h_layout.addWidget(self.label_blue)
        h_layout.addWidget(self.textBox_blue)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_line_width)
        h_layout.addWidget(self.textBox_line_width)
        h_layout.addWidget(self.label_levels)
        h_layout.addWidget(self.textBox_levels)
        v_layout.addLayout(h_layout)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label_drawing_id)
        h_layout.addWidget(self.textBox_drawing_id)
        h_layout.addWidget(self.button_add_draw_formula)
        h_layout.addWidget(self.button_remove_draw_formula)
        h_layout.addWidget(self.button_show_drawing)
        v_layout.addLayout(h_layout)

        h_main_layout.addWidget(container)
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.text_area)
        h_main_layout.addLayout(h_layout)

        self.setLayout(h_main_layout)





        self.all_draw_elements:list[QWidget] = []

        self.all_draw_elements.append(self.textBox_x_start_value)
        self.all_draw_elements.append(self.textBox_x_end_value)
        self.all_draw_elements.append(self.textBox_x_values_count)
        self.all_draw_elements.append(self.textBox_y_start_value)
        self.all_draw_elements.append(self.textBox_y_end_value)
        self.all_draw_elements.append(self.textBox_y_values_count)

        self.all_draw_elements.append(self.textBox_sub_expressions)
        self.all_draw_elements.append(self.textBox_X)
        self.all_draw_elements.append(self.textBox_Y)
        self.all_draw_elements.append(self.textBox_Z)

        self.all_draw_elements.append(self.textBox_red)
        self.all_draw_elements.append(self.textBox_green)
        self.all_draw_elements.append(self.textBox_blue)
        
        self.all_draw_elements.append(self.textBox_line_width)
        self.all_draw_elements.append(self.textBox_levels)




        self.contour_draw_elements:list[QWidget] = []

        self.contour_draw_elements.append(self.textBox_x_start_value)
        self.contour_draw_elements.append(self.textBox_x_end_value)
        self.contour_draw_elements.append(self.textBox_x_values_count)
        self.contour_draw_elements.append(self.textBox_y_start_value)
        self.contour_draw_elements.append(self.textBox_y_end_value)
        self.contour_draw_elements.append(self.textBox_y_values_count)

        self.contour_draw_elements.append(self.textBox_sub_expressions)
        self.contour_draw_elements.append(self.textBox_Z)

        self.contour_draw_elements.append(self.textBox_red)
        self.contour_draw_elements.append(self.textBox_green)
        self.contour_draw_elements.append(self.textBox_blue)
        
        self.contour_draw_elements.append(self.textBox_line_width)
        self.contour_draw_elements.append(self.textBox_levels)




        self.plot_draw_elements:list[QWidget] = []

        self.plot_draw_elements.append(self.textBox_x_start_value)
        self.plot_draw_elements.append(self.textBox_x_end_value)
        self.plot_draw_elements.append(self.textBox_x_values_count)
        self.plot_draw_elements.append(self.textBox_y_start_value)
        self.plot_draw_elements.append(self.textBox_y_end_value)
        self.plot_draw_elements.append(self.textBox_y_values_count)

        self.plot_draw_elements.append(self.textBox_sub_expressions)
        self.plot_draw_elements.append(self.textBox_X)
        self.plot_draw_elements.append(self.textBox_Y)

        self.plot_draw_elements.append(self.textBox_red)
        self.plot_draw_elements.append(self.textBox_green)
        self.plot_draw_elements.append(self.textBox_blue)
        
        self.plot_draw_elements.append(self.textBox_line_width)




        self.scatter_draw_elements:list[QWidget] = []

        self.scatter_draw_elements.append(self.textBox_x_start_value)
        self.scatter_draw_elements.append(self.textBox_x_end_value)
        self.scatter_draw_elements.append(self.textBox_x_values_count)
        self.scatter_draw_elements.append(self.textBox_y_start_value)
        self.scatter_draw_elements.append(self.textBox_y_end_value)
        self.scatter_draw_elements.append(self.textBox_y_values_count)

        self.scatter_draw_elements.append(self.textBox_sub_expressions)
        self.scatter_draw_elements.append(self.textBox_X)
        self.scatter_draw_elements.append(self.textBox_Y)

        self.scatter_draw_elements.append(self.textBox_red)
        self.scatter_draw_elements.append(self.textBox_green)
        self.scatter_draw_elements.append(self.textBox_blue)
        
        self.scatter_draw_elements.append(self.textBox_line_width)


    def enable_only_contour_draw_elements(self):
            
        for draw_element in self.all_draw_elements:
            if(draw_element in self.contour_draw_elements):
                if(draw_element.isEnabled()==False):
                    draw_element.setDisabled(False)
            elif(draw_element.isEnabled()==True):
                draw_element.setDisabled(True)


    def enable_only_plot_draw_elements(self):
        for draw_element in self.all_draw_elements:
            if(draw_element in self.plot_draw_elements):
                if(draw_element.isEnabled()==False):
                    draw_element.setDisabled(False)
            elif(draw_element.isEnabled()==True):
                draw_element.setDisabled(True)

    def enable_only_scatter_draw_elements(self):
        for draw_element in self.all_draw_elements:
            if(draw_element in self.scatter_draw_elements):
                if(draw_element.isEnabled()==False):
                    draw_element.setDisabled(False)
            elif(draw_element.isEnabled()==True):
                draw_element.setDisabled(True)

        


       