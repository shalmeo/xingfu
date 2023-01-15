from operator import and_
from typing import TYPE_CHECKING

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.students.impor import get_input_excel_markup
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.bot.states.root.students.impor import ImportStudents
from src.domain.root.usecases.root import RootService
from src.infrastructure.importers.excel.student.importer import StudentExcelImporter

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(
    ExcelCallbackData.filter(
        and_(F.action == ExcelAction.IMPORT, F.registry == Registry.STUDENTS)
    )
)
async def impor(c: types.CallbackQuery, state: FSMContext, ftl: TranslatorRunner):
    await c.message.edit_text(ftl.excel.impor.text())
    await state.set_state(ImportStudents.input_excel)


@router.message(
    F.document.file_name.casefold().endswith(".xlsx"),
    StateFilter(ImportStudents.input_excel),
)
async def on_input_excel(
    m: types.Message,
    bot: Bot,
    state: FSMContext,
    ftl: TranslatorRunner,
):
    downloaded = await bot.download(m.document.file_id)
    importer = StudentExcelImporter(downloaded)
    students = importer.import_()
    markup = get_input_excel_markup(ftl)
    await m.answer(
        ftl.excel.impor.detected.records.text(count=len(students)),
        reply_markup=markup,
    )
    await state.update_data(students=students)


@router.callback_query(
    ExcelCallbackData.filter(
        and_(F.action == ExcelAction.UPLOAD, F.registry == Registry.STUDENTS)
    ),
    StateFilter(ImportStudents.input_excel),
)
async def on_upload_students(
    c: types.CallbackQuery,
    state: FSMContext,
    root_service: RootService,
    ftl: TranslatorRunner,
):
    data = await state.get_data()
    count = await root_service.student.import_(data["students"])
    await c.message.delete()
    await c.message.answer(ftl.excel.impor.upload.records.text(count=count))
    await c.answer()
