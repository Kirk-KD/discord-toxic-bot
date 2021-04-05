from src import perms
from src.category import Category
from src.data import guilds_data, game_data
from src.command import Command
from src.game.game_manager import manager
from src.game.shop import shop
from src.game.stocks_collection import stocks
from src.handler import handler
from src.util import jsons
from src.util.parser import parse_member, parse_int


class Dev(Category):
    def __init__(self):
        super().__init__("Dev", "Developer only.", hidden=True)

    class Chain(Command):
        def __init__(self):
            super().__init__(["chain"], "chain <command... sep=;>", "chain commands.", perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            commands = " ".join(args).strip(";").split(";")
            for command in commands:
                await handler.handle(message, client, content=command)

    class ResetStocks(Command):
        def __init__(self):
            super().__init__(["resetstocks", "rs"], "resetstocks", "Reset stocks.", perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            for key in game_data.data["stocks"].keys():
                game_data.data["stocks"][key] = []

            stocks.update()
            game_data.update_data()

            await message.reply("> Stocks data reset.", mention_author=False)

    class UpdateStocks(Command):
        def __init__(self):
            super().__init__(["updatestocks", "us"], "updatestocks", "update stocks.", perm=perms.GLOBAL_DEV)

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

    class ForceGive(Command):
        def __init__(self):
            super().__init__(["forcegive", "fgive"], "forcegive <user> <item> <amount>", "Give item.",
                             perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            if len(args) >= 3:
                target = parse_member(message.guild, args[0])
                player = manager.get_player(target) if target else None
                amount = parse_int(args[-1])
                item = shop.get_item(" ".join(args[1:(-1 if amount else len(args))]))

                if player and amount and item:
                    player.give_item(item, amount)
                    game_data.update_data()
                    await message.reply("> Given {} {} **{}**.".format(target, amount, item), mention_author=False)


handler.add_category(Dev)
