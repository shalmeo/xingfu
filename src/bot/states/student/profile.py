from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    select_option = State()
