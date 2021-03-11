import discord
import os
from dotenv import load_dotenv

from src.commands import handler

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as {}'.format(client.user))


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    msg = message.content.strip()
    if len(msg) > 1 and msg[0] == '_':
        await handler.handle(message)

client.run(os.getenv('TOKEN'))
