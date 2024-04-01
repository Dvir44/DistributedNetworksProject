import numpy
import initializationModule
import communicationModule

def initiateRun(network: initializationModule.Initialization, comm : communicationModule.CommunicationModule):
    # running init() for every computer which must be defined, and puting messages into the network queue
    for comp in network.connectedComputers:
        algorithm_function = getattr(comp.algorithmFile, 'init', None)
        if callable(algorithm_function): # add the algorithm to each computer
            algorithm_function(comp, comm)
        else:
            print(f"Error: Function 'init' not found in {comp.algorithmFile}.py")
            return None
    
    ## running mainAlgorithm
    while not network.networkMessageQueue.empty():
        mess=network.networkMessageQueue.pop()
        comm.receive_message(mess, comm)
        print("**********************")
 
def main():
    pass

if __name__=="__main__":
    main()