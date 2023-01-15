from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.admin.interfaces.uow import IAdminUoW
from src.application.admin.usecases.admin import DeleteAdmin
from src.bot.keyboards.root.admins.callback_data import (
    AdminCallbackData,
    AdminAction,
)

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(AdminCallbackData.filter(F.action == AdminAction.DELETE))
async def on_delete_admin(
    c: types.CallbackQuery,
    callback_data: AdminCallbackData,
    uow: IAdminUoW,
    ftl: TranslatorRunner,
):
    await DeleteAdmin(uow)(callback_data.admin_id)
    await c.message.delete()
    await c.message.answer(ftl.root.profile.registry.user.successfully.deleted())
    await c.answer()
