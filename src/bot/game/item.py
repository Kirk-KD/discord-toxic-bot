from src.bot.emojis import item_emoji


class Item:
    """
    an item in the game.
    """

    def __init__(self, display_name: str, reference_names: list[str], description: str,
                 price: int, is_usable: bool, is_purchasable: bool, is_sellable: bool, effect_stackable: bool = False):
        self.display_name = display_name
        self.reference_names = reference_names
        self.description = description
        self.price = price
        self.is_usable = is_usable
        self.is_purchasable = is_purchasable
        self.is_sellable = is_sellable
        self.effect_stackable = effect_stackable

    def use(self, player, message, client):
        """
        returns a Embed or str to be sent after performing actions to the player.
        raises NotImplementedError if is usable and not implemented in child classes.

        :param player: Player
        :param message: Message
        :param client: Toxic
        :return: str or Embed
        :raise: NotImplementedError
        """

        if self.is_usable:
            raise NotImplementedError("You forgot to implement this item IDIOT.")
        else:
            return "You can't use this item lol."

    def __str__(self):
        return "{} {}".format(
            item_emoji(self.display_name), self.display_name
        )
