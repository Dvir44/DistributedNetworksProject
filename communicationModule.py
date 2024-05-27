import numpy
import initializationModule



class CommunicationModule:
    def __init__(self, network: initializationModule.Initialization, displayType: str):
        self.network = network
        self.delayCounter = 0
        self.displayType = displayType


    # Send a message from the source computer to the destination computer
    def send_message(self, source, dest, delay, message_info):
        for current_computer in self.network.connectedComputers:
            if (source == current_computer.getId()): # finding the current computer
                break
            
        
        # creating a new message, which will be put into the queue
        if not current_computer.state=="terminated":
            message = {'source_id':None, 'dest_id':None, 'arrival_time':0, 'delay_time':None,
                        'message_content':""}
            
            message['source_id'] = source
            message['dest_id'] = dest
            message['delay_time'] = delay
            message['arrival_time'] += delay+self.delayCounter
            message['message_content'] = message_info

            self.network.networkMessageQueue.push(message)
            self.delayCounter+=1
        
         # if display is text, print
            if self.displayType=="Text":
                print("message added to network queue: ",message)
           

    def send_to_all(self, source, delay, message_info):
        for current_computer in self.network.connectedComputers:
                if (source == current_computer.getId()): # finding the current computer
                    break
        for connected_computer in current_computer.connectedEdges:
            self.send_message(source, connected_computer, delay, message_info)
            




    def receive_message(self, message : dict, comm):
        if self.displayType=="Text":
            print("message being worked on: ", message)
        current_id = message['dest_id']
        

        for current_computer in self.network.connectedComputers:
            if current_computer.getId()==current_id: # finding the current computer
                algorithm_function = getattr(current_computer.algorithmFile, 'mainAlgorithm', None)
                
                values = [str(current_computer.getId()), str(current_computer.getColor()), str(current_computer.getRoot()), str(current_computer.getState())]

                if callable(algorithm_function):
                    algorithm_function(current_computer, comm) # run mainAlgorithm
                    if self.displayType=="Graph":
                        new_values = [str(current_computer.getId()), str(current_computer.getColor()), str(current_computer.getRoot()), str(current_computer.getState())]
                        if values!=new_values: # if some values have changed then append to the change list for the graph
                            self.network.node_color_dict.append(new_values)
                    
                else:
                    print(f"Error: Function 'mainAlgorithm' not found in {current_computer.algorithmFile}.py")
                    return None


def main():
    pass

if __name__=="__main__":
    main()