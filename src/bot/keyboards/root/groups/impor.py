from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_input_excel_markup(ftl: TranslatorRunner) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.upload(),
                callback_data=ExcelCallbackData(
                    action=ExcelAction.UPLOAD, registry=Registry.GROUPS
                ).pack(),
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
