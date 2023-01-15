from typing import TYPE_CHECKING

from aiogram import Router, types, F
from fluentogram import TranslatorRunner

from src.application.admin.interfaces.uow import IAdminUoW
from src.application.admin.usecases.admin import GetAdmin
from src.bot.constants import MISS
from src.bot.keyboards.root.admins.callback_data import (
    AdminCallbackData,
    AdminAction,
)
from src.bot.keyboards.root.admins.info import get_admin_info_markup

if TYPE_CHECKING:
    from src.infrastructure.localization.translator import TranslatorRunner

router = Router()


@router.callback_query(AdminCallbackData.filter(F.action == AdminAction.INFO))
async def on_admin_info(
    c: types.CallbackQuery,
    callback_data: AdminCallbackData,
    base_url: str,
    ftl: TranslatorRunner,
    uow: IAdminUoW,
):
    admin = await GetAdmin(uow)(callback_data.admin_id)
    text = ftl.root.profile.registry.admin.info(
        surname=admin.surname,
        name=admin.name,
        patronymic=admin.patronymic or MISS,
        phone=f"+{admin.user.phone}" if admin.user.phone else MISS,
        email=admin.user.email,
        telegram_id=str(admin.user.telegram_id) if admin.user.telegram_id else MISS,
        username=admin.user.telegram_username or MISS,
        birthday=admin.birthday,
        level=admin.level or MISS,
        description=admin.description or MISS,
        access_start=admin.access_start,
        access_end=admin.access_end,
        timezone=admin.user.timezone,
    )
    markup = get_admin_info_markup(ftl, callback_data.admin_id, base_url)
    await c.message.edit_text(text, reply_markup=markup)
    await c.answer()
