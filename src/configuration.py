"""This file represents configurations from files and environment."""
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass

# Data access (With Save configs)
from src.data_access.schedule import Schedule
from src.data_access.configurator import Configurator

# Models (Utils)
from src.classes.models.loger import setup_logger
from src.classes.models.notify_manager import NotifyManager
from src.classes.models.recorder import RecordManager
from src.classes.models.cameras import CameraManager

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
    configurator = Configurator(configs_dir)
    schedule = Schedule(configs_dir)

    # Utils
    notify_manager = NotifyManager()
    cameras_manager = CameraManager(save_dir=configs_dir, cameras=configurator.cameras)
    record_manager = RecordManager(save_dir=records_dir, cameras=configurator.cameras)


conf = Configuration()
