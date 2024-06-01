import math
import os
import random
import sys

import numpy as np
import initializationModule

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPointF, QRectF, QLineF, Qt, QTimer, QTime
import networkx as nx


class NodeInfoWindow(QSplitter):
    def __init__(self, node, parent=None):
        super().__init__(parent)

        stylesheet_file = os.path.join('./extra_files', 'graph_window.qss')
        with open(stylesheet_file, 'r') as f:
            self.setStyleSheet(f.read())
        self.setWindowIcon(QIcon('./extra_files/app_icon.jpeg'))

        values = node.values
        self.setWindowTitle(f"Node {values['id']} info")
      
        text_content = (
            f"Id : {values['id']}\n"
            f"Color : {values['color']}\n"
            f"Root : {values['root']}\n"
            f"State : {values['state']}\n"
            f"Received from : {values['source']}\n"
        )
        layout = QVBoxLayout(self)
        text_edit = QTextEdit(self)
        text_edit.setReadOnly(True)
        text_edit.setText(text_content)
        
        layout.addWidget(text_edit)
        self.resize(350, 300)



# node class
class Node(QGraphicsObject):
    def __init__(self, name: str, num_nodes: int, network: initializationModule.Initialization, parent=None):
        super().__init__(parent)
        self.name = name
        self.edges = []
        self.color = "#5AD469"
        self.num_nodes = num_nodes
        self.radius = self.calculate_radius()
        self.rect = QRectF(0, 0, self.radius * 2, self.radius * 2)
        
        self.info_window = None  # reference to the node info window
        
        comp = network.find_computer(int(self.name))
        self.values = {'id': comp.getId(), 'color': comp.getColor(), 'root': comp.getRoot(), 'state': comp.getState(), 'source': comp.getReceivedFrom()}
        
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:        
            self.info_window = NodeInfoWindow(self)
            self.info_window.show()
        super().mouseDoubleClickEvent(event)


    def calculate_radius(self):
        max_radius = 60  # maximum allowed radius
        min_radius = 2  # minimum allowed radius
        # adjusting radius based on the number of nodes
        radius = max(min_radius, max_radius / math.sqrt(self.num_nodes))
        return radius
        
        
    def add_edge(self, edge):
        self.edges.append(edge)
        
    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()
        return super().itemChange(change, value)
    
    
    def boundingRect(self) -> QRectF:
        return self.rect

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(
            QPen(
                QColor(self.color).darker(),
                2,
                Qt.SolidLine,
                Qt.RoundCap,
                Qt.RoundJoin,
            )
        )
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawEllipse(self.boundingRect())
        painter.setPen(QPen(QColor("white")))
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.name)
        
# edge class
class Edge(QGraphicsItem):
    def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
        super().__init__(parent)
        self.source = source
        self.dest = dest
        self.boldness = 2
        self.color = "#2BB53C"
        self.source.add_edge(self)
        self.dest.add_edge(self)

        self.line = QLineF()
        self.setZValue(-1)
        self.adjust()
        
    def adjust(self):
        # update edge position from source and destination node. Gets called when node is moved
        self.prepareGeometryChange()
        self.line = QLineF(
            self.source.pos() + self.source.boundingRect().center(),
            self.dest.pos() + self.dest.boundingRect().center(),
        )
    
    def boundingRect(self) -> QRectF:
        return (
            QRectF(self.line.p1(), self.line.p2())
            .normalized().adjusted( -self.boldness, -self.boldness, self.boldness, self.boldness)
        )
          
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        if self.source and self.dest:
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setPen(
                QPen(
                    QColor(self.color),
                    self.boldness,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin,
                )
            )
            painter.drawLine(self.line)


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
        if name in self.nx_layout:
            self.nx_layout_function = self.nx_layout[name]

            for value in self.nodes_map.values():
                if value:
                    threshold_distance = 3*value.radius/self.graph_scale
                    break


            # compute node position from layout function
            positions = self.nx_layout_function(self.graph)
            locations =[]
            
            for node, pos in positions.items():
                x, y = pos
                locations.append((x,y))

            changed=True
            while changed:
                changed=False
                for node, pos in positions.items():
                    x, y = pos
                    # adjust position if it overlaps with existing nodes
                    for loc in locations:
                        x2, y2 = loc
                        distance = math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
                        if distance < threshold_distance and x!=x2 and y!=y2:
                            angle = math.atan2(y2 - y, x2 - x)
                            x += 5*threshold_distance* math.cos(angle)
                            y += 5*threshold_distance* math.sin(angle)
                            distance = math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
                            changed=True
                            break
                            
                    locations[int(node)]=(x,y)
                    # scale x,y
                    x *= self.graph_scale
                    y *= self.graph_scale
                    # set the position for the node
                    item = self.nodes_map[node]
                    item.setPos(QPointF(x, y))
                    
                    # update positions
                    for node, (x, y) in positions.items():
                        new_x, new_y = locations[int(node)]
                        positions[node] = (new_x, new_y)
                    if changed:
                        break
                


                
                

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

        self.network = network
        self.comm = comm
        self.graph = nx.DiGraph()
        self.first_entry=True
        
        # adding node names
        vertex_names=[]
        for comp in self.network.connectedComputers:
            vertex_names.append(str(comp.getId()))
        self.graph.add_nodes_from(vertex_names)

        # adding edges
        for comp in self.network.connectedComputers:
            for connected in comp.connectedEdges:
                self.graph.add_edge(str(comp.getId()), str(connected))
                

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
        self.slider.setRange(-2000, -500)
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



        phases_h_layout = QHBoxLayout()
        
        self.next_phase_button = QPushButton("Next Phase")
        self.next_phase_button.clicked.connect(lambda: self.change_node_color(1))
        self.next_5_phase_button = QPushButton("Next 5 Phases")
        self.next_5_phase_button.clicked.connect(lambda: self.change_node_color(5))
        
        phases_h_layout.addWidget(self.next_phase_button)
        phases_h_layout.addWidget(self.next_5_phase_button)
        
        
        # Add the horizontal layouts to the main layout
        main_layout.addLayout(slider_h_layout)
        phases_h_layout.addWidget(self.slider_label)
        main_layout.addLayout(phases_h_layout)
        
        
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
        
    # accessed only when button is clicked, gets first value from the dictionary and changes its color
    def change_node_color(self, times):
        for _ in range(times):
            if self.network.node_values_change:
                node_name = self.network.node_values_change[0][0]
                new_color = self.network.node_values_change[0][1]
                
                node_item = self.view.nodes_map[node_name]            
                node_item.color = new_color
                
                node_item.values['id']=self.network.node_values_change[0][0]
                node_item.values['color']=self.network.node_values_change[0][1]
                node_item.values['root']=self.network.node_values_change[0][2]
                node_item.values['state']=self.network.node_values_change[0][3]
                node_item.values['source']=self.network.node_values_change[0][4]

                node_item.update()
                self.network.node_values_change.pop(0)  # Removes the first item


def visualize_network(network: initializationModule.Initialization, comm):
    graph_window = MainWindow(network, comm)
    stylesheet_file = os.path.join('./extra_files', 'graph_window.qss')
    with open(stylesheet_file, 'r') as f:
        graph_window.setStyleSheet(f.read())
    graph_window.setWindowIcon(QIcon('./extra_files/app_icon.jpeg'))

    graph_window.show()
    graph_window.resize(800, 600)
