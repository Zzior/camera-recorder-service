from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from const.button_string import *

back_rkb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=BACK_BS)]],
    resize_keyboard=True
)


def build_rkb(buttons: list[str], back: bool = True, adjust: int = 2) -> ReplyKeyboardMarkup:
    result = ReplyKeyboardBuilder()
    for button in buttons:
        result.add(KeyboardButton(text=button))

    if back:
        result.add(KeyboardButton(text=BACK_BS))

    result.adjust(adjust)
    return result.as_markup(resize_keyboard=True)


def build_ikb(buttons: dict[str, str] | list[str], adjust: int = 3) -> InlineKeyboardMarkup:
    result = InlineKeyboardBuilder()
    if isinstance(buttons, dict):
        for text, data in buttons.items():
            result.add(InlineKeyboardButton(text=text, callback_data=data))

    else:
        for text in buttons:
            result.add(InlineKeyboardButton(text=text, callback_data=text))

    result.adjust(adjust)
    return result.as_markup()


def build_select_cameras_ikb(cameras: list[str], selected: list[str], adjust: int = 3) -> InlineKeyboardMarkup:
    result = InlineKeyboardBuilder()
    for camera in cameras:
        text = ("✅" + camera) if camera in selected else camera
        result.add(InlineKeyboardButton(text=text, callback_data=camera))

    result.adjust(adjust)
    return result.as_markup()


def build_select_days_ikb(selected: list[str], adjust: int = 3) -> InlineKeyboardMarkup:
    result = InlineKeyboardBuilder()
    days = {"Monday": "1", "Tuesday": "2", "Wednesday": "3",
            "Thursday": "4", "Friday": "5", "Saturday": "6", "Sunday": "7"}

    for day, day_num in days.items():
        text = ("✅" + day) if day_num in selected else day
        result.add(InlineKeyboardButton(text=text, callback_data=day_num))

    result.adjust(adjust)
    return result.as_markup()


admin_main_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=FILES_BS), KeyboardButton(text=RECORDS_BS)],
        [KeyboardButton(text=SCHEDULE_BS), KeyboardButton(text=CAMERAS_BS)],
        [KeyboardButton(text=SETTINGS_BS)]
    ],
    resize_keyboard=True
)

admin_add_and_del_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ADD_BS), KeyboardButton(text=DELETE_BS)],
        [KeyboardButton(text=BACK_BS)]
    ],
    resize_keyboard=True
)

files_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=UPLOAD_BS), KeyboardButton(text=DELETE_BS)],
        [KeyboardButton(text=BACK_BS)]
    ],
    resize_keyboard=True
)

records_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=RECORDS_START_BS), KeyboardButton(text=RECORDS_STOP_BS)],
        [KeyboardButton(text=RECORDS_STATUS_BS), KeyboardButton(text=BACK_BS)]
    ],
    resize_keyboard=True
)

schedule_cameras_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=CONFIRM_BS), KeyboardButton(text=BACK_BS)]
    ],
    resize_keyboard=True
)

cameras_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ADD_BS), KeyboardButton(text=DELETE_BS)],
        [KeyboardButton(text=GET_PHOTO_BS), KeyboardButton(text=BACK_BS)]
    ],
    resize_keyboard=True
)
