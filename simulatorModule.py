import json
import numpy
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import threading
import initializationModule
import visualizationModule

class Simulator:
    def __init__(self):
        pass

def visualize():
    t1= threading.Thread(target=run_visualization_window)
    t1.start()
    t1.join()
    with open('network_variables.json', 'r') as f: # fill json file
        json.load(f)

def run_visualization_window():
    app = QApplication(sys.argv)
    main_window =visualizationModule.DistributedSimulatorApp()
    main_window.show()
    sys.exit(app.exec_())
    
def main():
    visualize()
    network= initializationModule.Initialization()
    network.toString()
    for comp in network.connectedComputers:
        comp.run()
if __name__=="__main__":
    main()