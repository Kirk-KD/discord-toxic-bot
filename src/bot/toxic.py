from src.bot.handler import handler
from src.bot.data import *
from src.logger import logger
from src.bot.game.stocks_collection import stocks
from src.bot.tasks_collection import BackgroundTasksCollection

from src.bot.util.jsons import *
from src.bot.game.game_manager import manager

import discord
import traceback


class Toxic(discord.Client):
    """
    The Toxic bot!
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.tasks = BackgroundTasksCollection(self)

    async def on_ready(self):
        self.init_data()
        self.init_guilds()
        self.init_stocks()
        guilds_data.update_data()
        game_data.update_data()

        await self.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="_help to get help noobs"
            )
        )

        print('Logged in as {}'.format(self.user))
        logger.write_line("=" * 100)
        logger.log("LOGIN")

        await self.tasks.start_tasks()

    async def on_guild_join(self, guild: discord.Guild):
        if str(guild.id) not in guilds_data.data.keys():
            guilds_data.data[str(guild.id)] = guild_json_setup(guild)

        for member in guild.members:
            if member not in guilds_data.data[str(guild.id)]["members"].keys():
                guilds_data.data[str(guild.id)]["members"][str(member.id)] = member_json_setup()

            if not manager.get_player(member):
                game_data.data["players"][str(member.id)] = player_json_setup()

        guilds_data.update_data()
        game_data.update_data()

    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        if str(member.id) not in guilds_data.data[str(member.guild.id)]["members"].keys():
            guilds_data.data[str(member.guild.id)]["members"][str(member.id)] = member_json_setup()

        if not manager.get_player(member):
            game_data.data[str(member.id)] = player_json_setup()

        guilds_data.update_data()
        game_data.update_data()

    async def on_message(self, message: discord.Message):
        if not self.is_ready() or message.author.bot or type(message.channel) is not discord.TextChannel:
            return

        msg = message.content.strip()
        if len(msg) > 1 and msg[0] == '_':
            await handler.handle(message, self)

    async def on_error(self, event, *args, **kwargs):
        if len(args) != 0:
            message = args[0]
            await message.reply("Hey uhh you broke me. Congrats. Error info has been recorded.")
            logger.log("ERROR", "Error caused by \"{}\" when using command \"{}\". Error message:\n{}".format(
                message.author, message.content, traceback.format_exc()
            ))
        else:
            logger.log("ERROR", "Error occurred outside command usage. Error message:\n{}".format(
                traceback.format_exc()
            ))

        traceback.print_exc()

    def init_data(self):
        if "stocks" not in game_data.data.keys():
            game_data.data["stocks"] = {
                "Toxic": [],
                "Acid": [],
                "xD Coffee": [],
                "Roll of Rick": [],
                "Guthib Dog": []
            }
        if "players" not in game_data.data.keys():
            game_data.data["players"] = {}

    def init_guilds(self):
        for guild in self.guilds:
            if str(guild.id) not in guilds_data.data.keys():
                guilds_data.data[str(guild.id)] = guild_json_setup(guild)

            for member in guild.members:
                if member.bot:
                    continue

                if str(member.id) not in guilds_data.data[str(guild.id)]["members"].keys():
                    guilds_data.data[str(guild.id)]["members"][str(member.id)] = member_json_setup()

                if not manager.get_player(member):
                    game_data.data["players"][str(member.id)] = player_json_setup()

        guilds_data.update_data()
        game_data.update_data()

    def init_stocks(self):
        stocks.update()
        game_data.update_data()
