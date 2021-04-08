from src.bot.data import game_data
from src.bot.game import player

import discord


class GameManager:
    def __init__(self):
        pass

    def get_player(self, member: discord.Member):
        if str(member.id) in game_data.data["players"].keys():
            return player.Player(member)

        return None


manager = GameManager()
