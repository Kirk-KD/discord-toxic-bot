"""
commands under category "Utilities"
"""

from src.command_handler import handler
from src.perms import *
from src.data import *

import discord

# TODO: ADD EMBEDS


@handler.add(["testing"], perm=EVERYONE)
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


@handler.add(["delete"], perm=OWNERS)
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


@handler.add(["slow", "sm"], perm=OWNERS)
async def slowmode(message, args, client):
    """sets slowmode of a channel"""

    if len(args) == 0 or not (parse_time(args[0]) or (parse_bool(args[0]) is False)):
        await message.reply(
            "Ayo gotta tell me how long you want the slowmode to be or \"off\" to turn it off",
            mention_author=False
        )
        return

    amount = int(parse_time(args[0]).seconds) if parse_time(args[0]) is not None else 0

    if amount < 0:
        await message.reply(
            "Ahh I see that you are not very familiar with time? A delay cannot be negative. You are welcome.",
            mention_author=False
        )
        return

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


@handler.add([], perm=OWNERS)
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

        if input_str.lower() == "none":
            return True

        for num in input_nums:
            n = parse_int(num)
            if not n or n >= len(guild_roles_):
                await fail("Invalid option: `{}`.".format(num))
                return False

            target_roles_list.append(guild_roles_[n].id)

        return True

    if guilds_data[str(message.author.guild.id)]["initialised"]:
        await message.reply("yo your server was already initialised lol", mention_author=False)
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
                     "Type their number(s) below separated by spaces! Type `none` for none."),
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
                     "Type their number(s) below separated by spaces! Type `none` for none."),
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
