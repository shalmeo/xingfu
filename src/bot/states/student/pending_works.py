from aiogram.fsm.state import StatesGroup, State


class PendingWorks(StatesGroup):
    select_work = State()
