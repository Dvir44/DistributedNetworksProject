import computer
import communicationModule

''' user implemented code that runs a broadcast algorithm'''

def mainAlgorithm(self: computer.Computer, communication : communicationModule.CommunicationModule):
    if  self.state != "terminated":
        communication.send_to_all(self.getId(), 2, "running a broadcast")
        self.setState("terminated")


def init(self: computer.Computer, communication : communicationModule.CommunicationModule):
    if (self.getId()==1):
        self.root=1
    if (self.getRoot()==1):
        communication.send_to_all(self.getId(), 1, "running a broadcast")
        self.setState("terminated")

def main():
    pass

if __name__=="__main__":
    main()