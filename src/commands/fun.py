from src.category import Category
from src.command import Command
from src.handler import handler
from src import perms

import random
import os
import requests
import youtube_search


class Fun(Category):
    def __init__(self):
        super().__init__("Fun", "Things that you might find... fun.")

    class EightBall(Command):
        def __init__(self):
            super().__init__(
                ["8ball"], "8ball <question>",
                "Having trouble deciding on something?", perms.EVERYONE
            )

        async def __call__(self, message, args, client):
            if len(args) < 1:
                await message.reply("Gotta ask me something lol.", mention_author=False)
                return

            responses = [
                "Yes.", "No.", "Yeah!", "Nah.", "Definitely.", "Of course not.", "Ask again later.", "Very much yes.",
                "My creator says yes.", "My creator says no.", "Yes imo.", "Maybe...", "Very likely, yes",
                "Very doubtful.", "Don't count on it tho.", "Certainly!", "Better not tell u :smirk:",
                "You'd better not get your hopes up.", "as long as you keep it a secret.", "nah."
            ]
            await message.reply(":8ball: {}".format(random.choice(responses)), mention_author=False)

    class Gif(Command):
        def __init__(self):
            super().__init__(
                ["gif", "notjif"], "gif <search>",
                "Finds a GIF on Tenor. Also don't you dare call it jif.", perms.EVERYONE
            )

        async def __call__(self, message, args, client):
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

    class Youtube(Command):
        def __init__(self):
            super().__init__(
                ["youtube", "yt"], "youtube <search>",
                "Finds a video on Youtube.", perms.EVERYONE
            )

        async def __call__(self, message, args, client):
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


handler.add_category(Fun)
