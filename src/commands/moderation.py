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
    """mutes a user"""

    if len(args) == 0:
        await message.reply(
            "Ummm hello??? Don't you think you need to tell me who to mute?"
            "Are you telling me to shut up??? Should I mute you???",
            mention_author=False
        )
        return
    mute_member_id = args[0]
    mute_time = None if len(args) < 2 else args[1]
    mute_reason = "None given" if len(args) < 3 else " ".join(args[2:])

    if not parse_member(message.guild, mute_member_id):
        await message.reply("I need a valid user ID as the first argument bro.", mention_author=False)
        return

    if not mute_time or not parse_time(mute_time):
        await message.reply("You need to tell me how long to mute, e.g. 10d5h30m20s", mention_author=False)
        return

    role = get(message.guild.roles, id=int(guilds_data[str(message.guild.id)]["settings"]["perm_ids"]["muted"]))
    mute_member = parse_member(message.guild, mute_member_id)
    time = parse_time(mute_time)

    # TODO: ADD OWNER/MOD CHECK
    # TODO: BUG FIX: CANNOT MUTE MOD/OWNER

    if role in mute_member.roles:
        await message.reply("Hey that user has already been muted you forgetful idiot!", mention_author=False)
        return

    prev_roles = []
    for i in range(len(mute_member.roles)):  # is working. do not touch.
        if i == 0:
            continue
        prev_roles.append(mute_member.roles[i])
        await mute_member.remove_roles(get(message.guild.roles, id=mute_member.roles[i].id))
    await mute_member.add_roles(role)

    embed_msg = discord.Embed(
        title="Mute", description="{} is now muted for {}.".format(
            user_mention(str(mute_member.id)), mute_time
        ), color=discord.Color.light_gray()
    ).set_author(
        name=mute_member.name, icon_url=mute_member.avatar_url
    ).add_field(
        name="Muted Until", value="`{}`".format(format_time(datetime.datetime.now() + time)), inline=True
    ).add_field(
        name="Reason", value="`{}`".format(mute_reason)
    ).set_footer(
        text="Muted by {} ({}) • {}".format(
            message.author.display_name, message.author, format_time(datetime.datetime.now())
        )
    )
    await message.reply(embed=embed_msg, mention_author=False)

    await asyncio.sleep(time.seconds)
    await mute_member.remove_roles(role)
    for r in prev_roles:
        await mute_member.add_roles(r)


@handler.add(perm=MODS)
async def warn(message, args, client):
    """warns a user"""

    if len(args) == 0:
        await message.reply("Who do you want me to warn lol")
        return

    warn_member_id = args[0]
    warn_member = parse_member(message.guild, warn_member_id)
    warn_reason = "None given" if len(args) < 2 else " ".join(args[1:])

    if not warn_member:
        await message.reply("Gotta give me a valid user ID to warn tho.")
        return

    embed_msg = discord.Embed(
        title="Warn", description="{} was warned! Reason: `{}`".format(
            user_mention(warn_member.id), warn_reason
        ), color=discord.Color.orange()
    ).set_author(
        name=warn_member.name, icon_url=warn_member.avatar_url
    ).set_footer(
        text="Warned by {} ({}) • {}".format(
            message.author.display_name, message.author, format_time(datetime.datetime.now())
        )
    )
    await message.reply(embed=embed_msg, mention_author=False)

    # TODO: IMPLEMENT INFRACTION SYSTEM

# TODO: ADD BAN AND KICK COMMAND
