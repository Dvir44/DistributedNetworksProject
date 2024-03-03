import string
import threading
import numpy
from computer import Computer

import initializationModule

# message format: specified in "Message Format.docx"

def send_message(message : list, network : initializationModule.Initialization):
    source_id = message[0]
    current_id = message[1]
    destinations = message[2]
    current_state = message[3]
    next_state = message[4]
    arrival_time = message[5]
    message_content = message[6]

    if (destinations=='a'):
        for current_computer in network.connectedComputers:
            if (current_id == current_computer.getId()): # finding the current computer
                break
        
        message[5]+=1 # increase arrival time by 1 for now
        print("connected to: ", current_computer.connectedEdges)
         # creating new messages that we put into the network pq, according to the destination field
        for connected_computers in current_computer.connectedEdges:
            new_message = message.copy()  # the put() operation into the pq is by reference
            new_message[0] = current_id
            new_message[1] = connected_computers
            network.networkMessageQueue.put(new_message)
            print("message added no network queue: ", new_message)

            
def receive_message(message : list, network : initializationModule.Initialization):
    print("message being worked on: ", message)
    current_id = message[1]
    
    for current_computer in network.connectedComputers:
        if current_computer.getId()==current_id: # finding the current computer
            algorithm_function = getattr(current_computer.algorithmFile, 'mainAlgorithm', None)
            
            if callable(algorithm_function):
                algorithm_function(current_computer, network, message) # run mainAlgorithm
            else:
                print(f"Error: Function 'mainAlgorithm' not found in {current_computer.algorithmFile}.py")
                return None

def main():
    pass

if __name__=="__main__":
    main()