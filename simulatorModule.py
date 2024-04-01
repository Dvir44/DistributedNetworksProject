import json
import numpy
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import threading
import initializationModule
import visualizationModule
import communicationModule
import runModule
import time

import networkVisualization


class Simulator:
    def __init__(self):
        pass

def run_visualization_window(app):
    main_window = visualizationModule.DistributedSimulatorApp()
    main_window.show()
    app.exec_()


def main():
    app = QApplication(sys.argv)
    run_visualization_window(app)
    
    start_time = time.time()
    
    network= initializationModule.Initialization()
    network.toString()
    
    comm = communicationModule.CommunicationModule(network)
    runModule.initiateRun(network, comm)
    print("--- %s seconds ---" % (time.time() - start_time))

    networkVisualization.visualize_network(network)
    
    
  
    
    
if __name__=="__main__":
    main()