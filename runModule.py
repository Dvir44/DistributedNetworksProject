import queue
import sys
import numpy
from visualizations.graphVisualization import visualize_network
import initializationModule
import communication


def initiateRun(network: initializationModule.Initialization, comm : communication): 
        old_values_list = [None]*network.computer_number
        # running init() for every computer which must be defined, and puting messages into the network queue
        for comp in network.connected_computers:
            algorithm_function = getattr(comp.algorithm_file, 'init', None)
            if callable(algorithm_function): # add the algorithm to each computer
                old_values = comp.__dict__.copy()
                old_values_list.append(old_values)

                algorithm_function(comp, comm)

                new_values = comp.__dict__
                if old_values!=new_values: # if display is graph then update values. NEED TO CHANGE THE IF STATEMENT
                    values = comp.__dict__.copy()
                    network.node_values_change.append(values)
            else:
                print(f"Error: Function 'init' not found in {comp.algorithm_file}.py")
                return None
        print("******************************************")
        

        """ for i, comp in enumerate(network.connected_computers):
            new_values = comp.__dict__
            if old_values_list[i]!=new_values: # if display is graph then update values. NEED TO CHANGE THE IF STATEMENT
                values = comp.__dict__.copy()
                network.node_values_change.append(values)
 """

        ## running mainAlgorithm
        while not network.network_message_queue.empty():
            mess=network.network_message_queue.pop()
            comm.receive_message(mess, comm)

def main():
    pass

if __name__=="__main__":
    main()