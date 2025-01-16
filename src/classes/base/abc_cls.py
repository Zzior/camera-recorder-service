from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path

from classes.data_classes import ProcessInfo, RecordInfo


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
    async def notify(self, event_name: str, message: str, deferred: bool = True, d_time=2) -> None:
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


class AbstractRecordManager(ABC):
    cameras: dict[str, str]
    save_dir: Path
    logger: Logger
    notify_manager: AbstractNotifyManager
    notify_name: str

    active_records: dict[str, ProcessInfo]
    error_records: dict[str, ProcessInfo]

    @abstractmethod
    def init(self) -> None:
        """for the type annotation, fill in the arguments in __init__
        but the function should not do anything, since it should inherit from Singleton"""

        # initialization of a single instance should be here
        pass

    @abstractmethod
    async def process_watcher(self) -> None:
        pass

    @abstractmethod
    async def run_record(self, camera: str, duration: int) -> bool:
        pass

    @abstractmethod
    async def stop_record(self, camera: str) -> None:
        pass

    @abstractmethod
    def get_records_status(self) -> dict[str, RecordInfo]:
        pass
