from dataclasses import dataclass
from pathlib import Path
import asyncio
import datetime
from logging import Logger, INFO, ERROR, WARNING

from src.classes.base.notify_writer import BaseNotifyWriter
from src.classes.base.singleton import Singleton
from src.utils.ping import ping


@dataclass
class RecordConfigs:
    video_date_name: str = "%Y_%m_%d_%H_%M"
    video_type: str = "mkv"
    video_bit: str = "512k"
    video_fps: str = "15"
    video_dimensions: str = "1280x720"
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    timeout: int = 5000000
    timeout_ping: int = 3


@dataclass
class ProcessInfo:
    rtsp_url: str
    process: asyncio.subprocess.Process
    start_time: datetime.datetime
    duration: int


class RecordManager(Singleton, BaseNotifyWriter):
    cameras: dict[str, str] = None
    save_dir: Path = None
    logger: Logger = None
    notify_manager = None
    notify_name = "Record status"

    record_config: RecordConfigs = RecordConfigs()
    active_records: dict[str, ProcessInfo] = dict()

    def __init__(self, save_dir: Path, cameras: dict[str, str], record_config: RecordConfigs = RecordConfigs):
        pass

    def init(self, save_dir, cameras, record_config=RecordConfigs()) -> None:
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)

        self.cameras = cameras
        self.record_config = record_config

    async def process_watcher(self,  sleep_time: int = 5, close_duration: int = 10):
        """control of running records"""
        await self.send_notify("process_watcher work")

        while True:
            now = datetime.datetime.now()

            cameras_to_check = list(self.active_records.keys())
            for camera in cameras_to_check:
                info = self.active_records.get(camera)
                recorded_time = (now - info.start_time).seconds

                return_code = info.process.returncode
                print(type(return_code))

                if (return_code == 0) and (recorded_time >= info.duration):
                    self.write_log(f"Ending recording for {camera}", INFO)
                    del self.active_records[camera]
                    continue

                # WRITE ---------------------------------------------------------------------------------
                elif return_code and (recorded_time < info.duration):
                    # Rerun record ------------------------------------------------------
                    self.write_log(f"Error ending recording for {camera}, return code: 0", ERROR)
                    temp = self.active_records.pop(camera)
                    record = await self.run_record(camera=camera, duration=info.duration - recorded_time)
                    if not record:
                        self.active_records[camera] = temp

                # when recording has not completed after + close_duration
                elif now - info.start_time > datetime.timedelta(seconds=info.duration + close_duration):
                    self.write_log(f"Camera {camera} forced shutdown!", WARNING)
                    await self.stop_record(camera)
                    continue

            await asyncio.sleep(sleep_time)

    @staticmethod
    def write_cmd(
            camera_name: str, rtsp: str, record_duration: str, config: RecordConfigs, save_path: Path
    ) -> list[str]:

        filename = datetime.datetime.now().strftime(config.video_date_name)
        filename = f"{filename}_{camera_name}.{config.video_type}"
        filepath = str(save_path / filename)

        cmd = [
            "ffmpeg", "-hide_banner", "-y", "-loglevel", "error", "-timeout", str(config.timeout),
            "-rtsp_transport", "tcp", "-i", rtsp,
            "-c:v", config.video_codec, "-b:v", config.video_bit,
            "-r", config.video_fps, "-s", config.video_dimensions,
            "-c:a", config.audio_codec, "-t", record_duration, filepath
        ]
        return cmd

    async def run_record(self, camera: str, duration: int) -> bool:
        """Start recording the stream from a camera and remove it from active records upon completion."""
        if camera not in self.cameras:
            self.write_log(f"Camera '{camera}' not found in `cameras`", WARNING)
            return False

        if camera in self.active_records:
            self.write_log(f"Camera '{camera}' is already being recorded", WARNING)
            return False

        if not await ping(self.cameras.get(camera), timeout=self.record_config.timeout_ping):
            self.write_log(f"Camera {camera} is not available", WARNING)
            return False

        cmd = self.write_cmd(camera_name=camera, rtsp=self.cameras[camera], record_duration=str(duration),
                             config=self.record_config, save_path=self.save_dir)

        # Run record
        process = await asyncio.create_subprocess_exec(*cmd)

        # Save info with record
        self.active_records[camera] = ProcessInfo(
            rtsp_url=self.cameras[camera],
            process=process,
            start_time=datetime.datetime.now(),
            duration=duration
        )
        self.write_log(f"Starting recording for {camera}", INFO)
        return True

    async def stop_record(self, camera: str) -> None:
        info: ProcessInfo = self.active_records.get(camera)
        if info:
            if info.process.returncode is None:
                self.write_log(f"Stopping recording for {camera}", INFO)
                info.process.terminate()
                await asyncio.sleep(5)
                if info.process.returncode is None:
                    self.write_log(f"Kill recording for {camera}", INFO)
                    info.process.kill()
                    await info.process.wait()

            del self.active_records[camera]

    def get_active_records(self) -> dict:
        """Return a dictionary of active records with their status."""
        return {camera: "active" for camera in self.active_records}
