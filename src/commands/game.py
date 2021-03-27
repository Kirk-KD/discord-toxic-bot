from src.category import Category
from src.command import CooldownCommand
from src.data import game_data
from src.game.game_manager import manager
from src.game.shop import shop
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

            if chance(60):
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

            player = manager.get_player(message.author)
            if chance(70):
                if chance(7):
                    amount = weighted_choice([(1, 0.92), (2, 0.06), (3, 0.02)])
                    item = shop.get_item(weighted_choice([
                        ("Apple",       0.4),
                        ("Coffee",      0.3),
                        ("Chocolate",   0.2),
                        ("Toxic Water", 0.1)
                    ]))
                    player.give_item(item, amount)

                    embed = discord.Embed(
                        title="You searched around...",
                        description="...and found {} **{}**!".format(amount, item.display_name),
                        color=discord.Color.green()
                    ).set_footer(
                        text="That's some sharp eyes bro"
                    )
                    await message.reply(embed=embed, mention_author=False)
                else:
                    amount = multiplier(int(random.triangular(10, 110, 50)), player.data["stats"]["multi"])
                    player.data["stats"]["txc"] += amount

                    embed = discord.Embed(
                        title="You searched around...",
                        description="...and found **txc${}**!".format(amount),
                        color=discord.Color.green()
                    ).set_footer(
                        text="That's some sharp eyes bro"
                    )
                    await message.reply(embed=embed, mention_author=False)
            else:
                if chance(90):
                    embed = discord.Embed(
                        title="You searched around...",
                        description="...and found NOTHING lmao",
                        color=discord.Color.red()
                    ).set_footer(
                        text="Haha noob"
                    )
                    await message.reply(embed=embed, mention_author=False)
                else:
                    killed = player.kill()
                    await message.author.send(
                        "Lmao you died noob. Buy some Toxic Water in the shop to save yourself next time!"
                        if killed else
                        "You drank th Toxic Water at the last second before you die, and it saved you!"
                    )

                    death_options = [
                        "You were hit by a car while searching in the middle of a street LMAO r u dumb?",
                        "Lol you wasn't looking where you are going and fell in a sewer and died.",
                        "Wow you searched all the way to Area51! And guess what? You were also shot in the head!",
                        "You did an unintentional science experiment about gravity."
                        "(Basically you fell down a cliff lol)",
                        "You were killed by another player who was also searching for stuff.",
                        "You tried to search inside you skull. Not only did you die, "
                        "you also found out you have a very small and smooth brain.",
                        "The developer thinks you are ugly and snapped you out of existence."
                    ]

                    embed = discord.Embed(
                        title="You died while searching lol",
                        description=random.choice(death_options),
                        color=discord.Color.red()
                    ).set_footer(
                        text="Haha noob"
                    )
                    await message.reply(embed=embed, mention_author=False)

            game_data.update_data()

    class UseItem(CooldownCommand):
        def __init__(self):
            super().__init__(["useitem", "use"], "useitem <item>", "Uses an item.", perms.EVERYONE, 3)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) == 0:
                await message.reply("Lmao you need to tell me what item you want to use.", mention_author=False)
                return

            player = manager.get_player(message.author)
            item = shop.get_item(args[0])
            if not item:
                await message.reply("Dude that item doesn't even exist what are you doing lol.", mention_author=False)
                return

            if not player.has_item(item):
                await message.reply("Lel you are so funny you don't even have that item.", mention_author=False)
                return

            if player.has_effect(item):
                await message.reply("Don't be so greedy, you already have that item's effect!", mention_author=False)
                return

            player.remove_item(item)
            response = await item.use(player, message)
            if response:
                if type(response) is discord.Embed:
                    await message.reply(embed=response, mention_author=False)
                else:
                    await message.reply(response, mention_author=False)

            game_data.update_data()

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

            player = manager.get_player(member)
            embed = discord.Embed(
                title="{}'s Balance :moneybag:".format(member),
                color=discord.Color.gold()
            ).add_field(
                name="Wallet",
                value=":dollar: `txc${}`".format(player.data["stats"]["txc"]),
                inline=False
            ).add_field(
                name="Bank",
                value=":dollar: `txc${} / {}`".format(player.data["bank"]["curr"], player.data["bank"]["max"]),
                inline=False
            ).add_field(
                name="Total",
                value=":dollar: `txc${}`".format(player.data["stats"]["txc"] + player.data["bank"]["curr"]),
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

            members_sorted = sorted(
                [member for member in message.guild.members if not member.bot],
                key=lambda m: manager.get_player(m).data["stats"]["txc"], reverse=True
            )

            emojis = ":first_place: :second_place: :third_place:".split()
            embed = discord.Embed(
                title="Top 10 rich bois in {}".format(message.guild.name),
                description="",
                color=discord.Color.gold()
            ).set_footer(
                text="You are at {} place\n\n".format(parse_place(members_sorted.index(message.author) + 1))
            )
            for i, p in enumerate(members_sorted):
                embed.description += "{} **{}** - {}\n".format(
                    emojis[i] if i < 3 else ":small_orange_diamond:", manager.get_player(p).data["stats"]["txc"], p
                )
                if i == 9:
                    break

            await message.reply(embed=embed, mention_author=False)


handler.add_category(Game)
