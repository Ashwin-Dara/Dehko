import queue
import threading
import time
from ActionMappings import *
 
# Procedure is an abstraction for a single action that was assigned by the user and that needs to be completed. 
# functions:
#   self.complete(self) - looks up the specified name within the action mapping table and executes the corresponding function
#   self.to_string(self) - Returns meta data about the procedure that was completed. 
class Procedure:
    # Constructor takes in the name of the procedure (should remain consistent with actions_mapping) and relevant arguments.
    def __init__(self, procedure_name, procedure_arg):
        self.procedure_name = procedure_name
        self.procedure_args = procedure_arg
        self.id = hash(procedure_name)

    # Executes function through lookup in mapping. 
    def complete(self):
        assert self.procedure_name in command_to_func_mapping.keys(), \
            "No defined function for that procedure type in command_to_func mapping." \
            "Please go to the file ActionMappings.py and initialize the dictionary. "
        command_to_func_mapping[self.procedure_name](self.procedure_args)

    # Returns string of meta data.
    def to_string(self):
        return f"Task Completed! Executed the script associated with the procedure: {self.procedure_name} - {self.id}."