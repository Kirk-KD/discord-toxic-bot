from src.category import Category
from src.command import Command
from src.handler import handler
from src import perms

from src.util.parser import *
from src.util.bot import *

import discord
import asyncio


class Moderation(Category):
    def __init__(self):
        super().__init__("Moderation", "The ruler's toolkit.")

    class Mute(Command):
        def __init__(self):
            super().__init__(
                ["mute", "shutup"], "mute <user> <time or \"forever\"> [<reason>]",
                "Shuts an annoying user up.", perms.MODS
            )

        async def __call__(self, message, args, client):
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
            if not time and args[1].lower() != "forever":
                await message.reply(
                    "Dude give me a valid time (eg 2d12h30m15s) as second argument or `forever`.", mention_author=False
                )
                return
            if member.bot:
                await message.reply("You cannot mute a bot.", mention_author=False)
                return

            muted_role = await self.make_muted_role(message)
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
            guilds_data.get_data("{}/members/{}/infractions".format(
                message.guild.id, member.id
            )).append(
                infraction_json_setup("Mute", reason, datetime.datetime.now())
            )
            guilds_data.update_data()

            if args[1].lower() != "forever":
                await asyncio.sleep(time.total_seconds())
                await member.remove_roles(muted_role)

        @staticmethod
        async def make_muted_role(message: discord.Message):
            muted_role = discord.utils.get(message.guild.roles, name="Muted")
            if not muted_role:
                try:
                    muted_role = await message.guild.create_role(name="Muted", reason="Use for muting")
                    for channel in message.guild.channels:
                        await channel.set_permissions(muted_role, send_messages=False, add_reactions=False)
                except discord.Forbidden:
                    await message.reply("I don't have permission to make a muted role man.", mention_author=False)
                    return None

            return muted_role

    class Unmute(Command):
        def __init__(self):
            super().__init__(
                ["unmute"], "unmute <user>",
                "Re-grants a user the right of speech.", perms.MODS
            )

        async def __call__(self, message, args, client):
            if len(args) < 1:
                await message.reply("Are you gonna tell me who to unmute or not???", mention_author=False)
                return

            member = parse_member(message.guild, args[0])
            muted_role = discord.utils.get(message.guild.roles, name="Muted")

            if not member:
                await message.reply("*sigh* give me a valid user ID or mention.", mention_author=False)
                return
            if not muted_role or muted_role not in member.roles:
                await message.reply(
                    "Fun fact: you can't unmute someone that isn't muted. Bet you didn't know this.",
                    mention_author=False
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

    class Warn(Command):
        def __init__(self):
            super().__init__(
                ["warn"], "warn <user> [<reason>]",
                "Warns a user. The main purpose is just to add an infraction.", perms.MODS
            )

        async def __call__(self, message, args, client):
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
            guilds_data.get_data("{}/members/{}/infractions".format(
                message.guild.id, warn_member.id
            )).append(
                infraction_json_setup("Warn", warn_reason, datetime.datetime.now())
            )
            guilds_data.update_data()

    class Kick(Command):
        def __init__(self):
            super().__init__(
                ["kick", "bye", "getlost"], "kick <user> [<reason>]",
                "Sometimes you just need to get rid of the annoying ones.", perms.OWNERS
            )

        async def __call__(self, message, args, client):
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
            guilds_data.get_data("{}/members/{}/infractions".format(
                message.guild.id, member.id
            )).append(
                infraction_json_setup("Kick", reason, datetime.datetime.now())
            )
            guilds_data.update_data()

    class Ban(Command):
        def __init__(self):
            super().__init__(
                ["ban", "hammer"], "ban <user> <time or \"forever\"> [<reason>]",
                "\"Get banned, sinner!\" -Thor or something, 2011", perms.OWNERS
            )

        async def __call__(self, message, args, client):
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
            guilds_data.get_data("{}/members/{}/infractions".format(
                message.guild.id, member.id
            )).append(
                infraction_json_setup("Ban", reason, datetime.datetime.now())
            )
            guilds_data.set_data("{}/members/{}/banned".format(
                message.guild.id, member.id
            ), True)
            guilds_data.update_data()

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

    class Unban(Command):
        def __init__(self):
            super().__init__(
                ["ban", "hammer"], "unban <user>",
                "Forgive the sins the sinner has committed.", perms.OWNERS
            )

        async def __call__(self, message, args, client):
            await message.channel.send("HERE")
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

            if not guilds_data.get_data("{}/members/{}/banned".format(
                    message.guild.id, member_id
            )):
                await message.reply("Sure. If you can teach me how to unban someone that isn't banned.",
                                    mention_author=False)
                return

            await message.guild.unban(member)
            guilds_data.set_data("{}/members/{}/banned".format(message.guild.id, member_id), False)

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

    class Infractions(Command):
        def __init__(self):
            super().__init__(
                ["infractions", "sins", "infracs"], "infractions [<user>]",
                "Uncover a user's sins they are trying to hide. (or yourself)", perms.MODS
            )

        async def __call__(self, message, args, client):
            member = message.author if len(args) < 1 else parse_member(message.guild, args[0])
            if not member:
                await message.reply("That is not a valid member my man.", mention_author=False)
                return

            inf_msg, counter = get_infractions(member)
            embed = discord.Embed(
                color=discord.Color.blue()
            ).set_author(
                name="{}'s infractions".format(member.name),
                icon_url=member.avatar_url
            ).add_field(
                name="Warns",
                value=counter["warn"],
                inline=True
            ).add_field(
                name="Mutes",
                value=counter["mute"],
                inline=True
            ).add_field(
                name="Kicks & Bans",
                value=counter["kick"] + counter["ban"],
                inline=True
            ).add_field(
                name="Total",
                value="{} infractions".format(counter["total"]),
                inline=False
            ).add_field(
                name="Last 10 infractions",
                value=inf_msg if inf_msg != "" else "This member has not committed any sins :/",
                inline=False
            ).set_footer(
                text="That's clean man" if inf_msg == "" else "You feel your sins crawling on you back"
            )

            await message.reply(embed=embed, mention_author=False)


handler.add_category(Moderation)
