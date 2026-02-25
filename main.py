import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode

from core.di_container import Container
from core.command_processor import CommandProcessor
from core.configs import config

from core.usecases.get_leetify_summary import GetLeetifySummary
from services.telegram_service.tg_bot_handlers import TgBotHandlers


async def main() -> None:
    leetify_uc = GetLeetifySummary()

 
    logging.basicConfig(level=logging.INFO)

    container = Container()

    container.register_singleton("config", config)
    container.register_singleton("command_processor", CommandProcessor(leetify_uc))



    bot_token = config.get("TELEGRAM_BOT_API_KEY")
    if not bot_token:
        raise RuntimeError("TELEGRAM_BOT_API_KEY is not set in .env")

    bot = Bot(token=bot_token)
    router = Router()

    # Поднимаем хендлеры Telegram
    TgBotHandlers(router, container.resolve("command_processor"))

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())