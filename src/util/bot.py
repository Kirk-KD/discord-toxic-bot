from src.data import *

from src.util.time import *

import discord


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


def get_infractions(member: discord.Member):
    infractions = get_data("{}/members/{}/infractions".format(
        str(member.guild.id), str(member.id)
    ))[::-1]  # reversed because newest is always last
    counter = {
        "mute": 0,
        "warn": 0,
        "kick": 0,
        "ban": 0
    }
    res = []

    for inf in infractions:
        res.append("**{}** `{}` • {}".format(
            inf["action"], inf["reason"], inf["time"]
        ))
        counter[inf["action"].lower()] += 1

    # res = ["**{}** {} • {}".format(
    #     inf["action"], inf["reason"], inf["time"]
    # ) for inf in infractions]
    # res = "\n".join((res[:14] if len(res) >= 15 else res))  # 15 max

    return "\n".join(res), counter
