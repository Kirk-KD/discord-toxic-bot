from src.handler import handler
from src.data import *
from src.logger import logger

from src.util.jsons import *
from src.game.game_manager import manager

import discord
import traceback


class Toxic(discord.Client):
    """
    The Toxic bot!
    """

    async def on_ready(self):
        await self.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="_help to get help noobs"
            )
        )

        self.init_guilds()
        guilds_data.update_data()
        game_data.update_data()

        print('Logged in as {}'.format(self.user))
        logger.write_line("=" * 100)
        logger.log("LOGIN")

    async def on_guild_join(self, guild: discord.Guild):
        if str(guild.id) not in guilds_data.data.keys():
            guilds_data.data[str(guild.id)] = guild_json_setup(guild)

        for member in guild.members:
            if member not in guilds_data.data[str(guild.id)]["members"].keys():
                guilds_data.data[str(guild.id)]["members"][str(member.id)] = member_json_setup()

            if not manager.get_player(member):
                game_data.data[str(member.id)] = player_json_setup()

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
        if message.author.bot or type(message.channel) is not discord.TextChannel:
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
                    game_data.data[str(member.id)] = player_json_setup()

                game_data.data[str(member.id)]["effects"] = []  # needs to find a better way later

        guilds_data.update_data()
        game_data.update_data()
