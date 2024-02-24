import string
import numpy
from computer import Computer

import initializationModule

# message format: id##destination_ids##


def send_message(self: Computer, message: str, network: initializationModule.Initialization=""):
    print(type(network.connectedComputers))
    for i in network.connectedComputers:
        i.receiveMessages.put(message)
        #network.connectedComputers[i].receiveMessages.put(message)
            
        
def receive_message(self: Computer, network: initializationModule.Initialization=""):
    # do some more things that are according to the message format, like change state or whatever
    if (not self.receiveMessages.empty()):
        self.setState(1)
        message = self.receiveMessages.get()
        message_format = message.split("##")
        print("Message source: ", self.getId(), " Message: ", message_format[2])
        send_message(self, message, network)
        
def main():
    pass

if __name__=="__main__":
    main()