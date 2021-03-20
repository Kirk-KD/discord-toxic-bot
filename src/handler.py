class Handler:
    def __init__(self):
        self.categories = []

    def add_category(self, category):
        self.categories.append(category())

    async def handle(self, message, client):
        msg = message.content.strip()[1:]
        args = msg.split()
        name = args.pop(0).lower()

        if command := self.get_command(name):
            await command(message, args, client)

    def get_command(self, name):
        for category in self.categories:
            if command := category.get_command(name):
                return command

        return None


handler = Handler()