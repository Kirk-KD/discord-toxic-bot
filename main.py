"""
the bot starts running from here!
"""

from src.commands import (
    utilities,
    moderation,
    fun
)

from src.command_handler import handler
from src.data import *

from src.util.jsons import *

from dotenv import load_dotenv
import os
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

        for guild in client.guilds:
            guilds_data[str(guild.id)] = (
                guilds_data[str(guild.id)]
                if str(guild.id) in guilds_data.keys()
                else guild_json_setup(guild)
            )
        update_data()

        print('Logged in as {}'.format(self.user))

    async def on_guild_join(self, guild: discord.Guild):  # TODO: TEST
        """
        called when client joins a new guild

        :param guild: Guild
        :return: None
        """

        guilds_data[str(guild.id)] = (
            guilds_data[str(guild.id)]
            if str(guild.id) in guilds_data.keys()
            else guild_json_setup(guild)
        )
        update_data()

    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        if str(member.id) not in guilds_data[str(member.guild.id)]["members"].keys():
            guilds_data[str(member.guild.id)]["members"][str(member.id)] = member_json_setup()
            update_data()

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


# load env
load_dotenv()

# login
intents = discord.Intents.all()
client = Toxic(intents=intents)
client.run(os.getenv('TOKEN'))
