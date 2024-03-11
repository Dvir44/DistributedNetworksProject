import string
import threading
import numpy
from computer import Computer

import initializationModule
import runModule

class CommunicationModule:
    # message format: specified in "Message Format.docx"
    def __init__(self):
        self.network = runModule.network
        self.message = {'source_id':None, 'dest_id':None, 'arrival_time':0, 'delay_time':None,
                        'message_content':"", 'state':None}
    
    # Send a message from the source computer to the destination computer
    def send_message(self, source, dest, delay, message_info):
        for current_computer in self.network.connectedComputers:
                if (source == current_computer.getId()): # finding the current computer
                    break
        self.message['source_id'] = source
        self.message['dest_id'] = dest
        self.message['delay_time'] = delay
        self.message['arrival_time'] += 1+delay
        self.message['message_content'] = message_info
        self.network.networkMessageQueue.put(self.message)
        self.message['state']=1
        print("message added to network queue: ", self.message)

    def send_to_all(self, source, delay, message_info):
        self.network.networkMessageQueue.put(self.message)
        for current_computer in self.network.connectedComputers:
                if (source == current_computer.getId()): # finding the current computer
                    break
        for connected_computers in current_computer.connectedEdges:
            self.send_message(source, connected_computers, delay, message_info)
            

    def receive_message(self):
        print("message being worked on: ", self.message)
        current_id = self.message['dest_id']

        for current_computer in self.network.connectedComputers:
            if current_computer.getId()==current_id: # finding the current computer
                algorithm_function = getattr(current_computer.algorithmFile, 'mainAlgorithm', None)

                if callable(algorithm_function):
                    algorithm_function(current_computer, CommunicationModule()) # run mainAlgorithm
                else:
                    print(f"Error: Function 'mainAlgorithm' not found in {current_computer.algorithmFile}.py")
                    return None


'''
def send_message(message : list, network : initializationModule.Initialization):
    source_id = message[0]
    current_id = message[1]
    destinations = message[2]
    current_state = message[3]
    next_state = message[4]
    arrival_time = message[5]
    message_content = message[6]
    message_delay = message[7]

    if (destinations=='a'):
        for current_computer in network.connectedComputers:
            if (current_id == current_computer.getId()): # finding the current computer
                break
        
        message[5] = message[5] + 1 + message_delay # increase arrival time by 1 and the delay
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
'''
def main():
    pass

if __name__=="__main__":
    main()