import queue
import computer
import communicationModule

''' user implemented code that runs a broadcast algorithm'''

def mainAlgorithm(self: computer.Computer, communication):
    if self.state == 1:
        self.messageQueue.queue.clear()
    else:
        print(self.getId(), end=" ")
        print("H")
        communication.send_to_all(self.getId, 2, "running a broadcast")
        self.setState(1)

def init(self: computer.Computer, communication):
    if (self.getId()==3):
        self.root=1
    if (self.getRoot()==1):
        print(self.getId(), end=" ")
        print("N")
        communication.send_to_all(self.getId(), 1, "running a broadcast")

def main():
    pass

if __name__=="__main__":
    main()