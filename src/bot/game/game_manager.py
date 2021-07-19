import discord

from src.bot.game.player import Player


class GameManager:
    def __init__(self):
        pass

    async def get_player(self, member: discord.Member):
        p = Player(member)
        await p.set_data()

        return p


manager = GameManager()
