from aiogram import Router, types
from aiogram.filters import Text
from aiogram_dialog import DialogManager, StartMode

from src.bot.states.student.profile import Profile

router = Router()


@router.message(Text(contains="личный кабинет", ignore_case=True))
async def on_profile(m: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(Profile.select_option, mode=StartMode.RESET_STACK)
