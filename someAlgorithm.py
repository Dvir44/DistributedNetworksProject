import computer
from communication  import Communication

''' user implemented code that runs a broadcast algorithm'''

def mainAlgorithm(self: computer.Computer, communication : Communication, message = None):
    if  self.state != "terminated":
        communication.send_to_all(self.id, "running a broadcast")
        self.color = "#7427e9"
        self.state = "terminated"


def init(self: computer.Computer, communication : Communication, message = None):
    if self.is_root:
        print(self.id, " is root")
        communication.send_to_all(self.id, "running a broadcast")
        self.color = "#000000"
        self.state = "terminated"