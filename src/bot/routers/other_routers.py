from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext

from bot.routers.commands import start_command

other_routers = Router(name="settings")


@other_routers.message()
async def empty_fsm(message: Message, state: FSMContext) -> None:
    await start_command(message, state)
