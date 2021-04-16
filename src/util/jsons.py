import json
import discord
import datetime

from src.bot.data import stocks_data

from src.util.time import format_time


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
        "banned": False,
        "muted": False,
        "timers": {
            "ban": None,
            "mute": None
        },
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
        "time": format_time(time)
    }


def player_json_setup():
    """
    returns a json dict for a player in game.json

    :return: dict
    """

    return {
        "stats": {
            "txc": 1000,
            "exp": 0,
            "multi": 0,
            "streak": 0
        },
        "bank": {
            "max": 5000,
            "curr": 0
        },
        "timers": {
            "streak": None
        },
        "inv": {},
        "effects": [],
        "stocks": {s["_id"]: 0 for s in stocks_data.all()}
    }
