from src.game.item import Item
from src.game.inv_slot import InvSlot
from src.dict_convertible import JSONSavable


class Inventory(JSONSavable):
    def __init__(self):
        self.inv = []

    def add_item(self, item: Item, amount: int=1):
        if slot := self.get_slot(item.name):
            slot.amount += amount
        else:
            self.inv.append(InvSlot(item, amount, self))

    def get_slot(self, item_name: str):
        for slot in self.inv:
            if slot.item.name == item_name:
                return slot

        return None

    def convert(self):
        return [slot.convert() for slot in self.inv]
