import queue
import random
import numpy

class Computer:
    '''
    Computer Class - create a vertex in the full topology with the next members:
    ID - the id of the computer
    ConnectedEdges - who the computer is connected to
    Messages - a messages queue that the commputer have
    '''
    # Default constructor
    def __init__(self):
        self.id = None
        self.connectedEdges = []
        self.delays = []
        self.sendMessages = queue.Queue()
        self.receiveMessages = queue.Queue()
        self.algorithm=None
        self.state = 0
        self.root = 0

    def __str__(self):
        return f"id = {self.id}\nconnected edges = {self.connectedEdges}\ndelays = {self.delays}\n"
    
    #Getters
    def getId(self):
        return self.id
    def getConnectedEdges(self):
        return self.connectedEdges
    def getDelays(self):
        return self.delays
    def getState(self):
        return self.state
    def getRoot(self):
        return self.root
    
    def setState(self, num: int):
        self.state=num
    
    def run(self, network):
        self.algorithm(self, network)
def main():
    pass

if __name__=="__main__":
    main()