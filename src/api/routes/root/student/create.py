from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.root.student.create import StudentCreateRequest
from src.application.student.dto.student import StudentCreateDTO
from src.application.student.interfaces.uow import IStudentUoW
from src.application.student.usecases.student import AddStudent
from src.application.user.dto.user import UserCreateDTO
from src.domain.user.models.user import UserRole

router = APIRouter()


@router.post(
    "/student",
    status_code=201,
    responses={409: {"detail": "..."}},
)
async def student_create(
    student: StudentCreateRequest, uow: IStudentUoW = Depends(providers.uow_provider)
):
    await AddStudent(uow)(
        UserCreateDTO(
            email=student.email,
            timezone=student.timezone,
            phone=student.phone,
            role=UserRole.ADMIN,
            telegram_id=student.telegram_id,
            telegram_username=student.telegram_username,
        ),
        StudentCreateDTO(
            name=student.name,
            surname=student.surname,
            patronymic=student.patronymic,
            birthday=student.birthday,
        ),
    )
