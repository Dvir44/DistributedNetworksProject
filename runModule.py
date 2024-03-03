import threading
import numpy

import initializationModule
import communicationModule

def initiateRun():
    network= initializationModule.Initialization()
    network.toString()

    # running init() for every computer which must be defined, and puting messages into the network queue
    for comp in network.connectedComputers:
        algorithm_function = getattr(comp.algorithmFile, 'init', None)
        #comp.algorithm = algorithm_function
        if callable(algorithm_function): # add the algorithm to each computer
            algorithm_function(comp)
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
        
    """ for comp in network.connectedComputers:
        print("aaa")
        #print(comp.messageQueue.get())
        if not comp.messageQueue.empty():
            print("bbb")
            algorithm_function = getattr(comp.algorithmFile, 'mainAlgorithm', None)
            
            #comp.algorithm = algorithm_function
            if callable(algorithm_function): # add the algorithm to each computer
                algorithm_function(comp, network)
                comp.runMainAlgorithm()
            else:
                print(f"Error: Function 'runAlgorithm' not found in {comp.algorithmFile}.py")
                return None """






    #while not network.networkMessageQueue.empty():
        #top_message = network.networkMessageQueue.get()
        ##print(top_message)
        #communicationModule.receive_message(top_message, network)
        
    #print(network.networkMessageQueue.get())
    #print(network.networkMessageQueue.get())
    #print(network.networkMessageQueue.get())



    """ threads = []

    # Function which will run in a thread for every computer
    def run_computer(comp):
        comp.run(network)

    for comp in network.connectedComputers:
        thread = threading.Thread(target=run_computer, args=(comp,))
        threads.append(thread)
        thread.start()

    # done
    for thread in threads:
        thread.join() 
 """
def main():
    pass

if __name__=="__main__":
    main()