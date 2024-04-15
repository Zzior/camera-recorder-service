from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class QueryFilter(BaseFilter):
    def __init__(self, query_list: list[str] | tuple[str]) -> None:
        self.query_list = query_list

    async def __call__(self, query: CallbackQuery) -> bool:
        if query.data in self.query_list:
            return True

        return False


class MessageFilter(BaseFilter):
    def __init__(self, message_list: list[str] | tuple[str]) -> None:
        self.message_list = message_list

    async def __call__(self, message: Message) -> bool:
        if message.text in self.message_list:
            return True

        return False
