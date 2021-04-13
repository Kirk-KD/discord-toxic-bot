"""
integers representing permission levels and a permission checking function
"""

import discord
import os

from src.bot.data import guilds_data


def perm_check(member: discord.Member, perm: int):
    """
    checks permissions of member:
    EVERYONE = 0
    MODS = 1
    OWNERS = 2
    DEV = 3

    :param member: Member
    :param perm: int
    :return: bool
    """

    if perm == 0:  # everyone
        return True

    if perm <= 4:  # global dev
        if str(member.id) == os.getenv("DEV"):
            return True

    if perm <= 3:  # dev
        if str(member.id) == os.getenv("DEV") and str(member.guild.id) == os.getenv("DEV_SERVER"):
            return True

    if perm <= 2:  # owners
        if member.id == member.guild.owner_id:
            return True
        for role in member.roles:
            if role.id in guilds_data.get(member.guild.id)["settings"]["perm_ids"]["owner"]:
                return True

    if perm <= 1:  # moderators
        for role in member.roles:
            if role.id in guilds_data.get(member.guild.id)["settings"]["perm_ids"]["mod"]:
                return True

    return False


# perms
EVERYONE = 0
MODS = 1
OWNERS = 2
DEV = 3
GLOBAL_DEV = 4
perm_names = ["Everyone", "Mods", "Owners", "Dev"]
