from functools import wraps
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup  # ReplyKeyboardRemove

from src.bot.structures.fsm import Admin
from src.bot.structures.keyboards import admin_main_rkb, records_rkb
from src.const.button_string import BACK_BS
from src.const.message_answers import (
    MESSAGE_NOT_REG_ANS, MAIN_MENU_ANS,
    ACTIVE_RECORDS_ANS, RECORDS_ACTIVE_ANS, ACTIVE_RECORDS_NONE_ANS, RECORDS_ERROR_ANS
)


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


async def send_record_status(message: Message, status: dict[str, list], kb: ReplyKeyboardMarkup = None) -> None:
    ans = ACTIVE_RECORDS_ANS
    for camera, info in status.items():
        ans += (f"\n{RECORDS_ACTIVE_ANS if info[0] else RECORDS_ERROR_ANS}"
                f"  ─  {camera}  ─  {(info[1] / 60):.1f}min")

    if ans == ACTIVE_RECORDS_ANS:
        ans = ACTIVE_RECORDS_NONE_ANS

    await message.answer(ans, reply_markup=kb)
