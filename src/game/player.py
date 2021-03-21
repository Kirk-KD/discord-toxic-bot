from src.game.inventory import Inventory
from src.game.item import Item
from src.dict_convertible import JSONSavable
from src.data import game_data


class Player(JSONSavable):
    def __init__(self, user_id: str):
        self.user_id = user_id

        self.level = 0
        self.exp = 0
        self.txc = 1000

        self.inventory = Inventory()

    def give_item(self, item: Item, amount: int=1):
        self.inventory.add_item(item, amount)

    def use_item(self, message, item_name: str):
        if slot := self.inventory.get_slot(item_name):
            slot.use(message, self)

    def convert(self):
        return {
            "level": self.level,
            "exp": self.exp,
            "txc": self.txc,
            "inv": self.inventory.convert()
        }

    def save_data(self):
        game_data.set_data(self.user_id, self.convert())
        game_data.update_data()
