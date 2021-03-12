import discord
import os

# temporarily hard-coded
rank_1 = ["819740268106219550"]
rank_2 = ["819739943022493747"]
rank_3 = ["819739572556267541"]


def perm_check(member: discord.Member, perm: int):
    if perm == 0:  # everyone
        return True

    if perm <= 4:  # dev
        if str(member.id) == os.getenv("DEV"):
            return True

    if perm <= 3:  # owners
        for role in member.roles:
            if str(role.id) in rank_3:
                return True

    if perm <= 2:  # moderators
        for role in member.roles:
            if str(role.id) in rank_2:
                return True

    if perm <= 1:  # normal
        for role in member.roles:
            if str(role.id) in rank_1 + rank_2:
                return True

    return False


EVERYONE = 0
NORMAL = 1
MODS = 2
OWNERS = 3
DEV = 4
