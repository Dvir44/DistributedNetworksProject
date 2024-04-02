import math
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPointF, QRectF, QLineF, Qt
import networkx as nx



# node class
class Node(QGraphicsObject):
    def __init__(self, name: str, num_nodes: int, parent=None):
        super().__init__(parent)
        self.name = name
        self.edges = []
        self.color = "#5AD469"
        self.num_nodes = num_nodes
        self.radius = self.calculate_radius()
        self.rect = QRectF(0, 0, self.radius * 2, self.radius * 2)
        
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        
        
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
        self.boldness = 5
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
    def __init__(self, graph: nx.DiGraph, parent=None):
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
            "planar": nx.planar_layout,
            "random": nx.random_layout,
            "shell_layout": nx.shell_layout,
            "kamada_kawai_layout": nx.kamada_kawai_layout,
            "spring_layout": nx.spring_layout,
            "spiral_layout": nx.spiral_layout,
        }

        self.load_graph()
        self.set_nx_layout("circular")

    def get_nx_layouts(self) -> list:
        return self.nx_layout.keys()

    def set_nx_layout(self, name: str):
        if name in self.nx_layout:
            self.nx_layout_function = self.nx_layout[name]

            # compute node position from layout function
            positions = self.nx_layout_function(self.graph)
            for node, pos in positions.items():
                x, y = pos
                x *= self.graph_scale
                y *= self.graph_scale   
                item = self.nodes_map[node]
                item.setPos(QPointF(x, y))

    def load_graph(self):
        # Load graph into QGraphicsScene using Node class and Edge class

        self.scene.clear()
        self.nodes_map.clear()

        # add nodes
        for node in self.graph:
            item = Node(node, self.num_nodes)
            self.scene.addItem(item)
            self.nodes_map[node] = item

        # add edges
        for a, b in self.graph.edges:
            source = self.nodes_map[a]
            dest = self.nodes_map[b]
            self.scene.addItem(Edge(source, dest))
            
        
        
        
class MainWindow(QWidget):
    def __init__(self, network, comm, parent=None):
        super().__init__(parent)
        self.network = network
        self.comm = comm
        self.graph = nx.DiGraph()
        self.first_entry=True
        
        num_computers = self.network.getNumberOfComputers()
        vertex_names = [str(i) for i in range(1, num_computers)]
        self.graph.add_nodes_from(vertex_names) # adding nodes

        for comp in self.network.connectedComputers: # adding edges
            for connected in comp.connectedEdges:
                self.graph.add_edge(str(comp.id), str(connected))


        self.view = GraphView(self.graph)
        self.choice_combo = QComboBox()
        self.choice_combo.addItems(self.view.get_nx_layouts())
        self.next_phase_button = QPushButton("Next Phase")
        self.next_phase_button.clicked.connect(self.next_phase_action)
        
        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.choice_combo)
        v_layout.addWidget(self.view)
        v_layout.addWidget(self.next_phase_button)  # Add the button to the layout
        self.choice_combo.currentTextChanged.connect(self.view.set_nx_layout)
        

            
    # space key pressed, same as clicking on next phase button
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.next_phase_action()
        else:
            super().keyPressEvent(event)    
        
    # continue to the next "receive_message" run
    def next_phase_action(self):
        if self.first_entry:
            for comp in self.network.connectedComputers:
                algorithm_function = getattr(comp.algorithmFile, 'init', None)
                if callable(algorithm_function): # add the algorithm to each computer
                    algorithm_function(comp, self.comm)
                else:
                    print(f"Error: Function 'init' not found in {comp.algorithmFile}.py")
                    return None
            self.first_entry=False
        else:
            if not self.network.networkMessageQueue.empty():
                self.comm.receive_message(self.network.networkMessageQueue.pop(), self.comm, self)
    
    
    # from communication, change node color request
    def change_node_color(self, node_name, new_color):
        if node_name in self.graph.nodes:
            node_item = self.view.nodes_map[node_name]
            node_item.color = new_color
            node_item.update()

def visualize_network(network, comm):
    app = QApplication(sys.argv)    
    widget = MainWindow(network, comm)
    widget.show()
    widget.resize(800, 600)
    sys.exit(app.exec())