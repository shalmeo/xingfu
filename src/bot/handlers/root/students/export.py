from operator import and_

from aiogram import Router, F, types

from src.application.student.interfaces.uow import IStudentUoW
from src.application.student.usecases.student import GetAllStudents
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.infrastructure.exporters.excel.student.exporter import StudentExcelExporter

router = Router()


@router.callback_query(
    ExcelCallbackData.filter(
        and_(F.action == ExcelAction.EXPORT, F.registry == Registry.STUDENTS)
    )
)
async def export(c: types.CallbackQuery, uow: IStudentUoW):
    exporter = StudentExcelExporter(template_path="resources/excel/students.xlsx")
    exporter.set_title("Реестр")
    students = await GetAllStudents(uow)()
    output = exporter.save(students)
    file = types.BufferedInputFile(
        file=output.read(),
        filename="Реестр Учеников.xlsx",
    )
    await c.message.answer_document(file)
    await c.answer()
