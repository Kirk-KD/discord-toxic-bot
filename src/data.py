"""
stores data read from json files
"""

from src.util import *

# load data
guilds_data = read_json("saved_data/guilds.json")


def update_guilds_data():
    """
    updates guilds.json according to guilds_data

    :return: None
    """

    write_json("saved_data/guilds.json", guilds_data)
