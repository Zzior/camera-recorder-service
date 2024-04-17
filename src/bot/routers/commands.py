from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


from src.configuration import conf
from src.bot.structures.templates import admin_main_menu
from src.const.message_answers import FIRST_START_ANS, NOT_PERMISSION_ANS
commands_router = Router(name='commands')


@commands_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    """Start command handler."""

    if not conf.configurator.admins:
        conf.configurator.add_admin(message.from_user.full_name, message.from_user.id)
        await message.answer(FIRST_START_ANS)
        await admin_main_menu(message, state)

    elif message.from_user.id in conf.configurator.admins.values():
        await admin_main_menu(message, state)

    else:
        await message.answer(NOT_PERMISSION_ANS)
