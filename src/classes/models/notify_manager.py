from logging import Logger

from aiogram import Bot

from src.classes.base.abc_cls import AbstractNotifyManager
from src.classes.base.singleton import Singleton


class NotifyManager(AbstractNotifyManager, Singleton):
    events = {}
    bot = None
    logger = None

    def configurate(self,  bot: Bot, loger: Logger, events: dict[str, list[int]] = None):
        self.events = events if events is not None else {}
        self.bot = bot
        self.logger = loger

    def subscribe(self, event_name: str, tg_id: int) -> None:
        if (event_name in self.events) and (tg_id not in self.events[event_name]):
            self.events[event_name].append(tg_id)

    def unsubscribe(self, event_name: str, tg_id: int) -> None:
        if (event_name in self.events) and (tg_id in self.events[event_name]):
            self.events[event_name].remove(tg_id)

    def add_event(self, event_name: str) -> None:
        if event_name not in self.events:
            self.events[event_name] = []

    async def notify(self, event_name: str, message: str) -> None:
        for tg_id in self.events[event_name]:
            try:
                await self.bot.send_message(chat_id=tg_id, text=message)
            except Exception as e:
                self.logger.error(f"Error while notifying\nevent: {event_name}\ntg_id: {tg_id}\nException: {e}")
