import asyncio

import discord

from src.data import guilds_data
from src.game.stocks_collection import stocks


class BackgroundTasksCollection:
    def __init__(self, client: discord.Client):
        self.client = client

    async def start_tasks(self):
        for name in dir(self):
            if name.startswith("task_"):
                self.client.loop.create_task(await getattr(self, name)())

    # tasks
    async def task_update_stocks(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            await asyncio.sleep(60 * 30)
            stocks.update()

    # async def task_time_check(self):
    #     await self.client.wait_until_ready()
    #     while not self.client.is_closed():
    #         await asyncio.sleep(1)
    #
    #         for guild in guilds_data.data.values():
    #             if guild["initialised"]:
    #                 for member in guild["members"].values():
    #                     pass
