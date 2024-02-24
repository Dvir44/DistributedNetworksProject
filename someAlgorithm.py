import queue
import computer
import communicationModule

def runAlgorithm(self: computer.Computer, network): # broadcast
    init_broadcast(self)
    populate_queues(self)
    while(self.getState()!=1):
        #if (not self.receiveMessages.empty()): # there is a message
        communicationModule.receive_message(self, network)
            
def init_broadcast(self: computer.Computer):
    if (self.getId()==3):
        self.root=1

def populate_queues(self: computer.Computer):
    if (self.getRoot()==1):
        self.receiveMessages.put(str(self.getId())+"##"+"a"+"##"+"message from root"+"##"+"0")
    


def runAlgorithm2(self: computer):
    print(self.getId())
    if (self.getId()==5):
        print("Im number 5")
    else:
        print("Im not")

def main():
    pass