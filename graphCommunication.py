import time
import numpy

from graphVisualization import MainWindow
class CommunicationModule:
    def __init__(self, network):
        self.network = network
        self.delayCounter = 0
    
    
    # Send a message from the source computer to the destination computer
    def send_message(self, source, dest, delay, message_info):
        for current_computer in self.network.connectedComputers:
            if (source == current_computer.getId()): # finding the current computer
                break

        if not current_computer.state=="terminated":
        # creating a new message, which will be put into the queue
            message = {'source_id':None, 'dest_id':None, 'arrival_time':0, 'delay_time':None,
                        'message_content':""}
            
            message['source_id'] = source
            message['dest_id'] = dest
            message['delay_time'] = delay
            message['arrival_time'] += delay+self.delayCounter
            message['message_content'] = message_info
            print("message added to network queue: ",message)
            self.network.networkMessageQueue.push(message)
            self.delayCounter+=1

    def send_to_all(self, source, delay, message_info):
        for current_computer in self.network.connectedComputers:
                if (source == current_computer.getId()): # finding the current computer
                    break
        for connected_computer in current_computer.connectedEdges:
            self.send_message(source, connected_computer, delay, message_info)
            
            
    def receive_message(self, message : dict, comm, widget: MainWindow):
        print("message being worked on: ", message)

        for current_computer in self.network.connectedComputers:
            if (message['source_id'] == current_computer.getId()): # finding the current computer
                break
            
        
        if current_computer.state=="terminated":
            widget.change_node_color(str(message['source_id']), "#000000")


        current_id = message['dest_id']
        for current_computer in self.network.connectedComputers:
            if current_computer.getId()==current_id: # finding the current computer
                algorithm_function = getattr(current_computer.algorithmFile, 'mainAlgorithm', None)

                if callable(algorithm_function):
                    algorithm_function(current_computer, comm) # run mainAlgorithm
                else:
                    print(f"Error: Function 'mainAlgorithm' not found in {current_computer.algorithmFile}.py")
                    return None

