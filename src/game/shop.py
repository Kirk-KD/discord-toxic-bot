from src.game import item, effect, game_manager

import discord
import inspect
import random


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

        def use(self, player, message=None):
            exp = round(random.triangular(1, 100, 60))
            player.data["stats"]["exp"] += exp

            return discord.Embed(
                title="You shoved a whole chocolate bar in your mouth!",
                description="It tastes so good that you gained **{}** EXP!".format(exp),
                color=discord.Color.green()
            )

    class Coffee(item.Item):
        def __init__(self):
            super().__init__("Coffee", ["coffee"],
                             "Drinking this will give you a 15% multi for 5-15 minutes!",
                             15000, True, True, True)

        async def use(self, player, message=None):
            minute = random.randint(5, 15)
            effect_ = effect.Effect(minute * 60, {"multi": 15})

            embed = discord.Embed(
                title="You drank your coffee!",
                description="It gave you +25% multi for {} minutes!".format(minute),
                color=discord.Color.green()
            )
            await message.reply(embed=embed, mention_author=False)

            await effect_.start(player, self)

    class Apple(item.Item):
        def __init__(self):
            super().__init__("Apple", ["apple"], "An apple a day keeps nothing away! It will give you some money tho.",
                             150, True, False, True)

        async def use(self, player, message=None):
            amount = random.randint(100, 1000)
            player.data["stats"]["txc"] += amount

            return discord.Embed(
                title="You ate an apple!",
                description="And received **{}$txc**, for some reason!".format(amount),
                color=discord.Color.green()
            )

    def get_item(self, name: str):
        """
        gets an item by name. returns None if item is not found.

        :param name: str
        :return: Item or None
        """

        for item_ in self.items:
            if name in [item_.display_name] + item_.reference_names:
                return item_

        return None


shop = Shop()
