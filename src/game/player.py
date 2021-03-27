from src.data import game_data
from src.game import item

import discord


class Player:
    def __init__(self, member: discord.Member):
        self.member = member
        self.data = game_data.data[str(self.member.id)]

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

    def use_item(self, item_: item.Item):
        """
        call the item's user() method on the player, then returns the message returned by the item.

        :param item_: Item
        :return: str or Embed
        """

        return item_.use(self)

    def has_effect(self, item_: item.Item):
        """
        returns whether or not the player has an effect.

        :param item_: Item
        :return: bool
        """

        return item_.display_name in self.data["effects"]
