from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup  # ReplyKeyboardRemove

from src.bot.structures.fsm import Admin
from src.bot.structures.keyboards.keyboards import admin_main_rkb


async def message_not_reg(message: Message, kb: ReplyKeyboardMarkup = None) -> None:
    await message.answer("Choose an option⬇️", reply_markup=kb)


async def admin_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("🏠Main Menu", reply_markup=admin_main_rkb)
    await state.set_state(Admin.main_menu)
