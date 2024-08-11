import http
import http.server
import json
import os
import re
import socketserver
import threading
import sys
import time
import json

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import simulator.runModule as runModule
import simulator.communication as communication
import simulator.initializationModule as initializationModule
import simulator.MainMenu as MainMenu
import visualizations.graphVisualization as graphVisualization


def simulation_creation():
    ''' creates network, communication module and loads data from network.json .'''
    MainMenu.menu()
    network= initializationModule.Initialization()
    if network.logging_type!="Short":
        print(network)
        
    comm = communication.Communication(network)

    return network, comm

def simulation_run(data: str, network: initializationModule.Initialization, comm: communication.Communication):
    ''' runs user submitted algorithm on created network.'''
    if data['Display'] == "Graph":
        app = QApplication(sys.argv)
        graphVisualization.visualize_network(network, comm)
        thread = threading.Thread(target=runModule.initiateRun, args=(network, comm))
        thread.start()
        thread.join()
        sys.exit(app.exec_())
    else:
        runModule.initiateRun(network, comm)
        

def main():
    sys.stdout = open("./output.txt", "w") # change default output
    start_time = time.time()
    
    network, comm = simulation_creation()
    with open('network_variables.json', 'r') as f:
        data = json.load(f)
    simulation_run(data, network, comm)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__=="__main__":
    main()
