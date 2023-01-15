from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.admins.callback_data import AdminCallbackData, AdminAction
from src.bot.keyboards.root.profile import ProfileCallbackData

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_admin_info_markup(
    ftl: TranslatorRunner, admin_id: UUID, base_url: str
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=ftl.change(),
                web_app=WebAppInfo(url=ftl.web.admin.update.url(base_url=base_url, id=str(admin_id))),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.delete(),
                callback_data=AdminCallbackData(
                    admin_id=admin_id, action=AdminAction.DELETE
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text=ftl.back(),
                callback_data=ProfileCallbackData(action=Registry.ADMINS).pack(),
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
