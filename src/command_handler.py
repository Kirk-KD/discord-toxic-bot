"""
CommandHandler class and its instance for handling commands
"""

from src.command import Command
from src.perms import *
from src.data import *
import discord


class CommandHandler:
    """
    stores and handles commands
    """

    def __init__(self):
        """
        initialises the CommandHandler
        """

        self.commands = {}

    def add(self, aliases=None, perm=0):
        """
        a decorator function that adds a command and its aliases to self.commands

        :param aliases: None or list<str>
        :param perm: int
        :return: function
        """

        if aliases is None:
            aliases = []

        def inner(command):
            for name in aliases + [command.__name__]:
                self.commands[name] = Command(command, perm)
            return command

        return inner

    async def handle(self, message: discord.Message, client: discord.Client):
        """
        a function that does a permission check and executes a command

        :param message: Message
        :param client: Client
        :return: None
        """
        msg = message.content.strip()[1:]
        args = msg.split()
        name = args.pop(0).lower()

        if not guilds_data[str(message.author.guild.id)]["initialised"] and name != "setup":
            await message.reply(
                "Hey tell your server owner to do a `_setup` first, then you can order me around!", mention_author=False
            )
            return

        if name in self.commands.keys():
            if perm_check(message.author, self.commands[name].perm):
                await self.commands[name].call(message, args, client)
            else:
                await message.reply(
                    "Whoa hold on you don't have permission to use that! Begone, peasant!", mention_author=False
                )


# create instance
handler = CommandHandler()
