import json
import discord
import datetime

from src.bot.data import stocks_data

from src.util.time import format_time


def guild_dict_setup(guild: discord.Guild):
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
        data["members"][str(member.id)] = member_dict_setup()

    return data


def member_dict_setup():
    return {
        "banned": False,
        "muted": False,
        "timers": {
            "ban": None,
            "mute": None
        },
        "infractions": []
    }


def infraction_dict_setup(action: str, reason: str, time: datetime.datetime):
    return {
        "action": action,
        "reason": reason,
        "time": format_time(time)
    }


def player_dict_setup():
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


def giveaway_dict_setup(name: str, start_time: datetime.datetime, duration: datetime.timedelta, winners: int):
    return {
        "name": name,
        "start": format_time(start_time),
        "duration": duration,
        "winners": winners,
        "participants": []
    }
