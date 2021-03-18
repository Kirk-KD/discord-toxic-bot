"""
commands under category "Utilities"
"""

from src.command_handler import handler
from src.perms import *

from src.util.parser import *
from src.util.bot import *

import discord
import math
import asyncio


@handler.add(
    ["testing"], perm=EVERYONE, usage="test [<args...>]", category="Utilities"
)
async def test(message, args, client):
    """a simple testing command that serves no purpose"""

    embed = discord.Embed(
        title="Im working alright lmaooo",
        color=discord.Color.green()
    ).add_field(
        name="Args",
        value=str(args)
    ).add_field(
        name="Client",
        value="<" + str(client).split()[-1]
    ).set_footer(text=timestamp())

    await message.reply(embed=embed, mention_author=False)


@handler.add(
    [], perm=OWNERS, usage="setup", category="Utilities"
)
async def setup(message, args, client):
    """setup command! setup process will be in the owner's DM"""

    async def fail(fail_msg):
        fail_embed = discord.Embed(
            title="Setup Failed!",
            description="{} Gotta restart now lmao. Go back to your server and type `_setup`.".format(fail_msg),
            color=discord.Color.red()
        )
        await message.author.send(embed=fail_embed)

    async def get_user_input(guild_roles_, target_roles_list, msg_embed):
        input_str = await dm_input(message, msg_embed, client)
        input_nums = input_str.split()

        for num in input_nums:
            n = parse_int(num)
            if not n or n >= len(guild_roles_):
                await fail("Invalid option: `{}`.".format(num))
                return False

            target_roles_list.append(guild_roles_[n].id)

        return True

    if guilds_data[str(message.author.guild.id)]["initialised"]:
        await message.reply(
            ("yo your server was already initialised lol. "
             "Do you wish to redo setup? Reply `yes` in 10 seconds if you do."), mention_author=False
        )

        def check(m):
            return m.channel == message.channel and m.author == message.author
        try:
            msg = await client.wait_for("message", check=check, timeout=10)
            if msg.content.lower() != "yes":
                await message.channel.send("Setup redo canceled.")
                return
            else:
                # initialise settings
                set_data("{}/settings/perm_ids/owner".format(message.guild.id), [])
                set_data("{}/settings/perm_ids/mod".format(message.guild.id), [])
                set_data("{}/initialised".format(message.guild.id), False)
                update_data()
        except asyncio.exceptions.TimeoutError:
            await message.channel.send("Setup redo canceled.")
            return

    await message.reply("Alrighty i'll be waiting for you in your dm", mention_author=False)

    # switch to DM
    guild_roles = message.guild.roles
    owner_roles = []
    mod_roles = []

    embed = discord.Embed(
        title="Toxic bot setup for `{}`".format(message.guild.name),
        description="Let's get started then!",
        color=discord.Color.green()
    ).set_thumbnail(url=message.guild.icon_url)
    await message.author.send(embed=embed)

    embed = discord.Embed(
        title="What are the roles for **\"owners\"**?",
        description=("They are the ones that can use (almost) every command. "
                     "Type their number(s) below separated by spaces!"),
        color=discord.Color.blue()
    )
    for i, r in enumerate(guild_roles):
        embed.add_field(name=str(i), value=r.name, inline=True)
    if not await get_user_input(guild_roles, owner_roles, embed):
        return

    embed = discord.Embed(
        title="What are the roles for **\"moderators\"**?",
        description=("They are the ones that can use `warn`, `mute` and other commands "
                     "except the owner only ones (`kick`, `slowmode`, `ban`). "
                     "Type their number(s) below separated by spaces!"),
        color=discord.Color.blue()
    )
    for i, r in enumerate(guild_roles):
        embed.add_field(name=str(i), value=r.name + (" `owner`" if r.id in owner_roles else ""), inline=True)
    if not await get_user_input(guild_roles, mod_roles, embed):
        return

    set_data("{}/settings/perm_ids/owner".format(message.guild.id), owner_roles.copy())
    set_data("{}/settings/perm_ids/mod".format(message.guild.id), mod_roles.copy())
    set_data("{}/initialised".format(message.guild.id), True)
    update_data()

    embed = discord.Embed(
        title="Toxic bot setup complete!",
        description="`Owners` {}\n`Mods` {}".format(
            ", ".join([discord.utils.get(guild_roles, id=r).name for r in owner_roles]),
            ", ".join([discord.utils.get(guild_roles, id=r).name for r in mod_roles])
        ),
        color=discord.Color.green()
    )
    await message.author.send(embed=embed)


@handler.add(
    [], perm=EVERYONE, usage="help", category="Utilities"
)
async def help_(message, args, client):
    """get some help."""

    cmd_names = []
    pages = []
    page_count = int(math.ceil(handler.cmd_count / 5))
    cmd_idx = 0

    def page(page_i, cmd_i):
        embed = discord.Embed(
            title="Help",
            description="Here is a list of commands!",
            color=discord.Color.blue()
        ).set_footer(
            text="page {}/{}".format(
                page_i + 1, page_count
            )
        )

        index = cmd_i
        for command in sorted(handler.commands.values(), key=lambda c: c.name):
            if command.name in cmd_names:
                continue

            cmd_names.append(command.name)
            embed.add_field(
                name=command.name,
                value="`{}`".format(command.usage),
                inline=False
            )

            index += 1
            if index >= cmd_i + 5:
                break

        return embed, cmd_i

    def check(reaction, user):
        return user == message.author

    for i in range(page_count):
        p, idx = page(i, cmd_idx)
        cmd_idx = idx
        pages.append(p)

    try:
        page_idx = 0
        msg = await message.channel.send(embed=pages[0], mention_author=False)
        await msg.add_reaction("◀")
        await msg.add_reaction("▶")

        emoji = ""
        while True:
            if emoji == "▶":
                page_idx = (page_idx + 1) if page_idx < page_count - 1 else 0
                await msg.edit(embed=pages[page_idx])
            elif emoji == "◀":
                page_idx = (page_idx - 1) if page_idx > 0 else page_count - 1
                await msg.edit(embed=pages[page_idx])

            try:
                res = await client.wait_for("reaction_add", timeout=120.0, check=check)
                if res is None:
                    break
                if str(res[1]) != client.user.name:
                    emoji = str(res[0].emoji)
                    await msg.remove_reaction(res[0].emoji, res[1])
            except TimeoutError:
                break

        await msg.clear_reactions()
    except discord.NotFound:  # message deleted
        pass


@handler.add(
    ["delete"], perm=OWNERS, usage="clear <int>", category="Utilities"
)
async def clear(message, args, client):
    """deletes messages"""

    num = parse_int(args[0])
    if len(args) == 0 or num is None:
        await message.reply("Dude u need to tell me how many messages to delete lol", mention_author=False)
        return

    if num <= 0:
        await message.reply(
            "Trying to break me huh? Try to delete {} messages yourself".format(num), mention_author=False
        )
        return

    deleted = await message.channel.purge(limit=num)
    if len(deleted) <= 3:
        embed = discord.Embed(
            title=str(len(deleted)) + " messages deleted",
            description="{} fine, deleted. Its just {} messages cant you do it yourself you lazy bum??".format(
                message.author.mention, len(deleted)
            ),
            color=discord.Color.green()
        ).set_footer(text=timestamp())
        await message.channel.send(embed=embed)
        return

    embed = discord.Embed(
        title=str(len(deleted)) + " messages deleted",
        description="{} Alright, {} messages deleted.".format(
            message.author.mention, len(deleted)
        ),
        color=discord.Color.green()
    ).set_footer(text=timestamp())
    await message.channel.send(embed=embed)


@handler.add(
    ["slow", "sm"], perm=OWNERS, usage="slowmode <time>|off", category="Utilities"
)
async def slowmode(message, args, client):
    """sets slowmode of a channel"""

    if len(args) == 0 or not (parse_time(args[0]) or (parse_bool(args[0]) is False)):
        await message.reply(
            "Ayo gotta tell me how long you want the slowmode to be or \"off\" to turn it off",
            mention_author=False
        )
        return

    amount = int(parse_time(args[0]).total_seconds()) if parse_time(args[0]) is not None else 0

    if amount == 0:
        if message.channel.slowmode_delay == 0:
            await message.reply("Slowmode was already off you nerd.", mention_author=False)
            return

        embed = discord.Embed(
            title="Slowmode is now off",
            color=discord.Color.green()
        ).set_footer(text=timestamp())
        await message.reply(embed=embed, mention_author=False)
    else:
        embed = discord.Embed(
            title="Slowmode set to {}".format(args[0]),
            description="Now suffer from the slowness!",
            color=discord.Color.green()
        ).set_footer(text=timestamp())
        await message.reply(embed=embed, mention_author=False)

    await message.channel.edit(slowmode_delay=amount)


@handler.add(
    ["user", "info", "ui"], perm=EVERYONE, usage="userinfo [<mention|id>]", category="Utilities"
)
async def userinfo(message, args, client):
    member = parse_member(message.guild, args[0]) if len(args) > 0 else message.author
    if not member:
        await message.reply("That member doesn't even exist what are you doing lmao", mention_author=False)
        return

    embed = get_user_info(member, message)
    await message.reply(embed=embed, mention_author=False)
