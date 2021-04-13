import datetime
import asyncio

from src.bot.data import game_data


class Effect:
    def __init__(self, duration: int or None, buff_data: dict[str, int]):
        self.duration = duration
        self.buff_data = buff_data

    async def start(self, player, item):
        player.data["effects"].append({
            "item": item.display_name,
            "end_time": str(datetime.datetime.now() + datetime.timedelta(0, self.duration)),
            "stats": self.buff_data
        })
        for stat, val in self.buff_data.items():
            player.data["stats"][stat] += val
