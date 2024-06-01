import numpy
import initializationModule

import usefulFunctions

class CommunicationModule:
    def __init__(self, network: initializationModule.Initialization, displayType: str):
        self.network = network
        self.displayType = displayType

    # Send a message from the source computer to the destination computer
    def send_message(self, source, dest, message_info):
        current_computer = self.network.find_computer(source)
            
        edge_tuple = (min(source, dest), max(dest, source)) # represents edge source->dest or dest->source
        delay = self.network.edgesDelays.get(edge_tuple, 0)        
        
        # creating a new message which will be put into the queue
        if not current_computer.state=="terminated":
            destination_computer = self.network.find_computer(dest)
                      
            # updating destination computer clock
            if destination_computer.internalClock != 0:
                destination_computer.internalClock = max(0, min(current_computer.internalClock+delay, destination_computer.internalClock))
            else:
                destination_computer.internalClock = current_computer.internalClock+delay
            
            message = {
            'source_id': source,
            'dest_id': dest,
            'arrival_time': current_computer.internalClock + delay,
            'content': message_info
            }
            self.network.networkMessageQueue.push(message)
        
            # if display is text, print
            if self.displayType=="Text":
                pass
                #print("message added to network queue: ",message)
        
    def send_to_all(self, source_id, message_info):
        source_computer = self.network.find_computer(source_id)
        for index, connected_computer_id in enumerate(source_computer.connectedEdges):
            self.send_message(source_id, connected_computer_id, message_info)
            
    def receive_message(self, message : dict, comm):
        #if self.displayType=="Text":
        print("message received: ", message)
            
        current_id = message['dest_id']
        source_id = message['source_id']
        
        current_computer = self.network.find_computer(current_id)
        current_computer.receivedFrom = source_id
        
        algorithm_function = getattr(current_computer.algorithmFile, 'mainAlgorithm', None)
        
        values = [str(current_computer.getId()), str(current_computer.getColor()), str(current_computer.getRoot()), str(current_computer.getState()), str(current_computer.getReceivedFrom())] # current values

        if callable(algorithm_function):
            algorithm_function(current_computer, comm) # run mainAlgorithm
            if self.displayType=="Graph":
                new_values = [str(current_computer.getId()), str(current_computer.getColor()), str(current_computer.getRoot()), str(current_computer.getState()), str(current_computer.getReceivedFrom())] # updated values
                if values!=new_values: # if some values have changed then append to the change list for the graph display
                    self.network.node_values_change.append(new_values)
            
        else:
            print(f"Error: Function 'mainAlgorithm' not found in {current_computer.algorithmFile}.py")
            return None
 
def main():
    pass

if __name__=="__main__":
    main()