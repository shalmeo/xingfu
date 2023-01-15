from enum import Enum
from typing import TYPE_CHECKING

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


class ProfileAction(Enum):
    DISTRIBUTIONS = "DISTRIBUTIONS"


class ProfileCallbackData(CallbackData, prefix="profile"):
    action: Registry | ProfileAction


def get_profile_markup(ftl: TranslatorRunner) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.root.profile.registry.admins.button(),
                callback_data=ProfileCallbackData(action=Registry.ADMINS).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.root.profile.registry.teachers.button(),
                callback_data=ProfileCallbackData(action=Registry.TEACHERS).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.root.profile.registry.students.button(),
                callback_data=ProfileCallbackData(action=Registry.STUDENTS).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.root.profile.registry.groups.button(),
                callback_data=ProfileCallbackData(action=Registry.GROUPS).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.root.profile.registry.uncertains.button(),
                callback_data=ProfileCallbackData(action=Registry.UNCERTAINS).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.root.profile.distriburions.button(),
                callback_data=ProfileCallbackData(
                    action=ProfileAction.DISTRIBUTIONS
                ).pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
