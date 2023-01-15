from uuid import UUID
from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.root.student.update import StudentUpdateRequest
from src.application.student.dto.student import StudentUpdateDTO
from src.application.student.interfaces.uow import IStudentUoW
from src.application.student.usecases.student import UpdateStudent
from src.application.user.dto.user import UserUpdateDTO
from src.domain.user.models.user import UserRole

router = APIRouter()


@router.put("/student/{id}", status_code=204, responses={409: {"detail": "Conflict"}})
async def student_update(
    id: UUID,
    student: StudentUpdateRequest,
    uow: IStudentUoW = Depends(providers.uow_provider),
):
    await UpdateStudent(uow)(
        UserUpdateDTO(
            email=student.email,
            timezone=student.timezone,
            phone=student.phone,
            role=UserRole.TEACHER,
            telegram_id=student.telegram_id,
            telegram_username=student.telegram_username,
        ),
        StudentUpdateDTO(
            id=id,
            name=student.name,
            surname=student.surname,
            patronymic=student.patronymic,
            birthday=student.birthday,
            access_start=student.access_start,
            access_end=student.access_end,
        ),
    )
