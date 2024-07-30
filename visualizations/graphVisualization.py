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

import visualizations.graph_functions as gf
import visualizations.graph_layout_creation as glc


class GraphVisualizer(QWidget):
    def __init__(self, network: initializationModule.Initialization, comm, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulator for Distributed Networks")

        self.change_stack = []  # used for "undo" button press

        self.network = network
        self.comm = comm
        self.graph = nx.DiGraph()
        self.num_nodes = len(self.graph)  # used for node radius calculation
        self.first_entry = True

        # adding node names
        vertex_names = [str(comp.id) for comp in self.network.connected_computers]
        self.graph.add_nodes_from(vertex_names)

        # adding edges
        for comp in self.network.connected_computers:
            for connected in comp.connectedEdges:
                self.graph.add_edge(str(comp.id), str(connected))

        self.pos = nx.spring_layout(self.graph, k=0.5, iterations=20)  # You can tweak the k and iterations parameters

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.num_nodes = len(self.graph)  # used for node radius calculation

        # space between nodes
        self.graph_scale = 200
        # map node name to Node object (str->Node)
        self.nodes_map = {}

        self.nx_layout = {
            "circular": nx.circular_layout,
            "random": nx.random_layout,
        }

        self.load_graph()

        self.set_nx_layout("circular")

        self.zoom_factor = 1.15
        self.zoom_step = 1.1

        self.view.wheelEvent = self.wheelEvent
        
        self.layoutCreation()

    def get_nx_layouts(self) -> list:
        return self.nx_layout.keys()

    def set_nx_layout(self, name: str):
        if self.graph.number_of_nodes() > 200:
            self.set_nx_layout_large_graph(name)

        elif name == "circular":
            self.nx_layout_function = self.nx_layout[name]
            positions = self.nx_layout_function(self.graph)

            for node, pos in positions.items():
                x, y = pos
                x *= self.graph_scale
                y *= self.graph_scale
                item = self.nodes_map[node]
                item.setPos(QPointF(x, y))

        else:  # random layout
            if name in self.nx_layout and self.nx_layout[name] is not None:
                self.nx_layout_function = self.nx_layout[name]

                item_radius = next(iter(self.nodes_map.values())).radius
                threshold_distance = 2 * item_radius / self.graph_scale

                # compute node position from layout function
                positions = self.nx_layout_function(self.graph)
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

    def load_graph(self):
        # Load graph into QGraphicsScene using Node class and Edge class
        self.scene.clear()
        self.nodes_map.clear()

        # add nodes
        for node in self.graph:
            item = Node(node, self.num_nodes, self.network)
            self.scene.addItem(item)
            self.nodes_map[node] = item

        # add edges
        for a, b in self.graph.edges:
            source = self.nodes_map[a]
            dest = self.nodes_map[b]
            self.scene.addItem(Edge(source, dest))

    def layoutCreation(self):
        glc.layoutCreation(self)


    def wheelEvent(self, event):
        gf.wheelEvent(self, event)

    def regenarate_clicked(self):
        gf.regenarate_clicked(self)

    def toggle_timer(self):
        gf.toggle_timer(self)

    def update_timer_interval(self):
        gf.update_timer_interval(self)

    def update_slider_label(self):
        gf.update_slider_label(self)

    def undo_change(self):
        gf.undo_change(self)

    def reset(self):
        gf.reset(self)
        
    def change_node_color(self, times):
        gf.change_node_color(self, times)
        
    def update_node_color(self, node_name, values_change_dict):
        gf.update_node_color(self, node_name, values_change_dict)


def visualize_network(network: initializationModule.Initialization, comm):
    graph_window = GraphVisualizer(network, comm)
    stylesheet_file = os.path.join('./designFiles', 'graph_window.qss')
    with open(stylesheet_file, 'r') as f:
        graph_window.setStyleSheet(f.read())
    graph_window.setWindowIcon(QIcon('./designFiles/app_icon.jpeg'))

    graph_window.show()
    graph_window.resize(1000, 800)