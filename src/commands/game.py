from src.category import Category
from src.command import CooldownCommand
from src.handler import handler
from src import perms

from src.util.parser import *
from src.util.bot import *

import discord
import random


def chance(percent: int or float):
    return random.uniform(0.0, 100.0) <= percent


class Game(Category):
    def __init__(self):
        super().__init__("Game", "A cross-server game with txc (toxic coin) as the currency!")

    class Beg(CooldownCommand):
        def __init__(self):
            super().__init__(
                ["beg"], "beg", "Gotta start somewhere.", perms.EVERYONE, 15
            )

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            characters = [  # expand later
                "The developer", "Toxic xD", "Trump", "Pewdiepie", "Brackeys", "Tim from twt",
                "The kid that stole your candy when you were in kindergarten", "Rick Astley", "Stick Bug",
                "That fat admin", "Meme man", "Developers of stackoverflow, programmer's saviors", "Monke",
                "Big lizard", "That teacher who leaves extra homeworks for the weekends", "I", "you", "Wumpus",
                "Dani Milkman", "Milkman Karlson", "Billy", "Billy's brother Willy", "Jacksepticeye",
                "The soul who has been tortured by c++ for eternity", "Danny DeVito", "Danny DeYeeto",
                "GrayStillPlays", "Github Cat"
            ]

            if chance(50):
                amount = int(random.triangular(15, 1000, 75))
                game_data.data[str(message.author.id)]["txc"] += amount
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

    class Balance(CooldownCommand):  # TODO: CHANGE
        def __init__(self):
            super().__init__(
                ["balance", "money", "txc", "bal"], "balance [<user>]", "See how rich you or other people are!",
                perms.EVERYONE, 3
            )

        async def __call__(self, message, args, client):
            member = message.author if len(args) == 0 else parse_member(message.guild, args[0])
            if not member:
                await message.reply("That user doesn't exist lol", mention_author=False)

            embed = discord.Embed(
                title="{}'s Balance".format(member),
                description="txc${}".format(game_data.data[str(member.id)]["txc"]),
                color=discord.Color.blue()
            )
            await message.reply(embed=embed, mention_author=False)


handler.add_category(Game)
