from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from fluentogram import TranslatorRunner

from src.bot.keyboards.root.start import get_start_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


router = Router()


@router.message(Command("start"), StateFilter("*"))
async def on_cmd_start(message: Message, ftl: TranslatorRunner):
    text = ftl.start.welcome()
    markup = get_start_markup(ftl)
    await message.answer(text, reply_markup=markup)
