import discord


class CommandHandler:
    def __init__(self):
        self.commands = {}

    def add(self, aliases: list=[]):
        def inner(command):
            for name in aliases + [command.__name__]:
                self.commands[name] = command
            return command

        return inner

    async def handle(self, message: discord.Message):
        msg = message.content.strip()[1:]
        args = msg.split()
        name = args.pop(0).lower()

        if name in self.commands.keys():
            await self.commands[name](message, args)
