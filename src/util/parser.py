import discord
import datetime
import re


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

    # https://stackoverflow.com/questions/4628122/how-to-construct-a-timedelta-object-from-a-simple-string
    regex = re.compile(r'((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
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


def parse_channel(guild: discord.Guild, channel_id: str):
    """
    returns a Channel if found one in guild using channel_id, None otherwise

    :param guild: Guild
    :param channel_id: str
    :return: Channel or None
    """

    if not parse_int(channel_id) and not parse_int(channel_id[2:-1]):
        return None

    for c in guild.channels:
        if c.id == (parse_int(channel_id) if parse_int(channel_id) is not None else parse_int(channel_id[2:-1])):
            return c

    return None
