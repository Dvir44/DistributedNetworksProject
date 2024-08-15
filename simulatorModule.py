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
        """Load default variables from the JSON file."""
        try:
            with open(NETWORK_VARIABLES, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

def main():
    sys.stdout = open(OUTPUT_FILE, "w") # change default output
    
    network_variables = load_network_variables()
    data = MainMenu.menu(network_variables)
    start_time = time.time()
    network= initializationModule.Initialization(network_variables)
    if network.logging_type!="Short":
        print(network)
    
    # with open(NETWORK_VARIABLES, 'r') as f:
    #     data = json.load(f)

    comm = communication.Communication(network)

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
    main()
