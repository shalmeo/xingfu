from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from src.application.admin.dto.admin import AdminDTO
from src.bot.keyboards.paginate import add_paginate_buttons, IPaginate
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.admins.callback_data import (
    AdminCallbackData,
    AdminAction,
    AdminPageController,
)
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_admins_registry_markup(
    ftl: TranslatorRunner,
    admins: list[AdminDTO],
    paginate: IPaginate,
    base_url: str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for admin in admins:
        text = ftl.root.profile.registry.admin.button(
            surname=admin.surname, name=admin.name
        )
        builder.button(
            text=text,
            callback_data=AdminCallbackData(
                admin_id=admin.id, action=AdminAction.INFO
            ).pack(),
        )

    builder.adjust(3)

    add_paginate_buttons(builder, AdminPageController, paginate)

    builder.row(
        InlineKeyboardButton(
            text=ftl.web.create.record.button(),
            web_app=WebAppInfo(url=ftl.web.admin.create.url(base_url=base_url)),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=ftl.excel.export.button(),
            callback_data=ExcelCallbackData(
                action=ExcelAction.EXPORT, registry=Registry.ADMINS
            ).pack(),
        ),
        InlineKeyboardButton(
            text=ftl.excel.impor.button(),
            callback_data=ExcelCallbackData(
                action=ExcelAction.IMPORT, registry=Registry.ADMINS
            ).pack(),
        ),
    )

    builder.row(InlineKeyboardButton(text=ftl.back(), callback_data="to_profile"))

    return builder.as_markup()
