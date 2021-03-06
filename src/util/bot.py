from src.bot.data import guilds_data

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


async def get_infractions(member: discord.Member):
    """
    gets a member's infractions.

    :param member: Member
    :return: tuple[str, dict]
    """

    infractions = (await guilds_data.get(member.guild.id))["members"][str(member.id)]["infractions"][::-1]
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
