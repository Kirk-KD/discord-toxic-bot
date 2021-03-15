"""
Command object
"""


class Command:
    """
    A command object that will be stored inside a CommandHandler
    """

    def __init__(self, func, perm: int, usage: str):
        """
        Initialises the Command

        :param func: function
        :param perm: int
        :param usage: str
        """

        self.call = func
        self.perm = perm
        self.name = self.call.__name__.strip("_")
        self.usage = usage
