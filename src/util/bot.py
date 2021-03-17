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
        "ban": 0,
        "total": 0
    }
    res = []

    for inf in infractions:
        res.append("**{}** • {}\n`{}`\n".format(
            inf["action"], inf["time"], inf["reason"]
        ))
        counter[inf["action"].lower()] += 1
        counter["total"] += 1

    res = "\n".join(res[:9] if len(res) > 10 else res)

    return res, counter


def get_user_info(member: discord.Member, message: discord.Message):
    embed = discord.Embed(
        color=discord.Color.blue()
    ).set_author(
        name="User info of {}".format(member),
        icon_url=member.avatar_url
    ).add_field(
        name="User Name",
        value="{} ({})".format(member.display_name, member)
    ).add_field(
        name="User ID",
        value=member.id
    ).add_field(
        name="Infractions",
        value=get_infractions(member)[1]["total"]
    ).add_field(
        name="Joined Server",
        value=format_time(member.joined_at)
    ).add_field(
        name="Joined Discord",
        value=format_time(member.created_at)
    ).add_field(
        name="Boosting Since",
        value=format_time(p) if (p := member.premium_since) else "Not Boosting"
    ).set_footer(
        text="Requested by {}".format(signature(message.author))
    )

    return embed
