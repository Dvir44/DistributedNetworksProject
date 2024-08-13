import json
import os
import random
import re
import time
import numpy
from simulator.computer import Computer
import simulator.initializationModule as initializationModule


class Communication:
    def __init__(self, network: initializationModule.Initialization):
        self.network = network
        
    # Send a message from the source computer to the destination computer
    def send_message(self, source, dest, message_info, arrival_time = None):
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
        source_computer = self.network.network_dict.get(source_id)
        for index, connected_computer_id in enumerate(source_computer.connectedEdges):
            self.send_message(source_id, connected_computer_id, message_info, arrival_time)

            
    def receive_message(self, message : dict, comm):
        if self.network.logging_type=="Long":
            print(message)
            
        received_id = message['dest_id']
        received_computer = self.network.network_dict.get(received_id)
        self.run_algorithmm(received_computer, 'mainAlgorithm', message['arrival_time'], message['content'] )

        
        
    def run_algorithmm(self, comp: Computer, function_name: str, arrival_time = None, message_content=None):
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