import computer
import communicationModule
import numpy as np
''' 
user implemented code that runs a BFS algorithm

we have the following data for each computer:
- state - activated / diactivated (every computer starts at deactivated and changes to terminated when he finishes)
- parent - the parents id
- distance - the distance that they change during the algorithm 
'''

colors = ["blue", "red", "green", "yellow", "purple", "pink", "orange", "cyan", "magenta", "lime", "teal", "lavender", "brown", "maroon", "navy", "olive", "coral", "salmon", "gold", "silver"]
def mainAlgorithm(self: computer.Computer, communication : communicationModule.CommunicationModule, message):
    if  self.state != "activated":
        message = message.split(" ")
        dist = float(message[-3])
        parent = int(message[-1])
        
        if dist + 1 < self.distance:
            self.state = "activated"
            self.parent = parent
            self.distance = dist + 1
            self.color = colors[int(dist)]
            communication.send_to_all(self._id, f"running a BFS with distance {self.distance} from {self._id}")
            self.state ="deactivated"
            



def init(self: computer.Computer, communication : communicationModule.CommunicationModule, message = None):
    if self.is_root:
        print(f"{self._id} is the root")
        self.parent = self._id
        self.distance = 0
        communication.send_to_all(self._id, f"running a BFS with distance {self.distance} from {self.parent}")
        self.color = "#000000"
        self.state = "terminated"
    else:
        self.parent = None
        self.distance = np.inf


def main():
    pass

if __name__=="__main__":
    main() 