from uuid import UUID
from fastapi import APIRouter, Depends

from src.api import providers
from src.application.group.interfaces.uow import IGroupUoW
from src.application.group.usecases.group import GetGroup
from src.api.responses.root.group.get import (
    GroupResponse,
    StudentResponse,
    TeacherResponse,
)

router = APIRouter()


@router.get("/group/{id}")
async def get_group(id: UUID, uow: IGroupUoW = Depends(providers.uow_provider)):
    group = await GetGroup(uow)(id)
    teacher = None
    if group.teacher:
        teacher = TeacherResponse(
            id=group.teacher.id,
            name=group.teacher.name,
            surname=group.teacher.surname,
            patronymic=group.teacher.patronymic,
        )
    return GroupResponse(
        name=group.name,
        description=group.description,
        teacher=teacher,
        students=[
            StudentResponse(
                id=student.id,
                name=student.name,
                surname=student.surname,
                patronymic=student.patronymic,
            )
            for student in group.students
        ],
    )
