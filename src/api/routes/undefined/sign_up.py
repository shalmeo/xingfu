from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.undefined.create import UndefinedCreateRequest
from src.application.undefined.dto.undefined import UndefinedCreateDTO
from src.application.undefined.interfaces.uow import IUndefinedUoW
from src.application.undefined.usecases.undefined import AddUndefined
from src.application.user.dto.user import UserCreateDTO
from src.domain.user.models.user import UserRole

router = APIRouter()


@router.post("/undefined")
async def create_undefined(undefined: UndefinedCreateRequest, uow: IUndefinedUoW = Depends(providers.uow_provider)):
    await AddUndefined(uow)(
        UserCreateDTO(
            email=undefined.email,
            timezone=undefined.timezone,
            phone=undefined.phone,
            role=UserRole.UNCERTAIN,
            telegram_id=undefined.telegram_id,
            telegram_username=undefined.telegram_username,
        ),
        UndefinedCreateDTO(
            name=undefined.name,
            surname=undefined.surname,
            patronymic=undefined.patronymic,
            birthday=undefined.birthday,
        ),
    )


#   await some.send_message()
