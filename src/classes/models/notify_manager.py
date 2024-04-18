import asyncio
from logging import Logger

from aiogram import Bot

from src.classes.base.abc_cls import AbstractNotifyManager
from src.classes.base.singleton import Singleton

from src.const.logs_strings import SEND_NOTIFY_ERR_LOG


class NotifyManager(AbstractNotifyManager, Singleton):
    events = {}
    bot = None
    logger = None
    deferred_messages: dict[str, str] = {}
    deferred_status = False

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

    async def notify(self, event_name: str, message: str, deferred: bool = True, d_time=2) -> None:
        if deferred and self.deferred_status:
            self.deferred_messages[event_name] += f"\n{message}"

        elif deferred:
            self.deferred_messages[event_name] = message
            self.deferred_status = True
            task = asyncio.create_task(self.deferred_notify(d_time))

        else:
            for tg_id in self.events[event_name]:
                try:
                    await self.bot.send_message(chat_id=tg_id, text=message)
                except Exception as e:
                    self.logger.error(SEND_NOTIFY_ERR_LOG.format(name=event_name, id=tg_id, e=e))

    async def deferred_notify(self, d_time: int = 2) -> None:
        await asyncio.sleep(d_time)
        copy = self.deferred_messages.copy()
        self.deferred_messages = {}
        self.deferred_status = False

        for event_name, messages in copy.items():
            await self.notify(event_name=event_name, message=messages, deferred=False)

