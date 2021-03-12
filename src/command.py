"""
Command object
"""


class Command:
    """
    A command object that will be stored inside a CommandHandler
    """

    def __init__(self, func, perm: int):
        """
        Initialises the Command

        :param func: function
        :param perm: int
        """

        self.call = func
        self.perm = perm
