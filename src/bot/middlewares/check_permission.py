from aiogram import BaseMiddleware, types
from typing import Dict, Any, Awaitable, Callable


class AdminChecker(BaseMiddleware):
    def __init__(self, admins: list[int]):
        self.admins = admins

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        if self.admins and user_id not in self.admins:
            await event.answer("You not have permission!")
            return
        return await handler(event, data)
