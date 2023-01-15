from uuid import UUID
from fastapi import APIRouter, Depends

from src.api import providers
from src.application.admin.interfaces.uow import IAdminUoW
from src.application.admin.usecases.admin import GetAdmin, GetAllAdmins
from src.api.responses.root.admin.get import (
    Admin,
    AdminResponse,
    AdminsReponse,
)

router = APIRouter()


@router.get("/admin/{id}")
async def get_admin(id: UUID, uow: IAdminUoW = Depends(providers.uow_provider)):
    admin = await GetAdmin(uow)(id)

    return AdminResponse(
        surname=admin.surname,
        name=admin.name,
        patronymic=admin.patronymic,
        phone=admin.user.phone,
        telegram_id=admin.user.telegram_id,
        telegram_username=admin.user.telegram_username,
        birthday=admin.birthday.strftime(r"%Y-%m-%d"),
        email=admin.user.email,
        level=admin.level,
        description=admin.description,
        timezone=admin.user.timezone,
        access_start=admin.access_start.strftime(r"%Y-%m-%d"),
        access_end=admin.access_end.strftime(r"%Y-%m-%d"),
    )


@router.get("/admins")
async def get_admins(uow: IAdminUoW = Depends(providers.uow_provider)):
    admins = await GetAllAdmins(uow)()

    return AdminsReponse(
        admins=[
            Admin(
                id=admin.id,
                name=admin.name,
                surname=admin.surname,
                patronymic=admin.patronymic,
            )
            for admin in admins
        ]
    )
