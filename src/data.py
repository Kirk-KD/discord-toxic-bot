"""
stores data read from json files
"""

from src.util.jsons import *


class Data:
    def __init__(self, path: str):
        self.path = path
        self.data = read_json(self.path)

    def set_data(self, path: str, val):
        keys = path.split("/")
        d = self.data
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = val

    def get_data(self, path: str):
        keys = path.split("/")
        c = self.data
        for key in keys:
            c = c[key]

        return c

    def update_data(self):
        write_json("saved_data/guilds.json", self.data)


# load data
guilds_data = Data("saved_data/guilds.json")
