from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    main_menu = State()

    files = State()
    records = State()
    schedule = State()
    cameras = State()
    settings = State()
