from logging import Logger

from classes.base.abc_cls import AbstractNotifyWriter, AbstractNotifyManager


class BaseNotifyWriter(AbstractNotifyWriter):
    notify_manager: AbstractNotifyManager = None
    notify_name: str
    logger: Logger = None

    def init(self):
        """for the type annotation, fill in the arguments in __init__
        but the function should not do anything, since it should inherit from Singleton"""
        pass

    def configurate_notifier(self, notify_manager: AbstractNotifyManager = None, logger: Logger = None) -> None:
        if isinstance(notify_manager, AbstractNotifyManager):
            self.notify_manager = notify_manager
            self.notify_manager.add_event(self.notify_name)

        if isinstance(logger, Logger):
            self.logger = logger

    async def send_notify(self, notify_message: str, deferred: bool = True, d_time=2) -> None:
        if isinstance(self.notify_manager, AbstractNotifyManager):
            await self.notify_manager.notify(self.notify_name, notify_message, deferred, d_time)

    def write_log(self, log_info: str, log_level: int) -> None:
        if isinstance(self.logger, Logger):
            self.logger.log(log_level, log_info)
