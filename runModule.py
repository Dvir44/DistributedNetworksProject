import numpy
from visualizations.graphVisualization import visualize_network
import initializationModule
import communicationModule

def initiateRun(network: initializationModule.Initialization, comm : communicationModule.CommunicationModule):
        # running init() for every computer which must be defined, and puting messages into the network queue
        for comp in network.connected_computers:
            algorithm_function = getattr(comp.algorithm_file, 'init', None)
            if callable(algorithm_function): # add the algorithm to each computer
                curr_color=comp.getColor()
                algorithm_function(comp, comm)

                if network.display_type=="Graph" and comp.getColor()!=curr_color: # if display is graph then update color
                    network.node_values_change.append([str(comp.id), str(comp.getColor()), str(comp.getRoot()), str(comp.getState()), str(comp.getReceivedFrom())])
            else:
                print(f"Error: Function 'init' not found in {comp.algorithm_file}.py")
                return None
        print("******************************************")
        
        ## running mainAlgorithm
        while not network.network_message_queue.empty():
            mess=network.network_message_queue.pop()
            comm.receive_message(mess, comm)

def main():
    pass

if __name__=="__main__":
    main()