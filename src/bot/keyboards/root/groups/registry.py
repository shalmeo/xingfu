from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from src.application.group.dto.group import GroupDTO
from src.bot.keyboards.paginate import add_paginate_buttons, IPaginate
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.bot.keyboards.root.groups.callback_data import (
    GroupCallbackData,
    GroupAction,
    GroupPageController,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_groups_registry_markup(
    ftl: TranslatorRunner,
    groups: list[GroupDTO],
    paginate: IPaginate,
    base_url: str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for group in groups:
        text = ftl.root.profile.registry.group.button(name=group.name)
        builder.button(
            text=text,
            callback_data=GroupCallbackData(
                group_id=group.id, action=GroupAction.INFO
            ).pack(),
        )

    builder.adjust(3)

    add_paginate_buttons(builder, GroupPageController, paginate)

    builder.row(
        InlineKeyboardButton(
            text=ftl.web.create.record.button(),
            web_app=WebAppInfo(url=ftl.web.group.create.url(base_url=base_url)),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=ftl.excel.export.button(),
            callback_data=ExcelCallbackData(
                action=ExcelAction.EXPORT, registry=Registry.GROUPS
            ).pack(),
        ),
        InlineKeyboardButton(
            text=ftl.excel.impor.button(),
            callback_data=ExcelCallbackData(
                action=ExcelAction.IMPORT, registry=Registry.GROUPS
            ).pack(),
        ),
    )

    builder.row(InlineKeyboardButton(text=ftl.back(), callback_data="to_profile"))

    return builder.as_markup()
