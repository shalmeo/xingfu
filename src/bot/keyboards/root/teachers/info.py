from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.teachers.callback_data import (
    TeacherCallbackData,
    TeacherAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_teacher_info_markup(
    ftl: TranslatorRunner, teacher_id: UUID, base_url: str
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.change(),
                web_app=WebAppInfo(url=ftl.web.teacher.update.url(base_url=base_url, id=str(teacher_id))),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.delete(),
                callback_data=TeacherCallbackData(
                    teacher_id=teacher_id, action=TeacherAction.DELETE
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.back(),
                callback_data=ProfileCallbackData(action=Registry.TEACHERS).pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
