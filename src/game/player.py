import random

from src.data import game_data
from src.game import item

import discord

from src.game.shop import shop


class Player:
    def __init__(self, member: discord.Member):
        self.member = member
        self.data = game_data.data["players"][str(self.member.id)]

    def has_item(self, item_: item.Item):
        """
        returns whether or not the player has an item.

        :param item_: Item
        :return: bool
        """

        return item_.display_name in self.data["inv"].keys()

    def give_item(self, item_: item.Item, amount: int=1):
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

    def remove_item(self, item_: item.Item, amount: int=1):
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

    def kill(self):
        """
        kills the player (removes all item, clear wallet) and returns if the player is actually dead.

        :return: bool
        """

        if self.has_item(shop.get_item("Toxic Water")):
            self.remove_item(shop.get_item("Toxic Water"))
            return False

        self.data["stats"]["txc"] = 0
        self.data["inv"] = {}
        self.data["effects"] = []

        return True

    async def gain_exp(self, amount: int=1):
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
