import queue
import computer
import communicationModule

''' user implemented code that runs a broadcast algorithm'''

def runAlgorithm(self: computer.Computer, network):
    root_selection(self) # root selection
    populate_queues(self)
    while(self.getState()!=1):
        if (not self.messageQueue.empty()): # there is a message in queue
            communicationModule.receive_message(self, network)
            self.setState(1)
            
def root_selection(self: computer.Computer):
    if (self.getId()==3):
        self.root=1

def populate_queues(self: computer.Computer):
    if (self.getRoot()==1):
        self.messageQueue.put(str(self.getId())+"##"+"a"+"##"+"message started at root, running a broadcast"+"##"+"0")
    
def runAlgorithm2(self: computer):
    print(self.getId())
    if (self.getId()==5):
        print("Im number 5")
    else:
        print("Im not")

def main():
    pass