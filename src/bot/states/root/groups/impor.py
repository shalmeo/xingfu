from aiogram.fsm.state import StatesGroup, State


class ImportGroups(StatesGroup):
    input_excel = State()
