from src.bot import perms
from src.bot.category import Category
from src.bot.data import stocks_data
from src.bot.command import Command
from src.bot.game.game_manager import manager
from src.bot.game.shop import shop
from src.bot.game.stocks_collection import stocks
from src.bot.handler import handler
from src.util.parser import parse_member, parse_int
from src.logger import logger


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
            for stock in stocks_data.all():
                stocks_data.set(stock["_id"], {"data": []})

            stocks.update()

            await message.reply("> Stocks data reset.", mention_author=False)

    class ResetBalance(Command):
        def __init__(self):
            super().__init__(["resetbalance", "rb"], "resetbalance <user>", "Reset a user's balance.",
                             perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            if len(args) > 0:
                target = parse_member(message.guild, args[0])
                player = manager.get_player(target) if target else None
                if player:
                    player.data["stats"]["txc"] = 0
                    player.data["bank"]["curr"] = 200
                    player.data["bank"]["max"] = 1000
                    player.update_data()

                    await message.reply("> Player balance cleared.", mention_author=False)

    class UpdateStocks(Command):
        def __init__(self):
            super().__init__(["updatestocks", "us"], "updatestocks", "update stocks.", perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            stocks.update()

            await message.reply("> Forced stock update.", mention_author=False)

    class DataWipe(Command):
        def __init__(self):
            super().__init__(["datawipe"], "datawipe [\"game\" or \"guilds\"]", "Data wipe.", perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            if len(args) != 0:
                # if args[0].lower() == "game": TODO
                #     jsons.write_json("data/game.json", {})
                # elif args[0].lower() == "guilds":
                #     jsons.write_json("data/guilds.json", {})

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
                    player.update_data()
                    await message.reply("> Given {} {} **{}**.".format(target, amount, item), mention_author=False)

    class ForceError(Command):
        def __init__(self):
            super().__init__(["forceerror", "ferror"], "forceerror <msg>", "Cause an error.", perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            raise Exception(" ".join(args) if len(args) else "Forced error.")

    class Log(Command):
        def __init__(self):
            super().__init__(["log"], "log <msg>", "Log an message.", perm=perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            logger.info(" ".join(args))

    class Count(Command):
        def __init__(self):
            super().__init__(["count"], "count", "count servers.", perms.GLOBAL_DEV)

        async def __call__(self, message, args, client):
            await message.reply("> There are {} guilds.".format(len(client.guilds)), mention_author=False)
            await message.author.send("\n".join([g.name for g in client.guilds]))


handler.add_category(Dev)
