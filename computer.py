import queue

class Computer:
    '''
    Computer Class - create a vertex in the full topology with the next members:
    ID - the id of the computer
    ConnectedEdges - computer ids that the computer is connected to (int type)
    Delays - the delay to each edge in the same order as ConnectedEdges list
    Messages - a messages queue that the computer has
    Algorithm - the algorithm the computer runs
    State - computer state
    root - whether the computer is a root
    color - computer color
    '''
    # Default constructor
    def __init__(self):
        self.id = None
        self.connectedEdges = []
        self.delays = []
        self.messageQueue = queue.Queue()
        self.algorithmFile=None
        self.state = None
        self.root = False
        self.color = None
        
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
    def getColor(self):
        return self.color
    
    
    
    def setState(self, num: int):
        self.state=num
        
    def setColor(self, new_color: str):
        self.color=new_color

def main():
    pass

if __name__=="__main__":
    main()