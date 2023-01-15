from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.teacher.usecases.teacher import DeleteTeacher
from src.bot.keyboards.root.teachers.callback_data import (
    TeacherCallbackData,
    TeacherAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(TeacherCallbackData.filter(F.action == TeacherAction.DELETE))
async def on_delete_teacher(
    c: types.CallbackQuery,
    callback_data: TeacherCallbackData,
    uow: ITeacherUoW,
    ftl: TranslatorRunner,
):
    await DeleteTeacher(uow)(callback_data.teacher_id)
    await c.message.delete()
    await c.message.answer(ftl.root.profile.registry.user.successfully.deleted())
    await c.answer()
