import computer
import communicationModule

''' 
user implemented code that runs a BFS algorithm

we have the following data for each computer:
- state - activated / diactivated (every computer starts at deactivated and changes to terminated when he finishes)
- parent - the parents id
- distance - the distance that they change during the algorithm 
'''

colors = ["blue", "red", "green", "yellow", "purple", "pink"]

def mainAlgorithm(self: computer.Computer, communication : communicationModule.CommunicationModule, message):
    if  self.state != "activated":
        message = message.split(" ")
        dist = float(message[-3])
        parent = int(message[-1])
        
        if dist + 1 < self.getDistance():
            self.setState("activated")
            self.setParent(parent)
            self.setDistance(dist+1)
            self.setColor(colors[int(dist)])
            communication.send_to_all(self.id, f"running a BFS with distance {self.getDistance()} from {self.getId()}")
            self.setState("deactivated")
            



def init(self: computer.Computer, communication : communicationModule.CommunicationModule, message = None):
    if (self.getRoot()):
        print(f"{self.getId()} is the root")
        self.setParent(self.getId())
        self.setDistance(0)
        communication.send_to_all(self.id, f"running a BFS with distance {self.getDistance()} from {self.getParent()}")
        self.setColor("#000000")
        self.setState("terminated")


def main():
    pass

if __name__=="__main__":
    main() 