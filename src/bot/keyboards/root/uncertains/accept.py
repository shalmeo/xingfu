from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.bot.keyboards.root.uncertains.callback_data import (
    UncertainAcceptRoleCallbackData,
    UncertainCallbackData,
    UncertainAction,
)
from src.domain.user.models.user import UserRole

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_uncertain_accept_markup(
    ftl: TranslatorRunner, uncertain_id: UUID
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.teacher(),
                callback_data=UncertainAcceptRoleCallbackData(
                    uncertain_id=uncertain_id,
                    role=UserRole.TEACHER,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.student(),
                callback_data=UncertainAcceptRoleCallbackData(
                    uncertain_id=uncertain_id,
                    role=UserRole.STUDENT,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.back(),
                callback_data=UncertainCallbackData(
                    uncertain_id=uncertain_id,
                    action=UncertainAction.INFO,
                ).pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
