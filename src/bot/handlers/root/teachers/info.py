from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.teacher.usecases.teacher import GetTeacher
from src.bot.constants import MISS
from src.bot.keyboards.root.teachers.callback_data import (
    TeacherCallbackData,
    TeacherAction,
)
from src.bot.keyboards.root.teachers.info import get_teacher_info_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(TeacherCallbackData.filter(F.action == TeacherAction.INFO))
async def on_teacher_info(
    c: types.CallbackQuery,
    callback_data: TeacherCallbackData,
    base_url: str,
    uow: ITeacherUoW,
    ftl: TranslatorRunner,
):
    teacher = await GetTeacher(uow)(callback_data.teacher_id)
    text = ftl.root.profile.registry.teacher.info(
        surname=teacher.surname,
        name=teacher.name,
        patronymic=teacher.patronymic or MISS,
        phone=f"+{teacher.user.phone}" if teacher.user.phone else MISS,
        email=teacher.user.email,
        telegram_id=str(teacher.user.telegram_id) if teacher.user.telegram_id else MISS,
        username=teacher.user.telegram_username or MISS,
        birthday=teacher.birthday,
        level=teacher.level or MISS,
        description=teacher.description or MISS,
        access_start=teacher.access_start,
        access_end=teacher.access_end,
        timezone=teacher.user.timezone,
    )
    markup = get_teacher_info_markup(ftl, callback_data.teacher_id, base_url)
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()
