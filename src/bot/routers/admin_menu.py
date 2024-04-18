import asyncio

from aiogram.types import Message, input_file
from aiogram.fsm.context import FSMContext
from aiogram import Router

from src.utils.ping import ping
from src.configuration import conf
from src.bot.structures.fsm import Admin
from src.bot.structures.templates import admin_main_menu, check_back_button, message_not_reg, send_record_status

from src.const.message_answers import *  # from src.const.button_string import *
from src.bot.structures.keyboards import *

admin_router = Router(name="admin")


@admin_router.message(Admin.main_menu)
@check_back_button
async def admin_router_main_menu(message: Message, state: FSMContext):
    if message.text == FILES_BS:
        await message.answer("soon")

    elif message.text == RECORDS_BS:
        await state.set_state(Admin.records)
        statuses = conf.record_manager.get_records_status()
        await send_record_status(message=message, status=statuses, kb=records_rkb)

    elif message.text == SCHEDULE_BS:
        await message.answer("soon")

    elif message.text == CAMERAS_BS:
        await message.answer(LOAD_STATUSES_ANS, reply_markup=cameras_rkb)
        await state.set_state(Admin.cameras)

        # get all status of cameras
        cameras_status = await conf.cameras_manager.get_statuses()
        statuses_message = CAM_STATUSES_LIST_ANS
        for camera, status in cameras_status.items():
            statuses_message += f"\n{CAMERA_ONLINE_ANS if status else CAMERA_OFFLINE_ANS} ─  {camera}"

        await message.answer(statuses_message)

    elif message.text == SETTINGS_BS:
        await message.answer("soon")


# ===================================== Records ===================================================
@admin_router.message(Admin.records)
@check_back_button
async def admin_router_records(message: Message, state: FSMContext):
    if message.text == RECORDS_START_BS:
        await state.set_state(Admin.records_run_name)
        await message.answer(RECORDS_SELECT_CAMERA_ANS, reply_markup=build_rkb(conf.configurator.cameras.keys()))

    elif message.text == RECORDS_STOP_BS:
        active_records = conf.record_manager.active_records.keys()
        if active_records:
            await state.set_data({"active_cameras": active_records})
            await state.set_state(Admin.records_stop)
            await message.answer(
                RECORDS_SELECT_CAMERA_ANS,
                reply_markup=build_rkb(active_records)
            )
        else:
            await message.answer(ACTIVE_RECORDS_NONE_ANS)

    elif message.text == RECORDS_STATUS_BS:
        statuses = conf.record_manager.get_records_status()
        await send_record_status(message=message, status=statuses, kb=records_rkb)

    else:
        await message_not_reg(message, records_rkb)


@admin_router.message(Admin.records_run_name)
@check_back_button
async def admin_router_records_start(message: Message, state: FSMContext):
    if message.text in conf.configurator.cameras:
        if message.text not in conf.record_manager.get_records_status():
            await state.set_data({"name": message.text})
            await state.set_state(Admin.records_run_duration)
            await message.answer(RECORDS_ENTER_DURATION_ANS, reply_markup=back_rkb)
        else:
            await message.answer(RECORDS_SELECT_CAMERA_REC_ANS)
    else:
        await message.answer(RECORDS_SELECT_CAMERA_ANS)


@admin_router.message(Admin.records_run_duration)
@check_back_button
async def admin_router_records_run_duration(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and int(message.text) > 0:
        name = await state.get_data()
        await conf.record_manager.run_record(camera=name["name"], duration=int(message.text)*60)
        await admin_main_menu(message, state)

    else:
        await message.answer(RECORDS_ENTER_DURATION_ANS)


@admin_router.message(Admin.records_stop)
@check_back_button
async def admin_router_records_stop(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text in data["active_cameras"]:
        t = asyncio.create_task(conf.record_manager.stop_record(message.text))
        await message.answer(RECORDS_STOP_ACCEPTED_ANS.format(name=message.text))
        await admin_main_menu(message, state)

    else:
        await message.answer(RECORDS_SELECT_CAMERA_ANS)


# ===================================== Cameras ===================================================
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

    else:
        await message_not_reg(message, cameras_rkb)


@admin_router.message(Admin.cameras_add_name)
@check_back_button
async def admin_router_cameras_add_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(ENTER_CAMERA_NAME_ANS)

    elif message.text not in conf.configurator.cameras:
        await state.set_data({"name": message.text})
        await state.set_state(Admin.cameras_add_rtsp)
        await message.answer(ADD_CAMERA_RTSP_ANS)

    else:
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
