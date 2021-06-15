import random
import discord

from src.bot.data import game_data
from src.bot.game import item


class Player:
    def __init__(self, member: discord.Member):
        self.member = member
        self.data = game_data.get(self.member.id)

    def has_item(self, item_: item.Item):
        """
        returns whether or not the player has an item.

        :param item_: Item
        :return: bool
        """

        return item_.display_name in self.data["inv"].keys()

    def count_item(self, item_: item.Item):
        """
        returns the amount of item the player has.

        :param item_: Item
        :return: int
        """

        return 0 if not self.has_item(item_) else self.data["inv"][item_.display_name]

    def give_item(self, item_: item.Item, amount: int = 1):
        """
        gives an amount of item to the player.

        :param item_: Item
        :param amount: int
        :return: None
        """

        if self.has_item(item_):
            self.data["inv"][item_.display_name] += amount
        else:
            self.data["inv"][item_.display_name] = amount

    def remove_item(self, item_: item.Item, amount: int = 1):
        """
        removes an amount of item form the player and returns the amount of items removed.

        :param item_: Item
        :param amount: int
        :return: int
        """

        if not self.has_item(item_):
            return 0

        temp = self.data["inv"][item_.display_name]
        self.data["inv"][item_.display_name] -= amount
        if self.data["inv"][item_.display_name] <= 0:
            self.data["inv"].pop(item_.display_name, None)
            return amount - temp

        return amount

    def has_effect(self, item_: item.Item):
        """
        returns whether or not the player has an effect.

        :param item_: Item
        :return: bool
        """

        return item_.display_name in self.data["effects"]

    async def kill(self):
        """
        kills the player (removes all item, clear wallet) and returns if the player is actually dead.

        :return: bool
        """

        from src.bot.game.shop import shop

        if self.has_item(shop.get_item("Toxic Water")):
            self.remove_item(shop.get_item("Toxic Water"))
            await self.member.send(
                "You drank the Toxic Water at the last second before you die, and it saved you! That was close!"
            )
        else:
            self.data["stats"]["txc"] = 0
            self.data["inv"] = {}
            self.data["effects"] = []
            await self.member.send("Lmao you died noob. Buy some Toxic Water in the shop to save yourself next time!")

    async def gain_exp(self, amount: int = 1):
        """
        gives the player some exp.

        :param amount: int
        :return: None
        """

        before = self.data["stats"]["exp"]

        self.data["stats"]["exp"] += amount
        self.data["bank"]["max"] += amount * random.randint(10, 100)

        if before // 100 != self.data["stats"]["exp"] // 100:
            self.data["bank"]["max"] += random.randint(500, 1000)
            await self.member.send("Ayy you leveled up to level {}!".format(self.data["stats"]["exp"] // 100))

    def multiplier(self, amount: int):
        return round(amount + round(amount * (self.data["stats"]["multi"] / 100)))

    def update_data(self):
        game_data.set(self.member.id, {"data": self.data})
