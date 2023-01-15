from uuid import UUID
from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.root.teacher.update import TeacherUpdateRequest
from src.application.teacher.dto.teacher import TeacherUpdateDTO
from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.teacher.usecases.teacher import UpdateTeacher
from src.application.user.dto.user import UserUpdateDTO
from src.domain.user.models.user import UserRole

router = APIRouter()


@router.put("/teacher/{id}", status_code=204, responses={409: {"detail": "Conflict"}})
async def teacher_update(
    id: UUID,
    teacher: TeacherUpdateRequest,
    uow: ITeacherUoW = Depends(providers.uow_provider),
):
    await UpdateTeacher(uow)(
        UserUpdateDTO(
            email=teacher.email,
            timezone=teacher.timezone,
            phone=teacher.phone,
            role=UserRole.TEACHER,
            telegram_id=teacher.telegram_id,
            telegram_username=teacher.telegram_username,
        ),
        TeacherUpdateDTO(
            id=id,
            name=teacher.name,
            surname=teacher.surname,
            patronymic=teacher.patronymic,
            birthday=teacher.birthday,
            level=teacher.level,
            description=teacher.description,
            access_start=teacher.access_start,
            access_end=teacher.access_end,
        ),
    )
