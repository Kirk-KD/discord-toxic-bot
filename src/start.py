from src.bot.data import guilds_data


for guild in guilds_data.all():
    d = guild["data"]
    d["giveaways"] = {}
    guilds_data.set(guild["_id"], d)
