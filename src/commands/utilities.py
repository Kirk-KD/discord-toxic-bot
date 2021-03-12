"""
commands under category "Utilities"
"""

from src.command_handler import handler
from src.perms import *
from src.data import *


@handler.add(["testing"], perm=EVERYONE)
async def test(message, args, client):
    """a simple testing command that serves no purpose"""

    await message.reply("Im working alright lmao **| args={} | client={}**".format(args, client))
    print(args)


@handler.add(["delete"], perm=OWNERS)
async def clear(message, args, client):
    """deletes n amount of messages"""

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
async def slowmode(message, args, client):
    """sets slowmode of a channel"""

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


@handler.add(["init", "initialise"], perm=OWNERS)
async def setup(message, args, client):
    """setup command! setup process will be in the owner's DM"""

    if guilds_data[str(message.author.guild.id)]["initialised"]:
        await message.reply("yo your server was already initialised lol")
        return

    await message.reply("Alrighty i'll be waiting for you in your dm")

    async def fail():
        await message.author.send(
            "One or more role IDs you provided is not found or invalid ¯\\_(ツ)_/¯\n"
            "Now you have to restart LMAO. Not sorry, your fault."
        )

    async def get_ids(msg):
        reply = (await dm_input(
            message, msg, client
        )).strip()
        ids = reply.split()

        for i in range(len(ids)):
            if not validate_role_id(message.author.guild, ids[i]):
                await fail()
                return None

            ids[i] = parse_int(ids[i])

        return ids

    # get role IDs for owners
    owner_ids = await get_ids(
        "Let's get started then! First we need to set up some roles for Owners, Mods, and Users.\n "
        "What are the roles for the **owners**? Paste their role ID(s) here and separate them with spaces\n"
        "(they are the ones that can use ban, kick, slowmode, and use every other commands)"
    )
    if not owner_ids:
        return

    # get role IDs for mods
    mod_ids = await get_ids(
        "Okok and what are the roles for the **mods**? Paste their role ID(s) here and separate them with spaces\n"
        "(they are the ones that can use mute, warn and use every other commands except for the owner ones)"
    )
    if not mod_ids:
        return

    # get role IDs for users
    user_ids = await get_ids(
        "Noted. Now what are the roles for the **users**? Paste their role ID(s) here and separate them with spaces\n"
        "(they are the ones that have no power, but can use all other bot commands)"
    )
    if not user_ids:
        return

    # get muted role ID
    mute_id = parse_int((await dm_input(
        message, "Alright. Now, there are always spammers, so what is the **muted** role ID?", client
    )).strip().split()[0])

    if not mute_id:
        await message.author.send(
            "The role ID you provided is not found or invalid ¯\\_(ツ)_/¯\n"
            "Now you have to restart LMAO. Not sorry, your fault."
        )
        return

    # save settings
    role_ids = guilds_data[str(message.author.guild.id)]["settings"]["perm_ids"]
    role_ids["owner"] = owner_ids
    role_ids["mod"] = mod_ids
    role_ids["user"] = user_ids
    role_ids["muted"] = mute_id
    guilds_data[str(message.author.guild.id)]["initialised"] = True
    update_guilds_data()

    await message.author.send("**Setup complete!** You can now enjoy making me serve you like a slave. YAY!")
