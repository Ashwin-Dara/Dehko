import queue
import threading
import time
from ActionMappings import *


class Procedure:
    def __init__(self, procedure_name, procedure_arg):
        self.procedure_name = procedure_name
        self.procedure_args = procedure_arg
        # To make the process of debugging easier we should be giving every single procedure
        # a unique ID based on the time it was created
        self.id = None

    def complete(self):
        assert self.procedure_name in command_to_func_mapping.keys(), \
            "No defined function for that procedure type in command_to_func mapping." \
            "Please go to the file ActionMappings.py and initialize the dictionary. "
        command_to_func_mapping[self.procedure_name](self.procedure_args)

    def to_string(self):
        return f"Task Completed! Executed the script associated with the procedure: {self.procedure_name}."