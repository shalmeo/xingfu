from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from src.application.student.dto.student import StudentDTO
from src.bot.keyboards.paginate import add_paginate_buttons, IPaginate
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.bot.keyboards.root.students.callback_data import (
    StudentCallbackData,
    StudentAction,
    StudentPageController,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_students_registry_markup(
    ftl: TranslatorRunner,
    students: list[StudentDTO],
    paginate: IPaginate,
    base_url: str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for student in students:
        text = ftl.root.profile.registry.student.button(
            surname=student.surname, name=student.name
        )
        builder.button(
            text=text,
            callback_data=StudentCallbackData(
                student_id=student.id, action=StudentAction.INFO
            ).pack(),
        )

    builder.adjust(3)

    add_paginate_buttons(builder, StudentPageController, paginate)

    builder.row(
        InlineKeyboardButton(
            text=ftl.web.create.record.button(),
            web_app=WebAppInfo(url=ftl.web.student.create.url(base_url=base_url)),
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text=ftl.excel.export.button(),
            callback_data=ExcelCallbackData(
                action=ExcelAction.EXPORT, registry=Registry.STUDENTS
            ).pack(),
        ),
        InlineKeyboardButton(
            text=ftl.excel.impor.button(),
            callback_data=ExcelCallbackData(
                action=ExcelAction.IMPORT, registry=Registry.STUDENTS
            ).pack(),
        ),
    )

    builder.row(InlineKeyboardButton(text=ftl.back(), callback_data="to_profile"))

    return builder.as_markup()
