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
        data = json.load(f)
        print("Info received from visualization:")
        for key, value in data.items():
            print(f"{key}: {value}")

def run_visualization_window():
    app = QApplication(sys.argv)
    main_window =visualizationModule.DistributedSimulatorApp()
    main_window.show()
    sys.exit(app.exec_())
    
def main():
    visualize()
    network= initializationModule.Initialization()

if __name__=="__main__":
    main()