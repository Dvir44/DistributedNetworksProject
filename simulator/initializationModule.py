import importlib
import json
import os
import random
import sys

import numpy as np
from simulator.computer import Computer
import heapq
import math
from itertools import combinations

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])  # Path compression
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            # Union by rank
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1



class CustomMinHeap:
    def __init__(self):
        self.heap = []
        self.counter = 0  # unique sequence count
        
    def push(self, message_format):
        heapq.heappush(self.heap, (message_format['arrival_time'], self.counter, message_format))
        self.counter += 1
        
    def pop(self) -> dict:
        priority, priority2, message_format = heapq.heappop(self.heap)
        return message_format
        
    def empty(self) -> bool: 
        return len(self.heap) == 0

    def size(self) -> int:
        return len(self.heap)


class Initialization:
    '''
    Initialization Class - sets up the network parameters and topology based on user input
    '''
    def __init__(self):
        self.load_config()
        self.connected_computers = [Computer() for _ in range(self.computer_number)]
        self.network_message_queue = CustomMinHeap()
        self.node_values_change = [] # for graph display
        self.edges_delays={} # holds the delays of each edge in the network

        self.create_computer_ids()
        
        self.network_dict = {}
        for i in self.connected_computers:
            self.network_dict[i.id] = i
        self.root_selection()

        self.create_connected_computers()
        self.load_algorithms(self.algorithm_path)
        self.delays_creation()
        
        
    def load_config(self):
        with open('network_variables.json', 'r') as f:
            data = json.load(f)
        self.computer_number = int(data.get('Number of Computers', 10))
        self.topologyType = data.get('Topology', 'Line')
        self.id_type = data.get('ID Type', 'Sequential')
        self.display_type = data.get('Display', 'Text')
        self.root_type = data.get('Root', 'Random')
        self.delay_type = data.get('Delay', 'Random')
        self.algorithm_path = data.get('Algorithm', 'no_alg_provided')
        lambda_value_str = data.get('Lambda Value', 1.5)
        self.logging_type = data.get('Logging', 'Short')

        
        
    def __str__(self) -> list:
        result = [
            f"Number of Computers: {self.computer_number}",
            f"Topology: {self.topologyType}",
            f"ID Type: {self.id_type}",
             f"Display Type: {self.display_type}",
            "\nComputers:"
        ]
        result.extend(str(comp) for comp in self.connected_computers)
        return "\n".join(result)
            
    def delays_creation(self):
        if self.delay_type=="Random":
            self.random_delay()
        else:
            self.constant_delay()
            
    # Creates random delay for every edge
    def random_delay(self):
        for comp in self.connected_computers:
            comp.delays = [None] * len(comp.connectedEdges)
            for i, connected in enumerate(comp.connectedEdges):
                edge_tuple = (comp.id, connected) if comp.id < connected else (connected, comp.id) # unique representation of the edge as a tuple
                
                if edge_tuple not in self.edges_delays: # if not already in edgesDelays, generate a random delay, and insert into edgesDelays
                    random_num = random.random()
                    self.edges_delays[edge_tuple] = random_num
                
                comp.delays[i] = self.edges_delays[edge_tuple]
                
    # Creates constant delay for every edge
    def constant_delay(self):
        for comp in self.connected_computers:
            comp.delays = [None] * len(comp.connectedEdges)
            for i, connected in enumerate(comp.connectedEdges):
                edge_tuple = (comp.id, connected) if comp.id < connected else (connected, comp.id) # unique representation of the edge as a tuple
                
                if edge_tuple not in self.edges_delays: # if not already in edgesDelays, generate a delay of 1 and insert into edgesDelays
                    self.edges_delays[edge_tuple] =1
                
                comp.delays[i] = self.edges_delays[edge_tuple]



    #Creates network topology
    def create_connected_computers(self):
        topology_functions = {
            "Random": self.create_random_topology,
            "Line": self.create_line_topology,
            "Clique": self.create_clique_topology,
            "Tree": self.create_tree_topology,
            "Star": self.create_star_topology,
            }
        
        topology_function = topology_functions[self.topologyType]
        topology_function()
        
        connected = self.is_connected()
        while (not connected):
            topology_function()
            connected = self.is_connected()

    def is_connected(self):
        uf = UnionFind(len(self.connected_computers))

        for node in self.connected_computers:
            for neighbor in node.connectedEdges:
                uf.union(self.connected_computers.index(node), self.connected_computers.index(self.network_dict[neighbor]))

        root = uf.find(0)
        return all(uf.find(i) == root for i in range(len(self.connected_computers)))

    # Create computer IDs based on the IdType
    def create_computer_ids(self):
        id_functions = {
        "Random": self.create_random_ids,
        "Sequential": self.create_sequential_ids,
        }
        
        id_function = id_functions[self.id_type]
        id_function()


    # Create random computer IDs (ensuring uniqueness)
    def create_random_ids(self):
        used_ids = set()
        for comp in self.connected_computers:
            comp_id = random.randint(100, 100 * self.computer_number - 1)
            while comp_id in used_ids:
                comp_id = random.randint(100, 100 * self.computer_number - 1)
            comp.id = comp_id
            used_ids.add(comp_id)

    # Create sequential computer IDs
    def create_sequential_ids(self):
        for i, comp in enumerate(self.connected_computers):
            comp.id = i
            

    # Create a random topology for the network
    def create_random_topology(self):
        ids_list = [comp.id for comp in self.connected_computers]

        if len(self.connected_computers) == 2:
            # Connect the first computer to the second
            self.connected_computers[0].connectedEdges.append(self.connected_computers[1].id)
            self.connected_computers[1].connectedEdges.append(self.connected_computers[0].id)

        elif len(self.connected_computers) == 3:
            # Generate all possible connected graphs for 3 nodes
            possible_edges = list(combinations(ids_list, 2))  # All pairs of nodes
            connected_graphs = [
                [(0, 1), (1, 2)],  # Line: 0-1-2
                [(0, 1), (0, 2)],  # Star: 0-1, 0-2
                [(0, 1), (1, 2), (0, 2)]  # Triangle: 0-1-2-0
            ]

            # Choose one random connected graph
            chosen_edges = random.choice(connected_graphs)

            # Create the connections based on the chosen graph
            for u, v in chosen_edges:
                self.connected_computers[u].connectedEdges.append(self.connected_computers[v].id)
                self.connected_computers[v].connectedEdges.append(self.connected_computers[u].id)

        else:
            for i, comp in enumerate(self.connected_computers):
                # Determine a random number of edges (between 1 and 2 * log(computer_number - 1))
                num_edges = random.randint(1, 2 * int(math.log(self.computer_number - 1)))
                # Choose num_edges unique vertices (excluding comp.id)
                connected_to_vertices = random.sample([j for j in ids_list if j != comp.id], num_edges)

                # Add connections
                comp.connectedEdges.extend(connected_to_vertices)

                # Ensure bi-directional connection
                for connected_to_id in connected_to_vertices:
                    for comp_other in self.connected_computers:
                        if comp_other.id == connected_to_id:
                            comp_other.connectedEdges.append(comp.id)
                            break

            # Remove duplicates
            for comp in self.connected_computers:
                comp.connectedEdges = list(set(comp.connectedEdges))

    # Create line topology for the network
    def create_line_topology(self):
        for i in range(self.computer_number - 1):
            # Connect each computer to the next one in line
            self.connected_computers[i].connectedEdges.append(self.connected_computers[i+1].id)
            self.connected_computers[i + 1].connectedEdges.append(self.connected_computers[i].id)  # Ensure bi-directional connection


    # Create clique topology for the network
    def create_clique_topology(self):        
        # Connect each computer to every other computer
        for i in range(self.computer_number):
            for j in range(i + 1, self.computer_number):
                # Ensure bi-directional connection
                self.connected_computers[i].connectedEdges.append(self.connected_computers[j].id)
                self.connected_computers[j].connectedEdges.append(self.connected_computers[i].id)

        # Removing duplicates
        for comp in self.connected_computers:
            comp.connectedEdges = list(set(comp.connectedEdges)) 

    def create_tree_topology(self, max_height=None):
        if max_height is None:
            max_height = int(np.log2(self.computer_number)) + 1

        # Find the root node based on the is_root field
        root = None
        for comp in self.connected_computers:
            if getattr(comp, 'is_root', False):
                root = comp
                break

        # Initialize a queue with the root node and track their heights
        queue = [(root, 0)]
        next_computer_index = 0
        
        used_computers = set([root.id])

        # While there are still computers to connect
        while len(used_computers) < self.computer_number:
            if not queue:
                break
            # Take the next node and its height from the queue
            parent, height = queue.pop(0)
            
            if height >= max_height:
                continue
            
            # Determine a random number of children for the current parent using Poisson distribution
            children_count = np.random.poisson(self.lambda_value)  # using lambda value from config

            # Ensure the number of children is at least 1 and does not exceed the remaining nodes
            children_count = min(max(1, children_count), self.computer_number - len(used_computers))

            for _ in range(children_count):
                if len(used_computers) >= self.computer_number:
                    break
                # Find the next available computer to connect
                while next_computer_index in used_computers or next_computer_index >= self.computer_number:
                    next_computer_index += 1
                if next_computer_index >= self.computer_number:
                    break
                # Connect the parent to the child
                child = self.connected_computers[next_computer_index]
                parent.connectedEdges.append(child.id)
                child.connectedEdges.append(parent.id)  # Ensure bi-directional connection
                
                # Add the child to the queue with its height
                queue.append((child, height + 1))
                used_computers.add(next_computer_index)
                next_computer_index += 1

        # Removing duplicates
        for comp in self.connected_computers:
            comp.connectedEdges = list(set(comp.connectedEdges))

    def create_star_topology(self):
        root = None
        for comp in self.connected_computers:
            if getattr(comp, 'is_root', False):
                root = comp
                break

        # Connect all other nodes to the hub
        for comp in self.connected_computers:
            if comp.id != root.id:
                root.connectedEdges.append(comp.id)
                comp.connectedEdges.append(root.id)  # Ensure bi-directional connection


    def load_algorithms(self, algorithm_module_path):
        if algorithm_module_path == 'no_alg_provided':
            print("No algorithm was provided")
            #exit()

            directory, file_name = os.path.split("./algorithms/someAlgorithm.py")
            base_file_name, _ = os.path.splitext(file_name)
            sys.path.insert(0,directory)

            algorithm_module = importlib.import_module(base_file_name)
            for comp in self.connected_computers:
                comp.algorithm_file = algorithm_module
        try:
            directory, file_name = os.path.split(algorithm_module_path)
            base_file_name, _ = os.path.splitext(file_name)
            sys.path.insert(0,directory)

            algorithm_module = importlib.import_module(base_file_name)
            for comp in self.connected_computers:
                comp.algorithm_file = algorithm_module

        except ImportError:
            print(f"Error: Unable to import {base_file_name}.py")
            return None

    def root_selection(self):
        if self.root_type == "Random":
            selected_computer = random.choice(self.connected_computers)
            selected_computer.is_root=True
        elif self.root_type=="Min ID":
            selected_computer = min(self.connected_computers, key=lambda computer: computer.id)
            selected_computer.is_root=True

    def find_computer(self, id: int) -> Computer:
        for comp in self.connected_computers:
            if comp.id == id:
                return comp
        return None

def main():
    init = Initialization()
    init.toString()

if __name__=="__main__":
    main()