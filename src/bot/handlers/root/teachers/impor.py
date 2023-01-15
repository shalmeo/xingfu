from operator import and_
from typing import TYPE_CHECKING

from aiogram import Router, F, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from fluentogram import TranslatorRunner

from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.teachers.impor import get_input_excel_markup
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.bot.states.root.teachers.impor import ImportTeachers
from src.domain.root.usecases.root import RootService
from src.infrastructure.importers.excel.teacher.importer import TeacherExcelImporter

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(
    ExcelCallbackData.filter(
        and_(F.action == ExcelAction.IMPORT, F.registry == Registry.TEACHERS)
    )
)
async def impor(c: types.CallbackQuery, state: FSMContext, ftl: TranslatorRunner):
    await c.message.edit_text(ftl.excel.impor.text())
    await state.set_state(ImportTeachers.input_excel)


@router.message(
    F.document.file_name.casefold().endswith(".xlsx"),
    StateFilter(ImportTeachers.input_excel),
)
async def on_input_excel(
    m: types.Message,
    bot: Bot,
    state: FSMContext,
    ftl: TranslatorRunner,
):
    downloaded = await bot.download(m.document.file_id)
    importer = TeacherExcelImporter(downloaded)
    teachers = importer.import_()
    markup = get_input_excel_markup(ftl)
    await m.answer(
        ftl.excel.impor.detected.records.text(count=len(teachers)),
        reply_markup=markup,
    )
    await state.update_data(teachers=teachers)


@router.callback_query(
    ExcelCallbackData.filter(
        and_(F.action == ExcelAction.UPLOAD, F.registry == Registry.TEACHERS)
    ),
    StateFilter(ImportTeachers.input_excel),
)
async def on_upload_teachers(
    c: types.CallbackQuery,
    state: FSMContext,
    root_service: RootService,
    ftl: TranslatorRunner,
):
    data = await state.get_data()
    count = await root_service.teacher.import_(data["teachers"])
    await c.message.delete()
    await c.message.answer(ftl.excel.impor.upload.records.text(count=count))
    await c.answer()
