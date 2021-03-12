"""
the bot starts running from here!
"""

from src.commands.utilities import *

from src.command_handler import handler
from src.data import *
from src.util import *

from dotenv import load_dotenv


class Toxic(discord.Client):
    """
    The Toxic bot!
    """

    async def on_ready(self):
        """
        called when the bot is online and read

        :return: None
        """

        for guild in client.guilds:
            guilds_data[str(guild.id)] = (guilds_data[str(guild.id)]
                                          if str(guild.id) in guilds_data.keys()
                                          else guild_json_setup(guild))

        update_guilds_data()

        print('Logged in as {}'.format(self.user))

    async def on_message(self, message: discord.Message):
        """
        called when a message is sent by a user

        :param message: Message
        :return: None
        """

        if message.author.bot:
            return

        msg = message.content.strip()
        if len(msg) > 1 and msg[0] == '_':
            await handler.handle(message, self)


# loads env
load_dotenv()

# login
client = Toxic()
client.run(os.getenv('TOKEN'))
