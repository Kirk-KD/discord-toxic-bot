import discord
import threading
from dotenv import load_dotenv
import os

from src.bot.toxic import Toxic
from src.control_panel.runner import run
from src.logger import logger

from src.bot.commands import (
    utilities,
    moderation,
    fun,
    game,
    dev
)

if __name__ == '__main__':
    logger.info("STARTING...")
    load_dotenv()

    token = os.getenv("TOKEN")
    intents = discord.Intents.all()
    client = Toxic(intents=intents)

    threading.Thread(target=run).start()
    client.run(token)
