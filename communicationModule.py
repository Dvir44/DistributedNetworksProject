import string
import threading
import numpy
from computer import Computer

import initializationModule

# message format: specified in "Message Format.docx"

def send_message(self: Computer, message: str, network: initializationModule.Initialization=""):
    message_format = message.split("##")
    if (message_format[1]=='a'):
        for i in network.connectedComputers:
            # ugly code, but we assumed each computer has simply 'int id' in its getConnectedEdges list,
            # instead of an actual Class Computer. So must compare the networks computers to the ids in the
            # current computer list
            if (i.getId() in self.getConnectedEdges()):
                message_format[0]=str(self.getId())
                corrected_message = "##".join(message_format)
                i.messageQueue.put(corrected_message)

    else: # need to implement code to send to certain destinations
        pass
            
        
def receive_message(self: Computer, network: initializationModule.Initialization=""):
    # do some more things that are according to the message format, like change state or whatever
    if (not self.messageQueue.empty()):
        message = self.messageQueue.get()
        message_format = message.split("##")
        print(message_format[0])
        print("My id is: ", self.getId(), "Message source: ", message_format[0], " Message: ", message_format[2])
        send_message(self, message, network)
        
def main():
    pass

if __name__=="__main__":
    main()