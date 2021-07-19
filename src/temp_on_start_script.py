# this script can be edited and ran before restarting the bot
# to fix small issues in the database or to do a complete data wipe.

from src.bot.data import game_data
import asyncio


async def main():
    print(await game_data.get(521347381636104212))

asyncio.run(main())

