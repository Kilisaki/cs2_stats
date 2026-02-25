from typing import Callable, Dict, Tuple, Awaitable


class CommandProcessor:
    """
    Асинхронный мультиплатформенный обработчик команд.
    Поддерживает / ! ? префиксы.
    """

    def __init__(self, leetify_service) -> None:
        self.leetify_service = leetify_service
        self._commands: Dict[
            str, Callable[[Tuple[str, ...]], Awaitable[str]]
        ] = {}

        self._register_builtin()

    def _register_builtin(self) -> None:
        self.register("start", self._start)
        self.register("help", self._help)
        self.register("allstats", self._allstats)

    def register(
        self,
        name: str,
        handler: Callable[[Tuple[str, ...]], Awaitable[str]],
    ) -> None:
        self._commands[name.lower()] = handler

    def _parse(self, text: str) -> Tuple[str, Tuple[str, ...]]:
        normalized = text.strip()
        if not normalized:
            return "", tuple()

        while normalized and normalized[0] in {"/", "!", "?"}:
            normalized = normalized[1:]

        parts = normalized.split()
        command = parts[0].lower() if parts else ""
        args = tuple(parts[1:])
        return command, args

    async def process(self, text: str) -> str:
        command, args = self._parse(text)

        if not command:
            return "Я не понял команду. Напишите /help"

        handler = self._commands.get(command)
        if not handler:
            return f"Неизвестная команда '{command}'. Попробуйте /help"

        return await handler(args)

    # ===== BUILTIN COMMANDS =====

    async def _start(self, args: Tuple[str, ...]) -> str:
        return "Бот готов. Используйте /allstats <steam64_id>"

    async def _help(self, args: Tuple[str, ...]) -> str:
        return "Доступные команды:\n/start\n/help\n/allstats <steam64_id>"

    async def _allstats(self, args: Tuple[str, ...]) -> str:
        if not args:
            return "Использование: /allstats <steam64_id>"

        steam64_id = args[0]

        data = await self.leetify_service.execute(steam64_id)
        if not data:
            return "Не удалось получить данные."

       # player = data.get("player", {})
        #summary = data.get("summary", {})

        return data