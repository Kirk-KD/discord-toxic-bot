"""
commands under category "Moderation"
"""

import asyncio

from src.command_handler import handler
from src.perms import *
from src.data import *


@handler.add(
    ["shutup"], perm=MODS, usage="mute <mention|id> <time>|\"forever\" [<reason>]"
)
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

    if member.bot:
        await message.reply("You cannot mute a bot.", mention_author=False)
        return

    if not member:
        await message.reply("I need a valid user ID as the first argument lol.", mention_author=False)
        return
    if not time and args[1].lower() != "forever":
        await message.reply(
            "Dude give me a valid time (eg 2d12h30m15s) as second argument or `forever`.", mention_author=False
        )
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
        description="{} was muted! Yeah just shutup LMAOOO".format(
            member.mention
        ),
        color=discord.Color.light_gray()
    ).add_field(
        name="Muted until", value="`{}`".format(
            format_time(datetime.datetime.now() + time) if args[1].lower() != "forever" else "Forever"
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

    if args[1].lower() != "forever":
        await asyncio.sleep(time.total_seconds())
        await member.remove_roles(muted_role)


@handler.add(
    [], perm=MODS, usage="unmute <mention|id>"
)
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


@handler.add(
    [], perm=MODS, usage="warn <mention|id> [<reason>]"
)
async def warn(message, args, client):
    """warns a user"""

    if len(args) == 0:
        await message.reply("Who do you want me to warn lol")
        return

    warn_member_id = args[0]
    warn_member = parse_member(message.guild, warn_member_id)
    warn_reason = "None given" if len(args) < 2 else " ".join(args[1:])

    if warn_member.bot:
        await message.reply("You cannot warn a bot.", mention_author=False)
        return

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


@handler.add(
    ["bye", "getlost"], perm=OWNERS, usage="kick <mention|id> [reason]"
)
async def kick(message, args, client):
    if len(args) < 1:
        await message.reply("Who do I kick? You?", mention_author=False)

    member = parse_member(message.guild, args[0])
    reason = " ".join(args[1:]) if len(args) > 1 else "None given"

    if not member:
        await message.reply("Come on man give me a valid user.", mention_author=False)
        return

    if member.bot:
        await message.reply("You cannot kick a bot.", mention_author=False)
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
            message.guild.name
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

    # add infraction
    get_data("{}/members/{}/infractions".format(
        message.guild.id, member.id
    )).append(
        infraction_json_setup("Kick", reason, datetime.datetime.now())
    )
    update_data()


@handler.add(
    ["hammer"], perm=OWNERS, usage="ban <time>|\"forever\" <mention|id> [reason]"
)
async def ban(message, args, client):
    if len(args) < 1:
        await message.reply("Tell me who to ban or I ban you.", mention_author=False)
        return
    if len(args) < 2:
        await message.reply(
            "Gotta tell me how long to ban the sinner or `forever` to ban forever.", mention_author=False
        )
        return

    member = parse_member(message.guild, args[0])
    time = parse_time(args[1])
    reason = " ".join(args[2:]) if len(args) > 2 else "None given"

    if member.bot:
        await message.reply("You cannot ban a bot.", mention_author=False)
        return

    if not member:
        await message.reply("Give me a valid user.", mention_author=False)
        return
    if not time and args[1].lower() != "forever":
        await message.reply("Invalid time.", mention_author=False)
        return

    await member.ban(reason=reason)

    # add infraction
    get_data("{}/members/{}/infractions".format(
        message.guild.id, member.id
    )).append(
        infraction_json_setup("Ban", reason, datetime.datetime.now())
    )
    set_data("{}/members/{}/banned".format(
        message.guild.id, member.id
    ), True)
    update_data()

    embed = discord.Embed(
        title="Ban",
        description="LMAO {} was banned!".format(
            member.mention
        ),
        color=discord.Color.red()
    ).add_field(
        name="Banned until",
        value="`{}`".format(
            format_time(datetime.datetime.now() + time)
        ) if args[1].lower() != "forever" else "`Forever`"
    ).add_field(
        name="Reason",
        value="`{}`".format(reason)
    ).set_author(
        name=member.name,
        icon_url=member.avatar_url
    ).set_footer(
        text="Banned by {}".format(signature(message.author))
    )
    await message.reply(embed=embed, mention_author=False)

    embed = discord.Embed(
        title="You were banned from {}".format(
            message.guild.name
        ),
        description="Get hammered LMAOOO",
        color=discord.Color.red()
    ).add_field(
        name="Banned until",
        value="`{}`".format(
            format_time(datetime.datetime.now() + time)
        ) if args[1].lower() != "forever" else "`Forever`"
    ).add_field(
        name="Reason",
        value="`{}`".format(reason)
    ).set_footer(
        text="Banned by {}".format(signature(message.author))
    ).set_thumbnail(
        url=message.guild.icon_url
    )
    await member.send(embed=embed)

    if time:
        await asyncio.sleep(time.total_seconds())
        await member.unban()


@handler.add(
    [], perm=OWNERS, usage="unban <id>"
)
async def unban(message, args, client):
    if len(args) < 1:
        await message.reply("Tell me who to unban.", mention_author=False)
        return

    member_id = parse_int(args[0])
    if not member_id:
        await message.reply("Invalid ID lol.", mention_author=False)
        return

    member = await client.fetch_user(member_id)
    if not member:
        await message.reply("That member doesn't even exist lol.", mention_author=False)
        return

    if not get_data("{}/members/{}/banned".format(
        message.guild.id, member_id
    )):
        await message.reply("Sure. If you can teach me how to unban someone that isn't banned.", mention_author=False)
        return

    await message.guild.unban(member)

    embed = discord.Embed(
        title="Unban",
        description="{} was unbanned!".format(member.mention),
        color=discord.Color.green()
    ).set_author(
        name=member.name,
        icon_url=member.avatar_url
    ).set_footer(
        text="Unbanned by {}".format(
            signature(message.author)
        )
    )
    await message.reply(embed=embed, mention_author=False)
