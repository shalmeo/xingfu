from aiogram.fsm.state import StatesGroup, State


class ImportStudents(StatesGroup):
    input_excel = State()
