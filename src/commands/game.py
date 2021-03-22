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
                ["beg"], "beg", "Gotta start somewhere.", perms.EVERYONE, 25
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

    class Balance(CooldownCommand):
        def __init__(self):
            super().__init__(
                ["balance", "money", "txc", "bal"], "balance [<user>]", "See how rich you or other people are!",
                perms.EVERYONE, 3
            )

        async def __call__(self, message, args, client):
            member = message.author if len(args) == 0 else parse_member(message.guild, args[0])
            if not member:
                await message.reply("That user doesn't exist lol", mention_author=False)

            player = game_data.data[str(member.id)]

            embed = discord.Embed(
                title="{}'s Balance".format(member),
                color=discord.Color.blue()
            ).add_field(
                name="Wallet",
                value="`txc${}`".format(player["txc"])
            ).add_field(
                name="Bank",
                value="`txc${}`".format(player["bank"]["curr"])
            ).add_field(
                name="Inv Worth",
                value="`txc$TODO`",  # TODO: IMPLEMENT
                inline=False
            )
            await message.reply(embed=embed, mention_author=False)

    class Leaderboard(CooldownCommand):
        def __init__(self):
            super().__init__(
                ["leaderboard", "lb", "rich"], "leaderboard",
                "Who's the richest in your server?", perms.EVERYONE, 3
            )

        async def __call__(self, message, args, client):
            player = game_data.data[str(message.author.id)]
            players = sorted(
                [member for member in message.guild.members if not member.bot],
                key=lambda m: game_data.data[str(m.id)]["txc"], reverse=True
            )

            emojis = ":first_place: :second_place: :third_place:".split()
            embed = discord.Embed(
                title="Rich bois in {}".format(message.guild.name),
                description="",
                color=discord.Color.gold()
            ).set_footer(
                text="You are at {} place\n\n".format(self.parse_place(players.index(message.author) + 1))
            )
            for i, p in enumerate(players):
                embed.description += "{} **{}** - {}\n".format(
                    emojis[i] if i < 3 else ":small_orange_diamond:", game_data.data[str(p.id)]["txc"], p
                )
                if i == 9:
                    break

            await message.reply(embed=embed, mention_author=False)

        def parse_place(self, n):
            s = str(n)
            suffixes = "st nd rd".split()
            return s + (suffixes[int(s[-1]) - 1] if 0 < int(s[-1]) < 4 else "th")


handler.add_category(Game)