import json
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os

class SimulationInProgressWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("Simulation In Process")

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Dictionary to store checkbox values with default values
        self.checkbox_values = {
            "Number of Computers": "11",
            "Topology": "Random",
            "ID Type": "Sequential",
            "Delay": "Random",
            "Display": "Graph",
            "Root": "Random"
        }

        self.setGeometry(0, 0, 1500, 900)
        self.setWindowTitle("Simulator for Distributed Networks")

        self.start_window()

    
    def update_label_value(self, key, value):
        # Update the value of the specified label
        if key in self.label_values:
            self.label_values[key].setText(f"{key}: {value}")


    def start_window(self):
        self.label_values = {}
        y_offset = 200  # Adjust the vertical position of label
        for key, value in self.checkbox_values.items():
            label = QLabel(f"{key}: {value}", self)
            label.setGeometry(50, y_offset, 500, 30)  # Set position and size of label
            y_offset += 30  # Increase vertical position for the next label
            self.label_values[key] = label  # Store label reference

        
        
        # Creating the title label
        title_label = QLabel(self)
        title_label.setText("Distributed Simulator Project")
        title_label.move(500, 25)
        title_label.setFont(QFont("Times font", 20))
        title_label.resize(450, 40)

        # Adding another label under the title
        info_label = QLabel(self)
        info_label.setText("Please upload your Python algorithm file:")
        info_label.move(50, 100)
        info_label.setFont(QFont("Times font", 16))
        info_label.resize(650, 50)

        # Adding a button to upload a file for the algorithm
        upload_file_button = QPushButton("Upload Python File", self)
        upload_file_button.setGeometry(50, 150, 200, 30)
        upload_file_button.clicked.connect(lambda: self.on_upload_algorithm())

        # Adding a final confirmation button
        confirm_button = QPushButton("Submit", self)
        confirm_button.setGeometry(550, 700, 150, 30)
        confirm_button.clicked.connect(lambda: self.on_submit_all())

        # Adding checkboxes
        checkbox_layout = QVBoxLayout()

        self.add_line_edit_button(checkbox_layout, "Change Number of Computers",
                                  self.checkbox_values["Number of Computers"], "Default = 0", "Number of Computers")
        self.add_line_edit_button(checkbox_layout, "Choose Topology",
                                  self.checkbox_values["Topology"], "Random, Clique, Line, Tree, Star", "Topology")
        self.add_line_edit_button(checkbox_layout, "Choose ID Type",
                                  self.checkbox_values["ID Type"], "Random, Sequential", "ID Type")
        self.add_line_edit_button(checkbox_layout, "Enable Delay",
                                  self.checkbox_values["Delay"], "Random, Constant", "Delay")
        self.add_line_edit_button(checkbox_layout, "Choose Display Type",
                                  self.checkbox_values["Display"], "Text, Graph", "Display")
        self.add_line_edit_button(checkbox_layout, "Root Selection",
                                  self.checkbox_values["Root"], "No Root, Min ID, Random", "Root")
        
        checkbox_layout.setSpacing(20)  # Set spacing between checkboxes

        checkbox_widget = QWidget(self)
        checkbox_widget.setLayout(checkbox_layout)
        checkbox_widget.setGeometry(800, 100, 500, 500)  # Increase the width to accommodate larger checkboxes

    def add_line_edit_button(self, layout, label_text, default_value, placeholder_text, checkbox_label):
        # add here the fields that need to be a comboBox
        comboBox_list=["Topology",
                       "ID Type",
                       "Display",
                       "Root",
                       "Delay",
                       ]
        
        if checkbox_label in comboBox_list:
            combo_label = QLabel(label_text, self)
            combo_label.setFont(QFont("Times font", 12))
            layout.addWidget(combo_label)
            
            items_list = placeholder_text.split(", ")
            items_list.insert(0, "")  # add empty string as the first item
            combo_box = QComboBox(self)
            combo_box.addItems(items_list)
            combo_box.setCurrentText("")
            layout.addWidget(combo_box)
            
            def print_selected_value(value):
                if not value=="":
                    #print(f"Chosen {checkbox_label}: {value}")
                    self.checkbox_values[checkbox_label] = value  # Save the value to the dictionary
                    self.update_label_value(checkbox_label, value) # update real time shown value

            combo_box.currentTextChanged.connect(print_selected_value)
            return
            
        # anything that isnt a comboBox
        checkbox = QCheckBox(label_text, self)
        checkbox_font = QFont()
        checkbox_font.setPointSize(12)  # Set larger font size for checkboxes
        checkbox.setFont(checkbox_font)

        line_edit = QLineEdit(self)
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setVisible(False)  # Initially, hide the line edit

        submit_button = QPushButton("Submit", self)
        submit_button.setVisible(False)  # Initially, hide the submit button

        checkbox.stateChanged.connect(lambda state, le=line_edit, sb=submit_button, text=label_text:
                                    self.on_checkbox_state_changed(state, le, sb, text))

        layout.addWidget(checkbox)

        # Using a horizontal layout for the text box and button
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(line_edit)
        hbox_layout.addWidget(submit_button)

        layout.addLayout(hbox_layout)

        def on_submit():
            value = line_edit.text() if line_edit.isVisible() else default_value
            #print(f"Chosen {checkbox_label}: {value}")
            self.checkbox_values[checkbox_label] = value  # Save the value to the dictionary
            self.update_label_value(checkbox_label, value) # update real time shown value
        submit_button.clicked.connect(on_submit)
            
        
        
    def on_checkbox_state_changed(self, state, line_edit, submit_button, label_text):
        line_edit.setVisible(state == 2)  # 2 means checked
        submit_button.setVisible(state == 2)  # Show the line edit and submit button when checked


    def on_upload_algorithm(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Upload Python File', '/home', "Python Files (*.py)")
        if fname:
            _, file_extension = os.path.splitext(fname)
            if file_extension.lower() == '.py':
                with open(fname, 'r') as file:
                    self.checkbox_values["Algorithm"] = fname
            else:
                QMessageBox.warning(self, 'Error', 'Please select a Python file (.py)', QMessageBox.Ok)

    def on_submit_all(self):
        json_data = json.dumps(self.checkbox_values, indent=4)
        with open("network_variables.json", "w") as json_file:
            json_file.write(json_data)

        self.close()


def menu():
    app = QApplication(sys.argv)
    menu_window = MenuWindow()
    menu_window.setWindowIcon(QIcon('./designFiles/app_icon.jpeg'))
    stylesheet_file = os.path.join('./designFiles', 'main_window.qss')
    with open(stylesheet_file, 'r') as f:
        menu_window.setStyleSheet(f.read())
    
    menu_window.show()
    
    app.exec_()
