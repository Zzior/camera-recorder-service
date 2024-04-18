from dataclasses import dataclass
from pathlib import Path
import asyncio
import datetime
from logging import Logger, INFO, ERROR, WARNING

from src.classes.base.notify_writer import BaseNotifyWriter
from src.classes.base.singleton import Singleton
from src.utils.ping import ping

from src.const.logs_strings import *
from src.const.notify_string import *


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
    error_records: dict[str, ProcessInfo] = dict()

    def __init__(self, save_dir: Path, cameras: dict[str, str], record_config: RecordConfigs = RecordConfigs):
        pass

    def init(self, save_dir, cameras, record_config=RecordConfigs()) -> None:
        self.save_dir = save_dir
        self.save_dir.mkdir(parents=True, exist_ok=True)

        self.cameras = cameras
        self.record_config = record_config

    async def process_watcher(self,  sleep_time: int = 5, close_duration: int = 10, min_run_duration: int = 60) -> None:
        """control of running records"""
        while True:
            now = datetime.datetime.now()

            cameras_to_check = list(self.active_records.keys())
            for camera in cameras_to_check:
                info = self.active_records.get(camera)
                recorded_time = (now - info.start_time).seconds
                return_code = info.process.returncode

                # Record done
                if (return_code == 0) and (recorded_time >= info.duration):
                    del self.active_records[camera]
                    self.write_log(END_RECORD_LOG.format(name=camera), INFO)
                    await self.send_notify(END_RECORD_NFY.format(name=camera))

                # Record error
                elif (return_code is not None) and (recorded_time < info.duration):
                    stdout, stderr = await info.process.communicate()
                    self.write_log(END_RECORD_LOG.format(name=camera, rc=return_code, sout=stdout, serr=stderr), ERROR)
                    await self.send_notify(ERROR_RECORD_NFY.format(name=camera))
                    self.error_records[camera] = self.active_records.pop(camera)

                # when recording has not completed after + close_duration
                elif now - info.start_time > datetime.timedelta(seconds=info.duration + close_duration):
                    self.write_log(FORCED_STOP_LOG.format(name=camera), WARNING)
                    await self.stop_record(camera)

            error_records = list(self.error_records.keys())
            for e_camera in error_records:
                e_info = self.error_records.get(e_camera)
                e_recorded_time = (now - e_info.start_time).seconds
                duration = e_info.duration - e_recorded_time

                if (duration > min_run_duration) and (await ping(self.cameras[e_camera])):
                    self.write_log(RESUME_RECORD_LOG.format(name=e_camera), INFO)
                    await self.send_notify(RESUME_RECORD_NFY.format(name=e_camera))
                    await self.run_record(camera=e_camera, duration=e_info.duration - e_recorded_time)
                    del self.error_records[e_camera]

                elif (e_info.duration - e_recorded_time) < close_duration:
                    del self.error_records[e_camera]
                    self.write_log(REACHED_RECORD_LOG.format(name=e_camera), WARNING)

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
            self.write_log(CAMERA_NOT_FOUND_LOG.format(name=camera), WARNING)
            return False

        elif camera in self.active_records:
            self.write_log(CAMERA_NOW_RECORD_LOG.format(name=camera), WARNING)
            return False

        elif not await ping(self.cameras.get(camera), timeout=self.record_config.timeout_ping):
            self.write_log(CAMERA_NOT_PING_LOG.format(name=camera), WARNING)
            return False

        cmd = self.write_cmd(camera, self.cameras[camera], str(duration), self.record_config, self.save_dir)

        # Run record
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        # Save info with record
        self.active_records[camera] = ProcessInfo(rtsp_url=self.cameras[camera], process=process,
                                                  start_time=datetime.datetime.now(), duration=duration)

        self.write_log(RECORD_RUN_LOG.format(name=camera), INFO)
        await self.send_notify(RECORD_RUN_NFY.format(name=camera))
        return True

    async def stop_record(self, camera: str) -> None:
        info: ProcessInfo = self.active_records.get(camera)
        if info:
            del self.active_records[camera]
            if info.process.returncode is None:
                self.write_log(STOP_RECORD_LOG.format(name=camera), INFO)
                info.process.terminate()
                await asyncio.sleep(5)

                if info.process.returncode is None:
                    self.write_log(KILL_RECORD_LOG.format(name=camera), INFO)
                    info.process.kill()
                    await info.process.wait()

    def get_records_status(self) -> dict[str, list]:
        """
        Return a dictionary of records with their current status and remaining duration.
        Each entry in the dictionary has a key as the camera name and the value as a list containing:
        - a boolean indicating whether the recording is active (True) or in error (False)
        - an integer representing the seconds left in the recording duration
        """
        result: dict[str, list] = {}
        now = datetime.datetime.now()

        # Helper function to update result
        def update_status(records, is_active):
            for camera, info in records.items():
                time_left: int = info.duration - (now - info.start_time).seconds
                result[camera] = [is_active, time_left]

        update_status(self.active_records, True)
        update_status(self.error_records, False)

        return result
