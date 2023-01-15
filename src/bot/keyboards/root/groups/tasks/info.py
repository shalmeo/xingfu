from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from src.application.student.dto.student import StudentDTO
from src.bot.keyboards.paginate import add_paginate_buttons, IPaginate
from src.bot.keyboards.root.groups.callback_data import (
    GroupAction,
    GroupCallbackData,
)
from src.bot.keyboards.root.groups.tasks.callback_data import (
    GroupStudentCallbackData,
    TaskCallbackData,
    TaskAction,
    GroupStudentsPageController,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_task_markup(
    ftl: TranslatorRunner,
    students: list[StudentDTO],
    paginate: IPaginate,
    task_id: UUID,
    group_id: UUID,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for student in students:
        builder.button(
            text=ftl.root.profile.registry.group.task.student.button(
                surname=student.surname, name=student.name
            ),
            callback_data=GroupStudentCallbackData(student_id=student.id).pack(),
        )

    builder.adjust(6)

    add_paginate_buttons(builder, GroupStudentsPageController, paginate)

    builder.row(
        InlineKeyboardButton(
            text=ftl.attached.files(),
            callback_data=TaskCallbackData(
                task_id=task_id, action=TaskAction.ATTACHED_FILES
            ).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=ftl.back(),
            callback_data=GroupCallbackData(
                action=GroupAction.TASKS, group_id=group_id
            ).pack(),
        )
    )

    return builder.as_markup()
