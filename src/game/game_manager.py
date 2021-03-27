from src.data import game_data
from src.game import player

import discord


class GameManager:
    def __init__(self):
        pass

    def get_player(self, member: discord.Member):
        if str(member.id) in game_data.data.keys():
            return player.Player(member)

        raise KeyError("Player not registered in game_data!")  # shouldn't reach here


manager = GameManager()
