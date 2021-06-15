import discord

from src.bot.data import guilds_data
from src.bot.perms import perm_check


class Handler:
    def __init__(self):
        self.categories = []

    def add_category(self, category):
        self.categories.append(category())

    async def handle(self, message: discord.Message, client, content=None):
        msg = message.content.strip()[1:] if not content else content
        args = msg.split()
        name = args.pop(0).lower()

        if not guilds_data.get(message.guild.id)["initialised"] and name != "setup":
            await message.reply(
                "Hey tell your server owner to do a `_setup` first, then you can order me around!",
                mention_author=False
            )
            return

        if command := self.get_command(name):
            if perm_check(message.author, command.perm):
                try:
                    await command(message, args, client)
                except discord.Forbidden:
                    await message.reply(":eyes: I don't have permission to do that tho.", mention_author=False)
            else:
                await message.reply(
                    "Whoa hold on you don't have permission to use that! Begone, peasant!", mention_author=False
                )

    def get_command(self, name: str):
        for category in self.categories:
            if command := category.get_command(name):
                return command

        return None

    def get_category(self, name: str):
        for category in self.categories:
            if (category.name.lower() == name.lower()) and not category.hidden:
                return category

        return None


handler = Handler()
