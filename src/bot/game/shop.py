import asyncio
import discord
import inspect
import random

from src.bot.game import item, effect
from src.bot.game.game_manager import manager

from src.util.game import chance
from src.util.parser import parse_member


class Shop:
    """
    a collection of Items.
    """

    def __init__(self):
        self.items = []

        item_names = [item_name for item_name in dir(self) if not item_name.startswith("__")]

        for item_name in item_names:
            if inspect.isclass(getattr(self, item_name)):
                self.items.append(getattr(self, item_name)())

    # items
    class ToxicWater(item.Item):
        def __init__(self):
            super().__init__("Toxic Water", ["toxicwater", "toxic", "water"],
                             "This bottle of unpleasant liquid, for some weird reason, can revive you!",
                             80000, False, True, True)

    class Chocolate(item.Item):
        def __init__(self):
            super().__init__("Chocolate", ["chocolate", "choco"],
                             "Eating this wonderful thing will give you a random amount of EXP!",
                             30000, True, True, True)

        async def use(self, player, message, client):
            exp = round(random.triangular(1, 100, 60))
            await player.gain_exp(exp)

            return discord.Embed(
                title="You ate a chocolate bar!",
                description="It tastes so good that you gained **{}** EXP!".format(exp),
                color=discord.Color.green()
            )

    class Coffee(item.Item):
        def __init__(self):
            super().__init__("Coffee", ["coffee"],
                             "Drinking this will give you a 15% multi for 5-15 minutes!",
                             15000, True, True, True)

        async def use(self, player, message, client):
            minute = random.randint(5, 15)
            effect_ = effect.Effect(minute * 60, {"multi": 15})

            embed = discord.Embed(
                title="You drank your coffee!",
                description="It gave you +15% multi for {} minutes!".format(minute),
                color=discord.Color.green()
            )
            await message.reply(embed=embed, mention_author=False)

            await effect_.start(player, self)

    class Apple(item.Item):
        def __init__(self):
            super().__init__("Apple", ["apple"], "An apple a day keeps nothing away! It will give you some money tho.",
                             150, True, False, True)

        async def use(self, player, message, client):
            amount = random.randint(100, 1000)
            player.data["stats"]["txc"] += amount

            return discord.Embed(
                title="You ate an apple!",
                description="And received **{}$txc**, for some reason!".format(amount),
                color=discord.Color.green()
            )

    class CursedSeal(item.Item):
        def __init__(self):
            super().__init__("Cursed Seal", ["cursedseal", "curse", "seal", "cursed"],
                             "Using this on someone will give them a -5% to -30% multiplier for 30 minutes! "
                             "Btw it has a 30% chance or backfiring, just saying.",
                             50000, True, True, True, effect_stackable=True)

        async def use(self, player, message, client):
            if player.has_effect(self):
                return "Lol you are already cursed, you can't use the seal!"

            await message.reply("Who do you want to curse (30% chance of backfiring)?", mention_author=False)

            try:
                input_msg = await client.wait_for("message",
                                                  check=lambda m: (m.author == message.author and
                                                                   m.channel == message.channel),
                                                  timeout=30)
            except asyncio.TimeoutError:
                return "What the hell you didn't reply. You just wasted a seal."

            member = parse_member(message.guild, input_msg.content)
            if not member:
                return "Lol that user doesn't exist. You just wasted a seal."

            target = await manager.get_player(member)
            amount = -random.randint(10, 30)
            e = effect.Effect(30 * 60, {"multi": amount})

            if message.author == member:
                await message.reply(
                    "Um ok, you cursed yourself and received a multiplier of **{}%** for 30 minutes.".format(amount),
                    mention_author=False
                )
                await e.start(player, self)

            if target.has_effect(self):
                return "Dude they have already been cursed, give them a BREAK. You just wasted a seal."

            if chance(30):
                await message.reply(
                    ("You tried to curse someone, but BOOM \\*uno reverse\\* TAKE THAT! "
                     "You received a multiplier of **{}%** for 30 minutes.".format(amount)),
                    mention_author=False
                )
                await e.start(player, self)
            else:
                await message.reply(
                    "{} has been cursed with **{}%** multi for 30 minutes!".format(member, amount),
                    mention_author=False
                )
                await e.start(target, self)

    class BankToken(item.Item):
        def __init__(self):
            super().__init__("Bank Token", ["banktoken", "bank", "token"],
                             "Get some extra bank space by giving this to the bank!",
                             10000, True, False, True)

        async def use(self, player, message, client):
            gain = random.randint(500, 10000)
            player.data["bank"]["max"] += gain
            await player.update_data()

            return "You used your bank token, and the bank gave you **txc${}** more bank space!".format(gain)

    def get_item(self, name: str):
        """
        gets an item by name. returns None if item is not found.

        :param name: str
        :return: Item or None
        """

        for item_ in self.items:
            if name.lower() in [item_.display_name.lower()] + item_.reference_names:
                return item_

        return None


shop = Shop()
