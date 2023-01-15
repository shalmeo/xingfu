from aiogram.fsm.state import StatesGroup, State


class ImportAdmins(StatesGroup):
    input_excel = State()
