from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer

# create graph visualization layout
def layoutCreation(self):
    self.choice_combo = QComboBox()
    self.choice_combo.addItems(self.get_nx_layouts())
    self.choice_combo.currentTextChanged.connect(self.set_nx_layout)

    self.regenarate_button = QPushButton("regenarate")
    self.regenarate_button.clicked.connect(self.regenarate_clicked)

    main_layout = QVBoxLayout(self)
    main_layout.addWidget(self.choice_combo)
    main_layout.addWidget(self.regenarate_button)
    main_layout.addWidget(self.view)

    slider_h_layout = QHBoxLayout()

    self.slider = QSlider(Qt.Horizontal)
    self.slider.setRange(-2000, -1)
    self.slider.setValue(-1000)
    self.slider.valueChanged.connect(self.update_timer_interval)

    self.slider_label = QLabel(f"{abs(self.slider.value() / 1000)} seconds per tick")
    self.slider.valueChanged.connect(self.update_slider_label)

    self.timer = QTimer(self)
    self.timer.timeout.connect(lambda: self.change_node_color(1))

    self.run_checkbox = QCheckBox()
    self.run_checkbox.stateChanged.connect(self.toggle_timer)
    run_label = QLabel("Run")
    slider_h_layout.addWidget(self.run_checkbox)
    slider_h_layout.addWidget(run_label)
    slider_h_layout.addWidget(self.slider)

    buttons_layout = QGridLayout()
    self.next_phase_button = QPushButton("Next Phase")
    self.next_phase_button.clicked.connect(lambda: self.change_node_color(1))
    self.next_5_phase_button = QPushButton("Next 5 Phases")
    self.next_5_phase_button.clicked.connect(lambda: self.change_node_color(5))
    self.undo_button = QPushButton('Undo', self)
    self.undo_button.clicked.connect(self.undo_change)
    self.reset_button = QPushButton('Reset', self)
    self.reset_button.clicked.connect(self.reset)

    buttons_layout.addWidget(self.next_phase_button, 0, 0)
    buttons_layout.addWidget(self.next_5_phase_button, 0, 1)
    buttons_layout.addWidget(self.undo_button, 1, 0)
    buttons_layout.addWidget(self.reset_button, 1, 1)
    buttons_layout.addWidget(self.slider_label, 0, 2)

    # Add the horizontal layouts to the main layout
    main_layout.addLayout(slider_h_layout)
    main_layout.addLayout(buttons_layout)