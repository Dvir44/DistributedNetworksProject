import queue
import computer
import communicationModule

''' user implemented code that runs a broadcast algorithm'''

def mainAlgorithm(self: computer.Computer, network, message):
    if self.state == 1:
        self.messageQueue.queue.clear()
    else:
        communicationModule.send_message(message, network)
        self.setState(1)

def init(self: computer.Computer):
    if (self.getId()==3):
        self.root=1
    if (self.getRoot()==1):
        message = [self.id, self.id, "a",0, 0, 0, "running a broadcast"]
        self.messageQueue.put(message)

def main():
    pass