"""Простой DI‑контейнер для приложения.

Предоставляет два типа регистрации:
- register_singleton: готовый экземпляр, который возвращается как есть.
- register_factory: функция, которая создаёт экземпляр при каждом вызове
  или кешируется при первом создании (lazy singleton).
"""

from typing import Any, Callable, Dict, Tuple


class Container:
    def __init__(self):
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Tuple[Callable[["Container"], Any], bool]] = {}

    def register_singleton(self, name: str, instance: Any) -> None:
        """Зарегистрировать готовый экземпляр."""
        self._singletons[name] = instance

    def register_factory(self, name: str, factory: Callable[["Container"], Any], *, cache: bool = False) -> None:
        """Зарегистрировать фабрику.

        Args:
            name: ключ для доступа через resolve.
            factory: функция, принимающая контейнер и возвращающая объект.
            cache: если True – создаёт lazy‑singleton.
        """

        self._factories[name] = (factory, cache)

    def resolve(self, name: str) -> Any:
        """Получить экземпляр по имени."""
        if name in self._singletons:
            return self._singletons[name]

        if name in self._factories:
            factory, cache = self._factories[name]
            instance = factory(self)
            if cache:
                self._singletons[name] = instance
            return instance

        raise KeyError(f"Service '{name}' is not registered in the container")
