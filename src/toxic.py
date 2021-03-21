from src.handler import handler
from src.data import *
from src.util.jsons import *

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

        for guild in self.guilds:
            guilds_data.set_data(str(guild.id), (
                guilds_data.get_data(str(guild.id))
                if str(guild.id) in guilds_data.data.keys()
                else guild_json_setup(guild)
            ))
        guilds_data.update_data()

        print('Logged in as {}'.format(self.user))

    async def on_guild_join(self, guild: discord.Guild):
        """
        called when client joins a new guild

        :param guild: Guild
        :return: None
        """

        guilds_data.set_data(
            str(guild.id), (
                guilds_data.get_data(str(guild.id))
                if str(guild.id) in guilds_data.data.keys()
                else guild_json_setup(guild)
            )
        )
        guilds_data.update_data()

    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        if str(member.id) not in guilds_data.get_data("{}/members".format(str(member.guild.id))).keys():
            guilds_data.set_data("{}/members/{}".format(
                str(member.guild.id), str(member.id)
            ), member_json_setup())
            guilds_data.update_data()

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
