class Computer:
    """
    A class representing A computer in the network.
    
    Attributes:
        id: the id of the computer.
        ConnectedEdges: computer ids that the computer is connected to (int type).
        Delays: the delay to each edge in the same order as ConnectedEdges list.
        algorithm: the algorithm the computer runs.
        state: computer state.
        root: whether the computer is a root.
        color: computer color.
        _internal_clock: used for delay.
    """
    
    def __init__(self):
        self.id = None
        self.connectedEdges = []
        self.delays = []
        self.algorithm_file=None
        self.state = None
        self.is_root = False
        self.color = "olivedrab"
                
        self._internal_clock = 0
        
    def __str__(self):
        return f"id = {self.id}\nconnected edges = {self.connectedEdges}\ndelays = {self.delays}\n"
    
    def getConnectedEdges(self):
        return self.connectedEdges
    def getDelays(self):
        return self.delays
