"""
stores data read from json files
"""

from src.util import *

# load data
guilds_data = read_json("saved_data/guilds.json")


def update_data():
    """
    updates guilds.json according to guilds_data

    :return: None
    """

    write_json("saved_data/guilds.json", guilds_data)


def get_data(path: str):
    """
    gets a value in guilds_data by a path-like string

    :param path: str
    :return: Any
    """

    keys = path.split("/")
    c = guilds_data
    for key in keys:
        c = c[key]

    return c


def set_data(path: str, val):
    """
    sets a value in guilds_data by a path-like string

    :param path: str
    :param val: Any
    :return: None
    """

    keys = path.split("/")
    d = guilds_data
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = val
