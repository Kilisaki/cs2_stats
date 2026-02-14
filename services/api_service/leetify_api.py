import aiohttp
from typing import Optional, List, Dict, Any, Union

class LeetifyAPI:
    """
    Асинхронный клиент для работы с API Leetify.
    
    Args:
        steam64_id (str): Steam64 ID игрока
    """
    
    BASE_URL = "https://api-public.cs-prod.leetify.com/v3"

    def __init__(self, steam64_id: str):
        self.steam64_id = steam64_id
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Контекстный менеджер для автоматического создания сессии."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер для автоматического закрытия сессии."""
        if self.session:
            await self.session.close()

    async def _get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Внутренний метод для выполнения GET-запросов.
        
        Args:
            endpoint (str): Конечная точка API
            params (Dict, optional): Параметры запроса
            
        Returns:
            Optional[Dict]: JSON-ответ от API или None при ошибке
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()
            
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Ошибка запроса: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None

    async def get_matches(self, limit: int = 10) -> Optional[Dict]:
        """
        Получение последних матчей игрока.
        
        Args:
            limit (int): Количество матчей (по умолчанию 10)
            
        Returns:
            Optional[Dict]: Данные о матчах или None при ошибке
        """
        endpoint = "profile/matches"
        params = {
            "steam64_id": self.steam64_id,
            "limit": limit
        }
        return await self._get(endpoint, params=params)


class LeetifyAPIDataWorker:
    """
    Класс для обработки данных, полученных от API Leetify.
    
    Args:
        matches_data (Union[List[Dict], Dict]): Данные о матчах, полученные из API
    """
    
    def __init__(self, matches_data: Union[List[Dict], Dict]):
        # Обрабатываем оба варианта: список матчей или объект с ключом "matches"
        if isinstance(matches_data, dict) and "matches" in matches_data:
            self.matches_data = matches_data["matches"]
        elif isinstance(matches_data, list):
            self.matches_data = matches_data
        else:
            self.matches_data = []
            print(f"Предупреждение: Неподдерживаемый формат данных: {type(matches_data)}")

    def print_match_ids_quick(self) -> None:
        """Быстрый вывод ID всех матчей в консоль."""
        match_ids = [str(match["id"]) for match in self.matches_data if "id" in match]
        print(", ".join(match_ids))
    
    def get_all_match_ids(self) -> List[str]:
        """
        Получить список всех ID матчей.
        
        Returns:
            List[str]: Список ID матчей
        """
        return [str(match["id"]) for match in self.matches_data if "id" in match]

    def get_top_matches(self, limit: int = 5) -> List[Dict]:
        """
        Получить топ-N матчей по рейтингу Leetify.
        
        Args:
            limit (int): Количество матчей в топе (по умолчанию 5)
            
        Returns:
            List[Dict]: Отсортированный список матчей
        """
        # Фильтруем матчи с рейтингом в stats
        matches_with_rating = [
            match for match in self.matches_data 
            if match.get("stats") and len(match["stats"]) > 0 
            and match["stats"][0].get("leetify_rating") is not None
        ]
        
        # Сортируем по рейтингу (по убыванию)
        sorted_matches = sorted(
            matches_with_rating, 
            key=lambda x: x["stats"][0]["leetify_rating"], 
            reverse=True
        )
        return sorted_matches[:limit]

    def get_matches_stats_summary(self) -> Dict[str, Any]:
        """
        Получить краткую статистику по всем матчам.
        
        Returns:
            Dict[str, Any]: Словарь со статистикой:
                - total_matches: общее количество матчей
                - avg_kd: средний KD (Kills/Deaths)
                - avg_rating: средний рейтинг Leetify
                - total_kills: общее количество убийств
                - total_deaths: общее количество смертей
        """
        total_matches = len(self.matches_data)
        
        total_kills = 0
        total_deaths = 0
        total_rating = 0.0
        rated_matches = 0
        
        for match in self.matches_data:
            if match.get("stats") and len(match["stats"]) > 0:
                stats = match["stats"][0]  # Берем первый элемент stats (статистика игрока)
                
                if stats.get("total_kills") is not None:
                    total_kills += stats["total_kills"]
                    total_deaths += stats.get("total_deaths", 0)
                
                if stats.get("leetify_rating") is not None:
                    total_rating += stats["leetify_rating"]
                    rated_matches += 1
        
        avg_kd = total_kills / total_deaths if total_deaths > 0 else 0.0
        avg_rating = total_rating / rated_matches if rated_matches > 0 else 0.0
        
        return {
            "total_matches": total_matches,
            "avg_kd": round(avg_kd, 2),
            "avg_rating": round(avg_rating, 2),
            "total_kills": total_kills,
            "total_deaths": total_deaths
        }
    
    def get_player_info(self) -> Dict[str, Any]:
        """
        Получить информацию об игроке из первого матча.
        
        Returns:
            Dict[str, Any]: Информация об игроке (steam64_id, name)
        """
        if self.matches_data and len(self.matches_data) > 0 and self.matches_data[0].get("stats"):
            stats = self.matches_data[0]["stats"][0]
            return {
                "steam64_id": stats.get("steam64_id"),
                "name": stats.get("name")
            }
        return {}
    
    def get_matches_by_map(self, map_name: str) -> List[Dict]:
        """
        Получить матчи на определенной карте.
        
        Args:
            map_name (str): Название карты (например, 'de_dust2')
            
        Returns:
            List[Dict]: Список матчей на указанной карте
        """
        return [match for match in self.matches_data if match.get("map_name") == map_name]
    
    def get_average_stats(self) -> Dict[str, float]:
        """
        Получить средние статистические показатели по всем матчам.
        
        Returns:
            Dict[str, float]: Словарь со средними значениями метрик
        """
        stats_sum = {
            "preaim": 0.0,
            "reaction_time": 0.0,
            "accuracy": 0.0,
            "accuracy_head": 0.0,
            "counter_strafing_shots_good_ratio": 0.0,
            "dpr": 0.0,
            "total_kills": 0,
            "total_deaths": 0,
            "total_assists": 0,
            "total_damage": 0
        }
        
        count = 0
        
        for match in self.matches_data:
            if match.get("stats") and len(match["stats"]) > 0:
                stats = match["stats"][0]
                count += 1
                
                for key in stats_sum.keys():
                    if key in stats and stats[key] is not None:
                        stats_sum[key] += stats[key]
        
        if count > 0:
            return {key: round(value / count, 2) for key, value in stats_sum.items()}
        return {}