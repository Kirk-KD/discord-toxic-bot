import random


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
