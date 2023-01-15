from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.groups.callback_data import GroupCallbackData, GroupAction
from src.bot.keyboards.root.profile import ProfileCallbackData

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_group_info_markup(
    ftl: TranslatorRunner, group_id: UUID, base_url: str
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.change(),
                web_app=WebAppInfo(
                    url=ftl.web.group.update.url(base_url=base_url, id=str(group_id))
                ),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.root.profile.registry.group.tasks.button(),
                callback_data=GroupCallbackData(
                    group_id=group_id, action=GroupAction.TASKS
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.delete(),
                callback_data=GroupCallbackData(
                    group_id=group_id, action=GroupAction.DELETE
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text=ftl.back(),
                callback_data=ProfileCallbackData(action=Registry.GROUPS).pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
