from src.handler import handler
from src.data import *

from src.util.jsons import *
from src.game.game_manager import manager

import discord


class Toxic(discord.Client):
    """
    The Toxic bot!
    """

    async def on_ready(self):
        """
        called when the bot is online and ready

        :return: None
        """

        self.init_guilds()

        print('Logged in as {}'.format(self.user))

    async def on_guild_join(self, guild: discord.Guild):
        """
        called when client joins a new guild

        :param guild: Guild
        :return: None
        """

        self.init_single_guild(guild)

    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        if str(member.id) not in guilds_data.get_data("{}/members".format(str(member.guild.id))).keys():
            guilds_data.set_data("{}/members/{}".format(
                str(member.guild.id), str(member.id)
            ), member_json_setup())
            guilds_data.update_data()

        if not manager.get_player(member):
            game_data.data[str(member.id)] = player_json_setup()

    async def on_message(self, message: discord.Message):
        """
        called when a message is sent by a user

        :param message: Message
        :return: None
        """

        if message.author.bot or type(message.channel) is not discord.TextChannel:
            return

        msg = message.content.strip()
        if len(msg) > 1 and msg[0] == '_':
            await handler.handle(message, self)

    def init_single_guild(self, guild):
        guilds_data.set_data(
            str(guild.id), (
                guilds_data.get_data(str(guild.id))
                if str(guild.id) in guilds_data.data.keys()
                else guild_json_setup(guild)
            )
        )
        guilds_data.update_data()

        for member in guild.members:
            if str(member.id) not in game_data.data.keys():
                game_data.set_data(
                    str(member.id), player_json_setup()
                )

    def init_guilds(self):
        for guild in self.guilds:
            self.init_single_guild(guild)

            for member in guild.members:
                if member.bot:
                    continue

                if str(member.id) not in game_data.data.keys():
                    game_data.set_data(
                        str(member.id), player_json_setup()
                    )

        game_data.update_data()
