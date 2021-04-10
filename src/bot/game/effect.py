from src.bot.data import game_data

import asyncio


class Effect:
    def __init__(self, duration: int, buff_data: dict[str, int]):
        self.duration = duration
        self.buff_data = buff_data

    async def start(self, player, item):
        pass  # TODO
