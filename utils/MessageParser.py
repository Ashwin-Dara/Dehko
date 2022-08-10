# Importing relevant libraries.
import re
from Models import NLPModel

# This class is responsible for taking the message as it is and breaking it
# down into the core components.
# In particular, we want to send in a message to this class, and it should be able to
# recover information about the (1) type of message (through NN classification) (2) arguments.
# All of this parsing will be primarily done through the use of regular expressions.
class MessageParser:
    # Defining the ReGex patterns.
    ping_pattern = r'^\s*@dehko'
    arg_pattern = r'~.*'

    # Constructor: takes in the message and NN and parses message using the 
    # defined ReGex patterns.
    def __init__(self, message, nn_model, comm_model):
        self.comm = comm_model
        self.nn = nn_model

        self.argument = None
        self.content_internal = message
        self.arg_matcher = re.compile(MessageParser.arg_pattern)
        r = self.arg_matcher.search(self.content_internal)
        if r:
            self.content_internal = self.content_internal.replace(r.group(0), "")
            self.argument = r.group(0).replace("~", "")

        # Classifying the type of command it was from the message using the NN
        self.type = nn_model.classify_command(self.content_internal)

    # Returns the argument that was extracted.
    def get_argument(self):
        return self.argument

    # Gets the command type that was extracted.
    def get_command_type(self):
        return self.type

    # Defines whether format was viable.
    def is_command_ping(self):
        r = re.match(MessageParser.ping_pattern, self.contents)
        return bool(r)

    # Prints relevant meta data used for debugging. 
    # Special characters in the first print statement are special unicode.
    def print_data(self):
        print("\n\n\033[4mMessage Parser Details\033[0m")
        print(f"Description of Command: `{self.content_internal}`. Argument[s] Detected: `{self.argument}`")

