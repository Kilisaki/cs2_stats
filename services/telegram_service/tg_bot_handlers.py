import logging
from aiogram import Dispatcher, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from core.command_processor import CommandProcessor


class TgBotHandlers:
    """Регистрирует aiogram v3 обработчики и прокидывает в них CommandProcessor."""

    def __init__(self, router: Router, cmd_processor: CommandProcessor):
        self.router = router
        self.cmd_processor = cmd_processor
        self.logger = logging.getLogger(__name__)
        self._register_handlers()

    def _register_handlers(self) -> None:
        # Aiogram v3: router.message.register
        # Любой текст с префиксом / ! ?
        self.router.message.register(self._handle_command_text, F.text.startswith(('/', '!', '?')))

    async def _handle_command_text(self, message: Message) -> None:
        response = await self.cmd_processor.process(message.text or "")
        await message.answer(response)
        self.logger.info("Command from %s: %s", message.from_user.id if message.from_user else "unknown", message.text)
