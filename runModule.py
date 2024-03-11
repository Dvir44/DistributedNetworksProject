import numpy
import initializationModule
import communicationModule

network= initializationModule.Initialization()

def getNetwork():
    return network


def initiateRun():
    network.toString()

    # running init() for every computer which must be defined, and puting messages into the network queue
    for comp in network.connectedComputers:
        algorithm_function = getattr(comp.algorithmFile, 'init', None)
        #print(algorithm_function)
        #comp.algorithm = algorithm_function
        if callable(algorithm_function): # add the algorithm to each computer
            algorithm_function(comp, communicationModule.CommunicationModule())
            #print("BBBB", network.networkMessageQueue)

            #comp.runInit(algorithm_function)
            if not comp.messageQueue.empty():
                message = comp.messageQueue.get()
                network.networkMessageQueue.put(message)
                #network.networkMessageQueue.put(message)
                comp.messageQueue.put(message)
        else:
            print(f"Error: Function 'init' not found in {comp.algorithmFile}.py")
            return None
    
    ## running mainAlgorithm
    print(network.networkMessageQueue.empty())
    comm = communicationModule.CommunicationModule()
    while not network.networkMessageQueue.empty():
        #print(network.networkMessageQueue.get())
        print("lalalala")
        #chosen_message = network.networkMessageQueue.get()
        comm.message=network.networkMessageQueue.get()
        #print("chosen", chosen_message)
        #actual_message=chosen_message
        comm.receive_message()

        #communicationModule.CommunicationModule.receive_message()
        print("**********************")
 
def main():
    pass

if __name__=="__main__":
    main()