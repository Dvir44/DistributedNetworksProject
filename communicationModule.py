import numpy
import initializationModule


class CommunicationModule:
    def __init__(self, network: initializationModule.Initialization):
        self.network = network
        self.displayType = network.display_type

    # Send a message from the source computer to the destination computer
    def send_message(self, source, dest, message_info):
        current_computer = self.network.find_computer(source)
            
        edge_tuple = (min(source, dest), max(dest, source)) # represents edge source->dest or dest->source
        delay = self.network.edges_delays.get(edge_tuple, 0)        
        
        # creating a new message which will be put into the queue
        if not current_computer.state == "terminated":
            destination_computer = self.network.find_computer(dest)
                      
            # updating destination computer clock
            if destination_computer._internal_clock != 0:
                destination_computer._internal_clock = max(0, min(current_computer._internal_clock + delay, destination_computer._internal_clock))
            else:
                destination_computer._internal_clock = current_computer._internal_clock + delay
            
            message = {
            'source_id': source,
            'dest_id': dest,
            'arrival_time': current_computer._internal_clock + delay,
            'content': message_info
            }
            self.network.network_message_queue.push(message)
        
            # if display is text, print
            if self.displayType=="Text":
                pass

        
    def send_to_all(self, source_id, message_info):
        source_computer = self.network.find_computer(source_id)
        for index, connected_computer_id in enumerate(source_computer.connectedEdges):
            self.send_message(source_id, connected_computer_id, message_info)
            
    def receive_message(self, message : dict, comm):
        print("message received: ", message)
            
        current_id = message['dest_id']
        source_id = message['source_id']
        
        current_computer = self.network.find_computer(current_id)
        current_computer.receivedFrom = source_id
        
        algorithm_function = getattr(current_computer.algorithm_file, 'mainAlgorithm', None)
        
        values = [str(current_computer.id), str(current_computer.getColor()), str(current_computer.getRoot()), str(current_computer.getState()), str(current_computer.getReceivedFrom())] # current values

        if callable(algorithm_function):
            algorithm_function(current_computer, comm, message['content']) # run mainAlgorithm
            if self.displayType=="Graph":
                new_values = [str(current_computer.id), str(current_computer.getColor()), str(current_computer.getRoot()), str(current_computer.getState()), str(current_computer.getReceivedFrom())] # updated values
                if values!=new_values: # if some values have changed then append to the change list for the graph display
                    self.network.node_values_change.append(new_values)
            
        else:
            print(f"Error: Function 'mainAlgorithm' not found in {current_computer.algorithm_file}.py")
            return None
 
def main():
    pass

if __name__=="__main__":
    main()