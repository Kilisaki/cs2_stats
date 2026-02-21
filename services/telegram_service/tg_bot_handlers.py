import logging
from aiogram import Dispatcher, types
from aiogram.filters import CommandStart

class TgBotHandlers:
    """Класс для обработки сообщений телеграм бота"""
    
    def __init__(self, dp: Dispatcher):
        self.dp = dp
        self.logger = logging.getLogger(__name__)
        self._register_handlers()
        
    def _register_handlers(self):
        """Регистрация всех обработчиков"""

        # Команда /start (aiogram v3)
        self.dp.message.register(self.cmd_start, CommandStart())
    
    async def cmd_start(self, message: types.Message):
        """Обработчик команды /start"""
        user_id = message.from_user.id
        await message.answer(
            f"👋 Привет, {message.from_user.first_name}!\n"
            "Я бот-помощник. Чем могу помочь?"
        )
        self.logger.info(f"User {user_id} started the bot")
