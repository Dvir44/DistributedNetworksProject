import math
import random

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer, QPointF

from visualizations.edge import Edge


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
    
    
    
def set_nx_layout_large_graph(self, positions):
        for node, pos in positions.items():
            window_size = self.size()
            item = self.nodes_map[node]
            x = random.randint(item.radius, window_size.width() - item.radius)
            y = random.randint(item.radius, window_size.height() - item.radius)
            item.setPos(QPointF(x, y))

        for edge in self.scene.items():
            if isinstance(edge, Edge):
                edge.boldness = -1
                edge.update()
                
                
def set_nx_layout_circular_graph(self, positions):
        for node, pos in positions.items():
            x, y = pos
            x *= self.graph_scale
            y *= self.graph_scale
            item = self.nodes_map[node]
            item.setPos(QPointF(x, y))

            

def set_nx_layout_random_small_graph(self, name, positions):
    if name in self.nx_layout and self.nx_layout[name] is not None:
        item_radius = next(iter(self.nodes_map.values())).radius
        threshold_distance = 2 * item_radius / self.graph_scale

        # compute node position from layout function
        locations = {node: (pos[0], pos[1]) for node, pos in positions.items()}  # holds position for each node

        changed = True
        while changed:
            changed = False
            for node, pos in positions.items():
                x, y = pos
                # adjust position if it overlaps with existing nodes
                for _, loc in locations.items():
                    x2, y2 = loc
                    distance = math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
                    if distance < threshold_distance and x != x2 and y != y2:
                        angle = math.atan2(y2 - y, x2 - x)
                        x += 5 * threshold_distance * math.cos(angle)
                        y += 5 * threshold_distance * math.sin(angle)
                        changed = True
                        break

                locations[node] = (x, y)

                # scale x,y
                x_scaled = x * self.graph_scale
                y_scaled = y * self.graph_scale

                # Set the position for the node
                item = self.nodes_map[node]
                item.setPos(QPointF(x_scaled, y_scaled))

                # update positions
                if changed:
                    for node, (x, y) in positions.items():
                        new_x, new_y = locations[node]
                        positions[node] = (new_x, new_y)
                    break
