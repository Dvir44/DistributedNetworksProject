import numpy
import initializationModule
import communicationModule

def initiateRun():
    network= initializationModule.Initialization()
    network.toString()

    # running init() for every computer which must be defined, and puting messages into the network queue
    for comp in network.connectedComputers:
        algorithm_function = getattr(comp.algorithmFile, 'init', None)
        print(algorithm_function)
        #comp.algorithm = algorithm_function
        if callable(algorithm_function): # add the algorithm to each computer
            algorithm_function(comp, communicationModule.CommunicationModule())
            #comp.runInit(algorithm_function)
            if not comp.messageQueue.empty():
                message = comp.messageQueue.get()
                network.networkMessageQueue.put(message)
                comp.messageQueue.put(message)
        else:
            print(f"Error: Function 'init' not found in {comp.algorithmFile}.py")
            return None
    
    ## running mainAlgorithm
    while not network.networkMessageQueue.empty():
        chosen_message = network.networkMessageQueue.get()
        actual_message=chosen_message
        communicationModule.receive_message(actual_message, network)
        print("**********************")
 
def main():
    pass

if __name__=="__main__":
    main()