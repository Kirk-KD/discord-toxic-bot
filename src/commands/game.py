from src.category import Category
from src.command import CooldownCommand
from src.data import game_data
from src.handler import handler
from src import perms

from src.util.parser import *

import discord
import random


class Game(Category):
    def __init__(self):
        super().__init__("Game", "A cross-server game with txc (toxic coin) as the currency!")

    class Beg(CooldownCommand):
        def __init__(self):
            super().__init__(
                ["beg"], "beg", "Gotta start somewhere.", perms.EVERYONE, 20
            )

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            # TODO: REMAKE

    class Search(CooldownCommand):
        def __init__(self):
            super().__init__(["search"], "search", "Search for stuff around you.", perms.EVERYONE, 20)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            # TODO: REMAKE

    class UseItem(CooldownCommand):
        def __init__(self):
            super().__init__(["useitem", "use"], "useitem <item>", "Uses an item.", perms.EVERYONE, 1)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) == 0:
                await message.reply("Lmao you need to tell me what item you want to use.", mention_author=False)
                return

            # TODO: REMAKE

    class Buy(CooldownCommand):
        pass  # TODO: IMPLEMENT

    class Balance(CooldownCommand):
        def __init__(self):
            super().__init__(
                ["balance", "money", "txc", "bal"], "balance [<user>]", "See how rich you or other people are!",
                perms.EVERYONE, 3
            )

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            member = message.author if len(args) == 0 else parse_member(message.guild, args[0])
            if not member:
                await message.reply("That user doesn't exist lol", mention_author=False)

            # TODO: REMAKE

    class Leaderboard(CooldownCommand):
        def __init__(self):
            super().__init__(
                ["leaderboard", "lb", "rich"], "leaderboard",
                "Who's the richest in your server?", perms.EVERYONE, 1
            )

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            # TODO: REMAKE


handler.add_category(Game)
