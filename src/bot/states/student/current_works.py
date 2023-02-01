from aiogram.fsm.state import StatesGroup, State


class CurrentWorks(StatesGroup):
    select_group = State()
