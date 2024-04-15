from pathlib import Path
import shutil
import json


def dump_json(file_location: Path, info: dict) -> None:
    with open(file_location, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4, ensure_ascii=False)


class Schedule:
    def __init__(self, configs_dir: Path) -> None:
        self.configs_dir = configs_dir
        self.app_config_path = self.configs_dir / "schedule.json"

        self.configs_dir.mkdir(parents=True, exist_ok=True)

        self.schedule: dict = self.load_config()

    def load_config(self) -> dict:
        try:
            with self.app_config_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            self.handle_config_error()

            self.schedule: dict = {}
            self.save_config()
            return self.schedule

    def handle_config_error(self) -> None:
        backup_path = self.configs_dir / "error_schedule.json"
        try:
            shutil.copy(self.app_config_path, backup_path)
        except FileNotFoundError:
            pass
        dump_json(self.app_config_path, {})

    def save_config(self) -> None:
        dump_json(self.app_config_path, self.schedule)

    def add(self, idc: str, time_start: str, time_record: int, days: list[int]) -> None:
        if not (time_start in self.schedule):
            self.schedule[time_start] = []

        self.schedule[time_start].append([idc, time_record, days])
        self.save_config()

    def delete(self, idc: str, time_start: str, time_record: int) -> None:
        for i in self.schedule[time_start]:
            if (idc in i) and (time_record in i):
                self.schedule[time_start].remove(i)
                break

        self.save_config()
