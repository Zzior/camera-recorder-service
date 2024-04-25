"""This file represents configurations from files and environment."""
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

# Data access (With Save configs)
from src.classes.models.configurator import Configurator

# Models (Utils)
from src.classes.models.loger import setup_logger
from src.classes.models.notify_manager import NotifyManager
from src.classes.models.record_manager import RecordManager
from src.classes.models.camera_manager import CameraManager
from src.classes.models.schedule_manager import ScheduleManager

app_dir: Path = Path(__file__).parent.parent


@dataclass
class Configuration:
    """All in one configuration's class."""
    app_dir = app_dir
    configs_dir = app_dir / "storage"
    logger = setup_logger(configs_dir / "app.log")

    load_dotenv(configs_dir / ".env")
    token = getenv("BOT_TOKEN")
    encoder = getenv("ENCODER")
    records_dir = Path(getenv("RECORDS_DIR")) if getenv("RECORDS_DIR") else (app_dir / "records")

    # Configs
    configurator = Configurator((configs_dir / "config.json"))

    # Utils
    notify_manager = NotifyManager()
    cameras_manager = CameraManager(save_dir=configs_dir, cameras=configurator.cameras)
    record_manager = RecordManager(save_dir=records_dir, cameras=configurator.cameras)
    schedule_manager = ScheduleManager(config_path=configs_dir/"schedule.json", record_manager=record_manager)


conf = Configuration()
