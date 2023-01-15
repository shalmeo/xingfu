from operator import and_

from aiogram import Router, F, types

from src.application.group.interfaces.uow import IGroupUoW
from src.application.group.usecases.group import GetAllGroups
from src.bot.keyboards.registry import Registry
from src.bot.keyboards.root.excel import ExcelCallbackData, ExcelAction
from src.infrastructure.exporters.excel.group.exporter import GroupExcelExporter

router = Router()


@router.callback_query(
    ExcelCallbackData.filter(
        and_(F.action == ExcelAction.EXPORT, F.registry == Registry.GROUPS)
    )
)
async def export(c: types.CallbackQuery, uow: IGroupUoW):
    exporter: GroupExcelExporter = GroupExcelExporter(
        template_path="resources/excel/groups.xlsx"
    )
    exporter.set_title("Реестр")
    groups = await GetAllGroups(uow)()
    output = exporter.save(groups)
    file = types.BufferedInputFile(
        file=output.read(),
        filename="Реестр Групп.xlsx",
    )
    await c.message.answer_document(file)
    await c.answer()
