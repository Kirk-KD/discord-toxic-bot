import random

from src.data import game_data


def multiplier(amount, multi):
    return amount + int(amount * (multi / 100))


def parse_place(n):
    s = str(n)
    suffixes = "st nd rd".split()
    return s + (suffixes[int(s[-1]) - 1] if 0 < int(s[-1]) < 4 else "th")


def chance(percent: int or float):
    return random.uniform(0.0, 100.0) <= percent


def give_item(player, item, amount=1):
    if item.name in player["inv"].keys():
        player["inv"][item.name] += amount
    else:
        player["inv"][item.name] = 1


async def use_item(message, item):
    player = game_data.data[str(message.author.id)]
    player["inv"][item.name] -= 1
    await item.use(message)


def kill_player(player):
    if "Toxic Potion" not in player["inv"].keys():
        player["inv"] = {}
        player["txc"] = 0
        return True

    return False
