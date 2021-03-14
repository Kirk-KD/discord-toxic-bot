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

    # TODO: IMPLEMENT


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
