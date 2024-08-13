import simulator.computer as computer
from simulator.communication import Communication
import numpy as np

''' 
user implemented code that runs a BFS algorithm

we have the following data for each computer:
- state - activated / diactivated (every computer starts at deactivated and changes to terminated when he finishes)
- parent - the parents id
- distance - the distance that they change during the algorithm 
'''

colors = ["blue", "red", "green", "yellow", "purple", "pink", "orange", "cyan", "magenta", "lime", "teal", "lavender", "brown", "maroon", "navy", "olive", "coral", "salmon", "gold", "silver"]

def mainAlgorithm(self: computer.Computer, communication: Communication, _arrival_time, message = None):
    if self.state != "activated":
        try:
            message_parts = message.split(" ")
            dist = float(message_parts[-3])
            parent = int(message_parts[-1])
        except (ValueError, IndexError) as e:
            print(f"Error processing message: {e}")
            return
        
        if dist + 1 < self.distance:
            self.state = "activated"
            self.parent = parent
            self.distance = dist + 1
            color_index = int(dist) % len(colors)
            self.color = colors[color_index]
            communication.send_to_all(self.id, f"running a BFS with distance {self.distance} from {self.id}", _arrival_time)
            self.state = "deactivated"
            
def init(self: computer.Computer, communication : Communication):
    if self.is_root:
        print(f"{self.id} is the root")
        self.parent = self.id
        self.distance = 0
        communication.send_to_all(self.id, f"running a BFS with distance {self.distance} from {self.parent}")
        self.color = "#000000"
        self.state = "terminated"
    else:
        self.parent = None
        self.distance = np.inf