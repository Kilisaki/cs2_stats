import asyncio
import logging
from aiogram import Bot, Dispatcher
from services.configs import config
from . import tg_bot_handlers


class TelegramBot:
    """Простой фасад для запуска aiogram-бота (v3)."""

    def __init__(self, cfg=config):
        self.config = cfg
        self.logger = logging.getLogger(__name__)

        bot_token = self.config.get("TELEGRAM_BOT_API_KEY") or self.config.get("BOT_TOKEN")
        if not bot_token:
            raise ValueError("BOT_TOKEN не найден в конфигурации")

        # aiogram v3: Dispatcher создаётся без Bot.
        self.bot = Bot(bot_token)
        self.dp = Dispatcher()

        # Регистрируем обработчики сообщений.
        self.handlers = tg_bot_handlers.TgBotHandlers(self.dp)
        self.logger.info("Bot initialized successfully")

    def run(self) -> None:
        """Запуск long-polling."""
        asyncio.run(self.dp.start_polling(self.bot))
