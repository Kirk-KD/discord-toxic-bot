from src.data import game_data
from src.game import player, item

import asyncio


class Effect:
    def __init__(self, duration: int, buff_data: dict[str, int]):
        self.duration = duration
        self.buff_data = buff_data

    def start(self, player_: player.Player, item_: item.Item):
        for key, val in self.buff_data.items():
            player_.data["stats"][key] += val

        player_.data["effects"].append(item_.display_name)
        game_data.update_data()

        asyncio.sleep(self.duration)

        for key, val in self.buff_data.items():
            player_.data["stats"][key] -= val
        player_.data["effects"].remove(item_.display_name)
        game_data.update_data()
