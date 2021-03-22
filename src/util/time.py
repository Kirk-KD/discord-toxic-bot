import datetime
import math

import discord


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
        member.display_name, member, timestamp()
    )


def format_timedelta(timedelta: datetime.timedelta):
    seconds = math.ceil(timedelta.total_seconds())
    print(seconds)
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "{}{}{}{}".format(
        "{} days, ".format(days) if days else "",
        "{}h ".format(hours) if hours or days else "",
        "{}m ".format(minutes) if minutes or hours or days else "",
        "{}s".format(seconds) if seconds or minutes or hours or days else ""
    )
