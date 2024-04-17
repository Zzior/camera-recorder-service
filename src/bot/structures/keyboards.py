from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.const.button_string import *

back_rkb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=BACK_BS)]],
    resize_keyboard=True
)


def build_rkb(buttons: list[str] | tuple[str] | set[str], back: bool = True) -> ReplyKeyboardMarkup:
    result = ReplyKeyboardBuilder()
    for button in buttons:
        result.add(KeyboardButton(text=button))

    if back:
        result.add(KeyboardButton(text=BACK_BS))

    result.adjust(2)

    return result.as_markup(resize_keyboard=True)


admin_main_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=FILES_BS), KeyboardButton(text=RECORDS_BS)],
        [KeyboardButton(text=SCHEDULE_BS), KeyboardButton(text=CAMERAS_BS)],
        [KeyboardButton(text=SETTINGS_BS)]
    ],
    resize_keyboard=True
)

get_photo_rkb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ADD_BS), KeyboardButton(text=DELETE_BS)],
        [KeyboardButton(text=GET_PHOTO_BS), KeyboardButton(text=BACK_BS)]
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

