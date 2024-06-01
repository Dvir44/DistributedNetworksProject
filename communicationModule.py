import numpy
import initializationModule



class CommunicationModule:
    def __init__(self, network: initializationModule.Initialization, displayType: str):
        self.network = network
        self.displayType = displayType

    # Send a message from the source computer to the destination computer
    def send_message(self, source, dest, message_info):
        for current_computer in self.network.connectedComputers:
            if (source == current_computer.getId()): # finding the current computer
                break
            
            
        edge_tuple = (min(source, dest), max(dest, source)) # represents edge source->dest or dest->source
        delay = self.network.edgesDelays.get(edge_tuple, 0)        
        

        # creating a new message, which will be put into the queue
        if not current_computer.state=="terminated":
                       
            for destination_computer in self.network.connectedComputers:
                if (destination_computer.getId()==dest): # finding the current computer
                    break
                
            message = {'source_id':None, 'dest_id':None, 'arrival_time':None, 'message_content':""}
            
            # updating destination computer clock
            if destination_computer.internalClock != 0:
                destination_computer.internalClock = max(0, min(current_computer.internalClock+delay, destination_computer.internalClock))
            else:
                destination_computer.internalClock = current_computer.internalClock+delay
                
            message['arrival_time'] = current_computer.internalClock+delay
            message['source_id'] = source
            message['dest_id'] = dest
            message['message_content'] = message_info
    
            self.network.networkMessageQueue.push(message)
        
            # if display is text, print
            if self.displayType=="Text":
                pass
                #print("message added to network queue: ",message)
           

           
           
    def send_to_all(self, source, message_info):
        for current_computer in self.network.connectedComputers:
                if (source == current_computer.getId()): # finding the current computer
                    break
        for index, connected_computer_id in enumerate(current_computer.connectedEdges):
            self.send_message(source, connected_computer_id, message_info)
            




    def receive_message(self, message : dict, comm):
        #if self.displayType=="Text":
        print("message received: ", message)
            
        current_id = message['dest_id']
        source_id = message['source_id']
        
        for current_computer in self.network.connectedComputers:
            if current_computer.getId()==current_id: # finding the current computer
                break
        
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
           



    def init_receive_message(self, message:dict, comm):
        
        pass

def main():
    pass

if __name__=="__main__":
    main()