from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.undefined.callback_data import (
    UndefinedCallbackData,
    UndefinedAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_undefined_info_markup(ftl: TranslatorRunner, undefined_id: UUID) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.accept(),
                callback_data=UndefinedCallbackData(
                    undefined_id=undefined_id,
                    action=UndefinedAction.ACCEPT,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.reject(),
                callback_data=UndefinedCallbackData(
                    undefined_id=undefined_id,
                    action=UndefinedAction.REJECT,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.back(),
                callback_data=ProfileCallbackData(action=Registry.UNCERTAINS).pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
