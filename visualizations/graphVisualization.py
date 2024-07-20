import math
import os
import random
import sys
import numpy as np
import networkx as nx

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import QPointF, QRectF, QLineF, Qt, QTimer, QTime

import initializationModule
from visualizations.node import Node
from visualizations.edge import Edge
     

class GraphView(QGraphicsView):
    def __init__(self, graph: nx.DiGraph, network: initializationModule.Initialization, parent=None):
        super().__init__()
        self.graph = graph
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.num_nodes = len(self.graph) # used for node radius calculation

        # space between nodes
        self.graph_scale = 200
        # map node name to Node object (str->Node)
        self.nodes_map = {}

        self.nx_layout = {
            "circular": nx.circular_layout,
            "random": nx.random_layout,
        }

        self.load_graph(network)

        self.set_nx_layout("circular")

        self.zoom_factor = 1.15
        self.zoom_step = 1.1


    def wheelEvent(self, event):
        # zoom in/out on wheel event
        if event.angleDelta().y() > 0:
            # zoom in
            self.scale(self.zoom_factor, self.zoom_factor)
        else:
            # zoom out
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)

    def get_nx_layouts(self) -> list:
        return self.nx_layout.keys()

    def set_nx_layout(self, name: str):
        if self.graph.number_of_nodes()>200:
            self.set_nx_layout_large_graph(name)
               
        elif name=="circular":
            self.nx_layout_function = self.nx_layout[name]
            positions = self.nx_layout_function(self.graph)

            for node, pos in positions.items():
                x, y = pos
                x *= self.graph_scale
                y *= self.graph_scale
                item = self.nodes_map[node]
                item.setPos(QPointF(x, y))

            
        else: # random layout
            if name in self.nx_layout and self.nx_layout[name] is not None:
                self.nx_layout_function = self.nx_layout[name]

                item_radius = next(iter(self.nodes_map.values())).radius
                threshold_distance = 2 * item_radius / self.graph_scale

                # compute node position from layout function
                positions = self.nx_layout_function(self.graph)
                locations = {node: (pos[0], pos[1]) for node, pos in positions.items()}  # holds position for each node

                changed=True
                while changed:
                    changed=False
                    for node, pos in positions.items():
                        x, y = pos
                        # adjust position if it overlaps with existing nodes
                        for _, loc in locations.items():
                            x2, y2 = loc
                            distance = math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
                            if distance < threshold_distance and x!=x2 and y!=y2:
                                angle = math.atan2(y2 - y, x2 - x)
                                x += 5*threshold_distance* math.cos(angle)
                                y += 5*threshold_distance* math.sin(angle)
                                changed=True
                                break
                        
                        locations[node]=(x,y)
                            
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
 
 
    def set_nx_layout_large_graph(self, name: str):
        self.nx_layout_function = self.nx_layout[name]
        positions = self.nx_layout_function(self.graph)

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
                
          
    def load_graph(self, network: initializationModule.Initialization):
        # Load graph into QGraphicsScene using Node class and Edge class
        self.scene.clear()
        self.nodes_map.clear()

        # add nodes
        for node in self.graph:
            item = Node(node, self.num_nodes, network)
            self.scene.addItem(item)
            self.nodes_map[node] = item

        # add edges
        for a, b in self.graph.edges:
            source = self.nodes_map[a]
            dest = self.nodes_map[b]
            self.scene.addItem(Edge(source, dest))
            
        
        
class MainWindow(QWidget):
    def __init__(self, network: initializationModule.Initialization, comm, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulator for Distributed Networks")

        self.change_stack = [] # used for "undo" button press

        self.network = network
        self.comm = comm
        self.graph = nx.DiGraph()
        self.first_entry=True
        # adding node names
        vertex_names=[]
        for comp in self.network.connected_computers:
            vertex_names.append(str(comp.id))
        self.graph.add_nodes_from(vertex_names)

        # adding edges
        for comp in self.network.connected_computers:
            for connected in comp.connectedEdges:
                self.graph.add_edge(str(comp.id), str(connected))
                
        self.pos = nx.spring_layout(self.graph, k=0.5, iterations=20)  # You can tweak the k and iterations parameters

        self.view = GraphView(self.graph, self.network)
        self.layoutCreation()

        
    def layoutCreation(self):
        self.choice_combo = QComboBox()
        self.choice_combo.addItems(self.view.get_nx_layouts())
        self.choice_combo.currentTextChanged.connect(self.view.set_nx_layout)

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
        
        self.slider_label = QLabel(f"{abs(self.slider.value()/1000)} seconds per tick")
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
        
    # generate a new layout if the current choice is "random"
    def regenarate_clicked(self):
        if self.choice_combo.currentText() == "random":
            self.view.set_nx_layout("random")
    
    # toggles timer based on the QCheckBox run_checkbox
    def toggle_timer(self):
        if self.run_checkbox.isChecked():
            self.timer.start(abs(self.slider.value()))
        else:
            self.timer.stop()
        
    # update the timer interval
    def update_timer_interval(self):
        new_interval = self.slider.value()
        self.timer.setInterval(abs(new_interval))
 
    def update_slider_label(self):
        self.slider_label.setText(f"{abs(self.slider.value()/1000)} seconds per tick")
        
    # accessed only when button is clicked, gets first value from the list and updates its values
    def change_node_color(self, times):
        for _ in range(times):
            if self.network.node_values_change:
                values_change_dict = self.network.node_values_change.pop(0)
                node_name = None
                for key, value in values_change_dict.items():
                    if node_name is None:
                        if key == 'id':
                            node_name = value
                            break
                        
                node_item = self.view.nodes_map[str(node_name)]
                
                # Store the current state of the node before changing
                previous_state = node_item.values.copy()
                
                for key, value in values_change_dict.items():
                    node_item.values[key] = value

                node_item.color = node_item.values['color']

                next_state = node_item.values.copy()
                self.change_stack.insert(0, (node_item, previous_state))
                self.change_stack.insert(1, (node_item, next_state))

                node_item.update()


    def undo_change(self):
        if self.change_stack:
            previous_node_item, previous_state = self.change_stack.pop(0)
            previous_node_item.values = previous_state
            previous_node_item.color = previous_state['color']
            
            _, next_state = self.change_stack.pop(0)
            self.network.node_values_change.insert(0, next_state)

            previous_node_item.update()

    def reset(self):
        while self.change_stack:
            self.undo_change()


def visualize_network(network: initializationModule.Initialization, comm):
    graph_window = MainWindow(network, comm)
    stylesheet_file = os.path.join('./extra_files', 'graph_window.qss')
    with open(stylesheet_file, 'r') as f:
        graph_window.setStyleSheet(f.read())
    graph_window.setWindowIcon(QIcon('./extra_files/app_icon.jpeg'))

    graph_window.show()
    #graph_window.showMaximized()
    graph_window.resize(1000, 800)
