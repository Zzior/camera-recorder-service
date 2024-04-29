import asyncio

from aiogram.types import Message, CallbackQuery, input_file
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot

from src.utils.ping import ping
from src.configuration import conf
from src.bot.structures.fsm import Admin
from src.bot.structures.templates import (
    admin_main_menu, check_back_button, message_not_reg, format_record_status,
    format_schedule, format_files, text_to_int, format_files_list)

from src.const.message_answers import *  # from src.const.button_string import *
from src.const.logs_strings import ADMIN_CAMERAS_IKB_LOG, ADMIN_DAYS_IKB_LOG, ADMIN_SCHEDULE_ADD_LOG
from src.bot.structures.keyboards import *
from src.classes.data_classes import Schedule

admin_router = Router(name="admin")


@admin_router.message(Admin.main_menu)
@check_back_button
async def admin_router_main_menu(message: Message, state: FSMContext):
    if message.text == FILES_BS:
        info = conf.file_manager.files_info()
        msg = format_files(info)
        await state.set_data({"max": len(info)-1, "files": info})
        await state.set_state(Admin.files)
        await message.answer(text=msg, reply_markup=files_rkb)

    elif message.text == RECORDS_BS:
        msg = format_record_status(conf.record_manager.get_records_status())
        await state.set_state(Admin.records)
        await message.answer(text=msg, reply_markup=records_rkb)

    elif message.text == SCHEDULE_BS:
        sch_message = format_schedule(conf.schedule_manager.get_schedules())
        await state.set_state(Admin.schedule)
        await message.answer(text=sch_message, reply_markup=admin_add_and_del_rkb)

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

    else:
        await message_not_reg(message, kb=admin_main_rkb)


# ===================================== Files =====================================================
@admin_router.message(Admin.files)
@check_back_button
async def admin_router_files(message: Message, state: FSMContext):
    if message.text == UPLOAD_BS:
        await message.answer("soon")

    elif message.text == DELETE_BS:
        await state.set_state(Admin.files_delete)
        await message.answer(FILES_DELETE_ANS, reply_markup=back_rkb)

    else:
        await message_not_reg(message, kb=files_rkb)


@admin_router.message(Admin.files_delete)
@check_back_button
async def admin_router_files_delete(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text:
        numbers = text_to_int(text=message.text, max_val=data["max"])
        if numbers:
            files = format_files_list(data["files"], numbers)
            await message.answer(FILES_DELETED_ANS)
            conf.file_manager.delete_files(files)
            await admin_main_menu(message, state)

        else:
            await message.answer(FILES_DELETE_ERR_ANS)
    else:
        await message.answer(FILES_DELETE_ANS)


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
        msg = format_record_status(conf.record_manager.get_records_status())
        await message.answer(text=msg)

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


# ===================================== Schedule ==================================================
@admin_router.message(Admin.schedule)
@check_back_button
async def admin_router_schedule(message: Message, state: FSMContext):
    if message.text == ADD_BS:
        await state.set_state(Admin.schedule_add_time)
        await message.answer(SCHEDULE_ENTER_TIME_ANS, reply_markup=back_rkb)

    elif message.text == DELETE_BS:
        if conf.schedule_manager.get_schedules():
            info = conf.schedule_manager.get_schedules()
            await state.set_data({"max": len(info)-1})
            await state.set_state(Admin.schedule_delete)
            await message.answer(SCHEDULE_DELETE_ANS, reply_markup=back_rkb)
        else:
            await message.answer(SCHEDULE_EMPTY_ANS)
    else:
        await message_not_reg(message, admin_add_and_del_rkb)


@admin_router.message(Admin.schedule_add_time)
@check_back_button
async def admin_router_schedule_add_time(message: Message, state: FSMContext):
    if conf.schedule_manager.is_valid_time(message.text):
        await state.set_data({"start_time": message.text})
        await state.set_state(Admin.schedule_add_duration)
        await message.answer(SCHEDULE_ENTER_DURATION_ANS)
    else:
        await message.answer(SCHEDULE_ENTER_TIME_ERR_ANS)


@admin_router.message(Admin.schedule_add_duration)
@check_back_button
async def admin_router_schedule_add_duration(message: Message, state: FSMContext):
    if message.text and message.text.isdigit() and 1440 >= int(message.text) >= 1:
        await state.update_data({"duration": int(message.text)*60, "cameras": []})
        await state.set_state(Admin.schedule_add_cameras)
        await message.answer(
            SCHEDULE_SELECT_CAMERAS_IKB_ANS,
            reply_markup=build_select_cameras_ikb(cameras=conf.configurator.cameras.keys(), selected=[])
        )
        await message.answer(SCHEDULE_SELECT_CAMERAS_RKB_ANS, reply_markup=schedule_cameras_rkb)

    else:
        await message.answer(SCHEDULE_ENTER_DURATION_ERR_ANS)


@admin_router.message(Admin.schedule_add_cameras)
@check_back_button
async def admin_router_schedule_add_cameras(message: Message, state: FSMContext):
    if message.text == CONFIRM_BS:
        cameras = await state.get_data()
        if cameras.get("cameras"):
            await state.set_state(Admin.schedule_add_days)
            await state.update_data({"days": []})
            await message.answer(SCHEDULE_SELECT_DAYS_ANS, reply_markup=build_select_days_ikb(selected=[]))

        else:
            await message.answer(SCHEDULE_SELECT_CAMERAS_EMPTY_ANS)
    else:
        await message.answer(SCHEDULE_SELECT_CAMERAS_ERR_ANS)


@admin_router.callback_query(Admin.schedule_add_cameras)
async def admin_router_schedule_add_cameras_ikb(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data in conf.configurator.cameras:
        data = await state.get_data()
        if callback.data in data["cameras"]:
            data["cameras"].remove(callback.data)
            await callback.answer(text=DELETED_ANS)
        else:
            data["cameras"].append(callback.data)
            await callback.answer(text=ADDED_ANS)

        await state.update_data(data)

        try:
            await bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=build_select_cameras_ikb(
                    cameras=conf.configurator.cameras.keys(), selected=data["cameras"]
                )
            )
        except Exception as e:
            ADMIN_CAMERAS_IKB_LOG.format(e)


@admin_router.message(Admin.schedule_add_days)
@check_back_button
async def admin_router_schedule_add_days_rkb(message: Message, state: FSMContext):
    if message.text == CONFIRM_BS:
        data = await state.get_data()
        if data["days"]:
            try:
                days = [int(day) for day in data["days"]]
                info = Schedule(
                    start_time=data["start_time"],
                    duration=data["duration"],
                    cameras=sorted(data["cameras"]),
                    days=sorted(days)
                )
                status = conf.schedule_manager.add_schedule(info=info)
            except Exception as e:
                ADMIN_SCHEDULE_ADD_LOG.format(e=e)
                status = 9

            if status == 0:
                await message.answer(SCHEDULE_CONFIRM_ANS)
                await admin_main_menu(message, state)

            else:
                await message.answer(SCHEDULE_ADD_ERR.format(name=status))
        else:
            await message.answer(SCHEDULE_SELECT_DAYS_EMPTY_ANS)
    else:
        await message.answer(SCHEDULE_SELECT_DATS_ERR_ANS)


@admin_router.callback_query(Admin.schedule_add_days)
async def admin_router_schedule_add_days_ikb(callback: CallbackQuery, state: FSMContext, bot: Bot):
    if callback.data and callback.data.isdigit() and (7 >= int(callback.data) >= 1):
        data = await state.get_data()
        if callback.data in data["days"]:
            data["days"].remove(callback.data)
            await callback.answer(text=DELETED_ANS)
        else:
            data["days"].append(callback.data)
            await callback.answer(text=ADDED_ANS)

        await state.update_data(data)

        try:
            await bot.edit_message_reply_markup(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                reply_markup=build_select_days_ikb(selected=data["days"])
            )
        except Exception as e:
            ADMIN_DAYS_IKB_LOG.format(e=e)


@admin_router.message(Admin.schedule_delete)
@check_back_button
async def admin_router_schedule_delete(message: Message, state: FSMContext):
    if message.text and message.text.isdigit():
        data = await state.get_data()
        index = int(message.text)
        if data["max"] >= index >= 0:
            conf.schedule_manager.del_schedule(index_from_get=index)
            await message.answer(SCHEDULE_DELETED_ANS)
            await admin_main_menu(message, state)

        else:
            await message.answer(SCHEDULE_DELETE_ERR_ANS)
    else:
        await message.answer(SCHEDULE_DELETE_ANS)


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
async def admin_router_camera_photo(message: Message):
    if message.text in conf.configurator.cameras:
        await message.answer(PHOTO_LOAD_ANS)
        photo_path = await conf.cameras_manager.get_photo(message.text)
        photo = input_file.BufferedInputFile.from_file(path=photo_path)
        await message.answer_photo(photo)

    else:
        await message.answer(PHOTO_CAMERA_SELECT_ANS)
