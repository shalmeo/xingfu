from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.students.callback_data import (
    StudentCallbackData,
    StudentAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_student_info_markup(
    ftl: TranslatorRunner, student_id: UUID, base_url: str
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.change(),
                web_app=WebAppInfo(url=ftl.web.student.update.url(base_url=base_url, id=str(student_id))),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.delete(),
                callback_data=StudentCallbackData(
                    student_id=student_id, action=StudentAction.DELETE
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.back(),
                callback_data=ProfileCallbackData(action=Registry.STUDENTS).pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
