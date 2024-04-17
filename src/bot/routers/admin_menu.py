from aiogram.types import Message, input_file
from aiogram.fsm.context import FSMContext
from aiogram import Router

from src.utils.ping import ping
from src.configuration import conf
from src.bot.structures.fsm import Admin
from src.bot.structures.templates import admin_main_menu, check_back_button

from src.const.message_answers import *  # from src.const.button_string import *
from src.bot.structures.keyboards import *

admin_router = Router(name="admin")


@admin_router.message(Admin.main_menu)
@check_back_button
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
@check_back_button
async def admin_router_cameras(message: Message, state: FSMContext):
    if message.text == ADD_BS:
        await state.set_state(Admin.cameras_add_name)
        await message.answer(ENTER_CAMERA_NAME_ANS, reply_markup=back_rkb)

    elif message.text == DELETE_BS:
        await state.set_state(Admin.cameras_delete_name)
        await message.answer(
            DEL_CAMERA_NAME_ANS,
            reply_markup=build_rkb(conf.configurator.cameras.keys())
        )

    elif message.text == GET_PHOTO_BS:
        await state.set_state(Admin.cameras_photo)
        await message.answer(PHOTO_CAMERA_SELECT_ANS, reply_markup=build_rkb(conf.configurator.cameras.keys()))


@admin_router.message(Admin.cameras_add_name)
@check_back_button
async def admin_router_cameras_add_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(ENTER_CAMERA_NAME_ANS)

    elif message.text not in conf.configurator.cameras:
        await message.answer(ADD_CAMERA_RTSP_ANS)
        await state.set_state(Admin.cameras_add_rtsp)
        await state.set_data({"name": message.text})

    elif message.text:
        await message.answer(ENTER_CAMERA_NAME_ERR_ANS)


@admin_router.message(Admin.cameras_add_rtsp)
@check_back_button
async def admin_router_cameras_add_rtsp(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(ADD_CAMERA_RTSP_ANS)

    elif message.text not in conf.configurator.cameras.values():
        if message.text.startswith(("rtsp://", "rtsps://")):
            status = await ping(message.text)
            if status:
                name = await state.get_data()
                conf.configurator.add_camera(name=name["name"], rtsp=message.text)
                await message.answer(CAMERA_ADDED_ANS.format(name=name["name"]))
                await admin_main_menu(message, state)

            else:
                await message.answer(ADD_CAMERA_PING_ERR_ANS)
        else:
            await message.answer(ADD_CAMERA_RTSP_NOT_ANS)
    else:
        await message.answer(ADD_CAMERA_RTSP_ERR_ANS)


@admin_router.message(Admin.cameras_delete_name)
@check_back_button
async def admin_router_cameras_delete_name(message: Message, state: FSMContext):
    if message.text in conf.configurator.cameras:
        await message.answer(DEL_CAMERA_DONE_ANS.format(name=message.text))
        conf.configurator.delete_camera(name=message.text)
        await admin_main_menu(message, state)

    else:
        await message.answer(DEL_CAMERA_NAME_ANS)


@admin_router.message(Admin.cameras_photo)
@check_back_button
async def admin_router_camera_photo(message: Message, state: FSMContext):
    if message.text in conf.configurator.cameras:
        await message.answer(PHOTO_LOAD_ANS)
        photo_path = await conf.cameras_manager.get_photo(message.text)
        photo = input_file.BufferedInputFile.from_file(path=photo_path)
        await message.answer_photo(photo)

    else:
        await message.answer(PHOTO_CAMERA_SELECT_ANS)
