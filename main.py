import asyncio
from services.api_service.leetify_api import LeetifyAPI, LeetifyAPIDataWorker
from services.telegram_service.tg_bot import TelegramBot
from services.configs import config

async def main():
    steam_id = "76561199090532443"
    # Создаем экземпляр API
    api = LeetifyAPI(steam_id)
    
    # Получаем данные о матчах
    matches = await api.get_matches(limit=30)  # Увеличил лимит до 30,
    
    if matches is None:
        print("Не удалось получить данные от API")
        return
    
    # Создаем обработчик данных
    data_worker = LeetifyAPIDataWorker(matches_data=matches)
    
    # Получаем и возвращаем статистику
    #return data_worker.get_matches_stats_summary()
    return data_worker.get_all_match_ids()


if __name__ == "__main__":
    # Создаем и запускаем проект
    asyncio.run(main())
    bot = TelegramBot(config)
    bot.run()
