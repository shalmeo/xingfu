from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.uncertains.callback_data import (
    UncertainCallbackData,
    UncertainAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_uncertain_info_markup(
    ftl: TranslatorRunner, uncertain_id: UUID
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.accept(),
                callback_data=UncertainCallbackData(
                    uncertain_id=uncertain_id,
                    action=UncertainAction.ACCEPT,
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.reject(),
                callback_data=UncertainCallbackData(
                    uncertain_id=uncertain_id,
                    action=UncertainAction.REJECT,
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
