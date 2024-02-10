from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

class DistributedSimulatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Dictionary to store checkbox values with default values
        self.checkbox_values = {
            "Choose Number of Computers": "0",
            "Choose Topology": "Random",
            "Choose ID Type": "Uniform",
            "Enable Delay": "0",
            "Algorithm": ""  # Algorithm text box value
        }

        self.setGeometry(0, 0, 1500, 900)
        self.setWindowTitle("Distributed Simulator Project")

        self.start_window()

    def start_window(self):
        # Creating the title label
        title_label = QLabel(self)
        title_label.setText("Distributed Simulator Project")
        title_label.move(500, 25)
        title_label.setFont(QFont("Times font", 20))
        title_label.resize(450, 40)

        # Adding another label under the title
        info_label = QLabel(self)
        info_label.setText("Please enter your algorithm in the next text box:")
        info_label.move(50, 100)
        info_label.setFont(QFont("Times font", 16))
        info_label.resize(650, 50)

        # Adding a text box
        algorithm_textbox = QTextEdit(self)
        algorithm_textbox.setGeometry(50, 150, 400, 200)
        algorithm_textbox.setPlainText("Please enter your algorithm here")  # Set initial text if needed
        # How to change the font to be bigger in the text box

        # Adding a button to submit the algorithm
        submit_algorithm_button = QPushButton("Submit Algorithm", self)
        submit_algorithm_button.setGeometry(50, 370, 150, 30)
        submit_algorithm_button.clicked.connect(lambda: self.on_submit_algorithm(algorithm_textbox))

        # Adding checkboxes
        checkbox_layout = QVBoxLayout()

        self.add_line_edit_button(checkbox_layout, "Choose Number of Computers",
                                  self.checkbox_values["Choose Number of Computers"], "Number of Computers:")
        self.add_line_edit_button(checkbox_layout, "Choose Topology",
                                  self.checkbox_values["Choose Topology"], "Topology:")
        self.add_line_edit_button(checkbox_layout, "Choose ID Type",
                                  self.checkbox_values["Choose ID Type"], "ID Type:")
        self.add_line_edit_button(checkbox_layout, "Enable Delay",
                                  self.checkbox_values["Enable Delay"], "Delay:")

        checkbox_layout.setSpacing(20)  # Set spacing between checkboxes

        checkbox_widget = QWidget(self)
        checkbox_widget.setLayout(checkbox_layout)
        checkbox_widget.setGeometry(800, 100, 500, 500)  # Increase the width to accommodate larger checkboxes

    def add_line_edit_button(self, layout, label_text, default_value, placeholder_text):
        checkbox = QCheckBox(label_text, self)
        checkbox_font = QFont()
        checkbox_font.setPointSize(16)  # Set larger font size for checkboxes
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
            print(f"{label_text}: {value}")
            self.checkbox_values[label_text] = value  # Save the value to the dictionary

        submit_button.clicked.connect(on_submit)

    def on_checkbox_state_changed(self, state, line_edit, submit_button, label_text):
        line_edit.setVisible(state == 2)  # 2 means checked
        submit_button.setVisible(state == 2)  # Show the line edit and submit button when checked

    def on_submit_algorithm(self, algorithm_textbox):
        algorithm = algorithm_textbox.toPlainText()
        print(f"Submitted Algorithm: {algorithm}")
        self.checkbox_values["Algorithm"] = algorithm  # Save the algorithm value


def main():
    app = QApplication(sys.argv)
    main_window = DistributedSimulatorApp()
    main_window.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
