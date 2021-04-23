import datetime
import discord
import random

from src.bot.category import Category
from src.bot.command import GameCommand
from src.bot.emojis import item_emoji, item_image, emojis
from src.bot.game.game_manager import manager
from src.bot.game.shop import shop
from src.bot.handler import handler
from src.bot.game.stocks_collection import stocks

from src.bot.consts import beg, search

from src.util.game import chance, multiplier, parse_place
from src.util.parser import parse_member, parse_int
from src.util.time import format_time


class Game(Category):
    def __init__(self):
        super().__init__("Game", "A cross-server game with txc (toxic coin) as the currency!")

    # currency
    class Beg(GameCommand):
        def __init__(self):
            super().__init__(
                ["beg"], "beg", "Gotta start somewhere.", 20
            )

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            player = manager.get_player(message.author)

            if chance(70):
                amount = multiplier(int(random.triangular(15, 500, 75)), player.data["stats"]["multi"])
                player.data["stats"]["txc"] += amount
                await player.gain_exp()

                player.update_data()

                embed = discord.Embed(
                    title="Got 'em",
                    description="**{}** felt bad for you and gave you **txc${}** lmaooo :money_mouth:".format(
                        random.choice(beg["characters"]), amount
                    ),
                    color=discord.Color.green()
                ).set_footer(text="big stonks")
                await message.reply(embed=embed, mention_author=False)
            else:
                embed = discord.Embed(
                    title="No one cares",
                    description="**{}** walked right pass you and "
                                "didn't waste their money on someone like you lol".format(
                                    random.choice(beg["characters"])
                                ),
                    color=discord.Color.red()
                ).set_footer(text="stonkn't :(")
                await message.reply(embed=embed, mention_author=False)

    class Search(GameCommand):
        def __init__(self):
            super().__init__(["search"], "search", "Search for stuff around you.", 20)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            player = manager.get_player(message.author)
            if chance(75):
                if chance(7):
                    amount = random.choices([1, 2, 3], [0.92, 0.06, 0.02])
                    item = shop.get_item(random.choices(search["items"]["names"], search["items"]["weights"]))
                    player.give_item(item, amount)
                    await player.gain_exp(2)

                    embed = discord.Embed(
                        title="You searched around...",
                        description="...and found {} **{}**!".format(amount, item),
                        color=discord.Color.green()
                    ).set_footer(
                        text="That's some sharp eyes bro"
                    )
                    await message.reply(embed=embed, mention_author=False)
                else:
                    amount = multiplier(int(random.triangular(10, 1000, 75)), player.data["stats"]["multi"])
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
                    player.kill()

                    embed = discord.Embed(
                        title="You died while searching lol",
                        description=random.choice(search["death"]),
                        color=discord.Color.red()
                    ).set_footer(
                        text="Haha noob"
                    )
                    await message.reply(embed=embed, mention_author=False)

            player.update_data()

    class Balance(GameCommand):
        def __init__(self):
            super().__init__(
                ["balance", "money", "txc", "bal"], "balance [<user>]", "See how rich you or other people are!", 3
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

    class Deposit(GameCommand):
        def __init__(self):
            super().__init__(["deposit", "dep"], "deposit <amount or \"all\">",
                             "Put your money in the bank so you don't lose EVERYTHING when you die.", 3)

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

            player.update_data()

            await message.reply("Alright, **txc${}** deposited safely into the bank.".format(amount),
                                mention_author=False)

    class Withdraw(GameCommand):
        def __init__(self):
            super().__init__(["withdraw", "with"], "withdraw <amount or \"all\">",
                             "Take some money out from the bank to spend!", 3)

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
            player.update_data()

            await message.reply("Alright, **txc${}** withdrawn from the bank.".format(amount),
                                mention_author=False)

    class Give(GameCommand):
        def __init__(self):
            super().__init__(["give", "share", "gift"], "give <user> ((<item> [<amount>]) or (<amount>))",
                             "Give money or items to other people!", 5)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) < 1:
                await message.reply("Lel who are you giving stuff to idiot.", mention_author=False)
                return

            if len(args) < 2:
                await message.reply("How much money or items do you want to give them lol.", mention_author=False)
                return

            player = manager.get_player(message.author)
            target_member = parse_member(message.guild, args[0])
            amount = parse_int(args[-1])
            autofill_amount = False

            if not target_member:
                await message.reply("Alright tell your non-existing friend I said hello. Now go play kiddo.",
                                    mention_author=False)
                return

            if not amount:
                if shop.get_item(" ".join(args[1:])):
                    amount = 1
                    autofill_amount = True
                else:
                    await message.reply("Um I think I need a valid number, maybe???", mention_author=False)
                    return

            target = manager.get_player(target_member)
            if not target:
                await message.reply("Dummy you can't give your stuff to bots.", mention_author=False)
                return

            if len(args) >= (2 if autofill_amount else 3):
                item_name = " ".join(args[1:-1] if not autofill_amount else args[1:])
                item = shop.get_item(item_name)

                if not item:
                    await message.reply("That item doesn't exist, stop making stuff up.", mention_author=False)
                    return

                if not player.has_item(item) or player.count_item(item) < amount:
                    await message.reply("You don't have enough to give lol.", mention_author=False)
                    return

                if target_member == message.author:
                    await message.reply("Um ok? You gave yourself {} **{}**. And?".format(amount, item),
                                        mention_author=False)
                    return

                player.remove_item(item, amount)
                target.give_item(item, amount)
                embed = discord.Embed(
                    title="You gave {} {} **{}**!".format(target.member, amount, item),
                    description="You gave {} {} **{}**, now you have **{}**.".format(
                        target.member, amount, item, (player.data["inv"][item.display_name] if
                                                      item.display_name in player.data["inv"].keys() else "0")
                    ),
                    color=discord.Color.green()
                )
            else:
                assert amount is not None
                if player.data["stats"]["txc"] < amount:
                    await message.reply("You don't have enough to give lol.", mention_author=False)
                    return

                if target_member == message.author:
                    await message.reply("Um ok? You gave yourself **txc${}**. And?".format(amount),
                                        mention_author=False)
                    return

                player.data["stats"]["txc"] -= amount
                target.data["stats"]["txc"] += amount
                embed = discord.Embed(
                    title="You gave {} **txc${}**!".format(target.member, amount),
                    description="You gave {} **txc${}**, now you have **txc${}**.".format(
                        target.member, amount, player.data["stats"]["txc"]
                    ),
                    color=discord.Color.green()
                )

            player.update_data()
            await message.reply(embed=embed, mention_author=False)

    # item
    class Shop(GameCommand):
        def __init__(self):
            super().__init__(["shop"], "shop [<item>]", "Visit the shop or show detail of an item!", 3)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) == 0:
                embed = discord.Embed(
                    title="The Toxic Shop",
                    description="",
                    color=discord.Color.gold()
                )
                for item in shop.items:
                    embed.description += "**{}** - txc${}\n*{}*\n\n".format(
                        item,
                        str(item.price) + (" *(not purchasable)*" if not item.is_purchasable else ""),
                        item.description
                    )

                await message.reply(embed=embed, mention_author=False)
            else:
                item = shop.get_item(" ".join(args[0:]))
                if not item:
                    await message.reply("Lel that item doesn't exist stupid.", mention_author=False)
                    return

                embed = discord.Embed(
                    title=item.display_name,
                    description=item.description,
                    color=discord.Color.gold()
                ).add_field(
                    name="Price",
                    value="txc${}".format(item.price),
                    inline=False
                ).add_field(
                    name="Purchasable?",
                    value=":white_check_mark:" if item.is_purchasable else ":x:"
                ).add_field(
                    name="Sellable?",
                    value=":white_check_mark:" if item.is_sellable else ":x:"
                ).add_field(
                    name="Usable?",
                    value=":white_check_mark:" if item.is_usable else ":x:"
                ).set_thumbnail(
                    url="attachment://g_{}.png".format(item.display_name.lower().replace(" ", "_") if
                                                       item.display_name in emojis.keys() else "place_holder")
                )

                await message.reply(file=item_image(item.display_name), embed=embed, mention_author=False)

    class Inventory(GameCommand):  # might need to add page system later
        def __init__(self):
            super().__init__(["inventory", "inv", "items"], "inventory [<user>]",
                             "See the things you or other people are somehow carrying all the time.", 3)

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

    class Use(GameCommand):  # TODO: BETTER USE SYSTEM
        def __init__(self):
            super().__init__(["use"], "use <item>", "Use an item.", 3)

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

            if player.has_effect(item) and not item.effect_stackable:
                await message.reply("Don't be so greedy, you already have that item's effect!", mention_author=False)
                return

            player.remove_item(item)
            response = await item.use(player, message, client)
            player.update_data()

            if response:
                if type(response) is discord.Embed:
                    await message.reply(embed=response, mention_author=False)
                else:
                    await message.reply(response, mention_author=False)

    class Buy(GameCommand):
        def __init__(self):
            super().__init__(["buy"], "buy <item> <amount>", "Buys an item from the shop.", 3)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) < 1:
                await message.reply("What do you want to buy dummy.", mention_author=False)
                return

            amount = parse_int(args[-1])
            if amount is None:
                amount = 1
                item = shop.get_item(" ".join(args))
            elif amount == 0:
                await message.reply("Uh, sure, you bought nothing. Have it for free.", mention_author=False)
                return
            else:
                item = shop.get_item(" ".join(args[:-1]))

            if not item or not item.is_purchasable:
                await message.reply("Lol the shop doesn't even sell that.", mention_author=False)
                return

            price = amount * item.price
            player = manager.get_player(message.author)
            if player.data["stats"]["txc"] < price:
                await message.reply("Well that sucks, you are poor and you can't afford it LMAO", mention_author=False)
                return

            player.data["stats"]["txc"] -= price
            player.give_item(item, amount)
            player.update_data()

            embed = discord.Embed(
                title="Successful Purchase",
                description="You bought {} **{}** for **txc${}**! Now you have **txc${}** left in your wallet.".format(
                    amount, item, price, player.data["stats"]["txc"]
                ),
                color=discord.Color.green()
            ).set_footer(
                text="ever wondered who the shop owner is?"
            )
            await message.reply(embed=embed, mention_author=False)

    class Sell(GameCommand):
        def __init__(self):
            super().__init__(["sell"], "sell <item> <amount>", "Sell something 10% the original price.", 3)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            if len(args) < 1:
                await message.reply("What do you want to sell dummy.", mention_author=False)
                return

            amount = parse_int(args[-1])
            if amount is None:
                amount = 1
                item = shop.get_item(" ".join(args))
            elif amount == 0:
                await message.reply("Hmm ok, you sold nothing for nothing. Have fun.", mention_author=False)
                return
            else:
                item = shop.get_item(" ".join(args[:-1]))

            if not item or not item.is_sellable:
                await message.reply("Lol the shop doesn't even want that.", mention_author=False)
                return

            player = manager.get_player(message.author)
            if player.count_item(item) < amount:
                await message.reply("Lol you don't even have enough, stop humiliating yourself.", mention_author=False)
                return

            print(amount)
            txc_gain = player.multiplier(item.price // 10 * amount)
            player.remove_item(item, amount)
            player.data["stats"]["txc"] += txc_gain
            player.update_data()

            embed = discord.Embed(
                title="Successful Sale",
                description="You sold {} **{}** for **txc${}**! You now have {} left.".format(
                    amount, item, txc_gain, player.count_item(item)
                ),
                color=discord.Color.green()
            ).set_footer(text="who is the shop owner tho")
            await message.reply(embed=embed, mention_author=False)

    # info
    class Profile(GameCommand):
        def __init__(self):
            super().__init__(["profile", "level", "levels"], "profile [<user>]",
                             "See yours or other people's stats!", 3)

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
            ).add_field(
                name="Multi",
                value="`{}%`".format(player.data["stats"]["multi"]),
                inline=True
            ).add_field(
                name="Wallet",
                value="`txc${}`".format(player.data["stats"]["txc"]),
                inline=True
            ).add_field(
                name="Bank",
                value="`txc${} / {}`".format(player.data["bank"]["curr"], player.data["bank"]["max"]),
                inline=True
            )

            await message.reply(embed=embed, mention_author=False)

    class Leaderboard(GameCommand):
        def __init__(self):
            super().__init__(
                ["leaderboard", "lb", "rich"], "leaderboard",
                "Who's the richest in your server?", 1
            )

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            members_sorted = sorted(
                [member for member in message.guild.members if not member.bot],
                key=lambda m: manager.get_player(m).data["stats"]["txc"], reverse=True
            )

            e = ":first_place: :second_place: :third_place:".split()
            embed = discord.Embed(
                title="Top 10 rich bois in {}".format(message.guild.name),
                description="",
                color=discord.Color.gold()
            ).set_footer(
                text="You are at {} place\n\n".format(parse_place(members_sorted.index(message.author) + 1))
            )
            for i, p in enumerate(members_sorted):
                embed.description += "{} **{}** - {}\n".format(
                    e[i] if i < 3 else ":small_orange_diamond:", manager.get_player(p).data["stats"]["txc"], p
                )
                if i == 9:
                    break

            await message.reply(embed=embed, mention_author=False)

    # gamble
    class Bet(GameCommand):
        def __init__(self):
            super().__init__(["bet", "dice"], "bet <amount>", "Take some risk and hopefully win some money!", 20)

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
                [parse_int(args[0]) if parse_int(args[0]) else player.data["stats"]["txc"],
                 player.data["stats"]["txc"], 50000]
            )
            player_roll = random.randint(1, 6)
            toxic_roll = random.randint(1, 6)

            embed = discord.Embed(
                title="{}'s dice game :game_die:".format(message.author),
                description="You bet **txc${}** and ".format(amount)
            ).add_field(
                name="You rolled",
                value="`{}`".format(player_roll)
            ).add_field(
                name="Toxic rolled",
                value="`{}`".format(toxic_roll)
            )

            if player_roll > toxic_roll:
                embed.description += "won **txc${}**!".format(multiplier(amount * 2, player.data["stats"]["multi"]))
                embed.color = discord.Color.green()
                embed.set_footer(text="stonks")

                await player.gain_exp(random.randint(2, 5))
                player.data["stats"]["txc"] += multiplier(amount * 2, player.data["stats"]["multi"])
            elif player_roll == toxic_roll:
                embed.description = "Draw!"
                embed.color = discord.Color.blue()
                embed.set_footer(text="lucky or unlucky?")

                await player.gain_exp(2)
            else:
                embed.description += "lost **txc${}**!".format(amount)
                embed.color = discord.Color.red()
                embed.set_footer(text="sucks to be you lol.")

                player.data["stats"]["txc"] -= amount

            player.update_data()
            await message.reply(embed=embed, mention_author=False)

    class Stocks(GameCommand):
        def __init__(self):
            super().__init__(["stocks", "stock", "stonks", "stonk"],
                             "stocks [(\"buy\" or \"sell\" or \"view\") <stock>] [<amount>]",
                             "They say you could become a rich boi doing this.", 5)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            player = manager.get_player(message.author)

            if len(args) == 0:
                embed = discord.Embed(
                    title=":chart_with_downwards_trend: Stocks :chart_with_upwards_trend:",
                    description="`stocks buy <amount> <name>` to buy\n"
                                "`stocks sell <amount> <name>` to sell\n"
                                "`stocks view <name>` to view growth",
                    color=discord.Color.blue()
                )

                for s in stocks.data:
                    stock = stocks.get_stock(s["_id"])
                    embed.add_field(
                        name=s["_id"] + " `{} owned`".format(player.data["stocks"][stock.name]),
                        value="**txc${}**".format(stock.current) + (
                            " :chart_with_upwards_trend:" if stock.record[-1] > stock.record[-2] else
                            (" :chart_with_downwards_trend:" if stock.record[-1] < stock.record[-2] else "")
                        ),
                        inline=False
                    )

                await message.reply(embed=embed, mention_author=False)
            else:
                if args[0].lower() == "view":
                    if len(args) < 2:
                        await message.reply("Which stock do you want to see dummy?", mention_author=False)
                        return

                    stock = stocks.get_stock(" ".join(args[1:]))
                    if not stock:
                        await message.reply("That stock literally doesn't exist.", mention_author=False)
                        return

                    embed = discord.Embed(
                        title="{} stock".format(stock.name),
                        description="Stocks update every hour. Showing previous 3 days.",
                        color=discord.Color.blue()
                    ).set_image(
                        url="attachment://{}.png".format(stock.name.lower().replace(" ", "_"))
                    )

                    await message.reply(file=discord.File(
                        stock.get_graph(), filename="{}.png".format(stock.name.lower().replace(" ", "_"))
                    ), embed=embed, mention_author=False)

                elif args[0].lower() == "buy":
                    if len(args) < 2:
                        await message.reply("How many do you want to buy idiot.", mention_author=False)
                        return

                    amount = parse_int(args[1])
                    if not amount:
                        await message.reply("Invalid number lel.", mention_author=False)
                        return

                    if len(args) < 3:
                        await message.reply("Which stock do you want to buy idiot.", mention_author=False)
                        return

                    stock = stocks.get_stock(" ".join(args[2:]))
                    if not stock:
                        await message.reply("Invalid stock name lel.", mention_author=False)
                        return

                    price = amount * stock.current
                    if price > player.data["stats"]["txc"]:
                        await message.reply("Lol you can't even afford it.", mention_author=False)
                        return

                    player.data["stats"]["txc"] -= price
                    player.data["stocks"][stock.name] += amount
                    player.update_data()

                    embed = discord.Embed(
                        title=":chart_with_downwards_trend: Stock Purchase :chart_with_upwards_trend:",
                        description="You purchased {} **{}** stock for **txc${}**".format(
                            amount, stock.name, price
                        ),
                        color=discord.Color.green()
                    ).set_footer(
                        text="future stonks?"
                    )

                    await message.reply(embed=embed, mention_author=False)

                elif args[0].lower() == "sell":
                    if len(args) < 2:
                        await message.reply("How many do you want to sell idiot.", mention_author=False)
                        return

                    amount = parse_int(args[1])
                    if not amount:
                        await message.reply("Invalid number lel.", mention_author=False)
                        return

                    if len(args) < 3:
                        await message.reply("Which stock do you want to sell idiot.", mention_author=False)
                        return

                    stock = stocks.get_stock(" ".join(args[2:]))
                    if not stock:
                        await message.reply("Invalid stock name lel.", mention_author=False)
                        return

                    if player.data["stocks"][stock.name] < amount:
                        await message.reply("Lol you don't have enough. Stop day dreaming.", mention_author=False)
                        return

                    player.data["stocks"][stock.name] -= amount
                    player.data["stats"]["txc"] += max(stock.current * amount, 1)
                    player.update_data()

                    embed = discord.Embed(
                        title=":chart_with_downwards_trend: Stock Trade :chart_with_upwards_trend:",
                        description="You sold {} **{}** stock for **txc${}**!".format(
                            amount, stock.name, max(stock.current * amount, 1)
                        ),
                        color=discord.Color.blue()
                    )
                    await message.reply(embed=embed, mention_author=False)

    # cooldown
    class Streak(GameCommand):
        def __init__(self):
            super().__init__(["streak", "streaks"], "streak", "Get a small price everyday and a big one on day 7!", 1)

        async def __call__(self, message, args, client):
            if not await self.check_cooldown(message):
                return

            player = manager.get_player(message.author)

            if player.data["timers"]["streak"] is not None:
                await message.reply(
                    "Chill out bro, your can get your next daily prize at `{}`!".format(
                        format_time(player.data["timers"]["streak"])
                    ), mention_author=False
                )
                return

            streak = player.data["stats"]["streak"]
            txc = 420 + streak * (15 + streak // 5)
            items = random.choices(["Apple", "Chocolate", "Coffee", "Cursed Seal", "Bank Token", "Toxic Water"],
                                   weights=[15, 15, 8, 4, 3, 1],
                                   k=random.choices([1, 2, 3, 4, 5], weights=[15, 5, 3, 2, 1], k=1)[0])
            give_items = chance(55)

            player.data["stats"]["streak"] += 1
            player.data["timers"]["streak"] = str(datetime.datetime.now() + datetime.timedelta(days=1))

            player.data["stats"]["txc"] += txc
            [player.give_item(shop.get_item(name)) for name in items] if give_items else None

            player.update_data()

            embed = discord.Embed(
                title="{}'s Daily Prize :hourglass:".format(message.author),
                description="You got **txc${}**{}!".format(
                    txc, " and {}".format(
                        ", ".join(["{} **{}**".format(items.count(name), shop.get_item(name)) for name in set(items)])
                    ) if give_items else ""
                ),
                color=discord.Color.gold()
            ).set_footer(
                text="Day {}".format(streak)
            )
            await message.reply(embed=embed, mention_author=False)


handler.add_category(Game)
