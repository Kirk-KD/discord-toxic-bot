class Command:
    def __init__(self, triggers: list, usage: str, description: str, perm: int):
        self.triggers = triggers
        self.usage = usage
        self.description = description
        self.perm = perm

    async def __call__(self, message, args, client):
        raise NotImplementedError()
