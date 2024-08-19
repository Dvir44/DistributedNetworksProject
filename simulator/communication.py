"""
Communication module for handling message passing between computers in a simulated network.

This module handles the sending and receiving of messages between computers in the network, including broadcasting messages and running algorithms.
"""
import json
import os
import random
import re
import time
import numpy
from simulator.computer import Computer
import simulator.initializationModule as initializationModule


class Communication:
    """
    A class to handle communication between computers in a distributed network simulation.
    
    Attributes:
        network (Initialization): The network initialization object containing the computers and configurations.
    """

    def __init__(self, network: initializationModule.Initialization):
        """
        Initializes the Communication instance with the given network.
        
        Args:
            network (Initialization): The initialized network containing the computers.
        """
        self.network = network
        
    # Send a message from the source computer to the destination computer
    def send_message(self, source, dest, message_info, arrival_time = None):
        """
        Sends a message from the source computer to the destination computer, with optional arrival time.
        
        Args:
            source (int): The ID of the source computer sending the message.
            dest (int): The ID of the destination computer receiving the message.
            message_info (str): The content of the message being sent.
            arrival_time (float, optional): The time at which the message should arrive. If None, it defaults to 0.
        """
        current_computer =  self.network.network_dict.get(source)

        if not current_computer.state == "terminated":
            # creating a new message which will be put into the queue
            if arrival_time is None:
                arrival_time = 0
                  
            if self.network.delay_type == 'Random':
                delay = random.random()
            elif self.network.delay_type == 'Constant':
                delay = 1
                
            message = {
            'source_id': source,
            'dest_id': dest,
            'arrival_time': arrival_time + delay,
            'content': message_info,
            }
            self.network.message_queue.push(message)
    
    
    def send_to_all(self, source_id, message_info, arrival_time = None):
        """
        Sends a message from the source computer to all connected computers.
        
        Args:
            source_id (int): The ID of the source computer sending the message.
            message_info (str): The content of the message being sent.
            arrival_time (float, optional): The time at which the message should arrive. If None, it defaults to 0.
        """
        source_computer = self.network.network_dict.get(source_id)
        for index, connected_computer_id in enumerate(source_computer.connectedEdges):
            self.send_message(source_id, connected_computer_id, message_info, arrival_time)

            
    def receive_message(self, message : dict, comm):
        """
        Receives a message and runs the appropriate algorithm on the destination computer.
        
        Args:
            message (dict): The message that was received.
            comm (Communication): The communication object handling the message passing.
        """
        if self.network.logging_type=="Long":
            print(message)
            
        received_id = message['dest_id']
        received_computer = self.network.network_dict.get(received_id)
        self.run_algorithmm(received_computer, 'mainAlgorithm', message['arrival_time'], message['content'] )

        
        
    def run_algorithmm(self, comp: Computer, function_name: str, arrival_time = None, message_content=None):
        """
        Runs the specified algorithm on the given computer, handling the provided message content and arrival time.
        
        Args:
            comp (Computer): The computer object on which to run the algorithm.
            function_name (str): The name of the function (algorithm) to be executed.
            arrival_time (float, optional): The time the message arrived, if applicable.
            message_content (str, optional): The content of the message being processed by the algorithm.
        """
        algorithm_function = getattr(comp.algorithm_file, function_name, None) 
        if callable(algorithm_function):
            if function_name == 'init':
                algorithm_function(comp, self)  # Call with two arguments
            elif function_name == 'mainAlgorithm':
                algorithm_function(comp, self, arrival_time, message_content)
        
            if self.network.display_type == "Graph" and comp.has_changed():
                self.network.node_values_change.append(comp.__dict__.copy())
                comp.reset_flag()
        else:
            print(f"Error: Function '{function_name}' not found in {comp.algorithm_file}.py")
            return None