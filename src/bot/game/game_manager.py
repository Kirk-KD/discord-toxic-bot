import discord

from src.bot.game import player


class GameManager:
    def __init__(self):
        pass

    def get_player(self, member: discord.Member):
        return player.Player(member)


manager = GameManager()
