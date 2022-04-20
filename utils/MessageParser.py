# This class is responsible for taking the message as it is and breaking it
# down into the core components.
#
# In particular, we want to send in a message to this class, and it should be able to
# recover information about the (1) type of message (through NN classification) (2) arguments.
# All of this will be primarily done through the use of regular expressions.
import re


class MessageParser:
    ping_pattern = r'^\s*@dehko'
    arg_pattern = r'~.*'

    def __init__(self, message):
        self.contents = message
        self.argument = None

        self.content_internal = re.sub(self.contents, MessageParser.ping_pattern, "")

        # Stopping the rest of the constructor from going if this was a ping to begin with
        if not self.is_command_ping():
            return

        self.arg_matcher = re.compile(MessageParser.arg_pattern)
        r = self.arg_matcher.search(self.contents)
        if r:
            self.argument = r.group(0).replace("~", "")

        self.type =

    def get_argument(self):
        return self.argument

    def get_command_type(self):
        return self.argument

    def is_command_ping(self):
        """
        >>> m = MessageParser("@dehko osidfjjiaosd")
        >>> m.is_command_ping()
        True
        >>> m = MessageParser(" @dehko osidfjjiaosd")
        >>> m.is_command_ping()
        True
        >>> m = MessageParser("     @dehko osidfjjiaosd")
        >>> m.is_command_ping()
        True
        >>> m = MessageParser("   1  @dehko osidfjjiaosd")
        >>> m.is_command_ping()
        False
        >>> m = MessageParser("@daehko osidfjjiaosd")
        >>> m.is_command_ping()
        False
        """
        r = re.match(MessageParser.ping_pattern, self.contents)
        return bool(r)
