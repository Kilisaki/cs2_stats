class DiscordHandlers:
    def __init__(self, bot, command_processor):
        self.bot = bot
        self.command_processor = command_processor
        self.prefix = "!"
        self.register()

    def register(self):

        @self.bot.event
        async def on_message(message):

            if message.author.bot:
                return

            text = message.content.strip()

            if not text.startswith(self.prefix):
                return

            command_text = text[len(self.prefix):]

            result = await self.command_processor.process(command_text)

            if result:
                await message.channel.send(result)