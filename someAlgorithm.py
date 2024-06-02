import computer
import communicationModule

''' user implemented code that runs a broadcast algorithm'''

def mainAlgorithm(self: computer.Computer, communication : communicationModule.CommunicationModule):
    if  self.state != "terminated":
        communication.send_to_all(self.id, "running a broadcast")
        self.setColor("#7427e9")
        self.setState("terminated")


def init(self: computer.Computer, communication : communicationModule.CommunicationModule):
    if (self.getRoot()):
        print(self.id, " is root")
        communication.send_to_all(self.id, "running a broadcast")
        self.setColor("#000000")
        self.setState("terminated")
        self.id=11


def main():
    pass

if __name__=="__main__":
    main() 