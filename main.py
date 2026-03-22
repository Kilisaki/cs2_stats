import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode

from core.di_container import Container
from core.command_processor import CommandProcessor
from core.configs import config

from core.usecases.get_leetify_summary import GetLeetifySummary
from services.telegram_service.tg_bot_handlers import TgBotHandlers
from services.discord_service.ds_bot_handlers import DiscordHandlers

import discord
from discord.ext import commands

async def main() -> None:
    leetify_uc = GetLeetifySummary()

    logging.basicConfig(level=logging.INFO)

    container = Container()
    container.register_singleton("config", config)
    container.register_singleton("command_processor", CommandProcessor(leetify_uc))

    # Telegram
    router = Router()
    TgBotHandlers(router, container.resolve("command_processor"))
    dp = Dispatcher()
    dp.include_router(router)

    telegram_bot = Bot(token=config.get("TELEGRAM_BOT_API_KEY"))

    # Discord
    intents = discord.Intents.default()
    intents.message_content = True

    discord_bot = commands.Bot(
        command_prefix="!",
        intents=intents
    )

    container.register_singleton("discord_bot", discord_bot)

    DiscordHandlers(
        discord_bot,
        container.resolve("command_processor")
    )

    await asyncio.gather(
        dp.start_polling(telegram_bot),
        #discord_bot.start(config.get("DISCORD_BOT_API_KEY"))
    )


if __name__ == "__main__":
    asyncio.run(main())