from src.category import Category
from src.command import CooldownCommand
from src.data import game_data
from src.game.game_manager import manager
from src.handler import handler
from src import perms

from src.util.game import *
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

            player = manager.get_player(message.author)
            characters = [  # expand later
                "The developer", "Toxic xD", "Trump", "Pewdiepie", "Brackeys", "Tim from twt",
                "The kid that stole your candy when you were in kindergarten", "Rick Astley", "Stick Bug",
                "That fat admin", "Meme man", "Developers of stackoverflow, programmer's saviors", "Monke",
                "Big lizard", "That teacher who leaves extra homeworks for the weekends", "I", "you", "Wumpus",
                "Dani Milkman", "Milkman Karlson", "Billy", "Billy's brother Willy", "Jacksepticeye",
                "The soul who has been tortured by c++ for eternity", "Danny DeVito", "Danny DeYeeto",
                "GrayStillPlays", "Github Cat"
            ]

            if chance(65):
                amount = multiplier(int(random.triangular(15, 1000, 75)), player.data["stats"]["multi"])
                player.data["stats"]["txc"] += amount
                game_data.update_data()

                embed = discord.Embed(
                    title="Got 'em",
                    description="**{}** felt bad for you and gave you **txc${}** lmaooo :money_mouth:".format(
                        random.choice(characters), amount
                    ),
                    color=discord.Color.green()
                ).set_footer(text="big stonks")
                await message.reply(embed=embed, mention_author=False)
            else:
                embed = discord.Embed(
                    title="No one cares",
                    description="**{}** walked right pass you and "
                                "didn't waste their money on someone like you lol".format(
                                    random.choice(characters)
                                ),
                    color=discord.Color.red()
                ).set_footer(text="stonkn't :(")
                await message.reply(embed=embed, mention_author=False)

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

    # class Buy(CooldownCommand):
    #     pass  # TODO: IMPLEMENT

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
