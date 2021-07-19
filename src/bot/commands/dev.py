from src.bot.category import Category
from src.bot.data import stocks_data
from src.bot.command import DevCommand
from src.bot.game.game_manager import manager
from src.bot.game.shop import shop
from src.bot.game.stocks_collection import stocks
from src.bot.handler import handler
from src.util.parser import parse_member, parse_int
from src.logger import logger


class Dev(Category):
    def __init__(self):
        super().__init__("Dev", "Developer only.", hidden=True)

    class Chain(DevCommand):
        def __init__(self):
            super().__init__(["chain"])

        async def __call__(self, message, args, client):
            commands = " ".join(args).strip(";").split(";")
            for command in commands:
                await handler.handle(message, client, content=command)

    class ResetStocks(DevCommand):
        def __init__(self):
            super().__init__(["resetstocks", "rs"])

        async def __call__(self, message, args, client):
            for stock in await stocks_data.all():
                await stocks_data.set(stock["_id"], {"data": []})

            await stocks.update()

            await message.reply("> Stocks data reset.", mention_author=False)

    class ResetBalance(DevCommand):
        def __init__(self):
            super().__init__(["resetbalance", "rb"])

        async def __call__(self, message, args, client):
            if len(args) > 0:
                target = parse_member(message.guild, args[0])
                player = await manager.get_player(target) if target else None
                if player:
                    player.data["stats"]["txc"] = 0
                    player.data["bank"]["curr"] = 200
                    player.data["bank"]["max"] = 1000
                    await player.update_data()

                    await message.reply("> Player balance cleared.", mention_author=False)

    class UpdateStocks(DevCommand):
        def __init__(self):
            super().__init__(["updatestocks", "us"])

        async def __call__(self, message, args, client):
            await stocks.update()

            await message.reply("> Forced stock update.", mention_author=False)

    class DataWipe(DevCommand):
        def __init__(self):
            super().__init__(["datawipe"])

        async def __call__(self, message, args, client):
            if len(args) != 0:
                # if args[0].lower() == "game": TODO
                #     jsons.write_json("data/game.json", {})
                # elif args[0].lower() == "guilds":
                #     jsons.write_json("data/guilds.json", {})

                await message.reply("> Reboot required. Commands will be disabled until reboot.", mention_author=False)
                handler.categories = []

    class ForceGive(DevCommand):
        def __init__(self):
            super().__init__(["forcegive", "fgive"])

        async def __call__(self, message, args, client):
            if len(args) >= 3:
                target = parse_member(message.guild, args[0])
                player = await manager.get_player(target) if target else None
                amount = parse_int(args[-1])
                item = shop.get_item(" ".join(args[1:(-1 if amount else len(args))]))

                if player and amount and item:
                    player.give_item(item, amount)
                    await player.update_data()
                    await message.reply("> Given {} {} **{}**.".format(target, amount, item), mention_author=False)

    class ForceError(DevCommand):
        def __init__(self):
            super().__init__(["forceerror", "ferror"])

        async def __call__(self, message, args, client):
            raise Exception(" ".join(args) if len(args) else "Forced error.")

    class Log(DevCommand):
        def __init__(self):
            super().__init__(["log"])

        async def __call__(self, message, args, client):
            logger.info(" ".join(args))

    class Count(DevCommand):
        def __init__(self):
            super().__init__(["count"])

        async def __call__(self, message, args, client):
            await message.reply("> There are {} guilds.".format(len(client.guilds)), mention_author=False)
            await message.author.send("\n".join([g.name for g in client.guilds]))

    class Trigger(DevCommand):
        def __init__(self):
            super().__init__(["trigger"])

        async def __call__(self, message, args, client):
            """triggers a temporary command for testing purposes."""

            # print(client.get_user(422087909634736160))

            return


handler.add_category(Dev)
