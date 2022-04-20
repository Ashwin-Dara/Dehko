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

# Overview of Message

# How to run multi-processed queues in python: https://docs.python.org/3/library/queue.html
# THIS ARTICLE IS MORE USEFUL THAN THE OTHER ARICLES: https://medium.datadriveninvestor.com/the-most-simple-explanation-of-threads-and-queues-in-python-cbc206025dd1

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

"""
  1 import logging
  2 import threading
  3 import time
  4 
  5 # Reference used: https://realpython.com/intro-to-python-threading/
  6 
  7 def functionWeWillThread(name):
  8     print("This is thread number " + name)
  9     time.sleep(0.5) # We need some sort of delay. Sleep is in seconds
 10 
 11 x = threading.Thread(target = functionWeWillThread, arg=("First Thread", ))
 12 x.start() 
 
 Need to learn how threading works for the process Queue.
 
 Essentially, once we get a certain amount of requests, start another thread and do it concurrently.
 Then when it falls below half the threshold, stop the thread and go back to single thread.
 
 Maybe it might be unnecessary to make multiple threads? It could just be running in the background.
"""

# Created for testing purposes. Want to make sure that the Procedure.complete() function works as intended.
def print_music_info(name):
    print("LINE 44 was printed:  " + name)

"""
import asyncio

async def counter_loop(x, n):
    for i in range(1, n + 1):
        print(f"Counter {x}: {i}")
        await asyncio.sleep(0.5)
    return f"Finished {x} in {n}"

async def main():
    slow_task = asyncio.create_task(counter_loop("Slow", 4))
    fast_coro = counter_loop("Fast", 2)

    print("Awaiting Fast")
    fast_val = await fast_coro
    print("Finished Fast")

    print("Awaiting Slow")
    slow_val = await slow_task
    print("Finished Slow")

    print(f"{fast_val}, {slow_val}")

asyncio.run(main())
"""

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
