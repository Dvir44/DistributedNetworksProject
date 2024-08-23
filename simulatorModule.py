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
import simulator.mainMenu as mainMenu
from simulator.mainMenu import NETWORK_VARIABLES
import visualizations.graphVisualization as graphVisualization

OUTPUT_FILE = './output.txt'

def load_network_variables():
    """
    Load default variables from the NETWORK_VARIABLES JSON file.
    
    Returns:
        dict: A dictionary of network variables loaded from the JSON file.
        
    Raises:
        FileNotFoundError: If the file is not found.
        json.JSONDecodeError: If the JSON is improperly formatted.
    """
    try:
        with open(NETWORK_VARIABLES, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def initializeSimulator():
    """
    Initializes the simulator by creating the network, communication instances, and loading network variables.
    
    Returns:
        tuple: A tuple containing the initialized network, communication instance, and the loaded network variables.
    """
    network_variables = load_network_variables()
    mainMenu.menu(network_variables)
    
    network= initializationModule.Initialization(network_variables)
    if network.logging_type!="Short":
        print(network)

    comm = communication.Communication(network)
    return network, comm, network_variables
 
 
def runSimulator(network: initializationModule.Initialization, comm:communication.Communication, network_variables: dict, start_time):
    """
    Runs the simulator based on user-provided network configuration and algorithm.
    
    Args:
        network (initializationModule.Initialization): The initialized network object.
        comm (communication.Communication): The communication object handling network communication.
        network_variables (dict): Dictionary of network parameters.
        start_time (float): The time when the simulation started.

    Returns:
        None
    """
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
    """
    Main entry point for the simulator. Redirects standard output to a log file and runs the simulator.
    """
    sys.stdout = open(OUTPUT_FILE, "w")
    network, comm, network_variables = initializeSimulator()
    
    start_time = time.time()
    runSimulator(network, comm, network_variables, start_time)