"""
some utility functions to organise and simplify the code
"""

import json
import discord
import datetime
import re


# parsers
def parse_int(s: str):
    """
    returns the number if is convertible to int, None otherwise

    :param s: str
    :return: int or None
    """

    if not s.isnumeric():
        return None
    try:
        return int(s)
    except ValueError:
        return None


def parse_bool(s: str):
    """
    returns a bool if convertible, None otherwise

    :param s: str
    :return: bool or None
    """

    if s.lower() in ["off", "false", "no"]:
        return False
    elif s.lower() in ["on", "true", "yes"]:
        return True

    return None


def parse_time(s: str):
    """
    returns a timedelta if convertible, None otherwise

    :param s: str
    :return: timedelta or None
    """

    regex = re.compile(r'((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
    parts = regex.match(s.lower())
    if not parts:
        return None
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return datetime.timedelta(**time_params)


def parse_member(guild: discord.Guild, user_id: str):
    """
    returns a Member if found one in guild using user_id, None otherwise

    :param guild: Guild
    :param user_id: str
    :return: Member or None
    """

    if not parse_int(user_id) and not parse_int(user_id[3:-1]):
        return None

    for m in guild.members:
        if m.id == (parse_int(user_id) if parse_int(user_id) is not None else parse_int(user_id[3:-1])):
            return m

    return None


# json
def read_json(file: str):
    """
    reads a JSON file and returns a dict parsed from its content

    :param file: str
    :return: dict
    """

    with open(file, "r") as f:
        content = f.read()
    return json.loads(content)


def write_json(file: str, data: dict):
    """
    writes data to a JSON file

    :param file: str
    :param data: dict
    :return: None
    """

    with open(file, "w") as f:
        f.write(json.dumps(data, indent=2))


def guild_json_setup(guild: discord.Guild):
    """
    returns a default json dict for a Guild in guilds.json

    :param guild: Guild
    :return: dict
    """

    data = {
        "initialised": False,
        "settings": {
            "perm_ids": {
                "owner": [],
                "mod": []
            },
            "disabled_cmds": [],
            "bot_channels": [],
            "welcome_channel": None
        },
        "members": {}
    }

    for member in guild.members:
        if member.bot:
            continue
        data["members"][str(member.id)] = member_json_setup()

    return data


def member_json_setup():
    """
    returns a default json dict for a Member in guilds.json

    :return: dict
    """

    return {
        "muted": False,
        "banned": False,
        "infractions": []
    }


def infraction_json_setup(action: str, reason: str, time: datetime.datetime):
    """
    returns a json dict for an infraction in guilds.json

    :param action: str
    :param reason: str
    :param time: datetime
    :return: dict
    """

    return {
        "action": action,
        "reason": reason,
        "time": int(time.timestamp())
    }


# message & guilds
async def dm_input(init_msg: discord.Message, prompt: discord.Embed or str, client: discord.Client):
    """
    wait for user input in DM after sending ask_str

    :param init_msg: Message
    :param prompt: Embed or str
    :param client: Client
    :return: str
    """

    def check(m: discord.Message):
        return m.author == init_msg.author and type(m.channel) is discord.DMChannel

    if type(prompt) is discord.Embed:
        await init_msg.author.send(embed=prompt)
    else:
        await init_msg.author.send(prompt)

    user_input = await client.wait_for("message", check=check)
    return user_input.content


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


# string format
def format_time(time):
    return str(time).split(".")[0]


def timestamp():
    return format_time(datetime.datetime.now())


def signature(member: discord.Member):
    """
    returns a signature of "<nick name> (<user name>) • <current time>"

    :param member: Member
    :return: str
    """

    return "{} ({}) • {}".format(
        member.display_name, member, format_time(datetime.datetime.now())
    )
