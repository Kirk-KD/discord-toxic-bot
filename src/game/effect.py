from src.data import game_data

import asyncio


class Effect:
    def __init__(self, duration: int, buff_data: dict[str, int]):
        self.duration = duration
        self.buff_data = buff_data

    async def start(self, player, item):
        """
        starts the effect on player.

        :param player: Player
        :param item: Item
        :return: None
        """

        for key, val in self.buff_data.items():
            player.data["stats"][key] += val

        player.data["effects"].append(item.display_name)
        game_data.update_data()

        await asyncio.sleep(self.duration)

        for key, val in self.buff_data.items():
            player.data["stats"][key] -= val
        player.data["effects"].remove(item.display_name)
        game_data.update_data()
