from aiogram.types import Message, CallbackQuery
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext

from ..routers.commands import start_command

other_routers = Router(name="settings")


@other_routers.message()
async def empty_fsm(message: Message, state: FSMContext) -> None:
    await start_command(message, state)
