from src import perms
from src.category import Category
from src.data import guilds_data, game_data
from src.command import Command
from src.game.stocks_collection import stocks
from src.handler import handler


class Dev(Category):
    def __init__(self):
        super().__init__("Dev", "Developer only.", hidden=True)

    class ResetStocks(Command):
        def __init__(self):
            super().__init__(["resetstocks"], "resetstocks", "Reset stocks.", perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            for key in game_data.data["stocks"].keys():
                game_data.data["stocks"][key] = []

            stocks.update()
            game_data.update_data()

            await message.reply("> Stocks data reset.", mention_author=False)

    class UpdateStocks(Command):
        def __init__(self):
            super().__init__(["updatestocks"], "updatestocks", "update stocks.", perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            stocks.update()
            game_data.update_data()

            await message.reply("> Forced stock update.", mention_author=False)


handler.add_category(Dev)
