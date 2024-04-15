from abc import ABC, abstractmethod
from logging import Logger


class AbstractNotifyManager(ABC):
    @abstractmethod
    def subscribe(self, event_name: str, listener: int) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, event_name: str, listener: int) -> None:
        pass

    @abstractmethod
    def add_event(self, event_name: str) -> None:
        pass

    @abstractmethod
    async def notify(self, event_name: str, message: str) -> None:
        pass


class AbstractNotifyWriter(ABC):
    notify_manager: AbstractNotifyManager
    notify_name: str
    logger: Logger

    @abstractmethod
    def init(self) -> None:
        """for the type annotation, fill in the arguments in __init__
        but the function should not do anything, since it should inherit from Singleton"""

        # initialization of a single instance should be here
        pass

    @abstractmethod
    def configurate_notifier(self, notify_manager: AbstractNotifyManager = None, logger: Logger = None) -> None:
        pass

    @abstractmethod
    async def send_notify(self, notify_message: str) -> None:
        pass

    @abstractmethod
    def write_log(self, log_info: str, log_level: int) -> None:
        pass
