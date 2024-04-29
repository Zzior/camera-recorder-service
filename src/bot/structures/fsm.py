from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    main_menu = State()

    files = State()
    records = State()
    schedule = State()
    cameras = State()
    settings = State()

    # Files
    files_upload = State()
    files_delete = State()

    # Cameras
    cameras_add_name = State()
    cameras_add_rtsp = State()
    cameras_delete_name = State()
    cameras_photo = State()

    # Records
    records_run_name = State()
    records_run_duration = State()
    records_stop = State()

    # Schedule
    schedule_add_time = State()
    schedule_add_duration = State()
    schedule_add_cameras = State()
    schedule_add_days = State()
    schedule_delete = State()
