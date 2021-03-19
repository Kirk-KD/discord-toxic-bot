"""
commands under category "Fun"
"""

from src.command_handler import handler
from src.perms import *

from src.util.parser import *
from src.util.bot import *

import discord
import random
import os
import json
import requests
import youtube_search


@handler.add(
    [], perm=EVERYONE, usage="8ball <question>", category="Fun"
)
async def _8ball(message, args, client):
    if len(args) < 1:
        await message.reply("Gotta ask me something lol.", mention_author=False)
        return

    responses = [
        "Yes.", "No.", "Yeah!", "Nah.", "Definitely.", "Of course not.", "Ask again later.", "Very much yes.",
        "My creator says yes.", "My creator says no.", "Yes imo.", "Maybe...", "Very likely, yes",
        "Very doubtful.", "Don't count on it tho.", "Certainly!", "Better not tell u :smirk:",
        "You may regret it later tho...", "You'd better not get your hopes up.", "as long as you keep it a secret."
    ]
    await message.reply(":8ball: {}".format(random.choice(responses)), mention_author=False)


@handler.add(
    ["notjif"], perm=EVERYONE, usage="gif <search>", category="Fun"
)
async def gif(message, args, client):  # TODO: TRY TO CHANGE TO EMBED
    if len(args) < 1:
        await message.reply("Tell me what you want to search for.", mention_author=False)
        return

    search = " ".join(args)
    url = "https://g.tenor.com/v1/search?q={}&key={}&ContentFilter=high&media_filter=basic".format(
        search, os.getenv("TENOR")
    )
    response = requests.get(url).json()

    if len(response["results"]) == 0:
        await message.reply("No gif found on tenor lol.", mention_author=False)
        return

    res_gif = random.choice(response["results"])
    await message.reply("Here's a gif from tenor!\n{}".format(res_gif["url"]), mention_author=False)


@handler.add(
    ["yt"], perm=EVERYONE, usage="youtube <search>", category="Fun"
)
async def youtube(message, args, client):
    if len(args) < 1:
        await message.reply("What do you want to search on youtube lol.", mention_author=False)
        return

    search = " ".join(args)
    results = youtube_search.YoutubeSearch(search).to_dict()
    if len(results) == 0:
        await message.reply("No video found on youtube lol.", mention_author=False)
        return

    res = random.choice(results)
    await message.reply("https://youtube.com{}".format(res["url_suffix"]), mention_author=False)
