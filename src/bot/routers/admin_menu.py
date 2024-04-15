from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router

from src.configuration import conf
from src.bot.structures.fsm import Admin
from src.bot.structures.keyboards.keyboards_string import *


admin_router = Router(name="admin")


@admin_router.message(Admin.main_menu)
async def admin_router_main_menu(message: Message, state: FSMContext):
    if message.text == FILES_BS:
        await message.answer("soon")

    elif message.text == RECORDS_BS:
        await message.answer("soon")

    elif message.text == SETTINGS_BS:
        await message.answer("soon")

    elif message.text == CAMERAS_BS:
        cameras_status = await conf.cameras_manager.get_statuses()
        statuses_message = "Cameras status:"

        for camera, status in cameras_status.items():
            statuses_message += f"\n{camera}: {status}"

        await message.answer(statuses_message)
        await state.set_state(Admin.cameras)

    elif message.text == SETTINGS_BS:
        await message.answer("soon")
