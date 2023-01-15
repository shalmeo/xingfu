from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from src.application.uncertain.dto.uncertain import UncertainDTO
from src.bot.keyboards.paginate import add_paginate_buttons, IPaginate
from src.bot.keyboards.root.uncertains.callback_data import (
    UncertainCallbackData,
    UncertainAction,
    UncertainPageController,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_uncertains_registry_markup(
    ftl: TranslatorRunner,
    uncertains: list[UncertainDTO],
    paginate: IPaginate,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for uncertain in uncertains:
        text = ftl.root.profile.registry.uncertain.button(
            surname=uncertain.surname, name=uncertain.name
        )
        builder.button(
            text=text,
            callback_data=UncertainCallbackData(
                uncertain_id=uncertain.id, action=UncertainAction.INFO
            ).pack(),
        )

    builder.adjust(3)

    add_paginate_buttons(builder, UncertainPageController, paginate)

    builder.row(InlineKeyboardButton(text=ftl.back(), callback_data="to_profile"))

    return builder.as_markup()
