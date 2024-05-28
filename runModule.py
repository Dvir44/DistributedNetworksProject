import numpy
from visualizations.graphVisualization import visualize_network
import initializationModule
import communicationModule

def initiateRun(network: initializationModule.Initialization, comm : communicationModule.CommunicationModule):
        # running init() for every computer which must be defined, and puting messages into the network queue
        for comp in network.connectedComputers:
            algorithm_function = getattr(comp.algorithmFile, 'init', None)
            if callable(algorithm_function): # add the algorithm to each computer
                curr_color=comp.getColor()
                algorithm_function(comp, comm)

                if network.displayType=="Graph" and comp.getColor()!=curr_color: # if display is graph then update color
                    network.node_values_change.append([str(comp.getId()), str(comp.getColor()), str(comp.getRoot()), str(comp.getState()), str(comp.getReceivedFrom())])

                    #network.node_color_dict.append([str(comp.getId()), str(comp.getColor())])
            else:
                print(f"Error: Function 'init' not found in {comp.algorithmFile}.py")
                return None
        
        ## running mainAlgorithm
        while not network.networkMessageQueue.empty():
            mess=network.networkMessageQueue.pop()
            comm.receive_message(mess, comm)
            if network.displayType=="Text":
                print("**********************")
    
def main():
    pass

if __name__=="__main__":
    main()