import discord # imports the discord module for discord/recreational integration
from inspect import signature # Not sure exactly what this doing (FIXME) (FIGURE OUT WHAT THIS IS DOING)
from discord.ext import commands

from main import nn_classifier # Importing the NLP classification model from the main class
from MessageParser import MessageParser # Importing the MessageParser class
from ProcessQueue import * # Importing all functions from the file 'ProcessQueue.py'

# Here are some 

# Useful References
# https://discordpy.readthedocs.io/en/stable/quickstart.html
# Previous REPL Project on Data Pipelines
# Should not be too difficult. Making the API calls and using the proper data structure will be the hardest part.

# Overview of Message


"""
---------- RECEIVING

1. Recieve a message from the users within the server.
2. Check if the message is directed towards the bot.
    - We will be able to do this via a special message structure.
    - @bot_name message...
3. If the message is directed towards the bot, we need to do some processing

---------- PROCESSING

1. Remove the @bot_name from the message string
2. If anything is enclosed around ~ https//:youtube.com... ~, it is a link. Store is as a corresponding "argument" pair
    - remove the link from the message
3. Classify the message.

----------- RESPONSE

1. Perform the appropriate action. Send Follow up messages if needed.
2. For the weather, think of a way to extract the city name out of the current text. May be difficult and need some autocorrelation.
3. Use the NLPModel class and the CommandModel class

------------ ANALYZE
1. Store the command that was called and the associated user
2. Store key phrases (similar to the zkie bot project)

"""

# Created for testing purposes. Want to make sure that the Procedure.complete() function works as intended.
def print_music_info(name):
    print("LINE 44 was printed:  " + name)

class QueueLoad:

    min_load = 0.1
    max_load = 3

    def __init__(self):
        self.num_bins = 5
        self.num_entries = 0
        self.queues = []
        for i in range(0, self.num_bins):
            self.queues = ProcessQueue()

    def get_load(self):
        return self.num_entries / self.num_bins

    # Need to figure out the best way to actually execute the currently assigned
    # functions that are associated with the process object.
    def complete(self):
        pass

    # If the load factor hits some critical mass, we will expand the number of
    # possible concurrent queues for program efficiency. The load factor will be
    # determined through experimentation.
    def expand_queues(self):
        i = 0
        temp = self.num_bins
        while i < temp:
            self.queues.add(ProcessQueue())
            self.num_bins += 1
            i += 1

    def queue_process(self, process):
        pr_id = process.get_process_id()

        if self.get_load() > QueueLoad.max_load:
            self.expand_queues()

        assigned_queue = pr_id % self.num_bins
        self.queues[assigned_queue].add(process)
        self.num_entries += 1




# We will create a queue for all of the requested processes. Moreover, we will maintain a load limit.
# The implementation will be a Linked List essentially. There will be a pointer to the head and the tail.
# This is for extremely fast insertions and deletions. They will be O(1).
# Link for Process Handling: drive link with diagram pending......
class ProcessQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add(self, obj):
        if self.head is None and self.tail is None:
            self.head = obj
            self.tail = obj
            self.size += 1
        else:
            self.tail.next = obj
            self.tail = obj
            self.size += 1

    def pop(self):
        if self.size == 0:
            return None
        if self.size == 1:
            first = self.head
            self.head = None
            self.tail = None
            self.size -= 1
            first.complete()
            return first
        else:
            first = self.head
            self.head = self.head.next
            first.next = None
            self.size -= 1
            first.complete()
            return first

    def size(self):
        return self.size

    def peek(self):
        if self.head is None:
            return "ProcessQueue is empty"
        else:
            return "Head Process in Queue:  " +\
                   self.head.to_string()

class Procedure:
    type_to_function = {}

    def __init__(self, procedure_type, fun, uid, argument=None):
        self.uid = uid
        self.type_to_function = {}
        self.argument = argument
        self.procedure_type = procedure_type
        self.fun = fun
        self.sig = None
        self.next = None

        if procedure_type not in Procedure.type_to_function.keys():
            self.init_process_to_function(fun)

    def init_process_to_function(self, fun):
        Procedure.type_to_function[self.procedure_type] = self.fun
        self.sig = signature(fun)

    def set_argument(self, arg):
        self.argument = arg

    def set_procedure_type(self, proc):
        self.procedure_type = proc

    def get_process_id(self):
        r_id = self.procedure_type + " " + self.argument + " " + self.uid
        return hash(r_id)

    def complete(self):
        assert self.procedure_type in Procedure.type_to_function.keys(), \
            "No defined function to complete for the specified procedure"

        Procedure.type_to_function[self.procedure_type](self.argument)

    def to_string(self):
        return f'Process Type: {self.procedure_type}. Num of Args Required: {len(self.sig.parameters)}'

client = discord.Client()
bot = commands.Bot

# Reference: https://github.com/Rapptz/discord.py/blob/master/examples/guessing_game.py

class MsgClient(discord.Client):

    def __init__(self):
        super()
        self.nlp_model = nn_classifier

    async def on_ready(self):
        print(f'Bot is ready. User name: {self.user}. ID: {self.user.id}')
        print("##########")

    async def on_message(self, message):
        # Checking if the author is the bot.
        # If so, we don't want to respond to ourselves, so we just return.
        if message.author.id == self.user.id:
            return

        # Taking the contents of the message and creating an object of the "MessageParser"
        # It will parse through the message that we just send and tell us key information about
        # the arguments, type, and etc.

        parsed_msg = MessageParser(message.content, self.nlp_model, self.command_model)
        if parsed_msg.is_command_ping():

            # Create a procedure of the "type" that we parsed the message
            # Extract the relevant arguments and pass them into the procedure
            # Push the procedure object onto the "Process Queue."
            procedure = Procedure(parsed_msg.get_command_type(), parsed_msg.get_argument())
            add_procedure_request(procedure)
            empty_procedure_queue()
