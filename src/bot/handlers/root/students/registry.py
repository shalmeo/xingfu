from contextlib import suppress
from typing import TYPE_CHECKING

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from fluentogram import TranslatorRunner

from src.application.common.exceptions.common import OffsetNegative
from src.application.common.usecases.common import get_paginate
from src.application.student.interfaces.uow import IStudentUoW
from src.application.student.usecases.student import GetStudents, GetStudentsCount
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.profile import ProfileCallbackData
from src.bot.keyboards.root.students.callback_data import StudentPageController
from src.bot.keyboards.root.students.registry import get_students_registry_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(ProfileCallbackData.filter(F.action == Registry.STUDENTS))
async def on_students_registry(
    c: types.CallbackQuery,
    state: FSMContext,
    base_url: str,
    uow: IStudentUoW,
    ftl: TranslatorRunner,
):
    offset, limit = 0, 9
    students = await GetStudents(uow)(offset, limit)
    count = await GetStudentsCount(uow)()
    paginate = get_paginate(count, offset, limit)
    text = ftl.root.profile.registry.students.text()
    markup = get_students_registry_markup(ftl, students, paginate, base_url)
    m = await c.message.edit_text(text, reply_markup=markup)
    await c.answer()

    await state.update_data(last_mid=m.message_id)


@router.callback_query(StudentPageController.filter())
async def page_controller(
    c: types.CallbackQuery,
    callback_data: StudentPageController,
    base_url: str,
    uow: IStudentUoW,
    ftl: TranslatorRunner,
):
    try:
        students = await GetStudents(uow)(callback_data.offset, callback_data.limit)
    except OffsetNegative:
        await c.answer()
        return

    count = await GetStudentsCount(uow)()
    paginate = get_paginate(count, callback_data.offset, callback_data.limit)

    if 1 <= paginate.current_page <= paginate.pages:
        markup = get_students_registry_markup(ftl, students, paginate, base_url)
        with suppress(TelegramAPIError):
            await c.message.edit_reply_markup(markup)
    await c.answer()
