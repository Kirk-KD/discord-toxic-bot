import asyncio
import datetime

import discord

from src.data import guilds_data
from src.game.stocks_collection import stocks
from src.util.time import string_to_datetime


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

    async def task_timer_check(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            await asyncio.sleep(1)

            for guild_id, guild in guilds_data.data.items():
                if guild["initialised"]:
                    for member_id, member in guild["members"].items():
                        if member["muted"] and string_to_datetime(member["timers"]["mute"]) <= datetime.datetime.now():
                            member["muted"] = False
                            member["timers"]["mute"] = None

                            g = discord.utils.get(self.client.guilds, id=int(guild_id))
                            m = discord.utils.get(g.members, id=int(member_id))

                            if g and m:
                                muted_role = discord.utils.get(g.roles, name="Muted")
                                if muted_role and muted_role in m.roles:
                                    await m.remove_roles(muted_role)

                        if member["banned"] and self.check_timer(member, "ban"):
                            member["banned"] = False
                            member["timers"]["ban"] = None

                            g = discord.utils.get(self.client.guilds, id=int(guild_id))
                            user = await self.client.fetch_user(int(member_id))

                            if g and user:
                                await g.unban(user)

            guilds_data.update_data()

    def check_timer(self, member_data: dict, key: str):
        """
        checks if a timer is done in a member data.

        :param member_data: dict
        :param key: str
        :return: bool
        """

        return member_data["timers"][key] and string_to_datetime(member_data["timers"][key]) <= datetime.datetime.now()
