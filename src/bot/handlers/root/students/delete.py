from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.student.interfaces.uow import IStudentUoW
from src.application.student.usecases.student import DeleteStudent
from src.bot.keyboards.root.students.callback_data import (
    StudentCallbackData,
    StudentAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(StudentCallbackData.filter(F.action == StudentAction.DELETE))
async def on_delete_student(
    c: types.CallbackQuery,
    callback_data: StudentCallbackData,
    uow: IStudentUoW,
    ftl: TranslatorRunner,
):
    await DeleteStudent(uow)(callback_data.student_id)
    await c.message.delete()
    await c.message.answer(ftl.root.profile.registry.user.successfully.deleted())
    await c.answer()
