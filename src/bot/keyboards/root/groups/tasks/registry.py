from typing import TYPE_CHECKING
from uuid import UUID

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fluentogram import TranslatorRunner

from src.application.task.dto.task import TaskDTO
from src.bot.keyboards.paginate import add_paginate_buttons, IPaginate
from src.bot.keyboards.root.groups.callback_data import (
    GroupCallbackData,
    GroupAction,
)
from src.bot.keyboards.root.groups.tasks.callback_data import (
    TaskCallbackData,
    TaskAction,
    TaskPageController,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


def get_group_tasks_markup(
    ftl: TranslatorRunner,
    tasks: list[TaskDTO],
    paginate: IPaginate,
    group_id: UUID,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for task in tasks:
        text = ftl.root.profile.registry.group.task.button(title=task.title)
        builder.button(
            text=text,
            callback_data=TaskCallbackData(
                task_id=task.id, action=TaskAction.INFO
            ).pack(),
        )

    builder.adjust(3)

    add_paginate_buttons(builder, TaskPageController, paginate)

    builder.row(
        InlineKeyboardButton(
            text=ftl.back(),
            callback_data=GroupCallbackData(
                group_id=group_id, action=GroupAction.INFO
            ).pack(),
        )
    )

    return builder.as_markup()
