from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from fluentogram import TranslatorRunner

from src.application.common.exceptions.common import OffsetNegative
from src.application.common.usecases.common import get_paginate
from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.teacher.usecases.teacher import GetTeachers, GetTeachersCount
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.teachers.callback_data import TeacherPageController
from src.bot.keyboards.root.teachers.registry import get_teachers_registry_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(ProfileCallbackData.filter(F.action == Registry.TEACHERS))
async def on_teachers_registry(
    c: types.CallbackQuery,
    state: FSMContext,
    base_url: str,
    uow: ITeacherUoW,
    ftl: TranslatorRunner,
):
    offset, limit = 0, 9
    teachers = await GetTeachers(uow)(offset, limit)
    count = await GetTeachersCount(uow)()
    paginate = get_paginate(count, offset, limit)
    text = ftl.root.profile.registry.teachers.text()
    markup = get_teachers_registry_markup(ftl, teachers, paginate, base_url)
    m = await c.message.edit_text(text, reply_markup=markup)
    await c.answer()

    await state.update_data(last_mid=m.message_id)


@router.callback_query(TeacherPageController.filter())
async def page_controller(
    c: types.CallbackQuery,
    callback_data: TeacherPageController,
    base_url: str,
    uow: ITeacherUoW,
    ftl: TranslatorRunner,
):
    try:
        teachers = await GetTeachers(uow)(callback_data.offset, callback_data.limit)
    except OffsetNegative:
        await c.answer()
        return

    count = await GetTeachersCount(uow)()
    paginate = get_paginate(count, callback_data.offset, callback_data.limit)

    if 1 <= paginate.current_page <= paginate.pages:
        markup = get_teachers_registry_markup(ftl, teachers, paginate, base_url)
        with suppress(TelegramAPIError):
            await c.message.edit_reply_markup(markup)
    await c.answer()
