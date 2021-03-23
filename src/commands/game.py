from src.category import Category
from src.command import CooldownCommand
from src.handler import handler
from src.game.shop import shop
from src import perms

from src.util.parser import *
from src.util.game import *

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

            player = game_data.data[str(message.author.id)]
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
                amount = multiplier(int(random.triangular(15, 1000, 75)), player["multi"])
                player["txc"] += amount
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

            player = game_data.data[str(message.author.id)]
            if chance(75):
                if chance(3):
                    item = shop.get_item(random.choice(["coffee", "toxicpotion"]))
                    give_item(player, item)
                    game_data.update_data()

                    embed = discord.Embed(
                        title="You searched around...",
                        description="...and found a **{}**!".format(item.name),
                        color=discord.Color.green()
                    ).set_footer(
                        text="That's some sharp eyes bro"
                    )
                    await message.reply(embed=embed, mention_author=False)
                else:
                    amount = multiplier(int(random.triangular(10, 110, 50)), player["multi"])
                    player["txc"] += amount
                    game_data.update_data()

                    embed = discord.Embed(
                        title="You searched around...",
                        description="...and found **txc${}**!".format(amount),
                        color=discord.Color.green()
                    ).set_footer(
                        text="That's some sharp eyes bro"
                    )
                    await message.reply(embed=embed, mention_author=False)
            else:
                if chance(95):
                    embed = discord.Embed(
                        title="You searched around...",
                        description="...and found NOTHING lmao",
                        color=discord.Color.red()
                    ).set_footer(
                        text="Haha noob"
                    )
                    await message.reply(embed=embed, mention_author=False)
                else:
                    killed = kill_player(player)
                    await message.author.send(
                        "Lmao you died noob. Buy a Toxic Potion in the shop to save yourself next time!"
                        if killed else
                        "You drank th Toxic Potion at the last second before you die, and it saved you life!"
                    )

                    death_options = [
                        "You were hit by a car while searching in the middle of a street LMAO r u dumb?",
                        "Lol you wasn't looking where you are going and fell in a sewer and died.",
                        "Wow you searched all the way to Area51! And guess what? You were also shot in the head!",
                        "You did an unintentional science experiment about gravity."
                        "(Basically you fell down a cliff lol)",
                        "You were killed by another player who was also searching for stuff.",
                        "You tried to search inside you skull. Not only did you die, "
                        "you also found out you have a very small and smooth brain."
                    ]

                    embed = discord.Embed(
                        title="You died while searching lol",
                        description=random.choice(death_options),
                        color=discord.Color.red()
                    ).set_footer(
                        text="Haha noob"
                    )
                    await message.reply(embed=embed, mention_author=False)

    class UseItem(CooldownCommand):
        def __init__(self):
            super().__init__(["useitem", "use"], "useitem <item>", "Uses an item.", perms.EVERYONE, 1)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) == 0:
                await message.reply("Lmao you need to tell me what item you want to use.", mention_author=False)
                return

            item = shop.get_item(args[0])
            if not item:
                await message.reply("That item doesn't exist what are you doing lol", mention_author=False)
                return

            if game_data.data[str(message.author.id)]["inv"][item.name] == 0:
                await message.reply("But you don't even have that item???", mention_author=False)
                return

            await use_item(message, item)
            game_data.update_data()

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
                "Who's the richest in your server?", perms.EVERYONE, 1
            )

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

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
                text="You are at {} place\n\n".format(parse_place(players.index(message.author) + 1))
            )
            for i, p in enumerate(players):
                embed.description += "{} **{}** - {}\n".format(
                    emojis[i] if i < 3 else ":small_orange_diamond:", game_data.data[str(p.id)]["txc"], p
                )
                if i == 9:
                    break

            await message.reply(embed=embed, mention_author=False)


handler.add_category(Game)
