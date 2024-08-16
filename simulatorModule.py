import json
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

NETWORK_VARIABLES = 'network_variables.json'
OUTPUT_FILE = './output.txt'

def load_network_variables():
        '''Load default variables from the JSON file.'''
        try:
            with open(NETWORK_VARIABLES, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

def initializeSimulator():
    '''Initializes the simulator by creating a network and communication instances and loading the network_variables dictionary.''' 
    network_variables = load_network_variables()
    MainMenu.menu(network_variables)
    
    network= initializationModule.Initialization(network_variables)
    if network.logging_type!="Short":
        print(network)

    comm = communication.Communication(network)
    return network, comm, network_variables
 
 
def runSimulator(network: initializationModule.Initialization, comm:communication.Communication, network_variables: dict, start_time):
    '''Runs the simulator according to user provided network configuration and algorithm'''
    if network_variables['Display'] == "Graph":
        app = QApplication(sys.argv)
        graphVisualization.visualize_network(network, comm)
        thread = threading.Thread(target=runModule.initiateRun, args=(network, comm))
        thread.start()
        thread.join()
        print("--- %s seconds ---" % (time.time() - start_time))
        sys.exit(app.exec_())
    else:
        runModule.initiateRun(network, comm)
        print("--- %s seconds ---" % (time.time() - start_time))



if __name__=="__main__":
    sys.stdout = open(OUTPUT_FILE, "w") # change default output
    network, comm, network_variables = initializeSimulator()
    
    start_time = time.time()
    runSimulator(network, comm, network_variables, start_time)