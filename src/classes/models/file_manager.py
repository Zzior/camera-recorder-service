import asyncio
from pathlib import Path
from os import path, remove
from datetime import datetime, timedelta

from src.classes.base.notify_writer import BaseNotifyWriter
from src.classes.base.abc_cls import AbstractRecordManager
from src.classes.base.singleton import Singleton
from src.classes.data_classes import FileInfo
from src.const.notify_string import FILE_DELETED_NFY


class FileManager(Singleton, BaseNotifyWriter):
    files_path: Path
    notify_name = "Files delete"
    record_manager: AbstractRecordManager

    def __init__(self, files_path: Path, record_manager: AbstractRecordManager = None):
        pass

    def init(self, files_path: Path, record_manager: AbstractRecordManager = None) -> None:
        self.files_path = files_path
        self.record_manager = record_manager

    async def file_task(self, interval=5, delete_days=6) -> None:
        while True:
            current_date = datetime.now()
            d_time = timedelta(days=delete_days)
            file_list = [file for file in self.files_path.iterdir() if file.is_file()]
            for i in file_list:
                creation_time = datetime.fromtimestamp(path.getctime(i))

                if current_date - creation_time > d_time:
                    remove(i)
                    await self.send_notify(FILE_DELETED_NFY.format(name=i.name))

            await asyncio.sleep(interval)

    def files_info(self) -> list[FileInfo]:
        result = []
        have_status = {}
        if self.record_manager and isinstance(self.record_manager, AbstractRecordManager):
            recording = self.record_manager.get_records_status()
            for camera, info in recording.items():
                have_status[info.file_name] = info.status

        file_list = sorted(file for file in self.files_path.iterdir() if file.is_file())

        for i in file_list:
            if i.name in have_status:
                result.append(FileInfo(file_name=i.name, file_size=path.getsize(i), record_status=have_status[i.name]))
            else:
                result.append(FileInfo(file_name=i.name, file_size=path.getsize(i)))

        return result

    def delete_files(self, files: list[str]) -> None:
        for file in files:
            try:
                remove(self.files_path / file)
            except Exception as e:
                print(e)
