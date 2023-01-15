from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram import Router, F, types
from aiogram.exceptions import TelegramAPIError
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner

from src.application.common.exceptions.common import OffsetNegative
from src.application.common.usecases.common import get_paginate
from src.application.group.usecases.group import GetGroup
from src.application.task.usecases.task import GetGroupTasks, GetGroupTasksCount
from src.bot.constants import MISS
from src.bot.keyboards.root.groups.callback_data import (
    GroupCallbackData,
    GroupAction,
)
from src.bot.keyboards.root.groups.tasks.callback_data import TaskPageController
from src.bot.keyboards.root.groups.tasks.registry import get_group_tasks_markup
from src.infrastructure.uow import SQLAlchemyUoW

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(GroupCallbackData.filter(F.action == GroupAction.TASKS))
async def on_tasks_registry(
    c: types.CallbackQuery,
    callback_data: GroupCallbackData,
    uow: SQLAlchemyUoW,
    ftl: TranslatorRunner,
):
    offset, limit = 0, 6
    group = await GetGroup(uow)(callback_data.group_id)
    tasks = await GetGroupTasks(uow)(callback_data.group_id, offset, limit)
    count = await GetGroupTasksCount(uow)(callback_data.group_id)
    paginate = get_paginate(count, offset, limit)
    markup = get_group_tasks_markup(ftl, tasks, paginate, callback_data.group_id)
    teacher = MISS
    if group.teacher:
        teacher = f"{group.teacher.surname} {group.teacher.name}"
    text = (
        ftl.root.profile.registry.group.info(
            name=group.name,
            teacher=teacher,
            description=group.description or MISS,
        )
        + "\n\n"
        + ftl.root.profile.registry.group.select.task()
    )
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()


@router.callback_query(TaskPageController.filter())
async def page_controller(
    c: types.CallbackQuery,
    callback_data: TaskPageController,
    state: FSMContext,
    uow: SQLAlchemyUoW,
    ftl: TranslatorRunner,
):
    group_id = (await state.get_data()).get("group_id")

    try:
        tasks = await GetGroupTasks(uow)(
            group_id, callback_data.offset, callback_data.limit
        )
    except OffsetNegative:
        await c.answer()
        return

    count = await GetGroupTasksCount(uow)(group_id)
    paginate = get_paginate(count, callback_data.offset, callback_data.limit)

    if 1 <= paginate.current_page <= paginate.pages:
        markup = get_group_tasks_markup(
            ftl,
            tasks,
            paginate,
            group_id,
        )
        with suppress(TelegramAPIError):
            await c.message.edit_reply_markup(markup)
    await c.answer()
