from operator import and_

from aiogram import Router, F, types

from src.application.admin.interfaces.uow import IAdminUoW
from src.application.admin.usecases.admin import GetAllAdmins
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.infrastructure.exporters.excel.admin.exporter import AdminExcelExporter

router = Router()


@router.callback_query(
    ExcelCallbackData.filter(
        and_(F.action == ExcelAction.EXPORT, F.registry == Registry.ADMINS)
    )
)
async def export(c: types.CallbackQuery, uow: IAdminUoW):
    exporter = AdminExcelExporter(template_path="resources/excel/admins.xlsx")
    exporter.set_title("Реестр")
    admins = await GetAllAdmins(uow)()
    output = exporter.save(admins)
    file = types.BufferedInputFile(
        file=output.read(),
        filename="Реестр Администраторов.xlsx",
    )
    await c.message.answer_document(file)
    await c.answer()
