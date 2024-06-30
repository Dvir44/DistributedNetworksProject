import computer
import communicationModule

''' user implemented code that runs a broadcast algorithm'''

def mainAlgorithm(self: computer.Computer, communication : communicationModule.CommunicationModule, message = None):
    if  self.state != "terminated":
        communication.send_to_all(self.id, "running a broadcast")
        self.color = "#7427e9"
        self.state = "terminated"


def init(self: computer.Computer, communication : communicationModule.CommunicationModule, message = None):
    if self.is_root:
        print(self._id, " is root")
        communication.send_to_all(self._id, "running a broadcast")
        self.color = "#000000"
        self.state = "terminated"
    #if self.id==79:
    #    self.id=11


def main():
    pass

if __name__=="__main__":
    main() 