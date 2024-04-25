import asyncio
from pathlib import Path
from datetime import datetime

from src.classes.base.singleton import Singleton
from src.classes.base.data_save import BaseDataSave
from src.classes.base.abc_cls import AbstractRecordManager
from src.classes.data_classes import Schedule


class ScheduleManager(Singleton, BaseDataSave):
    record_manager: AbstractRecordManager
    _config: dict[str, list[list]]

    def __init__(self, config_path: Path, record_manager: AbstractRecordManager) -> None:
        pass

    def init(self, config_path: Path, record_manager: AbstractRecordManager) -> None:
        self.record_manager = record_manager
        BaseDataSave.init(self=self, config_path=config_path)

    async def schedule_task(self, interval=5) -> None:
        while True:
            now = datetime.now()
            time = now.strftime("%H:%M")
            weekday = now.isoweekday()

            if time in self._config:
                for task_index in range(len(self._config[time])):
                    if not (weekday in self._config[time][task_index][2]):
                        continue

                    for camera in self._config[time][task_index][1].copy():
                        if camera in self.record_manager.cameras:
                            await self.record_manager.run_record(camera, self._config[time][task_index][0])
                        else:
                            self.del_camera(time, task_index, camera)

                # To avoid starting the recording again, this minute is skipped
                await asyncio.sleep(60)

            await asyncio.sleep(interval)

    def add_schedule(self, info: Schedule) -> int:
        """
            Adds a new schedule to the recording system.

            Validates and adds a new recording schedule based on the specified start time, duration,
            cameras to be used, and days of the week.

            Parameters:
                info (Schedule): Schedule.
            Returns:
                int: A status code indicating the result of the operation:
                    - 0: Schedule added successfully.
                    - 1: Invalid start time format.
                    - 2: Invalid duration (must be an integer from 1 to 86400).
                    - 3: One or more specified cameras are not registered in the system.
                    - 4: One or more specified days are invalid (must be integers from 1 to 7).
            """
        if not self.is_valid_time(info.start_time):
            return 1

        elif not (isinstance(info.duration, int) and (86400 >= info.duration >= 60)):
            return 2

        for camera in info.cameras:
            if camera not in self.record_manager.cameras:
                return 3

        for day in info.days:
            if not (isinstance(day, int) and (7 >= day >= 1)):
                return 4

        if info.start_time not in self._config:
            self._config[info.start_time] = []

        self._config[info.start_time].append([info.duration, info.cameras, info.days])
        self.save_config()
        return 0

    def del_schedule(self, index_from_get: int) -> None:
        get_index_now = 0
        for time, schedules in self._config.items():
            for list_index in range(len(schedules)):
                if get_index_now == index_from_get:
                    del self._config[time][list_index]
                    if not self._config[time]:
                        del self._config[time]
                        self.save_config()
                    return

                else:
                    get_index_now += 1

    def get_schedules(self) -> list[Schedule]:
        result = []
        index = 0
        for time, schedules in self._config.items():
            for schedule in schedules:
                result.append(
                    Schedule(start_time=time, duration=schedule[0], cameras=schedule[1], days=schedule[2], index=index)
                )
                index += 1
        return result

    def del_camera(self, time: str, task_index: int, camera: str) -> None:
        if ((time in self._config) and (len(self._config[time]) > task_index) and
                (camera in self._config[time][task_index][1])):

            self._config[time][task_index][1].remove(camera)

            # check if it's empty
            if self._config[time][task_index][1]:
                return
            del self._config[time][task_index]

            if self._config[time]:
                return
            del self._config[time]

    @staticmethod
    def is_valid_time(time_str: str) -> bool:
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
