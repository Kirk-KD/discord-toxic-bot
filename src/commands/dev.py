from src import perms
from src.category import Category
from src.data import guilds_data, game_data
from src.command import Command
from src.game.stocks_collection import stocks
from src.handler import handler
from src.util import jsons


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

    class DataWipe(Command):
        def __init__(self):
            super().__init__(["datawipe"], "datawipe [\"game\" or \"guilds\"]", "Data wipe.", perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            if len(args) != 0:
                if args[0].lower() == "game":
                    jsons.write_json("data/game.json", {})
                elif args[0].lower() == "guilds":
                    jsons.write_json("data/guilds.json", {})

                await message.reply("> Reboot required. Commands will be disabled until reboot.", mention_author=False)
                handler.categories = []


handler.add_category(Dev)
