from operator import and_

from aiogram import Router, F, types

from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.teacher.usecases.teacher import GetAllTeachers
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.infrastructure.exporters.excel.teacher.exporter import TeacherExcelExporter

router = Router()


@router.callback_query(
    ExcelCallbackData.filter(
        and_(F.action == ExcelAction.EXPORT, F.registry == Registry.TEACHERS)
    )
)
async def export(c: types.CallbackQuery, uow: ITeacherUoW):
    exporter = TeacherExcelExporter(template_path="resources/excel/teachers.xlsx")
    exporter.set_title("Реестр")
    teachers = await GetAllTeachers(uow)()
    output = exporter.save(teachers)
    file = types.BufferedInputFile(
        file=output.read(),
        filename="Реестр Учителей.xlsx",
    )
    await c.message.answer_document(file)
    await c.answer()
