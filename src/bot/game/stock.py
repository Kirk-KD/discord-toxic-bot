import io
import random
from math import exp, sqrt
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

from src.bot.data import stocks_data


class Stock:
    def __init__(self, name: str, record: list[int]):
        self.max_record = 24 * 3
        self.name = name
        self.gbm = create_gbm(100, 0.01, 0.09)
        self.record = [self.gbm() for _ in range(self.max_record)] if len(record) == 0 else record.copy()
        self.current = self.record[-1]

    async def update(self):
        self.record.append(self.gbm())
        if len(self.record) > self.max_record:
            self.record.pop(0)

        await stocks_data.set(self.name, {"data": self.record})

    def get_graph(self):
        marker_type = ("->" if self.record[-1] == self.record[-2] else
                       ("-^" if self.record[-1] >= self.record[-2] else "-v"))

        fg = Figure()
        ax = fg.gca()
        ax.plot(self.record, marker_type, markevery=[len(self.record) - 1])
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        graph_data = io.BytesIO()
        fg.savefig(graph_data)
        graph_data.seek(0)
        return graph_data


# https://towardsdatascience.com/create-a-stock-price-simulator-with-python-b08a184f197d
def create_gbm(s0, mu, sigma):
    st = s0

    def generate_value():
        nonlocal st

        st *= exp(
            (mu - 0.5 * sigma ** 2) * (1. / 365.) + sigma * sqrt(1. / 365.)
            * random.gauss(mu=0.001, sigma=random.triangular(1, 5, 1))
        )
        return round(st)

    return generate_value
