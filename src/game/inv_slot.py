from src.game.item import Item
from src.dict_convertible import JSONSavable


class InvSlot(JSONSavable):
    def __init__(self, item: Item, amount: int, inv):
        self.item = item
        self.amount = amount
        self.inv = inv

    async def use(self, message, player):
        self.amount -= 1
        await self.item.use(message, player)

        if self.amount == 0:
            self.inv.inv.remove(self)

    def convert(self):
        return {
            "name": self.item.name,
            "amount": self.amount
        }
