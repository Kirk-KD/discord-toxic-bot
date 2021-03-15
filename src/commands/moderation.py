"""
commands under category "Moderation"
"""

import asyncio
import discord

from src.command_handler import handler
from src.perms import *
from src.data import *


@handler.add(["shutup"], perm=MODS)
async def mute(message, args, client):
    """mutes a user"""

    if len(args) < 1:
        await message.reply(
            "Dude at least tell me who to mute? "
            "Are you just messing with me because I'm a bot? That's racist man. Not cool.",
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

    muted_role = await make_muted_role(message)
    if not muted_role:
        return

    if muted_role in member.roles:
        await message.reply("That guy is already muted lol.", mention_author=False)
        return

    await member.add_roles(muted_role)

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
        name="Reason", value="`{}`".format(reason)
    ).set_author(
        name=member.name,
        icon_url=member.avatar_url
    ).set_footer(
        text="Muted by {}".format(
            signature(message.author)
        )
    )
    await message.reply(embed=embed, mention_author=False)

    # add infraction
    get_data("{}/members/{}/infractions".format(
        message.guild.id, member.id
    )).append(
        infraction_json_setup("Mute", reason, datetime.datetime.now())
    )
    update_data()

    await asyncio.sleep(time.seconds)
    await member.remove_roles(muted_role)


@handler.add(perm=MODS)
async def unmute(message, args, client):
    if len(args) < 1:
        await message.reply("Are you gonna tell me who to unmute or not???", mention_author=False)
        return

    member = parse_member(message.guild, args[0])
    muted_role = await make_muted_role(message)

    if not muted_role:
        return
    if not member:
        await message.reply("*sigh* give me a valid user ID or mention.", mention_author=False)
        return
    if muted_role not in member.roles:
        await message.reply(
            "Fun fact: you can't unmute someone that isn't muted. Bet you didn't know this.", mention_author=False
        )
        return

    await member.remove_roles(muted_role)
    embed = discord.Embed(
        title="Unmute",
        description="{} was unmuted!".format(member.mention),
        color=discord.Color.green()
    ).set_author(
        name=member.name,
        icon_url=member.avatar_url
    ).set_footer(
        text="Unmuted by {}".format(
            signature(message.author)
        )
    )
    await message.reply(embed=embed, mention_author=False)


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
        title="Warn",
        description="{} was warned!".format(
            warn_member.mention, warn_reason
        ),
        color=discord.Color.orange()
    ).add_field(
        name="Reason",
        value="`{}`".format(warn_reason)
    ).set_author(
        name=warn_member.name, icon_url=warn_member.avatar_url
    ).set_footer(
        text="Warned by {}".format(
            signature(message.author)
        )
    )
    await message.reply(embed=embed_msg, mention_author=False)

    # add infraction
    get_data("{}/members/{}/infractions".format(
        message.guild.id, warn_member.id
    )).append(
        infraction_json_setup("Mute", warn_reason, datetime.datetime.now())
    )
    update_data()


@handler.add(perm=OWNERS)
async def kick(message, args, client):
    if len(args) < 1:
        await message.reply("Who do I kick? You?", mention_author=False)

    member = parse_member(message.guild, args[0])
    reason = " ".join(args[1:]) if len(args) > 1 else "None given"

    if not member:
        await message.reply("Come on man give me a valid user.", mention_author=False)
        return

    await member.kick(reason=reason)
    embed = discord.Embed(
        title="Kick",
        description="{} was kicked!".format(
            member.mention
        ),
        color=discord.Color.red()
    ).add_field(
        name="Reason",
        value="`{}`".format(reason)
    ).set_footer(
        text="Kicked by {}".format(
            signature(message.author)
        )
    ).set_author(
        name=member.name,
        icon_url=member.avatar_url
    )
    await message.reply(embed=embed, mention_author=False)

    embed = discord.Embed(
        title="You were kicked from {}".format(
            member.guild.name
        ),
        description="You can't join back until you get an invite LMAOOO",
        color=discord.Color.red()
    ).add_field(
        name="Reason",
        value="`{}`".format(reason)
    ).set_footer(
        text="Kicked by {}".format(
            signature(message.author)
        )
    ).set_thumbnail(
        url=message.guild.icon_url
    )
    await member.send(embed=embed)

# TODO: ADD BAN COMMAND
