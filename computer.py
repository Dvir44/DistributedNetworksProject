import queue
import random
import numpy

class Computer:
    '''
    Computer Class - create a vertex in the full topology with the next members:
    ID - the id of the computer
    ConnectedEdges - who the computer is connected to
    Delays - the delay to each edge in the same order as ConnectedEdges list
    Messages - a messages queue that the commputer have
    Algorithm - the algorithm that the computer needs to run from the user
    State - the state of the computer in the algorithm
    root - a member that tells if the computer is the root that starts the run
    '''
    # Default constructor
    def __init__(self):
        self.id = None
        self.connectedEdges = []
        self.delays = []
        self.messageQueue = queue.Queue()
        self.algorithmFile=None
        self.state = 0
        self.root = 0

    def __str__(self):
        return f"id = {self.id}\nconnected edges = {self.connectedEdges}\n"
    
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

def main():
    pass

if __name__=="__main__":
    main()