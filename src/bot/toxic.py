import datetime
import discord
from discord.ext import tasks
from discord_components import DiscordComponents
import traceback

from src.bot.game.stocks_collection import stocks
from src.bot.handler import handler
from src.bot.data import guilds_data, game_data, stocks_data
from src.logger import logger, Timer
from src.util.jsons import guild_json_setup, member_json_setup, player_json_setup
from src.util.time import string_to_datetime


class Toxic(discord.Client):
    """
    The Toxic bot!
    """

    def __init__(self, **options):
        super().__init__(**options)

    # events
    async def on_connect(self):
        logger.info("INITIALISING DATABASE...")

        timer = Timer()
        self.init_guilds()
        self.init_stocks()
        logger.timed(timer, "DB Initialization")

    async def on_ready(self):
        DiscordComponents(self)

        await self.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="WARNING: TESTING MODE"
            )
        )

        self.task_update_stocks.start()
        self.task_timer_check.start()
        self.task_streak_check.start()

        logger.info("CLIENT LOGIN")

    async def on_guild_join(self, guild: discord.Guild):
        if not guilds_data.get(guild.id):
            guilds_data.add(guild.id, {"data": guild_json_setup(guild)})

        for member in guild.members:
            if member.bot:
                continue

            g_data = guilds_data.get(guild.id)
            if str(member.id) not in g_data["members"].keys():
                g_data["members"][str(member.id)] = member_json_setup()
            guilds_data.set(guild.id, {"data": g_data})

            if not game_data.get(member.id):
                game_data.add(member.id, {"data": player_json_setup()})

    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        guild = member.guild
        g_data = guilds_data.get(guild.id)
        if str(member.id) not in g_data["members"].keys():
            g_data["members"][str(member.id)] = member_json_setup()
        guilds_data.set(guild.id, {"data": g_data})

        if not game_data.get(member.id):
            game_data.add(member.id, {"data": player_json_setup()})

    async def on_message(self, message: discord.Message):
        if message.author.bot or not isinstance(message.channel, discord.TextChannel) or not self.is_ready():
            return

        msg = message.content.strip()
        if len(msg) > 1 and msg[0] == '_':
            await handler.handle(message, self)

    async def on_error(self, event, *args, **kwargs):
        try:
            if len(args) != 0:
                message = args[0]
                await message.reply("Hey uhh you broke me. Congrats. Error info has been recorded.")
                logger.error(
                    "Error caused by \"{}\" in guild \"{}\" (ID={}) when using command \"{}\". "
                    "Error message:\n{}".format(
                        message.author, message.guild.name, message.guild.id,
                        message.content, traceback.format_exc()
                    ))
            else:
                logger.error("Error occurred outside command usage. Error message:\n{}".format(
                    traceback.format_exc()
                ))
        except discord.Forbidden:  # bot cannot send messages
            pass

    # tasks
    @tasks.loop(hours=1)
    async def task_update_stocks(self):
        stocks.update()

    @tasks.loop(seconds=2)
    async def task_timer_check(self):
        def check_timer(member_data: dict, key: str):
            return (member_data["timers"][key] and
                    string_to_datetime(member_data["timers"][key]) <= datetime.datetime.now())

        for guild in guilds_data.all():
            if guild["data"]["initialised"]:
                for member_id, member in guild["data"]["members"].items():
                    if member["muted"] and check_timer(member, "mute"):
                        member["muted"] = False
                        member["timers"]["mute"] = None

                        g = discord.utils.get(self.guilds, id=int(guild["_id"]))
                        m = discord.utils.get(g.members, id=int(member_id))

                        if g and m:
                            muted_role = discord.utils.get(g.roles, name="Muted")
                            if muted_role and muted_role in m.roles:
                                await m.remove_roles(muted_role)

                    if member["banned"] and check_timer(member, "ban"):
                        member["banned"] = False
                        member["timers"]["ban"] = None

                        g = discord.utils.get(self.guilds, id=int(guild["_id"]))
                        user = await self.fetch_user(int(member_id))

                        if g and user:
                            await g.unban(user)

                guilds_data.set(guild["_id"], guild)

        for member in game_data.all():
            for effect in member["data"]["effects"]:
                if effect["end_time"] and string_to_datetime(effect["end_time"]) <= datetime.datetime.now():
                    member["data"]["effects"].remove(effect)
                    game_data.set(member["_id"], member)

    @tasks.loop(seconds=30)
    async def task_streak_check(self):
        for player in game_data.all():
            d = player["data"]

            if (t := d["timers"]["streak"]) is not None and string_to_datetime(t) <= datetime.datetime.now():
                d["timers"]["streak"] = None
                game_data.set(player["_id"], {"data": d})

    # helpers
    def init_guilds(self):
        for guild in self.guilds:
            if not guilds_data.get(guild.id):
                guilds_data.add(guild.id, {"data": guild_json_setup(guild)})

            for member in guild.members:
                if member.bot:
                    continue

                g_data = guilds_data.get(guild.id)
                if str(member.id) not in g_data["members"].keys():
                    g_data["members"][str(member.id)] = member_json_setup()
                guilds_data.set(guild.id, {"data": g_data})

                if not game_data.get(member.id):
                    game_data.add(member.id, {"data": player_json_setup()})

    def init_stocks(self):
        if stocks_data.all().count() == 0:
            stock_names = ["Toxic", "Acid", "xD Coffee", "Roll of Rick", "Guthib Dog"]
            for name in stock_names:
                if not stocks_data.get(name):
                    stocks_data.add(name, {"data": []})

            stocks.update()
