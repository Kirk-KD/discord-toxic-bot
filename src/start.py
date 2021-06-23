from src.bot.data import guilds_data
import datetime


for guild in guilds_data.all():
    d = guild["data"]
    d["giveaways"] = {}
    guilds_data.set(guild["_id"], {"data": d})
