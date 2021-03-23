import discord


class Item:
    """
    an object representing an item in the game
    """

    def __init__(self, name: str, ref_names: list[str], description: str, usable: bool):
        self.name = name
        self.ref_names = ref_names
        self.description = description
        self.usable = usable

    async def use(self, message: discord.Message):
        """
        if the item is usable, raise NotImplementedError if a child class does not override this method

        :param message: Message
        :return: None
        """

        if self.usable:
            raise NotImplementedError()
        else:
            await message.reply("You can't use that lol.", mention_author=False)
