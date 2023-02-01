from aiogram.fsm.state import StatesGroup, State


class DoneWorks(StatesGroup):
    select_work = State()
