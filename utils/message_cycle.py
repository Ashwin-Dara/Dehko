import discord
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



