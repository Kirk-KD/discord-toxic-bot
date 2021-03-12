from src.command import Command
from src.perms import *


class CommandHandler:
    def __init__(self):
        self.commands = {}

    def add(self, aliases=None, perm=0):
        if aliases is None:
            aliases = []

        def inner(command):
            for name in aliases + [command.__name__]:
                self.commands[name] = Command(command, perm)
            return command

        return inner

    async def handle(self, message: discord.Message):
        msg = message.content.strip()[1:]
        args = msg.split()
        name = args.pop(0).lower()

        if name in self.commands.keys():
            if perm_check(message.author, self.commands[name].perm):
                await self.commands[name].call(message, args)
            else:
                await message.reply("Whoa hold on you don't have permission to use that! Begone, peasant!")


handler = CommandHandler()
