from src.bot.data import game_data


for player in game_data.all():
    d = player["data"]
    del d["streak"]
    game_data.set(player["_id"], {"data": d})
