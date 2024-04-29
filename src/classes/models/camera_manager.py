import asyncio
from pathlib import Path

from src.classes.base.notify_writer import BaseNotifyWriter
from src.classes.base.singleton import Singleton
from src.utils.ping import ping
from src.const.notify_string import CAMERA_ONLINE_NFY, CAMERA_OFFLINE_NFY, CAMERA_CHANGE_STATUS_NFY


class CameraManager(Singleton, BaseNotifyWriter):
    cameras_status: dict[str, bool] = {}
    cameras: dict[str, str] = None
    _save_dir: Path = None
    save_path: str = None
    notify_name = "Camera Status"

    def __init__(self, save_dir: Path, cameras: dict[str, str]):
        pass

    def init(self, save_dir: Path, cameras: dict[str, str]) -> None:
        self._save_dir = save_dir
        self._save_dir.mkdir(parents=True, exist_ok=True)
        self.save_path = str(self._save_dir / "photo.jpg")

        self.cameras = cameras

    async def status_checker(self, interval=5) -> None:
        while True:
            statuses = await self.get_statuses()
            message = ""
            for camera, status in statuses.items():
                if (camera not in self.cameras_status) or (status != self.cameras_status[camera]):
                    self.cameras_status[camera] = status
                    message += CAMERA_CHANGE_STATUS_NFY.format(
                        name=camera, status=CAMERA_ONLINE_NFY if status else CAMERA_OFFLINE_NFY)

            if message:
                await self.send_notify(message, deferred=False)

            await asyncio.sleep(interval)

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
