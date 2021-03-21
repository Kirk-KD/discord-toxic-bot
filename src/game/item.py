class Item:
    def __init__(self, name: str, description: str, effect: str):
        self.name = name
        self.description = description
        self.effect = effect

    async def use(self, message, player):
        print("MESSAGE WHEN PLAYER USE ITEM")
        raise NotImplementedError()
