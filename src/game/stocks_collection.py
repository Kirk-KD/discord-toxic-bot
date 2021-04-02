from src.data import game_data
from src.game.stock import Stock


class StocksCollection:
    def __init__(self):
        self.data = game_data.data["stocks"]

    def get_stock(self, name: str):
        """
        gets a stock by name.

        :param name: str
        :return: Stock
        """

        for key, val in self.data.items():
            if name.lower().replace(" ", "") == key.lower().replace(" ", ""):
                return Stock(key, val)

        return None

    def update(self):
        """
        updates all of the stocks.

        :return: None
        """

        for name in self.data.keys():
            stock = self.get_stock(name)
            stock.update()
            self.data[name] = stock.record.copy()

    def get_stock_path(self, stock: Stock):
        """
        gets the path to a stock's image.

        :param stock: Stock
        :return: str
        """

        return "stock_graphs/{}.png".format(stock.name.lower().replace(" ", "_"))


stocks = StocksCollection()
