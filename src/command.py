from src.perms import perm_names, EVERYONE, perm_check, DEV

from src.util.time import format_timedelta

import datetime
import discord


class Command:
    def __init__(self, triggers: list, usage: str, description: str, perm: int):
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


class CooldownCommand(Command):
    def __init__(self, triggers: list, usage: str, description: str, perm: int, cooldown: int):
        super().__init__(triggers, usage, description, perm)
        self.cooldown = cooldown
        self.cooldown_end = datetime.datetime.now()

    async def check_cooldown(self, message):
        # if perm_check(message.author, DEV):  # dev bypass cooldown
        #     return True

        if self.cooldown_end <= datetime.datetime.now():
            self.cooldown_end = datetime.datetime.now() + datetime.timedelta(seconds=self.cooldown)
            return True
        else:
            delta = self.cooldown_end - datetime.datetime.now()
            embed = discord.Embed(
                title="Ayo stop spamming",
                description="You can use that command again after {}!".format(
                    format_timedelta(delta)
                ),
                color=discord.Color.dark_blue()
            )
            await message.reply(embed=embed, mention_author=False)
            return False

    async def __call__(self, message, args, client):
        raise NotImplementedError()
