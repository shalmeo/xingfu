from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from src.application.undefined.dto.undefined import UndefinedDTO
from src.bot.keyboards.paginate import add_paginate_buttons, IPaginate
from src.bot.keyboards.root.undefined.callback_data import (
    UndefinedCallbackData,
    UndefinedAction,
    UndefinedPageController,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_undefineds_registry_markup(
    ftl: TranslatorRunner,
    undefineds: list[UndefinedDTO],
    paginate: IPaginate,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for undefined in undefineds:
        text = ftl.root.profile.registry.undefined.button(surname=undefined.surname, name=undefined.name)
        builder.button(
            text=text,
            callback_data=UndefinedCallbackData(undefined_id=undefined.id, action=UndefinedAction.INFO).pack(),
        )

    builder.adjust(3)

    add_paginate_buttons(builder, UndefinedPageController, paginate)

    builder.row(InlineKeyboardButton(text=ftl.back(), callback_data="to_profile"))

    return builder.as_markup()
