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


def main():
    sys.stdout = open("./output.txt", "w") # change default output
    
    MainMenu.menu()
    start_time = time.time()
    network= initializationModule.Initialization()
    print(network)
    
    with open('network_variables.json', 'r') as f:
        data = json.load(f)

    comm = communication.Communication(network)

    if data['Display'] == "Graph":
        app = QApplication(sys.argv)
        graphVisualization.visualize_network(network, comm)
        thread = threading.Thread(target=runModule.initiateRun, args=(network, comm))
        thread.start()
        #print("here", file=sys.__stdout__)  # Print to the original stdout
        thread.join()
        print("--- %s seconds ---" % (time.time() - start_time))

        sys.exit(app.exec_())
        
    else:
        runModule.initiateRun(network, comm)
        print("--- %s seconds ---" % (time.time() - start_time))

    


if __name__=="__main__":
    main()
