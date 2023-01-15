from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.group.interfaces.uow import IGroupUoW
from src.application.group.usecases.group import DeleteGroup
from src.bot.keyboards.root.groups.callback_data import GroupCallbackData, GroupAction

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(GroupCallbackData.filter(F.action == GroupAction.DELETE))
async def on_delete_group(
    c: types.CallbackQuery,
    callback_data: GroupCallbackData,
    uow: IGroupUoW,
    ftl: TranslatorRunner,
):
    await DeleteGroup(uow)(callback_data.group_id)
    await c.message.delete()
    await c.message.answer(ftl.root.profile.registry.group.successfully.deleted())
    await c.answer()
