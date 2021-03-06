import datetime
import discord
import asyncio

from src.bot.category import Category
from src.bot.command import Command
from src.bot.data import guilds_data
from src.bot.handler import handler
from src.bot import perms

from src.util.bot import get_infractions, dm_input
from src.util.parser import parse_int, parse_time, parse_bool, parse_member, parse_channel
from src.util.time import timestamp, format_time, signature, format_timedelta
from src.util.dicts import giveaway_dict_setup


class Utilities(Category):
    def __init__(self):
        super().__init__("Utilities", "Some useful commands.")

    class Test(Command):
        def __init__(self):
            super().__init__(
                ["test", "testing"], "test [<args...>]", "A simple testing command.", perms.EVERYONE
            )

        async def __call__(self, message, args, client):
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

    class Clear(Command):
        def __init__(self):
            super().__init__(
                ["clear", "delete"], "clear <amount>",
                "Deletes messages in the channel the command was issued in.", perms.OWNERS
            )

        async def __call__(self, message, args, client):
            if len(args) == 0:
                await message.reply("Dude u need to tell me how many messages to delete lol", mention_author=False)
                return

            num = parse_int(args[0])
            if num is None:
                await message.reply(
                    "Lmao that number is invalid.".format(num), mention_author=False
                )
                return

            deleted = await message.channel.purge(limit=num)
            if len(deleted) <= 3:
                embed = discord.Embed(
                    title=str(len(deleted)) + " messages deleted",
                    description="{} fine, deleted. Its just {} messages can't you do it yourself you lazy bum??".format(
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

    class Slowmode(Command):
        def __init__(self):
            super().__init__(
                ["slowmode", "slow", "sm"], "slowmode <time or \"off\">",
                "Sets slowmode in the channel the command was issued in.", perms.OWNERS
            )

        async def __call__(self, message, args, client):
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
            else:
                if amount > 21600:
                    await message.reply("Slow mode can't be more than 21600 seconds idiot.", mention_author=False)
                    return

                embed = discord.Embed(
                    title="Slowmode set to {}".format(args[0]),
                    description="Now suffer from the slowness!",
                    color=discord.Color.green()
                ).set_footer(text=timestamp())

            await message.channel.edit(slowmode_delay=amount)
            await message.reply(embed=embed, mention_author=False)

    class Giveaway(Command):
        def __init__(self):
            super().__init__(["giveaway", "ga"],
                             "giveaway (\"create\" or (\"reroll\" <giveaway_id>) or "
                             "(\"restart\" <giveaway_id>) or (\"delete\" <giveaway_id>))",
                             "Create and manage giveaways.", perms.OWNERS)

        async def __call__(self, message, args, client):
            if len(args) == 0:
                await message.reply(
                    "Pass in the second argument (`create`/`reroll`/`restart`/`delete`) ya idiot.",
                    mention_author=False
                )
                return

            action = args[0].lower()
            if action == "create":
                def check(m):
                    return m.channel == message.channel and m.author == message.author

                try:
                    # get giveaway name
                    await message.reply("Wanna start a giveaway huh. What is the name/prize of the giveaway?",
                                        mention_author=False)
                    g_name = (await client.wait_for("message", check=check, timeout=30)).content

                    # get giveaway winners
                    await message.reply("How many winners are there?", mention_author=False)
                    g_winners = parse_int((await client.wait_for("message", check=check, timeout=30)).content)
                    if g_winners == 0:
                        await message.reply("LMAO imagine making a giveaway with 0 winners.", mention_author=False)
                        return
                    if g_winners is None:
                        await message.reply("That is not a number my man.", mention_author=False)
                        return

                    # get giveaway duration
                    await message.reply("How long will the giveaway last?", mention_author=False)
                    duration = parse_time((await client.wait_for("message", check=check, timeout=30)).content)
                    if not duration:
                        await message.reply("Dude give me a valid time (eg 2d12h30m15s).", mention_author=False)
                        return

                    # get giveaway channel
                    await message.reply("Finally, which channel will the giveaway be hosted in?", mention_author=False)
                    g_channel = parse_channel(
                        message.guild, (await client.wait_for("message", check=check, timeout=30)).content
                    )
                    if not g_channel or type(g_channel) is not discord.TextChannel:
                        await message.reply("Either I can't find the channel, or that channel you gave me "
                                            "isn't a text channel.", mention_author=False)

                    # create giveaway
                    now = datetime.datetime.now()
                    embed = discord.Embed(
                        title="Giveaway: {}".format(g_name),
                        description="React below to participate!",
                        color=discord.Color.blurple()
                    ).add_field(
                        name="Winners", value="`{}`".format(g_winners), inline=False
                    ).add_field(
                        name="Duration", value="`{}`".format(format_timedelta(duration)), inline=False
                    ).add_field(
                        name="Ends At", value="`{}`".format(format_time(now + duration)), inline=False
                    ).set_footer(text=timestamp())

                    g_msg = await g_channel.send(embed=embed)
                    await g_msg.add_reaction("????")

                    guild_data = await guilds_data.get(message.guild.id)
                    giveaways = guild_data["giveaways"]
                    giveaway_data = giveaway_dict_setup(g_name, now, now + duration, g_winners, g_channel)

                    giveaways[str(g_msg.id)] = giveaway_data
                    await guilds_data.set(message.guild.id, {"data": guild_data})

                except asyncio.TimeoutError:
                    await message.reply("Why bother me when you don't even answer my questions.", mention_author=False)

            elif action == "reroll":
                pass

            elif action == "restart":
                pass

            elif action == "delete":
                pass

            else:
                await message.reply(
                    "Damn bro, you really thought I can do anything other than "
                    "`create`, `reroll`, `restart`, and `delete`?", mention_author=False
                )

    class Setup(Command):
        def __init__(self):
            super().__init__(
                ["setup"], "setup", "Sets the bot up in your server.", perms.OWNERS
            )

        async def __call__(self, message, args, client):
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

            if await guilds_data.get(message.guild.id)["initialised"]:
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
                        guild_data = await guilds_data.get(message.guild.id)
                        guild_data["settings"]["perm_ids"]["owner"] = \
                            guild_data["settings"]["perm_ids"]["mod"] = []
                        guild_data["initialised"] = False
                        await guilds_data.set(message.guild.id, {"data": guild_data})

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

            guild_data = await guilds_data.get(message.guild.id)
            guild_data["settings"]["perm_ids"]["owner"] = owner_roles
            guild_data["settings"]["perm_ids"]["mod"] = mod_roles
            guild_data["initialised"] = True
            await guilds_data.set(message.guild.id, {"data": guild_data})

            embed = discord.Embed(
                title="Toxic bot setup complete!",
                description="`Owners` {}\n`Mods` {}".format(
                    ", ".join([discord.utils.get(guild_roles, id=r).name for r in owner_roles]),
                    ", ".join([discord.utils.get(guild_roles, id=r).name for r in mod_roles])
                ),
                color=discord.Color.green()
            )
            await message.author.send(embed=embed)

    class Help(Command):
        def __init__(self):
            super().__init__(
                ["help"], "help [<category> or <command>]",
                "Displays the categories and commands", perms.EVERYONE
            )

        async def __call__(self, message, args, client):
            if len(args) == 0:
                embed = discord.Embed(
                    title="Help",
                    description="use `_help <category>` to get more detailed help you noob.",
                    color=discord.Color.blue()
                )

                i = 0
                for category in handler.categories:
                    if category.hidden:
                        continue

                    i += 1
                    embed.add_field(
                        name=category.name,
                        value="`{}`".format(category.description),
                        inline=i % 3 != 0  # to set to two columns instead of three
                    )

                await message.reply(embed=embed, mention_author=False)

            else:
                if (category := handler.get_category(args[0].lower())) and not category.hidden:
                    embed = discord.Embed(
                        title="Help of category `{}`".format(category.name),
                        color=discord.Color.blue(),
                        description=""
                    )

                    for command in category.commands:
                        embed.description += command.format_help()

                    await message.reply(embed=embed, mention_author=False)

                elif (command := handler.get_command(args[0].lower())) and not command.category.hidden:
                    embed = discord.Embed(
                        title="Help of command `{}`".format(command.name),
                        color=discord.Color.blue(),
                        description=command.format_help()
                    )

                    await message.reply(embed=embed, mention_author=False)

                else:
                    await message.reply("That category or command doesn't even exist lol.", mention_author=False)
                    return


handler.add_category(Utilities)
