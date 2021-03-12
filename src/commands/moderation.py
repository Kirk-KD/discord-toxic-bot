"""
commands under category "Moderation"
"""

import asyncio
from discord.utils import get

from src.command_handler import handler
from src.perms import *
from src.data import *


@handler.add(["shutup"], perm=MODS)
async def mute(message, args, client):
    if len(args) == 0:
        await message.reply(
            "Ummm hello??? Don't you think you need to tell me who to mute?"
            "Are you telling me to shut up??? Should I mute you???"
        )
        return
    mute_member = args[0]
    mute_time = None if len(args) < 2 else args[1]
    mute_reason = "None given" if len(args) < 3 else " ".join(args[2:])

    if not parse_member(message.guild, mute_member):
        await message.reply("I need a valid user ID as the first argument bro.")
        return

    if not mute_time or not parse_time(mute_time):
        await message.reply("You need to tell me how long to mute, e.g. 10d5h30m20s")
        return

    role = get(message.guild.roles, id=int(guilds_data[str(message.guild.id)]["settings"]["perm_ids"]["muted"]))
    member = parse_member(message.guild, mute_member)
    time = parse_time(mute_time)

    prev_roles = []
    for i in range(len(member.roles)):  # is working. do not touch
        if i == 0:
            continue
        prev_roles.append(member.roles[i])
        await member.remove_roles(get(message.guild.roles, id=member.roles[i].id))
    await member.add_roles(role)

    await message.reply("<@!{}> is now muted until {} lol. Reason: `{}`. Take that spammers!".format(
        member.id, str(datetime.datetime.now() + time).split(".")[0], mute_reason)
    )

    await asyncio.sleep(time.seconds)
    await member.remove_roles(role)
    for r in prev_roles:
        await member.add_roles(r)
