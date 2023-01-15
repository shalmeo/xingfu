from uuid import UUID
from fastapi import APIRouter, Depends

from src.api import providers
from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.teacher.usecases.teacher import GetTeacher, GetAllTeachers
from src.api.responses.root.teacher.get import (
    Teacher,
    TeacherResponse,
    TeachersReponse,
)

router = APIRouter()


@router.get("/teacher/{id}")
async def get_teacher(id: UUID, uow: ITeacherUoW = Depends(providers.uow_provider)):
    teacher = await GetTeacher(uow)(id)

    return TeacherResponse(
        surname=teacher.surname,
        name=teacher.name,
        patronymic=teacher.patronymic,
        phone=teacher.user.phone,
        telegram_id=teacher.user.telegram_id,
        telegram_username=teacher.user.telegram_username,
        birthday=teacher.birthday.strftime(r"%Y-%m-%d"),
        email=teacher.user.email,
        level=teacher.level,
        description=teacher.description,
        timezone=teacher.user.timezone,
        access_start=teacher.access_start.strftime(r"%Y-%m-%d"),
        access_end=teacher.access_end.strftime(r"%Y-%m-%d"),
    )


@router.get("/teachers")
async def get_teachers(uow: ITeacherUoW = Depends(providers.uow_provider)):
    teachers = await GetAllTeachers(uow)()

    return TeachersReponse(
        teachers=[
            Teacher(
                id=teacher.id,
                name=teacher.name,
                surname=teacher.surname,
                patronymic=teacher.patronymic,
            )
            for teacher in teachers
        ]
    )
