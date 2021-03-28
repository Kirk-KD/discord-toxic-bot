import discord

emojis = {
    "Apple":        825745714608340992,
    "Chocolate":    825745748829929493
}


def item_emoji(item_name: str):
    if item_name in emojis.keys():
        return "<:g_{}:{}>".format(item_name.lower().replace(" ", "_"), emojis[item_name])
    else:
        return "<:g_place_holder:825758386963349535>"