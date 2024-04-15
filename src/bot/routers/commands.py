from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


from src.configuration import conf
from src.bot.structures.templates import admin_main_menu

commands_router = Router(name='commands')


@commands_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    """Start command handler."""

    if not conf.configurator.admins:
        conf.configurator.add_admin(message.from_user.full_name, message.from_user.id)
        await message.answer("⚙️First launch\n👨‍💻Administrator rights have been granted")
        await admin_main_menu(message, state)

    elif message.from_user.id in conf.configurator.admins.values():
        await admin_main_menu(message, state)

    else:
        await message.answer("You not have permission!")
