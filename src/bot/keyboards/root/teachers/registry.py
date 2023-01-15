from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from src.application.teacher.dto.teacher import TeacherDTO
from src.bot.keyboards.paginate import add_paginate_buttons, IPaginate
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.bot.keyboards.root.teachers.callback_data import (
    TeacherCallbackData,
    TeacherAction,
    TeacherPageController,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_teachers_registry_markup(
    ftl: TranslatorRunner,
    teachers: list[TeacherDTO],
    paginate: IPaginate,
    base_url: str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for teacher in teachers:
        text = ftl.root.profile.registry.teacher.button(
            surname=teacher.surname, name=teacher.name
        )
        builder.button(
            text=text,
            callback_data=TeacherCallbackData(
                teacher_id=teacher.id, action=TeacherAction.INFO
            ).pack(),
        )

    builder.adjust(3)

    add_paginate_buttons(builder, TeacherPageController, paginate)

    builder.row(
        InlineKeyboardButton(
            text=ftl.web.create.record.button(),
            web_app=WebAppInfo(url=ftl.web.teacher.create.url(base_url=base_url)),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=ftl.excel.export.button(),
            callback_data=ExcelCallbackData(
                action=ExcelAction.EXPORT, registry=Registry.TEACHERS
            ).pack(),
        ),
        InlineKeyboardButton(
            text=ftl.excel.impor.button(),
            callback_data=ExcelCallbackData(
                action=ExcelAction.IMPORT, registry=Registry.TEACHERS
            ).pack(),
        ),
    )

    builder.row(InlineKeyboardButton(text=ftl.back(), callback_data="to_profile"))

    return builder.as_markup()
