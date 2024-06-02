import json
import os
import threading
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import initializationModule
import visualizations.visualizationModule as visualizationModule
import runModule
import communicationModule
import time
import visualizations.graphVisualization as graphVisualization

from runModule import exception_queue

class Simulator:
    def __init__(self):
        pass

def main():
    visualizationModule.menu()
    start_time = time.time()
    
    network= initializationModule.Initialization()
    print(network)
    
    with open('network_variables.json', 'r') as f:
        data = json.load(f)
        
    comm = communicationModule.CommunicationModule(network)

    if data['Display'] == "Graph":
        app = QApplication(sys.argv)
        thread = threading.Thread(target=lambda: runModule.initiateRun(network, comm))
        thread.start()
        graphVisualization.visualize_network(network, comm)
        thread.join()
        
        print("--- %s seconds ---" % (time.time() - start_time))

        if not exception_queue.empty():
            exit()
            

        sys.exit(app.exec_())
    else:
        runModule.initiateRun(network, comm)
        if not exception_queue.empty():
            exit()
        print("--- %s seconds ---" % (time.time() - start_time))

    


if __name__=="__main__":
    main()
