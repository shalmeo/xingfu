from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.root.admin.create import AdminCreateRequest
from src.application.admin.dto.admin import AdminCreateDTO
from src.application.admin.interfaces.uow import IAdminUoW
from src.application.admin.usecases.admin import AddAdmin
from src.application.user.dto.user import UserCreateDTO
from src.domain.user.models.user import UserRole

router = APIRouter()


@router.post(
    "/admin",
    status_code=201,
    responses={409: {"detail": "..."}},
)
async def admin_create(
    admin: AdminCreateRequest, uow: IAdminUoW = Depends(providers.uow_provider)
):
    await AddAdmin(uow)(
        UserCreateDTO(
            email=admin.email,
            timezone=admin.timezone,
            phone=admin.phone,
            role=UserRole.ADMIN,
            telegram_id=admin.telegram_id,
            telegram_username=admin.telegram_username,
        ),
        AdminCreateDTO(
            name=admin.name,
            surname=admin.surname,
            patronymic=admin.patronymic,
            birthday=admin.birthday,
            level=admin.level,
            description=admin.description,
        ),
    )
