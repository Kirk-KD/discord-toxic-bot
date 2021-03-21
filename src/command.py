from src.perms import perm_names


class Command:
    def __init__(self, triggers: list, usage: str, description: str, perm: int):
        self.triggers = triggers
        self.name = self.triggers[0]
        self.usage = usage
        self.description = description
        self.perm = perm

    async def __call__(self, message, args, client):
        raise NotImplementedError()

    def format_help(self):
        return "{} {}\n{}{}\n\n".format(
            "**{}** {}".format(
                self.usage.split()[0], "{}".format(
                    " ".join(self.usage.split()[1:])
                ) if len(self.usage.split()) != 1 else ""
            ), "`{} Only`".format(perm_names[self.perm]) if self.perm else "",
            "*{}*".format(self.description),
            "\naliases: {}".format(
                "**{}**".format(", ".join(self.triggers[1:]))
            ) if len(self.triggers) > 1 else ""
        )
