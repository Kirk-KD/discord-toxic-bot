import discord
import datetime
import random

from src.bot import perms
from src.bot.consts import cooldown
from src.bot.perms import perm_names, perm_check, GLOBAL_DEV

from src.util.time import format_timedelta


class Command:
    def __init__(self, triggers: list, usage: str, description: str, perm: int):
        self.category = None
        self.triggers = triggers
        self.name = self.triggers[0]
        self.usage = usage
        self.description = description
        self.perm = perm

    async def __call__(self, message, args, client):
        raise NotImplementedError()

    def format_help(self):
        return "{} {}\n{}{}\n\n".format(
            "**{}** {}".format(
                self.usage.split()[0], "{}".format(
                    " ".join(self.usage.split()[1:])
                ) if len(self.usage.split()) != 1 else ""
            ), "`{} Only`".format(perm_names[self.perm]) if self.perm else "",
            "*{}*".format(self.description),
            "\naliases: {}".format(
                "**{}**".format(", ".join(self.triggers[1:]))
            ) if len(self.triggers) > 1 else ""
        )


class GameCommand(Command):
    def __init__(self, triggers: list, usage: str, description: str, cooldown_: int):
        super().__init__(triggers, usage, description, perms.EVERYONE)
        self.cooldown = cooldown_
        self.users = {}

    async def check_cooldown(self, message):
        if perm_check(message.author, GLOBAL_DEV):  # dev bypass cooldown
            return True
        self.users[message.author.id] = (self.users[message.author.id]
                                         if message.author.id in self.users.keys()
                                         else datetime.datetime.now())

        if self.users[message.author.id] <= datetime.datetime.now():
            self.users[message.author.id] = datetime.datetime.now() + datetime.timedelta(seconds=self.cooldown)
            return True
        else:
            delta = self.users[message.author.id] - datetime.datetime.now()
            embed = discord.Embed(
                title=random.choice(cooldown),
                description="You can use that command again after {}!".format(
                    format_timedelta(delta)
                ),
                color=discord.Color.dark_blue()
            )
            await message.reply(embed=embed, mention_author=False)
            return False

    async def __call__(self, message, args, client):
        raise NotImplementedError()
