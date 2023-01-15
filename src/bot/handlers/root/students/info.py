from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.student.interfaces.uow import IStudentUoW
from src.application.student.usecases.student import GetStudent
from src.bot.constants import MISS
from src.bot.keyboards.root.students.callback_data import (
    StudentCallbackData,
    StudentAction,
)
from src.bot.keyboards.root.students.info import get_student_info_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(StudentCallbackData.filter(F.action == StudentAction.INFO))
async def on_student_info(
    c: types.CallbackQuery,
    callback_data: StudentCallbackData,
    base_url: str,
    ftl: TranslatorRunner,
    uow: IStudentUoW,
):
    student = await GetStudent(uow)(callback_data.student_id)
    text = ftl.root.profile.registry.student.info(
        surname=student.surname,
        name=student.name,
        patronymic=student.patronymic or MISS,
        phone=f"+{student.user.phone}" if student.user.phone else MISS,
        email=student.user.email,
        telegram_id=str(student.user.telegram_id) if student.user.telegram_id else MISS,
        username=student.user.telegram_username or MISS,
        birthday=student.birthday,
        access_start=student.access_start,
        access_end=student.access_end,
        timezone=student.user.timezone,
    )
    markup = get_student_info_markup(ftl, callback_data.student_id, base_url)
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()
