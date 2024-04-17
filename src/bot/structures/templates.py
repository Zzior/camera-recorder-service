from functools import wraps
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup  # ReplyKeyboardRemove

from src.bot.structures.fsm import Admin
from src.bot.structures.keyboards import admin_main_rkb
from src.const.button_string import BACK_BS
from src.const.message_answers import MESSAGE_NOT_REG_ANS, MAIN_MENU_ANS


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
