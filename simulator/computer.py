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
    
    def __init__(self,  ):     
        self._has_changed = False
                
        self.id = None
        self.connectedEdges = []
        self.delays = []
        self.algorithm_file=None
        self.state = None
        self.is_root = False
        self.color = "olivedrab"

    def __str__(self):
        return f"id = {self.id}\nconnected edges = {self.connectedEdges}\ndelays = {self.delays}\n"
    
    def __setattr__(self, name, value):
        # Only set the flag if the attribute is not private
        if not name.startswith('_') and getattr(self, name, None) != value:
            self._has_changed = True
        super().__setattr__(name, value)

    def reset_flag(self):
        self._has_changed = False

    def has_changed(self):
        return self._has_changed
    
    def getConnectedEdges(self):
        return self.connectedEdges
    def getDelays(self):
        return self.delays
