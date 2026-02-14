from services.api_service.leetify_api import LeetifyAPI, LeetifyAPIDataWorker
import asyncio

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
    return data_worker.get_average_stats()

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)