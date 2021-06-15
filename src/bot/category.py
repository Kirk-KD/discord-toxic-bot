import inspect


class Category:
    def __init__(self, name: str, description: str, hidden: bool = False):
        self.name = name
        self.description = description
        self.commands = []
        self.hidden = hidden

        command_names = [command_name for command_name in dir(self) if not command_name.startswith("__")]

        for command in command_names:
            if inspect.isclass(getattr(self, command)):
                c = getattr(self, command)()
                c.category = self
                self.commands.append(c)

    def get_command(self, name: str):
        for command in self.commands:
            if name in command.triggers:
                return command

        return None
