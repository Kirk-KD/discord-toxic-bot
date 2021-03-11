from .command_handler import CommandHandler
from .util import *

handler = CommandHandler()


@handler.add(["testing"])
async def test(message, args):
    await message.reply("Im working alright lmaoooo | args={}".format(args))


@handler.add(["delete"])
async def clear(message, args):
    if len(args) == 0 or not is_int(args[0]):
        await message.reply("Dude u need to tell me how many messages to delete lol")
        return

    num = int(args[0])
    deleted = await message.channel.purge(limit=num)

    if len(deleted) <= 3:
        await message.channel.send(
            "{} fine, deleted. Its just {} messages cant you do it yourself you lazy bum??".format(
                message.author.mention, len(deleted)
            )
        )
        return

    await message.channel.send("{} Alllllllright, {} messages deleted.".format(message.author.mention, len(deleted)))
