import queue
import sys
import numpy
from visualizations.graphVisualization import visualize_network
import simulator.initializationModule as initializationModule
import simulator.communication as communication


def initiateRun(network: initializationModule.Initialization, comm : communication.Communication):
    '''runs the algorithm on the created network'''
    # runs init() for every computer which must be defined, and puting messages into the network queue
    for comp in network.connected_computers:
        comm.run_algorithmm(comp, 'init')

    print("************************************************************************************")

    ## runs mainAlgorithm
    while not network.message_queue.empty():
        message = network.message_queue.pop()
        comm.receive_message(message, comm)