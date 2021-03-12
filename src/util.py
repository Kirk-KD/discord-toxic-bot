"""
some utility functions to organise and simplify the code
"""

import json
import discord


def parse_int(s: str):
    """
    returns the number if is convertible to int, None otherwise

    :param s: str
    :return: int or None
    """

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
                "mod": [],
                "user": []
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
        "infractions": 0
    }


async def dm_input(init_msg: discord.Message, ask_str: str, client: discord.Client):
    """
    wait for user input in DM after sending ask_str

    :param init_msg: Message
    :param ask_str: str
    :param client: Client
    :return: str
    """
    def check(m: discord.Message):
        return m.author == init_msg.author and type(m.channel) is discord.DMChannel

    await init_msg.author.send(ask_str)
    user_input = await client.wait_for("message", check=check)
    return user_input.content


def validate_role_id(guild: discord.Guild, role_id: str):
    parsed = parse_int(role_id)
    if not parsed or not guild.get_role(parsed):
        return False

    return True
