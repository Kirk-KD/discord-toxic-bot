import discord

from src.util.game import get_player


class Item:
    """
    an object representing an item in the game
    """

    def __init__(self, name: str, ref_names: list[str], description: str, price: int,
                 usable: bool, purchasable: bool, sellable: bool):
        self.name = name
        self.ref_names = ref_names
        self.description = description
        self.price = price

        self.usable = usable
        self.purchasable = purchasable
        self.sellable = sellable

    async def use(self, message: discord.Message):
        """
        if the item is usable, raise NotImplementedError if a child class does not override this method

        :param message: Message
        :return: None
        """

        if self.usable:
            raise NotImplementedError()
        else:
            await message.reply("You can't use that lol.", mention_author=False)

    async def sell(self, message: discord.Message):
        """
        sells the item.

        :param message: Message
        :return: None
        """

        if self.sellable:
            player = get_player(message.author.id)
            player["inv"][self.name] -= 1
            player["txc"] += self.price
        else:
            await message.reply("Lmao are you that poor, selling an item no shop will buy?", mention_author=False)

    async def buy(self, message: discord.Message, amount: int=1):
        """
        buys the item.

        :param message: Message
        :param amount: int
        :return: None
        """

        if self.sellable:
            player = get_player(message.author.id)
            player["txc"] -= self.price * amount
            if self.name in player["inv"].keys():
                player["inv"][self.name] += amount
            else:
                player["inv"][self.name] = amount
        else:
            await message.reply("lol this item is not for sale.", mention_author=False)

