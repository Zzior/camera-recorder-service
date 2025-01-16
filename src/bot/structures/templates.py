from functools import wraps
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup  # ReplyKeyboardRemove

from bot.structures.fsm import Admin
from bot.structures.keyboards import admin_main_rkb
from const.button_string import BACK_BS
from classes.data_classes import Schedule, RecordInfo, FileInfo
from const.message_answers import *


async def message_not_reg(message: Message, kb: ReplyKeyboardMarkup = None) -> None:
    await message.answer(MESSAGE_NOT_REG_ANS, reply_markup=kb)


async def admin_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(MAIN_MENU_ANS, reply_markup=admin_main_rkb)
    await state.set_state(Admin.main_menu)


def check_back_button(func):
    @wraps(func)
    async def wrapper(message: Message, state: FSMContext, *args, **kwargs):
        if message.text and message.text == BACK_BS:
            await admin_main_menu(message, state)
            return

        else:
            await func(message, state, *args, **kwargs)
    return wrapper


def format_record_status(status: dict[str, RecordInfo]) -> str:
    if not status:
        return ACTIVE_RECORDS_NONE_ANS

    ans = ACTIVE_RECORDS_ANS
    for camera, info in status.items():
        ans += (f"\n{RECORDS_ACTIVE_ANS if info.status else RECORDS_ERROR_ANS}"
                f"  ─  {camera}  ─  {(info.time_left / 60):.1f}min")

    return ans


def format_files(files: list[FileInfo]) -> str:
    if not files:
        return FILES_EMPTY_ANS

    ans = FILES_LIST_ANS
    for index in range(len(files)):
        if files[index].record_status is None:
            status = FILES_RECORD_N_ANS
        elif files[index].record_status:
            status = FILES_RECORD_T_ANS
        else:
            status = FILES_RECORD_F_ANS

        size = f"{files[index].file_size // (1024 * 1024)}mb"

        ans += FILES_LIST_FORMAT_ANS.format(
            id=index, name=files[index].file_name, size=size, status=status
        )

    return ans


def format_schedule(schedules: list[Schedule]) -> str:
    if not schedules:
        return SCHEDULE_EMPTY_ANS

    result = SCHEDULE_LIST_ANS
    for s in schedules:
        duration = f"{s.duration // 3600}h {s.duration % 3600 // 60}m"
        cameras = ", ".join(s.cameras)
        days = ", ".join([DAYS_STRING[day] for day in s.days])
        result += SCHEDULE_FORMAT_LIST_ANS.format(
            id=s.index, s=s.start_time, d=duration, c=f"[{cameras}]", days=f"[{days}]"
        )

    return result


def text_to_int(text: str, sep=" ", min_val: int = 0, max_val: int = None) -> set:
    parts = text.split(sep)
    numbers = set()

    for part in parts:
        try:
            num = int(part)
            if num >= min_val:
                if max_val is None or num <= max_val:
                    numbers.add(num)
        except ValueError:
            continue

    return numbers


def format_files_list(files: list[FileInfo], num_set: list[int] | set[int]) -> list[str]:
    result = []
    for index in num_set:
        try:
            if files[index].record_status is None:
                result.append(files[index].file_name)

        except (IndexError, TypeError):
            continue

    return result
