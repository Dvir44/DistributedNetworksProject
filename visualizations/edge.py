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

class Edge(QGraphicsItem):
    """
    A class representing an edge between two nodes in a graphical network.
    """
    
    DEFAULT_BOLDNESS = 2
    DEFAULT_COLOR = "#2BB53C"
    
    def __init__(self, source: Node, dest: Node, parent: QGraphicsItem = None):
        """
        Initialize an Edge instance.

        Args:
            source (Node): The source node.
            dest (Node): The destination node.
            parent (QGraphicsItem, optional): The parent QGraphicsItem. Defaults to None.
        """
        super().__init__(parent)
        self.source = source
        self.dest = dest
        self.boldness: int = self.DEFAULT_BOLDNESS
        self.color: str = self.DEFAULT_COLOR
        self.source.add_edge(self)
        self.dest.add_edge(self)

        self.line = QLineF()
        self.setZValue(-1)
        self.adjust()
        
    def adjust(self):
        """
        Update edge position based on source and destination node positions.
        This method is called when a node is moved.
        """
        self.prepareGeometryChange()
        self.line.setP1(self.source.pos() + self.source.boundingRect().center())
        self.line.setP2(self.dest.pos() + self.dest.boundingRect().center())
    
    def boundingRect(self) -> QRectF:
        """
        Returns the bounding rectangle of the edge, adjusted for line boldness.
        """
        return (
            QRectF(self.line.p1(), self.line.p2())
            .normalized().adjusted( -self.boldness, -self.boldness, self.boldness, self.boldness)
        )
          
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget=None):
        """
        Paints the edge as a line between the source and destination nodes.
        """
        if self.source and self.dest:
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setPen(QPen(QColor(self.color), self.boldness, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin,))
            painter.drawLine(self.line)