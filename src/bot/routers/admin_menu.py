from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Router

from src.configuration import conf
from src.bot.structures.fsm import Admin
from src.utils.ping import ping

from src.const.message_answers import *  # from src.const.button_string import *
from src.bot.structures.keyboards import *

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
        await message.answer(LOAD_STATUSES_ANS, reply_markup=get_photo_rkb)
        await state.set_state(Admin.cameras)

        # get all status of cameras
        cameras_status = await conf.cameras_manager.get_statuses()
        statuses_message = CAM_STATUSES_LIST_ANS
        for camera, status in cameras_status.items():
            statuses_message += f"\n{CAMERA_ONLINE_ANS if status else CAMERA_OFFLINE_ANS} ─  {camera}"

        await message.answer(statuses_message)

    elif message.text == SETTINGS_BS:
        await message.answer("soon")


@admin_router.message(Admin.cameras)
async def admin_router_cameras(message: Message, state: FSMContext):
    if message.text == ADD_BS:
        await state.set_state(Admin.cameras_add_name)
        await message.answer(ENTER_CAMERA_NAME_ANS, reply_markup=back_rkb)

    elif message.text == DELETE_BS:
        pass

    elif message.text == GET_PHOTO_BS:
        pass


@admin_router.message(Admin.cameras_add_name)
async def admin_router_cameras_add_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(ENTER_CAMERA_NAME_ANS)

    elif message.text not in conf.configurator.cameras:
        await message.answer(ENTER_CAMERA_RTSP_ANS)
        await state.set_state(Admin.cameras_add_rtsp)
        await state.set_data({"name": message.text})

    elif message.text:
        await message.answer(ENTER_CAMERA_NAME_ERR_ANS)


@admin_router.message(Admin.cameras_add_rtsp)
async def admin_router_cameras_add_rtsp(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(ENTER_CAMERA_RTSP_ANS)

    elif message.text not in conf.configurator.cameras.values():
        if message.text.startswith(("rtsp://", "rtsps://")):
            status = await ping(message.text)
            if status:
                name = await state.get_data()
                conf.configurator.add_camera(name=name["name"], rtsp=message.text)
                await message.answer(CAMERA_ADDED)
            else:
                await message.answer(ENTER_CAMERA_PING_ERR_ANS)
        else:
            await message.answer(ENTER_CAMERA_RTSP_NOT_ANS)

    else:
        await message.answer(ENTER_CAMERA_RTSP_ERR_ANS)
