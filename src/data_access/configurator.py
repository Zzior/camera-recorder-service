from pathlib import Path
import shutil
import json


def dump_json(file_location: Path, info: dict) -> None:
    with open(file_location, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4, ensure_ascii=False)


class Configurator:
    def __init__(self, configs_dir: Path) -> None:
        self.configs_dir = configs_dir
        self.app_config_path = self.configs_dir / "config.json"

        self.configs_dir.mkdir(parents=True, exist_ok=True)

        self.config = self.load_config()

        # Создаём ссылки на списки внутри config
        self.admins: dict[str, int] = self.config.setdefault("admins", {})
        self.cameras: dict[str, str] = self.config.setdefault("cameras", {})
        self.notifications: dict[str, list] = self.config.setdefault("notifications", {})

    def load_config(self) -> dict:
        try:
            with self.app_config_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            self.handle_config_error()
            return {"admins": {}, "cameras": {}, "notifications": {}}

    def handle_config_error(self) -> None:
        backup_path = self.configs_dir / "error_config.json"
        try:
            shutil.copy(self.app_config_path, backup_path)
        except FileNotFoundError:
            pass
        dump_json(self.app_config_path, {"admins": {}, "cameras": {}, "notifications": {}})

    def save_config(self) -> None:
        dump_json(self.app_config_path, self.config)

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

