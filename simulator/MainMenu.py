import json
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import os

# Constants
NETWORK_VARIABLES = 'network_variables.json'
CHECKBOX_LAYOUT_GEOMETRY = (800, 100, 500, 600)
COMBOBOX_OPTIONS = {
    "Topology": "Random, Clique, Line, Tree, Star",
    "ID Type": "Random, Sequential",
    "Delay": "Random, Constant",
    "Display": "Text, Graph",
    "Root": "No Root, Min ID, Random",
    "Logging": "Short, Medium, Long",
}


class SimulationInProgressWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 600)
        self.setWindowTitle("Simulation In Process")

class MenuWindow(QMainWindow):
    def __init__(self, network_variables_data):
        super().__init__()
        ##self.network_variables_file = network_variables_file
        self.checkbox_values = network_variables_data # Dictionary to store checkbox values with default values
        self.setGeometry(0, 0, 1500, 900)
        self.setWindowTitle("Simulator for Distributed Networks")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the UI components."""
        self.label_values = {}  
        self.create_labels()
        self.create_buttons()
        self.create_options()

    def update_value(self, key: str, value: str):
        """Update the value of the specified label.

        Args:
            key (str): The key to update.
            value (str): The value to set.
        """
        if key == "Max Depth":
            # Ensure the Max Depth is stored as an integer
            self.checkbox_values[key] = int(value) if value.isdigit() else 0
        else:
            self.checkbox_values[key] = value

        if key in self.label_values:
            self.label_values[key].setText(f"{key}: {value}")
            self.label_values[key].setWordWrap(True)


    def create_labels(self):
        """Create labels for displaying network variable values."""
        y_offset = 200
        for key, value in self.checkbox_values.items():
            label = QLabel(f"{key}: {value}", self)
            label.setGeometry(50, y_offset, 1000, 30)
            y_offset += 50
            self.label_values[key] = label
            self.label_values[key].setWordWrap(True)

        title_label = QLabel(self)
        title_label.setText("Distributed Simulator Project")
        title_label.move(500, 25)
        title_label.resize(450, 40)

        info_label = QLabel(self)
        info_label.setText("Please upload your Python algorithm file:")
        info_label.move(50, 100)
        info_label.resize(650, 50)



    def create_buttons(self):
        """Create buttons for the menu."""
        upload_file_button = QPushButton("Upload Python File", self)
        upload_file_button.setGeometry(50, 150, 200, 30)
        upload_file_button.clicked.connect(lambda: self.on_upload_algorithm())

        self.submit_button = QPushButton("Submit", self) 
        self.submit_button.setGeometry(550, 750, 150, 30)
        self.submit_button.clicked.connect(lambda: self.on_submit_all())



    def create_options(self):
        """Create options using combo boxes and number input for computer number."""
        checkbox_layout = QVBoxLayout()
        
        self.add_number_input(checkbox_layout)  # adding the number of computers option
        
        for key, options in COMBOBOX_OPTIONS.items():
            self.add_combo_box(checkbox_layout, key, options)

        # Create Max Depth input (initially hidden)
        self.max_depth_label = QLabel("Max Depth:", self)
        self.max_depth_input = QSpinBox(self)
        self.max_depth_input.setRange(1, 100)  # Set min and max value as needed
        self.max_depth_input.setValue(2)  # Default value

        # Initially hide the Max Depth input
        self.max_depth_label.hide()
        self.max_depth_input.hide()

        # Connect the Max Depth input to update_value
        self.max_depth_input.valueChanged.connect(lambda value: self.update_value("Max Depth", str(value)))

        # Add to the layout
        checkbox_layout.addWidget(self.max_depth_label)
        checkbox_layout.addWidget(self.max_depth_input)

        checkbox_layout.setSpacing(20)
        checkbox_widget = QWidget(self)
        checkbox_widget.setLayout(checkbox_layout)
        checkbox_widget.setGeometry(*CHECKBOX_LAYOUT_GEOMETRY)


    def add_number_input(self, layout):
        """Add number input field to the layout.

        Args:
            layout (QVBoxLayout): The layout to add the number input to.
        """
        number_label = QLabel("Number of Computers", self)
        layout.addWidget(number_label)

        self.number_input = QLineEdit(self)
        self.number_input.setPlaceholderText("Enter a number")
        layout.addWidget(self.number_input)

        # Initially disable the submit button
        self.submit_button.setEnabled(False)

        # Connect textChanged signal to validation logic
        self.number_input.textChanged.connect(self.validate_number_input)


    def validate_number_input(self, value):
        """Validate the number input and enable/disable the submit button."""
        if value.isdigit():
            number = int(value)
            if number > 100:
                QMessageBox.warning(self, 'Error', 'The number of computers cannot exceed 100.', QMessageBox.Ok)
                self.submit_button.setEnabled(False)
            else:
                self.update_value("Number of Computers", value)
                self.submit_button.setEnabled(True)
        else:
            # Disable the button if the input is not a valid number
            self.submit_button.setEnabled(False)
    
    
    def add_combo_box(self, layout, label_text, options):
        """Add a combo box to the layout.

        Args:
            layout (QVBoxLayout): The layout to add the combo box to.
            label_text (str): The label text for the combo box.
            options (str): The options for the combo box, separated by commas.
        """
        combo_label = QLabel(label_text, self)
        layout.addWidget(combo_label)

        combo_box = QComboBox(self)
        items_list = options.split(", ")
        items_list.insert(0, "")
        combo_box.addItems(items_list)
        combo_box.setCurrentText("")
        layout.addWidget(combo_box)

        combo_box.currentTextChanged.connect(lambda value: self.update_value(label_text, value))

        # Connect the topology combo box to show/hide the Max Depth input
        if label_text == "Topology":
            combo_box.currentTextChanged.connect(self.handle_topology_selection)
            
    def handle_topology_selection(self, value):
        """Show or hide the Max Depth input depending on the selected topology."""
        if value == "Tree":
            self.max_depth_label.show()
            self.max_depth_input.show()
        else:
            self.max_depth_label.hide()
            self.max_depth_input.hide()
            # If it's not "Tree", set Max Depth to 0
            self.update_value("Max Depth", "0")
    
    
    def on_upload_algorithm(self):
        """Handle the upload of a Python algorithm file."""
        fname, _ = QFileDialog.getOpenFileName(self, 'Upload Python File', '/home', "Python Files (*.py)")
        if fname:
            _, file_extension = os.path.splitext(fname)
            if file_extension.lower() == '.py':
                self.checkbox_values["Algorithm"] = fname
                self.update_value("Algorithm", fname)
            else:
                QMessageBox.warning(self, 'Error', 'Please select a Python file (.py)', QMessageBox.Ok)

   
    def on_submit_all(self):
        """Handle the final submission of all settings."""
        with open(NETWORK_VARIABLES, "w") as f:
            json.dump(self.checkbox_values, f, indent=4)
        self.close()

def menu(network_variables: dict):
    """Launch the menu application."""
    app = QApplication(sys.argv)
    menu_window = MenuWindow(network_variables)
    menu_window.setWindowIcon(QIcon('./designFiles/app_icon.jpeg'))
    stylesheet_file = os.path.join('./designFiles', 'main_window.qss')
    with open(stylesheet_file, 'r') as f:
        menu_window.setStyleSheet(f.read())
    
    menu_window.show()
    app.exec_()
