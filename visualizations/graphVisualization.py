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

import simulator.initializationModule as initializationModule
from visualizations.node import Node
from visualizations.edge import Edge

import visualizations.functions as gf
import visualizations.layout_creation as glc


class GraphVisualizer(QWidget):
    def __init__(self, network: initializationModule.Initialization, comm, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Simulator for Distributed Networks")

        self.change_stack = []  # used for "undo" button press

        self.network = network
        self.comm = comm
        self.graph = nx.DiGraph()
        self.num_nodes = self.network.computer_number
        self.nodes_map = {} # A dictionary mapping node names to Node objects (Str -> Node).
        self.nx_layout = {"circular": nx.circular_layout, "random": nx.random_layout,} # A dictionary mapping layout names to NetworkX layout functions.
        
        self.init_graph()
        self.init_ui()


    def init_graph(self):
        '''Initializes the graph by adding nodes and edges.'''
        self.add_nodes_to_graph()
        self.add_edges_to_graph()

    def add_nodes_to_graph(self):
        '''Adds nodes to the graph based on the network.'''
        vertex_names = [str(comp.id) for comp in self.network.connected_computers]
        self.graph.add_nodes_from(vertex_names)
            
    def add_edges_to_graph(self):
        '''Adds edges to the graph based on the network.'''
        for comp in self.network.connected_computers:
            for connected in comp.connectedEdges:
                self.graph.add_edge(str(comp.id), str(connected))

    def init_ui(self):
        '''Initializes the UI components, including the scene and view.'''
        self.scene = QGraphicsScene()  # manages and organizes the items that make up the visualization.
        self.view = QGraphicsView(self.scene) # visual display for the scene.
        self.graph_scale = 200
        self.load_graph()
        self.set_nx_layout("circular")
        self.zoom_factor = 1.15
        self.zoom_step = 1.1
        self.view.wheelEvent = self.wheelEvent
        self.layoutCreation()
        
    def get_nx_layouts(self) -> list:
        '''Returns the available NetworkX layouts as a list.'''
        return self.nx_layout.keys()

    def set_nx_layout(self, name: str):
        '''Sets the NetworkX layout for the graph visualization.'''
        self.nx_layout_function = self.nx_layout[name]
        positions = self.nx_layout_function(self.graph)
        
        if self.graph.number_of_nodes() > 200:
            glc.set_nx_layout_large_graph(self, positions)
        elif name == "circular":
            glc.set_nx_layout_circular_graph(self, positions)
        else:  # random layout with not a lot of nodes
            glc.set_nx_layout_random_small_graph(self, name, positions)

            
    def load_graph(self):
        '''Loads the graph into the QGraphicsScene using Node and Edge classes.'''
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
    
