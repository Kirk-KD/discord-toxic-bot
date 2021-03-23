class Item:
    def __init__(self, name: str, ref_names: list[str], description: str, usable: bool):
        self.name = name
        self.ref_names = ref_names
        self.description = description
        self.usable = usable

    async def use(self, message):
        if self.usable:
            raise NotImplementedError()
        else:
            await message.reply("You can't use that lol.", mention_author=False)
