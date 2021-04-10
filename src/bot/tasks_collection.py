import asyncio
import datetime

import discord

from src.bot.data import guilds_data, game_data
from src.bot.game.stocks_collection import stocks
from src.bot.util.time import string_to_datetime


class BackgroundTasksCollection:
    def __init__(self, client: discord.Client):
        self.client = client

    async def start_tasks(self):
        for name in dir(self):
            if name.startswith("task_"):
                self.client.loop.create_task(await getattr(self, name)())

    def check_timer(self, member_data: dict, key: str):
        """
        checks if a timer is done in a member data.

        :param member_data: dict
        :param key: str
        :return: bool
        """

        return member_data["timers"][key] and string_to_datetime(member_data["timers"][key]) <= datetime.datetime.now()

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

            for guild in guilds_data.all():
                if guild["data"]["initialised"]:
                    for member_id, member in guild["data"]["members"].items():
                        if member["muted"] and string_to_datetime(member["timers"]["mute"]) <= datetime.datetime.now():
                            member["muted"] = False
                            member["timers"]["mute"] = None

                            g = discord.utils.get(self.client.guilds, id=int(guild["_id"]))
                            m = discord.utils.get(g.members, id=int(member_id))

                            if g and m:
                                muted_role = discord.utils.get(g.roles, name="Muted")
                                if muted_role and muted_role in m.roles:
                                    await m.remove_roles(muted_role)

                        if member["banned"] and self.check_timer(member, "ban"):
                            member["banned"] = False
                            member["timers"]["ban"] = None

                            g = discord.utils.get(self.client.guilds, id=int(guild["_id"]))
                            user = await self.client.fetch_user(int(member_id))

                            if g and user:
                                await g.unban(user)

                    guilds_data.set(guild["_id"], guild)

            for member in game_data.all():
                for effect in member["data"]["effects"]:
                    if effect["end_time"] and string_to_datetime(effect["end_time"]) <= datetime.datetime.now():
                        member["data"]["effects"].remove(effect)
                        game_data.set(member["_id"], member)
