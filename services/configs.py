import dotenv
from pathlib import Path
from typing import Optional, Any
import os

class Config:
    """Единый интерфейс для работы с конфигурацией"""
    _instance: Optional['Config'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self) -> None:
        """Загрузка переменных окружения"""
        try:
            dotenv.load_dotenv(".env")
            print("Y Конфигурация успешно загружена")
        except Exception as e:
            print(f" Ошибка при загрузке .env файла: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получить значение переменной окружения"""
        return os.getenv(key, default)
    
    @property
    def database_url(self) -> str:
        """Пример специфического свойства"""
        return self.get("DATABASE_URL", "sqlite:///default.db")
    
# Создаем глобальный экземпляр для удобства
config = Config()
print(config.get("TELEGRAM_BOT_API_KEY"))