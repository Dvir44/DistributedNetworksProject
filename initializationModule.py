import importlib
import json
import os
import random
import sys
import computer
import heapq
import math

class CustomMinHeap:
    def __init__(self):
        self.heap = []
        self.counter = 0  # unique sequence count
        
    def push(self, message_format):
        heapq.heappush(self.heap, (message_format['arrival_time'], self.counter, message_format))
        self.counter += 1
    def pop(self):
        priority, priority2, message_format = heapq.heappop(self.heap)
        return message_format
        
    def empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

class Initialization:
    '''
    Initialization Class - sets up the network parameters and topology based on user input
    '''
    def __init__(self):
        self.load_config()
        self.connectedComputers = []
        self.connectedComputersCreation()
        self.loadAlgorithms(self.algorithm_path)
        self.networkMessageQueue = CustomMinHeap()
        self.node_values_change = [] # for graph
        self.rootSelection()
        self.edgesDelays={} # holds the delays of each edge in the graph
        self.delaysCreation()
        
        
    def load_config(self):
        with open('network_variables.json', 'r') as f:
            data = json.load(f)
        self.numberOfComputers = int(data.get('Number of Computers', 5))
        self.topologyType = data.get('Topology', 'Line')
        self.IdType = data.get('ID Type', 'Sequential')
        self.displayType = data.get('Display', 'Text')
        self.algorithm_path = data.get('Algorithm', 'no_alg_provided')
        self.rootType = data.get('Root', 'Random')
        self.delay = data.get('Delay', 'Random')
        
        
        
        
    def __str__(self):
        result = [
            f"Number of Computers: {self.numberOfComputers}",
            f"Topology: {self.topologyType}",
            f"ID Type: {self.IdType}",
            f"Display Type: {self.displayType}",
            f"Delays: {self.edgesDelays}",
            "\nComputers:"
        ]
        result.extend(str(comp) for comp in self.connectedComputers)
        return "\n".join(result)
            
    def delaysCreation(self):
        if self.delay=="Random":
            self.randomDelay()
        else:
            self.constantDelay()
            
    # Creates random delay for every edge
    def randomDelay(self):
        for comp in self.connectedComputers:
            comp.delays = [None] * len(comp.connectedEdges)
            for i, connected in enumerate(comp.connectedEdges):
                edge_tuple = (comp.id, connected) if comp.id < connected else (connected, comp.id) # unique representation of the edge as a tuple
                
                if edge_tuple not in self.edgesDelays: # if not already in edgesDelays, generate a random delay, and insert into edgesDelays
                    random_num = random.randint(1, 10)
                    self.edgesDelays[edge_tuple] = random_num
                
                comp.delays[i] = self.edgesDelays[edge_tuple]
                        
    '''
    ***********************************************************************************
        need to change to be bi-directional!!!
    ***********************************************************************************
    '''
    def constantDelay(self):
        for comp in self.connectedComputers:
            comp.delays = [None]*len(comp.connectedEdges)
            for i in range(len(comp.connectedEdges)):
                comp.delays[i]=5

    #Creates the connectedComputers list
    def connectedComputersCreation(self):
        self.connectedComputers = [computer.Computer() for _ in range(self.numberOfComputers)] 
        self.createComputersIds() #Fill the Id's according to the user choice
        
        if (self.topologyType == "Random"):
            self.createRandomTopology()
        elif (self.topologyType == "Line"):
            self.createLineTopology()
        elif (self.topologyType == "Clique"):
            self.createCliqueTopology()
        return
    

    # Create computer IDs based on the IdType
    def createComputersIds(self):
        if self.IdType == "Random":
            self.createRandomIds()
        elif self.IdType == "Sequential":
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

    # Create a random topology for the network
    def createRandomTopology(self):
        ids_list=[]
        for comp in self.connectedComputers:
            ids_list.append(comp.getId())

        for i, comp in enumerate(self.connectedComputers):
            # Determine a random number of edges (between 1 and numberOfComputers - 1)
            num_edges = random.randint(1, 2*int(math.log(self.numberOfComputers - 1)))
            # Choose num_edges unique vertices (excluding  comp.getId())
            connected_to_vertices = random.sample([j for j in ids_list if j != comp.getId()], num_edges)

            # Add connections
            comp.connectedEdges.extend(connected_to_vertices)

            # Ensure bi-directional connection
            for connected_to_id in connected_to_vertices:
                for comp in self.connectedComputers:
                    if comp.getId()==connected_to_id:
                        comp.connectedEdges.append(self.connectedComputers[i].getId())
                        break
                        
                
        # removing duplicates
        for comp in self.connectedComputers:
            comp.connectedEdges=list(set(comp.connectedEdges))

    # Create line topology for the network
    def createLineTopology(self):
        for i in range(self.numberOfComputers - 1):
            # Connect each computer to the next one in line
            self.connectedComputers[i].connectedEdges.append(self.connectedComputers[i+1].getId())
            self.connectedComputers[i + 1].connectedEdges.append(self.connectedComputers[i].getId())  # Ensure bi-directional connection


    # Create clique topology for the network
    def createCliqueTopology(self):        
        # Connect each computer to every other computer
        for i in range(self.numberOfComputers):
            for j in range(i + 1, self.numberOfComputers):
                # Ensure bi-directional connection
                self.connectedComputers[i].connectedEdges.append(self.connectedComputers[j].getId())
                self.connectedComputers[j].connectedEdges.append(self.connectedComputers[i].getId())

        # Removing duplicates
        for comp in self.connectedComputers:
            comp.connectedEdges = list(set(comp.connectedEdges)) 



    def loadAlgorithms(self, algorithm_module_path):
        if algorithm_module_path == 'no_alg_provided':
            print("No algorithm was provided")
            #exit()
            
            directory, file_name = os.path.split("./someAlgorithm.py")
            base_file_name, _ = os.path.splitext(file_name)
            sys.path.insert(0,directory)

            algorithm_module = importlib.import_module(base_file_name)
            for comp in self.connectedComputers:
                comp.algorithmFile = algorithm_module
        try:
            directory, file_name = os.path.split(algorithm_module_path)
            base_file_name, _ = os.path.splitext(file_name)
            sys.path.insert(0,directory)

            algorithm_module = importlib.import_module(base_file_name)
            for comp in self.connectedComputers:
                comp.algorithmFile = algorithm_module

        except ImportError:
            print(f"Error: Unable to import {base_file_name}.py")
            return None

    def rootSelection(self):
        if self.rootType == "Random":
            selected_computer = random.choice(self.connectedComputers)
            selected_computer.root=True
        elif self.rootType=="Min ID":
            selected_computer = min(self.connectedComputers, key=lambda computer: computer.getId())
            selected_computer.root=True




    def find_computer(self, id: int):
        for computer in self.connectedComputers:
            if computer.getId() == id:
                return computer
        return None

def main():
    init = Initialization()
    init.toString()

if __name__=="__main__":
    main()