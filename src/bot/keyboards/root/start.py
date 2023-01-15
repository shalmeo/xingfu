from typing import TYPE_CHECKING

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_start_markup(ftl: TranslatorRunner) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=ftl.root.profile.button())]]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
