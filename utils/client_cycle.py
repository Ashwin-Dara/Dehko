import discord
from inspect import signature
from discord.ext import commands
import random
import asyncio
import os
import re

# Useful References
# https://discordpy.readthedocs.io/en/stable/quickstart.html
# Previous REPL Project on Data Pipelines
# Should not be too difficult. Making the API calls and using the proper data structure will be the hardest part.

# Overview of Message Flow
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

# We will create a queue for all of the requested processes. Moreover, we will maintain a load limit.
# The implementation will be a Linked List essentially. There will be a pointer to the head and the tail.
# This is for extremely fast insertions and deletions. They will be O(1).
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

    def get_length(self):
        return self.size


class Procedure:
    type_to_function = {}

    def __init__(self, procedure_type, argument=None, fun=None):
        self.next = None
        self.type_to_function = {}
        self.argument = argument
        self.procedure_type = procedure_type
        self.fun = fun
        self.sig = None
        self.init_process_to_function(fun)

    def init_process_to_function(self, fun):
        Procedure.type_to_function[self.procedure_type] = self.fun
        self.sig = signature(fun)

    def set_argument(self, arg):
        self.argument = arg

    def set_procedure_type(self, proc):
        self.procedure_type = proc

    def complete(self):
        assert self.procedure_type in Procedure.type_to_function.keys(), \
            "No defined function to complete for the specified procedure"

        assert len(self.sig.parameters) == 1 and self.argument is not None, \
            "Please configure the argument"

        Procedure.type_to_function[self.procedure_type](self.argument)


client = discord.Client()
bot = commands.Bot


# Reference: https://github.com/Rapptz/discord.py/blob/master/examples/guessing_game.py

class MsgClient(discord.Client):
    def __init__(self):
        super()
        self.nlp_model = None
        self.command_model = None

    async def on_ready(self):
        print(f'Bot is ready. User name: {self.user}. ID: {self.user.id}')
        print("##########")

    def config_models(self, nlp, comm):
        self.nlp_model = nlp
        self.command_model = comm

    def classify_input(self, text):
        if self.nlp_model is None or self.command_model is None:
            assert False, "Please configure the appropriate obj. models for MsgClient Class."

    @staticmethod
    def sub_pattern(pattern, txt):
        return re.sub(pattern, '', txt)

    async def on_message(self, message):
        # Checking if the author is the bot. If so, we don't want to respond to ourselves.
        if message.author.id == self.user.id:
            return

        msg_string = message.content
        ping_pattern = fr'^\s*{self.user.id}'
        is_matched = re.match(ping_pattern, msg_string)

        if is_matched:
            pass


async def classify_input(n_model, c_model, text):
    pass


@client.event
async def on_message(message):
    pass
