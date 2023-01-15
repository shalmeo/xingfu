from aiogram.fsm.state import StatesGroup, State


class ImportTeachers(StatesGroup):
    input_excel = State()
