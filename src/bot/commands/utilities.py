import discord
from discord_components import Button, ButtonStyle, InteractionType
import asyncio

from src.bot.category import Category
from src.bot.command import Command
from src.bot.data import guilds_data
from src.bot.handler import handler
from src.bot import perms

from src.util.bot import get_infractions, dm_input
from src.util.parser import parse_int, parse_time, parse_bool, parse_member
from src.util.time import timestamp, format_time, signature


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

            await message.reply(embed=embed, mention_author=False, components=[
                Button(label="omg a button wooo so cool.")
            ])

            interaction = await client.wait_for("button_click", check=lambda i: (i.channel == message.channel and
                                                                                 i.user == message.author))
            await interaction.respond(content="Button clicked")

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

    class Userinfo(Command):
        def __init__(self):
            super().__init__(
                ["userinfo", "user", "info", "ui"], "userinfo [<user>]",
                "Displays info of a user or yourself.", perms.EVERYONE
            )

        async def __call__(self, message, args, client):
            member = parse_member(message.guild, args[0]) if len(args) > 0 else message.author
            if not member:
                await message.reply("That member doesn't even exist what are you doing lmao", mention_author=False)
                return

            if member.bot:
                await message.reply("I can't get info of a bot my man.", mention_author=False)
                return

            embed = self.get_user_info(member, message)
            await message.reply(embed=embed, mention_author=False)

        @staticmethod
        def get_user_info(member: discord.Member, message: discord.Message):
            embed = discord.Embed(
                color=discord.Color.blue()
            ).set_author(
                name="User info of {}".format(member),
                icon_url=member.avatar_url
            ).add_field(
                name="User Name",
                value="{} ({})".format(member.display_name, member)
            ).add_field(
                name="User ID",
                value=member.id
            ).add_field(
                name="Infractions",
                value=get_infractions(member)[1]["total"]
            ).add_field(
                name="Joined Server",
                value=format_time(member.joined_at)
            ).add_field(
                name="Joined Discord",
                value=format_time(member.created_at)
            ).add_field(
                name="Boosting Since",
                value=format_time(p) if (p := member.premium_since) else "Not Boosting"
            ).set_footer(
                text="Requested by {}".format(signature(message.author))
            )

            return embed

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

            if guilds_data.get(message.guild.id)["initialised"]:
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
                        guild_data = guilds_data.get(message.guild.id)
                        guild_data["settings"]["perm_ids"]["owner"] = \
                            guild_data["settings"]["perm_ids"]["mod"] = []
                        guild_data["initialised"] = False
                        guilds_data.set(message.guild.id, {"data": guild_data})

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

            guild_data = guilds_data.get(message.guild.id)
            guild_data["settings"]["perm_ids"]["owner"] = owner_roles
            guild_data["settings"]["perm_ids"]["mod"] = mod_roles
            guild_data["initialised"] = True
            guilds_data.set(message.guild.id, {"data": guild_data})

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
