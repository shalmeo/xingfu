from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from fluentogram import TranslatorRunner

from src.bot.keyboards.uncertain.start import get_start_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


router = Router()


@router.message(Command("start"), StateFilter("*"))
async def on_cmd_start(message: Message, base_url: str, ftl: TranslatorRunner):
    text = ftl.uncertain.start.text()
    sticker = ftl.sticker.welcome()
    markup = get_start_markup(ftl, base_url, message.from_user.id, message.from_user.username)
    await message.answer_sticker(sticker)
    await message.answer(text, reply_markup=markup)
