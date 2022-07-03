import re
from Models import NLPModel

# This class is responsible for taking the message as it is and breaking it
# down into the core components.
#
# In particular, we want to send in a message to this class, and it should be able to
# recover information about the (1) type of message (through NN classification) (2) arguments.
# All of this will be primarily done through the use of regular expressions.
class MessageParser:
    ping_pattern = r'^\s*@dehko'
    arg_pattern = r'~.*'

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

    def get_argument(self):
        return self.argument

    def get_command_type(self):
        return self.type

    def is_command_ping(self):
        r = re.match(MessageParser.ping_pattern, self.contents)
        return bool(r)

    def print_data(self):
        # Weird font is for bolding text within the terminal. 
        print("\n\n\033[4mMessage Parser Details\033[0m")
        print(f"Description of Command: `{self.content_internal}`. Argument[s] Detected: `{self.argument}`")

