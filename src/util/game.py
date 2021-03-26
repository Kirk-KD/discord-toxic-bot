import random
import discord

from src.data import game_data
from src.game.item import Item


def multiplier(amount: int, multi: int):
    """
    returns amount + amount * multi, parsed to int.

    :param amount: int
    :param multi: int
    :return: int
    """

    return amount + int(amount * (multi / 100))


def parse_place(n: int or str):
    """
    given a number or string and add "st", "nd", "rd", or "th" at the end accordingly.

    :param n: int or str
    :return:
    """

    s = str(n)
    suffixes = "st nd rd".split()
    return s + (suffixes[int(s[-1]) - 1] if 0 < int(s[-1]) < 4 else "th")


def chance(percent: int or float):
    """
    returns if a random float between 1-100 if less than or equal to percent.

    :param percent: int or float
    :return: bool
    """

    return random.uniform(0.0, 100.0) <= percent


def get_player(user_id: str or int):
    """
    gets a player in game_data.

    :param user_id: str or int
    :return: dict
    """

    return game_data.data[str(user_id)] if str(user_id) in game_data.data.keys() else None


def give_item(player: dict, item: Item, amount: int=1):
    """
    gives a player an item.

    :param player: dict
    :param item: Item
    :param amount: int
    :return: None
    """

    if item.name in player["inv"].keys():
        player["inv"][item.name] += amount
    else:
        player["inv"][item.name] = 1


async def use_item(message: discord.Message, item: Item):
    """
    uses an item.

    :param message: Message
    :param item: Item
    :return: None
    """

    player = get_player(message.author.id)
    player["inv"][item.name] -= 1
    await item.use(message)


def kill_player(player: dict):
    """
    tries to kill the player and returns if the player is actually killed.

    :param player: dict
    :return: bool
    """

    if "Toxic Potion" not in player["inv"].keys():
        player["inv"] = {}
        player["txc"] = 0
        return True

    return False
