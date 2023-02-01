from typing import TYPE_CHECKING
from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from fluentogram import TranslatorRunner

from src.bot.keyboards.student.start import get_start_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.message(Command("start"), StateFilter("*"))
async def on_cmd_start(m: types.Message, ftl: TranslatorRunner):
    text = ftl.start.welcome()
    markup = get_start_markup()
    await m.answer(text, reply_markup=markup)
