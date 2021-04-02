import random
from math import exp, sqrt
import matplotlib.pyplot as plt


class Stock:
    def __init__(self, name: str, record: list[int]):
        self.max_record = 24 * 3
        self.name = name
        self.gbm = create_gbm(100, 0.01, 0.09)
        self.record = [self.gbm() for _ in range(self.max_record)] if len(record) == 0 else record.copy()
        self.current = self.record[-1]

    def update(self):
        g = self.gbm()
        self.record.append(g)
        if len(self.record) > self.max_record:
            self.record.pop(0)

        self.save_graph()
        return g

    def save_graph(self):
        marker_type = ("->" if self.record[-1] == self.record[-2] else
                       ("-^" if self.record[-1] >= self.record[-2] else "-v"))
        plt.plot(self.record, marker_type, markevery=[len(self.record) - 1])
        plt.savefig("stock_graphs/{}.png".format(self.name.lower().replace(" ", "_")))
        plt.close("all")


# https://towardsdatascience.com/create-a-stock-price-simulator-with-python-b08a184f197d
def create_gbm(s0, mu, sigma):
    st = s0

    def generate_value():
        nonlocal st

        st *= exp((mu - 0.5 * sigma ** 2) * (1. / 365.) + sigma * sqrt(1. / 365.) * random.gauss(mu=0, sigma=1))
        return round(st)

    return generate_value
