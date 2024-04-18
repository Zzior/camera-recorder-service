import asyncio
from pathlib import Path
from logging import Logger  # , INFO, ERROR, WARNING

from src.classes.base.notify_writer import BaseNotifyWriter
from src.classes.base.singleton import Singleton
from src.utils.ping import ping


class CameraManager(Singleton, BaseNotifyWriter):
    cameras: dict[str, str] = None
    _save_dir: Path = None
    save_path: str = None
    logger: Logger = None
    notify_manager = None
    notify_name = "Camera Status"

    def __init__(self, save_dir: Path, cameras: dict[str, str]):
        pass

    def init(self, save_dir: Path, cameras: dict[str, str]) -> None:
        self._save_dir = save_dir
        self._save_dir.mkdir(parents=True, exist_ok=True)
        self.save_path = str(self._save_dir / "photo.jpg")

        self.cameras = cameras

    async def get_statuses(self) -> dict[str, bool]:
        result: dict[str, bool] = {}
        for camera, rtsp in self.cameras.items():
            status: bool = await ping(rtsp)
            result[camera] = status

        return result

    async def get_photo(self, camera: str) -> str:
        if camera in self.cameras:
            cmd = ["ffmpeg", "-hide_banner", "-y", "-loglevel", "error",
                   "-rtsp_transport", "tcp", "-i", self.cameras[camera],
                   "-an", "-r", "1", "-vframes", "1", "-y", "-f", "mjpeg", self.save_path]
            process = await asyncio.create_subprocess_exec(*cmd)
            await process.wait()
            return self.save_path
