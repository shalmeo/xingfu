from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.bot.keyboards.root.undefined.callback_data import (
    UndefinedAcceptRoleCallbackData,
    UndefinedCallbackData,
    UndefinedAction,
)
from src.domain.user.models.user import UserRole

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_undefined_accept_markup(ftl: TranslatorRunner, undefined_id: UUID) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.teacher(),
                callback_data=UndefinedAcceptRoleCallbackData(
                    undefined_id=undefined_id,
                    role=UserRole.TEACHER,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.student(),
                callback_data=UndefinedAcceptRoleCallbackData(
                    undefined_id=undefined_id,
                    role=UserRole.STUDENT,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.back(),
                callback_data=UndefinedCallbackData(
                    undefined_id=undefined_id,
                    action=UndefinedAction.INFO,
                ).pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
