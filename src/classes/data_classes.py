from dataclasses import dataclass
import datetime
import asyncio


@dataclass
class RecordConfigs:
    rtsp_transport: str = "tcp"
    video_date_name: str = "%Y_%m_%d_%H_%M"
    video_type: str = "mkv"
    video_bit: str = "512k"
    video_fps: str = "15"
    video_dimensions: str = "1280x720"
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    timeout: int = 3000000
    timeout_ping: int = 3


@dataclass
class ProcessInfo:
    rtsp_url: str
    process: asyncio.subprocess.Process
    start_time: datetime.datetime
    duration: int
    file_name: str


@dataclass
class RecordInfo:
    status: bool  # Recording or error
    start_time: datetime.datetime
    duration: int
    time_left: int
    file_name: str


@dataclass
class FileInfo:
    file_name: str
    file_size: int
    record_status: bool = None


@dataclass
class Schedule:
    """
    start_time (str): The start time for the recording schedule in HH:MM format.
    duration (int): Duration of the recording in seconds. Must be between 60 and 86400, inclusive.
    cameras (list[str]): A list of camera identifiers that will be used in the recording schedule.
    days (list[int]): A list of integers representing the days of the week the schedule applies to (1=Mon, 7=Sun).
    index (int): Issued in the get_schedules method, used in del_schedule in the Schedule_Manager methods.
    """
    start_time: str
    duration: int
    cameras: list[str]
    days: list[int]

    index: int = None
