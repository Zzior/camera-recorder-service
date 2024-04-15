from pathlib import Path
from logging import Logger  # , INFO, ERROR, WARNING

from src.classes.base.notify_writer import BaseNotifyWriter
from src.classes.base.singleton import Singleton
from src.utils.ping import ping


class CameraManager(Singleton, BaseNotifyWriter):
    cameras: dict[str, str] = None
    save_dir: Path = None
    logger: Logger = None
    notify_manager = None
    notify_name = "Camera Status"

    def __init__(self, save_dir: Path, cameras: dict[str, str]):
        pass

    def init(self, save_dir, cameras) -> None:
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)

        self.cameras = cameras

    async def get_statuses(self) -> dict[str, bool]:
        result: dict[str, bool] = {}
        for camera, rtsp in self.cameras.items():
            status: bool = await ping(rtsp)
            result[camera] = status

        return result
