"""
Node and NodeInfoWindow classes for graphical network visualization.

This module defines the `Node` and `NodeInfoWindow` classes, which are used to represent individual nodes in
a network and display their information in a graphical interface using PyQt5.
"""

import math
import os

import simulator.initializationModule as initializationModule

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRectF, Qt

class NodeInfoWindow(QWidget):
    """
    A class representing a window that displays information about a node in the network.
    
    This window displays various attributes of the node, such as its ID, color, and algorithm file.
    """

    def __init__(self, node, parent=None):
        """
        Initialize a NodeInfoWindow instance.

        Args:
            node (Node): The node whose information will be displayed.
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)

        # Set stylesheet and icon
        stylesheet_file = os.path.join('./designFiles', 'graph_window.qss')
        with open(stylesheet_file, 'r') as f:
            self.setStyleSheet(f.read())
        self.setWindowIcon(QIcon('./designFiles/app_icon.jpeg'))

        values = node.values
        self.setWindowTitle(f"Node {values.get('id', 'Unknown')} info")

        # Create text content for display
        text_content = ""
        for key, value in values.items():
            if key.startswith("_"):
                continue
            if key == "algorithm_file":
                filename = os.path.basename(str(value))
                text_content += f"{key} : {filename}\n"
            elif key not in ["delays",]:
                text_content += f"{key} : {value}\n"

        # Setup layout and text edit
        layout = QVBoxLayout(self)
        text_edit = QTextEdit(self)
        text_edit.setReadOnly(True)
        text_edit.setPlainText(text_content)
        
        layout.addWidget(text_edit)
        self.resize(350, 300)
        

class Node(QGraphicsObject):
    """
    A class representing a graphical node in a network visualization.
    
    Attributes:
        name (str): The name of the node.
        color (str): The color of the node.
        edges (list): A list of edges connected to this node.
        num_nodes (int): The total number of nodes in the network.
        radius (int): The radius of the node based on the total number of nodes.
        rect (QRectF): The bounding rectangle of the node.
        info_window (NodeInfoWindow): A reference to the node information window.
        values (dict): A dictionary holding the node's attributes.
    """
    
    MAX_RADIUS = 60
    MIN_RADIUS = 10
    TEXT_COLOR = "white"
    
    def __init__(self, name: str, num_nodes: int, network: initializationModule.Initialization, parent=None):
        """
        Initialize a Node instance.

        Args:
            name (str): The name of the node.
            num_nodes (int): The total number of nodes in the network.
            network (initializationModule.Initialization): The network to which this node belongs.
            parent (QGraphicsItem, optional): The parent QGraphicsItem. Defaults to None.
        """
        super().__init__(parent)
        comp = network.network_dict.get(int(name))
        
        self.name = name
        self.color = comp.color
        self.edges = []
        self.num_nodes = num_nodes
        self.radius = self._calculate_radius()
        self.rect = QRectF(0, 0, self.radius * 2, self.radius * 2)
        self.info_window = None  # reference to the node info window

        self.values = {key: value for key, value in comp.__dict__.items()}
        self._setup_graphics()
        
    def _setup_graphics(self):
        """
        Setup the graphical properties of the node.
        """
        self.setFlags(
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        
    def boundingRect(self) -> QRectF:
        """
        Returns the bounding rectangle of the node.

        Returns:
            QRectF: The bounding rectangle of the node.
        """
        return self.rect
        
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """
        Paint the node with its color and label.

        Args:
            painter (QPainter): The painter object used to draw the node.
            option (QStyleOptionGraphicsItem): Provides style options for the item.
            widget (QWidget, optional): The widget being painted. Defaults to None.
        """
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(self.color).darker(), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(QBrush(QColor(self.color)))
        painter.drawEllipse(self.boundingRect())
        
        
        
        #painter.setPen(QPen(QColor(self.TEXT_COLOR)))
        #painter.drawText(self.boundingRect(), Qt.AlignCenter, self.name)
        
        
        rect = self.boundingRect()
        font_size = self._calculate_text_size(painter, rect, self.name)
        
        # Set the calculated font size
        font = painter.font()
        font.setPointSize(font_size)
        painter.setFont(font)
        
        painter.setPen(QPen(QColor(self.TEXT_COLOR)))
        painter.drawText(rect, Qt.AlignCenter, self.name)
        
    
    def _calculate_text_size(self, painter: QPainter, rect: QRectF, text: str) -> int:
        """
        Calculate the maximum font size that fits the given text within the bounding rectangle.

        Args:
            painter (QPainter): The painter object used to calculate the font size.
            rect (QRectF): The bounding rectangle where the text needs to fit.
            text (str): The text that needs to be drawn.

        Returns:
            int: The font size that fits the text within the bounding rectangle.
        """
        font = painter.font()
        font_size = int(rect.height() / 2)  # Initial font size, can be adjusted
        font.setPointSize(font_size)
        painter.setFont(font)
        
        while True:
            text_rect = painter.boundingRect(rect, Qt.AlignCenter, text)
            if text_rect.width() <= rect.width() and text_rect.height() <= rect.height():
                return font_size
            font_size -= 1
            if font_size <= 1:  # Prevent the font size from becoming too small
                return 1
            font.setPointSize(font_size)
            painter.setFont(font)
    
    
    def _calculate_radius(self) -> int:
        """
        Calculate the radius of the node based on the number of nodes.

        Returns:
            int: The calculated radius.
        """
        radius = max(self.MIN_RADIUS, self.MAX_RADIUS / (1 + math.log(self.num_nodes)))
        return int(radius)
    
    def mouseDoubleClickEvent(self, event):
        """
        Handle double-click events on the node to display the node's information.

        Args:
            event (QMouseEvent): The mouse event.
        """
        if event.button() == Qt.LeftButton:        
            self.info_window = NodeInfoWindow(self)
            self.info_window.show()
        super().mouseDoubleClickEvent(event)
        
    def add_edge(self, edge):
        """
        Add an edge to the node.

        Args:
            edge (Edge): The edge to add.
        """
        self.edges.append(edge)
        
    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        """
        Handle changes to the node, such as position changes.

        Args:
            change (QGraphicsItem.GraphicsItemChange): The type of change.
            value: The new value for the change.

        Returns:
            The result of the base class implementation of itemChange.
        """
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edges:
                edge.adjust()
        return super().itemChange(change, value)
    
