from src.bot.toxic import Toxic
from src.control_panel.runner import run
from src.bot.commands import (
    utilities,
    moderation,
    fun,
    game,
    dev
)

import discord
import threading
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()

    token = os.getenv("TOKEN")
    intents = discord.Intents.all()
    client = Toxic(intents=intents)

    threading.Thread(target=run).start()
    client.run(token)
