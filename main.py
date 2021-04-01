from src.toxic import Toxic
from src.commands import (
    utilities,
    moderation,
    fun,
    game
)

import discord
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()

    token = os.getenv("TOKEN")
    intents = discord.Intents.all()
    client = Toxic(intents=intents)

    client.run(token)
