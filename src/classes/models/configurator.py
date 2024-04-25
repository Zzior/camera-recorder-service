from pathlib import Path

from src.classes.base.data_save import BaseDataSave
from src.classes.base.singleton import Singleton


class Configurator(Singleton, BaseDataSave):
    empty_data = {"admins": {}, "cameras": {}, "notifications": {}}
    admins: dict[str, int]
    cameras: dict[str, str]
    notifications: dict[str, list]

    def __init__(self, config_path: Path) -> None:
        pass

    def init(self, config_path: Path) -> None:
        BaseDataSave.init(self=self, config_path=config_path)
        # Создаём ссылки на списки внутри config
        self.admins: dict[str, int] = self._config.setdefault("admins", {})
        self.cameras: dict[str, str] = self._config.setdefault("cameras", {})
        self.notifications: dict[str, list] = self._config.setdefault("notifications", {})

    def add_admin(self, name: str, tg_id: int):
        self.admins[name] = tg_id
        self.save_config()

    def delete_admin(self, name):
        self.admins.pop(name)
        self.save_config()

    def add_camera(self, name: str, rtsp: str) -> None:
        self.cameras[name] = rtsp
        self.save_config()

    def delete_camera(self, name: str) -> None:
        self.cameras.pop(name)
        self.save_config()

