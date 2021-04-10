from src.bot.data import stocks_data
from src.bot.game.stock import Stock


class StocksCollection:
    def __init__(self):
        self.data = stocks_data.all()

    def get_stock(self, name: str):
        """
        gets a stock by name.

        :param name: str
        :return: Stock
        """

        for stock in stocks_data.all():
            if (name.lower().replace(" ", "") == stock["_id"].lower().replace(" ", "") or
                    name.lower().split()[0] == stock["_id"].lower().split()[0]):
                return Stock(stock["_id"], stock["data"])

        return None

    def update(self):
        """
        updates all of the stocks.

        :return: None
        """

        for s in stocks_data.all():
            stock = self.get_stock(s["_id"])
            stock.update()
            stocks_data.set(s["_id"], {"data": stock.record.copy()})

    def get_stock_path(self, stock: Stock):
        """
        gets the path to a stock's image.

        :param stock: Stock
        :return: str
        """

        return "stock_graphs/{}.png".format(stock.name.lower().replace(" ", "_"))


stocks = StocksCollection()
