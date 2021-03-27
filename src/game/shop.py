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

    class Coffee(item.Item):
        def __init__(self):
            super().__init__("Coffee", ["coffee"],
                             "Drinking this will give you a 25% multi for 5-15 minutes!",
                             15000, True, True, True)

        def use(self, player):
            minute = random.randint(5, 15)
            effect_ = effect.Effect(minute * 60, {"multi": 25})
            effect_.start(player, self)

            return discord.Embed(
                title="You drank your coffee!",
                description="It gave you +25% multi for {} minutes!".format(minute),
                color=discord.Color.green()
            )

    def get_item(self, name: str):
        """
        gets an item by name. returns None if item is not found.

        :param name: str
        :return: Item or None
        """

        for item_ in self.items:
            if name in item_.display_name + item_.reference_names:
                return item_

        return None


shop = Shop()
