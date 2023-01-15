from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.root.teacher.create import TeacherCreateRequest
from src.application.teacher.dto.teacher import TeacherCreateDTO
from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.teacher.usecases.teacher import AddTeacher
from src.application.user.dto.user import UserCreateDTO
from src.domain.user.models.user import UserRole

router = APIRouter()


@router.post(
    "/teacher",
    status_code=201,
    responses={409: {"detail": "..."}},
)
async def teacher_create(
    teacher: TeacherCreateRequest, uow: ITeacherUoW = Depends(providers.uow_provider)
):
    await AddTeacher(uow)(
        UserCreateDTO(
            email=teacher.email,
            timezone=teacher.timezone,
            phone=teacher.phone,
            role=UserRole.TEACHER,
            telegram_id=teacher.telegram_id,
            telegram_username=teacher.telegram_username,
        ),
        TeacherCreateDTO(
            name=teacher.name,
            surname=teacher.surname,
            patronymic=teacher.patronymic,
            birthday=teacher.birthday,
            level=teacher.level,
            description=teacher.description,
        ),
    )
