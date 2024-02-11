import json
import random
import numpy
import computer

class Initialization:
    '''
    Initialization Class - creates the basic parameters we get from the user in the visualization class
    and then we create the basic base for the simulation to run on
    '''
    #Defualt constructor
    def __init__(self):
        with open('network_variables.json', 'r') as f:
            data = json.load(f)
        self.numberOfComputers = data.get('Number of Computers',0)
        self.topologyType = data.get('Topology',0)
        self.IdType = data.get('ID Type',0)
        self.connectedComputers = []
        self.delayType = data.get('Delay',0)
    
    #Getters
    def getNumberOfComputers(self):
        return self.numberOfComputers
    def getTopologyType(self):
        return self.topologyType
    def getConnectedComputers(self):
        return self.connectedComputers
    
    # Create the delays that the computer has according to what he choose
    def createDelays(self):
        if self.delayType == "no delay":
            for comp in self.connectedComputers:
                comp.delays = {connected_to: 0 for connected_to in comp.connectedEdges}
        elif "constant" in self.delayType:
            # Extract the constant value from the delayType
            constant_delay = float(self.delayType.split()[1])  # The delayType is in the format "constant x"
            
            for comp in self.connectedComputers:
                comp.delays = {connected_to: constant_delay for connected_to in comp.connectedEdges}
        # Need to add a delay that's not constant (to ask Ran how to determine it)
        return

    #Creates the connectedComputers list
    def connectedComputersCreation(self):
        self.connectedComputers = [computer.Computer() for _ in range(self.numberOfComputers)] 
        self.createComputersIds() #Fill the Id's according to the user choice
        
        if (self.topologyType == "Random"):
            self.createRandomTopology()
        elif (self.topologyType == "Line"):
            self.createLineTopology()
        return
    
    # Create computer IDs based on the IdType
    def createComputersIds(self):
        if self.IdType == "Random":
            self.createRandomIds()
        elif self.IdType == "Uniform":
            self.createUniformIds()

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
    def createUniformIds(self):
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

    def createLineTopology(self):
        for i in range(self.numberOfComputers - 1):
            # Connect each computer to the next one in line
            self.connectedComputers[i].connectedEdges.append(i + 1)
            self.connectedComputers[i + 1].connectedEdges.append(i)  # Ensure bi-directional connection




def main():
    pass

if __name__=="__main__":
    main()