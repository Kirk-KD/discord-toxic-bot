import datetime
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
        member.display_name, member, format_time(datetime.datetime.now())
    )
