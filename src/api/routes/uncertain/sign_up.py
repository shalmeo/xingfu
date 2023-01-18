from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.uncertain.create import UncertainCreateRequest
from src.application.uncertain.dto.uncertain import UncertainCreateDTO
from src.application.uncertain.interfaces.uow import IUncertainUoW
from src.application.uncertain.usecases.uncertain import AddUncertain
from src.application.user.dto.user import UserCreateDTO
from src.domain.user.models.user import UserRole

router = APIRouter()


@router.post("/")
async def create_uncertain(uncertain: UncertainCreateRequest, uow: IUncertainUoW = Depends(providers.uow_provider)):
    await AddUncertain(uow)(
        UserCreateDTO(
            email=uncertain.email,
            timezone=uncertain.timezone,
            phone=uncertain.phone,
            role=UserRole.UNCERTAIN,
            telegram_id=uncertain.telegram_id,
            telegram_username=uncertain.telegram_username,
        ),
        UncertainCreateDTO(
            name=uncertain.name,
            surname=uncertain.surname,
            patronymic=uncertain.patronymic,
            birthday=uncertain.birthday,
        ),
    )
