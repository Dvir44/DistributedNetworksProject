import importlib
import json
import os
import queue
import random
import sys
import numpy
import computer
import heapq

class CustomMinHeap:
    def __init__(self):
        self.heap = []

    def push(self, message_format):
        heapq.heappush(self.heap, (message_format['arrival_time'], message_format))

    def pop(self):
        priority, message_format = heapq.heappop(self.heap)
        return message_format
    

class Initialization:
    '''
    Initialization Class - creates the basic parameters we get from the user in the visualization class
    and then we create the basic base for the simulation to run on
    '''
    #Defualt constructor
    def __init__(self):
        with open('network_variables.json', 'r') as f:
            data = json.load(f)
        self.numberOfComputers = int(data.get('Number of Computers',5))
        self.topologyType = data.get('Topology','L')
        self.IdType = data.get('ID Type','S')
        self.connectedComputers = []
        self.connectedComputersCreation()
        self.createComputersIds()
        algorithms = data.get('Algorithm', 'no_alg_provided')
        self.loadAlgorithms(algorithms)
        self.networkMessageQueue = CustomMinHeap()

    def toString(self):
        print(self.numberOfComputers)
        print(self.topologyType)
        print(self.IdType)
        for computer in self.connectedComputers:
            print(computer)

    #Getters
    def getNumberOfComputers(self):
        return self.numberOfComputers
    def getTopologyType(self):
        return self.topologyType
    def getConnectedComputers(self):
        return self.connectedComputers

    #Creates the connectedComputers list
    def connectedComputersCreation(self):
        self.connectedComputers = [computer.Computer() for _ in range(self.numberOfComputers)] 
        self.createComputersIds() #Fill the Id's according to the user choice
        
        if (self.topologyType == "R"):
            self.createRandomTopology()
        elif (self.topologyType == "L"):
            self.createLineTopology()
        elif (self.topologyType == "C"):
            self.createCliqueTopology()
        return
    
    # Create the clique topology for the network
    def createCliqueTopology(self):        
        # Connect each computer to every other computer
        for i in range(self.numberOfComputers):
            for j in range(i + 1, self.numberOfComputers):
                # Ensure bi-directional connection
                self.connectedComputers[i].connectedEdges.append(j)
                self.connectedComputers[j].connectedEdges.append(i)

        # Removing duplicates
        for comp in self.connectedComputers:
            comp.connectedEdges = list(set(comp.connectedEdges)) 

    # Create computer IDs based on the IdType
    def createComputersIds(self):
        if self.IdType == "R":
            self.createRandomIds()
        elif self.IdType == "S":
            self.createSequentialIds()

    # Create random computer IDs (ensuring uniqueness)
    def createRandomIds(self):
        used_ids = set()
        for comp in self.connectedComputers:
            comp_id = random.randint(100, 100 * self.numberOfComputers - 1)
            while comp_id in used_ids:
                comp_id = random.randint(100, 100 * self.numberOfComputers - 1)
            comp.id = comp_id
            used_ids.add(comp_id)

    # Create uniform computer IDs
    def createSequentialIds(self):
        for i, comp in enumerate(self.connectedComputers):
            comp.id = i

    def createRandomTopology(self):
        for i, comp in enumerate(self.connectedComputers):
            # Determine a random number of edges (between 1 and numberOfComputers - 1)
            num_edges = random.randint(1, self.numberOfComputers - 1)
            # Choose num_edges unique vertices (excluding i)
            connected_to_vertices = random.sample([j for j in range(self.numberOfComputers) if j != i], num_edges)

            # Add connections
            comp.connectedEdges.extend(connected_to_vertices)

            # Ensure bi-directional connection
            for connected_to in connected_to_vertices:
                self.connectedComputers[connected_to].connectedEdges.append(i)

        # removing duplicates
        for comp in self.connectedComputers:
            comp.connectedEdges=list(set(comp.connectedEdges))

    def createLineTopology(self):
        for i in range(self.numberOfComputers - 1):
            # Connect each computer to the next one in line
            self.connectedComputers[i].connectedEdges.append(i + 1)
            self.connectedComputers[i + 1].connectedEdges.append(i)  # Ensure bi-directional connection

    def loadAlgorithms(self, algorithm_module_path):
        if algorithm_module_path == 'no_alg_provided':
            print("No algorithm was provided")
            exit()
        try:
            directory, file_name = os.path.split(algorithm_module_path)
            base_file_name, _ = os.path.splitext(file_name)
            sys.path.insert(0,directory)

            algorithm_module = importlib.import_module(base_file_name)
            for comp in self.connectedComputers:
                comp.algorithmFile = algorithm_module
                print(comp.algorithmFile)

        except ImportError:
            print(f"Error: Unable to import {base_file_name}.py")
            return None

def main():
    init = Initialization()
    init.toString()

if __name__=="__main__":
    main()