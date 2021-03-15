"""
commands under category "Moderation"
"""

import asyncio
import discord
from discord.utils import get

from src.command_handler import handler
from src.perms import *
from src.data import *


@handler.add(["shutup"], perm=MODS)
async def mute(message, args, client):
    """mutes a user"""

    if len(args) < 1:
        await message.reply(
            "At least tell me who to mute man. "
            "Are you just playing with me because I'm a bot?",
            mention_author=False
        )
        return

    if len(args) < 2:
        await message.reply("Gotta tell me how long to mute tho.", mention_author=False)
        return

    member = parse_member(message.guild, args[0])
    time = parse_time(args[1])
    reason = " ".join(args[2:]) if len(args) > 2 else "None given"

    if not member:
        await message.reply("I need a valid user ID as the first argument lol.", mention_author=False)
        return

    if not time:
        await message.reply("Dude give me a valid time (eg 2d12h30m15s) as second argument.", mention_author=False)
        return

    embed = discord.Embed(
        title="Mute",
        description="{} was muted for `{}`! Yeah just shutup LMAOOO".format(
            member.mention, args[1].lower()
        ),
        color=discord.Color.light_gray()
    ).add_field(
        name="Muted until", value="`{}`".format(
            format_time(datetime.datetime.now() + time)
        )
    ).add_field(
        name="Reason", value=reason
    )
    await message.reply(embed=embed, mention_author=False)

    # TODO: CHANGE TO ROLE BASED MUTE SYSTEM
    set_data("{}/members/{}/muted".format(
        message.guild.id, member.id
    ), True)
    get_data("{}/members/{}/infractions".format(
        message.guild.id, member.id
    )).append(
        infraction_json_setup("Mute", reason, datetime.datetime.now() + time)
    )
    update_data()


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
            message.author.display_name, message.author, timestamp()
        )
    )
    await message.reply(embed=embed_msg, mention_author=False)

    # TODO: INFRACTION

# TODO: ADD BAN AND KICK COMMAND
