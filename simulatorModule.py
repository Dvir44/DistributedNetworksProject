import json
import numpy
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import threading
from visualizationModule import DistributedSimulatorApp

class Simulator:
    def __init__(self):
        pass

def run_visualization():
    app = QApplication(sys.argv)
    main_window = DistributedSimulatorApp()
    main_window.show()
    sys.exit(app.exec_())
    
    


def main():
    t1= threading.Thread(target=run_visualization)
    t1.start()
    t1.join()
    print("reading from json file:")
    with open('network_variables.json', 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            print(f"{key}: {value}")

if __name__=="__main__":
    main()