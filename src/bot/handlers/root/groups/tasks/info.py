from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram import Router, F, types
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner

from src.application.common.exceptions.common import OffsetNegative
from src.application.common.usecases.common import get_paginate
from src.application.student.usecases.student import (
    GetGroupStudents,
    GetGroupStudentsCount,
)
from src.application.task.usecases.task import GetTask
from src.bot.constants import MISS
from src.bot.keyboards.root.groups.tasks.callback_data import (
    TaskCallbackData,
    TaskAction,
    GroupStudentsPageController,
)
from src.bot.keyboards.root.groups.tasks.info import get_task_markup

from src.infrastructure.uow import SQLAlchemyUoW

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner


router = Router()


@router.callback_query(TaskCallbackData.filter(F.action == TaskAction.INFO))
async def on_task_info(
    c: types.CallbackQuery,
    callback_data: TaskCallbackData,
    state: FSMContext,
    uow: SQLAlchemyUoW,
    ftl: TranslatorRunner,
):
    offset, limit = 0, 6
    task = await GetTask(uow)(callback_data.task_id)
    students = await GetGroupStudents(uow)(task.group_id, offset, limit)
    count = await GetGroupStudentsCount(uow)(task.group_id)
    paginate = get_paginate(count, offset, limit)
    markup = get_task_markup(ftl, students, paginate, task.id, task.group_id)
    text = (
        ftl.root.profile.registry.group.task.info(
            title=task.title,
            lesson_date=task.lesson_date or MISS,
            deadline=task.deadline,
            description=task.description,
        )
        + "\n\n"
        + ftl.root.profile.registry.group.select.student()
    )

    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()

    await state.update_data(task_id=str(task.id))


@router.callback_query(GroupStudentsPageController.filter())
async def page_controller(
    c: types.CallbackQuery,
    callback_data: GroupStudentsPageController,
    state: FSMContext,
    uow: SQLAlchemyUoW,
    ftl: TranslatorRunner,
):
    data = await state.get_data()
    group_id = data.get("group_id")
    task_id = data.get("task_id")

    try:
        students = await GetGroupStudents(uow)(
            group_id, callback_data.offset, callback_data.limit
        )
    except OffsetNegative:
        await c.answer()
        return

    count = await GetGroupStudentsCount(uow)(group_id)
    paginate = get_paginate(count, callback_data.offset, callback_data.limit)

    if 1 <= paginate.current_page <= paginate.pages:
        markup = get_task_markup(ftl, students, paginate, task_id, group_id)

        with suppress(TelegramAPIError):
            await c.message.edit_reply_markup(markup)
    await c.answer()
