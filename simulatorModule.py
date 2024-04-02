import json
import numpy
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import initializationModule
import visualizationModule
import runModule

import communicationModule
import graphCommunication
import time

import graphVisualization
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
    
    with open('network_variables.json', 'r') as f:
        data = json.load(f)
    if data['Display']=="T":
        comm = communicationModule.CommunicationModule(network)
        runModule.initiateRun(network, comm)
    elif data['Display']=="G":
        comm = graphCommunication.CommunicationModule(network)
        graphVisualization.visualize_network(network, comm)

    print("--- %s seconds ---" % (time.time() - start_time))
    
    
  
    
    
if __name__=="__main__":
    main()