"""
integers representing permission levels and a permission checking function
"""

import os
from src.data import *


def perm_check(member: discord.Member, perm: int):
    """
    checks permissions of member:
    EVERYONE = 0
    USER = 1
    MODS = 2
    OWNERS = 3
    DEV = 4

    :param member: Member
    :param perm: int
    :return: bool
    """

    # TODO: simplify repeated code
    if perm == 0:  # everyone
        return True

    if perm <= 4:  # dev
        if str(member.id) == os.getenv("DEV") and str(member.guild.id) == os.getenv("DEV_SERVER"):
            return True

    if perm <= 3:  # owners
        if member.id == member.guild.owner_id:
            return True
        for role in member.roles:
            if str(role.id) in guilds_data[str(member.guild.id)]["settings"]["perm_ids"]["owner"]:
                return True

    if perm <= 2:  # moderators
        for role in member.roles:
            if str(role.id) in guilds_data[str(member.guild.id)]["settings"]["perm_ids"]["mod"]:
                return True

    if perm <= 1:  # users
        for role in member.roles:
            if str(role.id) in guilds_data[str(member.guild.id)]["settings"]["perm_ids"]["user"]:
                return True

    return False


# perms
EVERYONE = 0
USER = 1
MODS = 2
OWNERS = 3
DEV = 4
