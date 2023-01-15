from uuid import UUID
from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.root.admin.update import AdminUpdateRequest
from src.application.admin.dto.admin import AdminUpdateDTO
from src.application.admin.interfaces.uow import IAdminUoW
from src.application.admin.usecases.admin import UpdateAdmin
from src.application.user.dto.user import UserUpdateDTO
from src.domain.user.models.user import UserRole

router = APIRouter()


@router.put("/admin/{id}", status_code=204, responses={409: {"detail": "Conflict"}})
async def admin_update(
    id: UUID,
    admin: AdminUpdateRequest,
    uow: IAdminUoW = Depends(providers.uow_provider),
):
    await UpdateAdmin(uow)(
        UserUpdateDTO(
            email=admin.email,
            timezone=admin.timezone,
            phone=admin.phone,
            role=UserRole.TEACHER,
            telegram_id=admin.telegram_id,
            telegram_username=admin.telegram_username,
        ),
        AdminUpdateDTO(
            id=id,
            name=admin.name,
            surname=admin.surname,
            patronymic=admin.patronymic,
            birthday=admin.birthday,
            level=admin.level,
            description=admin.description,
            access_start=admin.access_start,
            access_end=admin.access_end,
        ),
    )
