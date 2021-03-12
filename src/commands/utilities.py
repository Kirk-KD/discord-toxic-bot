from src.command_handler import handler
from src.util import *
from src.perms import *


@handler.add(["testing"], perm=NORMAL)
async def test(message, args):
    await message.reply("Im working alright lmao | args={}".format(args))


@handler.add(["delete"], perm=OWNERS)
async def clear(message, args):
    num = parse_int(args[0])
    if len(args) == 0 or num is None:
        await message.reply("Dude u need to tell me how many messages to delete lol")
        return

    if num <= 0:
        await message.reply("Trying to break me huh? Try to delete {} messages yourself".format(num))
        return

    deleted = await message.channel.purge(limit=num)
    if len(deleted) <= 3:
        await message.channel.send(
            "{} fine, deleted. Its just {} messages cant you do it yourself you lazy bum??".format(
                message.author.mention, len(deleted)
            )
        )
        return

    await message.channel.send("{} Alright, {} messages deleted.".format(message.author.mention, len(deleted)))


@handler.add(["slow", "sm"], perm=OWNERS)
async def slowmode(message, args):
    if len(args) == 0 or not (parse_int(args[0]) or parse_bool(args[0]) is False):
        await message.reply(
            "Ayo gotta tell me how long in seconds you want the slowmode to be or \"off\" to turn it off"
        )
        return

    amount = parse_int(args[0]) if parse_int(args[0]) is not None else 0

    if amount < 0:
        await message.reply(
            "Ahh I see that you are not very familiar with time? A delay cannot be negative. You are welcome."
        )
        return

    await message.reply(
        "Slowmode set to {} seconds. Now suffer from the slowness!".format(amount) if amount != 0
        else ("Slowmode is now off." if message.channel.slowmode_delay != 0 else "Slowmode was already off you nerd.")
    )

    message.channel.slowmode_delay = amount


# TODO: ADD SETUP COMMAND FOR OWNER
# TODO: ADD BAN, KICK, WARN
