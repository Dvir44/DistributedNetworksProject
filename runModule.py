import threading
import numpy

import initializationModule


def initiateRun():
    network= initializationModule.Initialization()
    network.toString()
    threads = []

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

def main():
    pass

if __name__=="__main__":
    main()