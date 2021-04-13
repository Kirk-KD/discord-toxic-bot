import discord
import traceback

from src.bot.handler import handler
from src.bot.data import guilds_data, game_data, stocks_data
from src.bot.tasks_collection import BackgroundTasksCollection
from src.logger import logger
from src.util.jsons import guild_json_setup, member_json_setup, player_json_setup


class Toxic(discord.Client):
    """
    The Toxic bot!
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.tasks = BackgroundTasksCollection(self)

    async def on_ready(self):
        logger.info("INITIALISING DATABASE...")
        self.init_guilds()
        self.init_stocks()

        await self.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="_help to get help noobs"
            )
        )

        print('Logged in as {}'.format(self.user))
        logger.write_line("=" * 100)
        logger.info("CLIENT LOGIN")

        await self.tasks.start_tasks()

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
        if not self.is_ready() or message.author.bot or type(message.channel) is not discord.TextChannel:
            return

        msg = message.content.strip()
        if len(msg) > 1 and msg[0] == '_':
            await handler.handle(message, self)

    async def on_error(self, event, *args, **kwargs):
        if len(args) != 0:
            message = args[0]
            await message.reply("Hey uhh you broke me. Congrats. Error info has been recorded.")
            logger.error("Error caused by \"{}\" when using command \"{}\". Error message:\n{}".format(
                message.author, message.content, traceback.format_exc()
            ))
        else:
            logger.error("Error occurred outside command usage. Error message:\n{}".format(
                traceback.format_exc()
            ))

        traceback.print_exc()

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
