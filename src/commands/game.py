from src.category import Category
from src.command import CooldownCommand
from src.data import game_data
from src.emojis import item_emoji
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

    # currency
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
                "GrayStillPlays", "Github Cat", "linus"
            ]

            if chance(70):
                amount = multiplier(int(random.triangular(15, 1000, 75)), player.data["stats"]["multi"])
                player.data["stats"]["txc"] += amount
                await player.gain_exp()
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
            if chance(75):
                if chance(7):
                    amount = weighted_choice([(1, 0.92), (2, 0.06), (3, 0.02)])
                    item = shop.get_item(weighted_choice([
                        ("Apple",       0.4),
                        ("Coffee",      0.3),
                        ("Chocolate",   0.215),
                        ("Toxic Water", 0.085)
                    ]))
                    player.give_item(item, amount)
                    await player.gain_exp(2)

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
                    await player.gain_exp()

                    embed = discord.Embed(
                        title="You searched around...",
                        description="...and found **txc${}**!".format(amount),
                        color=discord.Color.green()
                    ).set_footer(
                        text="That's some sharp eyes bro"
                    )
                    await message.reply(embed=embed, mention_author=False)
            else:
                if chance(97):
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
                        "You drank the Toxic Water at the last second before you die, and it saved you!"
                    )

                    death_options = [
                        "You were hit by a car while searching in the middle of a street LMAO r u dumb?",
                        "Lol you wasn't looking where you were going and fell in a sewer and died.",
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
                return

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

    class Deposit(CooldownCommand):
        def __init__(self):
            super().__init__(["deposit", "dep"], "deposit <amount or \"all\">",
                             "Put your money in the bank so you don't lose EVERYTHING when you die.",
                             perms.EVERYONE, 3)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) == 0 or (args[0].lower() != "all" and parse_int(args[0]) is None):
                await message.reply("Hey tell me how much you want to deposit, or `all` to deposit all.",
                                    mention_author=False)
                return

            if parse_int(args[0]) == 0:
                await message.reply("You can't deposit nothing, stop trying to break me.", mention_author=False)
                return

            player = manager.get_player(message.author)

            if player.data["stats"]["txc"] == 0:
                await message.reply("Lol your wallet is as empty as your head.", mention_author=False)
                return

            amount = min([
                player.data["bank"]["max"] - player.data["bank"]["curr"],
                player.data["stats"]["txc"],
                parse_int(args[0]) if parse_int(args[0]) else player.data["stats"]["txc"]
            ])

            if player.data["bank"]["max"] - player.data["bank"]["curr"] == 0:
                await message.reply("Your bank is already maxed out!", mention_author=False)
                return

            player.data["bank"]["curr"] += amount
            player.data["stats"]["txc"] -= amount
            game_data.update_data()

            await message.reply("Alright, **txc${}** deposited safely into the bank.".format(amount),
                                mention_author=False)

    class Withdraw(CooldownCommand):
        def __init__(self):
            super().__init__(["withdraw", "with"], "withdraw <amount or \"all\">",
                             "Take some money out from the bank to spend!", perms.EVERYONE, 3)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) == 0 or (args[0].lower() != "all" and parse_int(args[0]) is None):
                await message.reply("Hey tell me how much you want to withdraw, or `all` to withdraw everything.",
                                    mention_author=False)
                return

            if parse_int(args[0]) == 0:
                await message.reply("You can't withdraw nothing, stop trying to break me.", mention_author=False)
                return

            player = manager.get_player(message.author)

            amount = min([
                player.data["bank"]["curr"],
                parse_int(args[0]) if parse_int(args[0]) else player.data["bank"]["curr"]
            ])

            player.data["stats"]["txc"] += amount
            player.data["bank"]["curr"] -= amount
            game_data.update_data()

            await message.reply("Alright, **txc${}** withdrawn from the bank.".format(amount),
                                mention_author=False)

    # item
    class Inventory(CooldownCommand):  # might need to add page system later
        def __init__(self):
            super().__init__(["inventory", "inv", "items"], "inventory [<user>]",
                             "See the things you or other people are somehow carrying all the time.", perms.EVERYONE, 3)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            member = message.author if len(args) == 0 else parse_member(message.guild, args[0])
            if not member:
                await message.reply("That user doesn't exist lol", mention_author=False)
                return

            player = manager.get_player(member)

            embed = discord.Embed(
                title="{}'s Inventory :file_folder:".format(member),
                description="There is literally nothing here lol." if len(player.data["inv"]) == 0 else "",
                color=discord.Color.gold()
            )

            for name, amount in sorted(player.data["inv"].items()):
                embed.description += "{} **{}** - {}\nID `{}`\n\n".format(
                    item_emoji(name), name, amount, shop.get_item(name).reference_names[0]
                )

            await message.reply(embed=embed, mention_author=False)

    class Use(CooldownCommand):
        def __init__(self):
            super().__init__(["use"], "use <item>", "Use an item.", perms.EVERYONE, 3)

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
            await player.gain_exp()
            response = await item.use(player, message)
            if response:
                if type(response) is discord.Embed:
                    await message.reply(embed=response, mention_author=False)
                else:
                    await message.reply(response, mention_author=False)

            game_data.update_data()

    # info
    class Profile(CooldownCommand):
        def __init__(self):
            super().__init__(["profile", "level", "levels"], "profile [<user>]",
                             "See yours or other people's stats!", perms.EVERYONE, 3)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            member = message.author if len(args) == 0 else parse_member(message.guild, args[0])
            if not member:
                await message.reply("That user doesn't exist lol", mention_author=False)

            player = manager.get_player(member)
            tot_exp = player.data["stats"]["exp"]
            exp = tot_exp % 100

            embed = discord.Embed(
                title="{}'s Profile :page_with_curl:".format(member),
                color=discord.Color.gold()
            ).add_field(
                name="Level {}".format(tot_exp // 100),
                value="[{}{}] {}%".format(
                    "■" * (n := exp // 5),
                    "□" * (20 - n),
                    exp
                ),
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

    class Bet(CooldownCommand):
        def __init__(self):
            super().__init__(["bet", "dice"], "bet <amount>", "Take some risk and hopefully win some money!",
                             perms.EVERYONE, 20)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) == 0 or (args[0].lower() != "all" and parse_int(args[0]) is None):
                await message.reply("Hey tell me how much you want to bet, or `all` to bet everything.",
                                    mention_author=False)
                return

            if parse_int(args[0]) == 0:
                await message.reply("You can't bet nothing idiot.", mention_author=False)
                return

            player = manager.get_player(message.author)

            if player.data["stats"]["txc"] == 0:
                await message.reply("Lol your wallet is as empty as your head.", mention_author=False)
                return

            amount = min(
                [parse_int(args[0]) if parse_int(args[0]) else player.data["stats"]["txc"], player.data["stats"]["txc"]]
            )
            player_roll = random.randint(1, 6)
            toxic_roll = random.randint(1, 6)

            embed = discord.Embed(
                title="{}'s dice game :game_die:".format(message.author),
                description=""
            ).add_field(
                name="You rolled",
                value="`{}`".format(player_roll)
            ).add_field(
                name="Toxic rolled",
                value="`{}`".format(toxic_roll)
            )

            if player_roll > toxic_roll:
                embed.description = "You won **txc${}**!".format(multiplier(amount, player.data["stats"]["multi"]))
                embed.color = discord.Color.green()
                embed.set_footer(text="stonks")

                await player.gain_exp(random.randint(2, 5))
                player.data["stats"]["txc"] += multiplier(amount, player.data["stats"]["multi"])
            elif player_roll == toxic_roll:
                embed.description = "Draw!"
                embed.color = discord.Color.blue()
                embed.set_footer(text="lucky or unlucky?")

                await player.gain_exp(2)
            else:
                embed.description = "You lost **txc${}**!".format(amount)
                embed.color = discord.Color.red()
                embed.set_footer(text="sucks to be you lol.")

                player.data["stats"]["txc"] -= amount

            game_data.update_data()
            await message.reply(embed=embed, mention_author=False)


handler.add_category(Game)
