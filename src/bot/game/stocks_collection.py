from src.bot.data import stocks_data
from src.bot.game.stock import Stock


class StocksCollection:
    """
    a wrapper for stocks_data.
    """

    async def all(self):
        return await stocks_data.all()

    async def get_stock(self, name: str):
        """
        gets a stock by name.

        :param name: str
        :return: Stock
        """

        for stock in await stocks_data.all():
            if (name.lower().replace(" ", "") == stock["_id"].lower().replace(" ", "") or
                    name.lower().split()[0] == stock["_id"].lower().split()[0]):
                return Stock(stock["_id"], stock["data"])

        return None

    async def update(self):
        """
        updates all of the stocks.

        :return: None
        """

        for s in await stocks_data.all():
            stock = await self.get_stock(s["_id"])
            await stock.update()


stocks = StocksCollection()
