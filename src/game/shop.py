from src.game.item import Item
from src.data import game_data

import inspect
import random
import discord


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

    def get_item(self, name: str):
        """
        gets an Item by referencing names (not display name) or None if not found.

        :param name: str
        :return: Item or None
        """

        for item in self.items:
            if name in item.ref_names:
                return item

        return None

    class ToxicPotion(Item):
        def __init__(self):
            super().__init__(
                "Toxic Potion", ["toxicpotion", "toxic"],
                "Consumed when you are dying and revives you, for some reason.",
                250000, False, True, False
            )

    class Coffee(Item):
        def __init__(self):
            super().__init__(
                "Coffee", ["coffee"],
                "Gives you a random stacking multiplier for every cup of coffee you drink.",
                500000, True, True, False
            )

        async def use(self, message):
            player = game_data.data[str(message.author.id)]
            amount = int(random.triangular(1, 8, 3))
            player["multi"] += amount
            game_data.update_data()

            embed = discord.Embed(
                title="You drank your Coffee!",
                description="It gave you an additional multi of {}%!".format(amount),
                color=discord.Color.green()
            ).set_footer(
                text="You now have a multi of {}%".format(player["multi"])
            )
            await message.reply(embed=embed, mention_author=False)


shop = Shop()
