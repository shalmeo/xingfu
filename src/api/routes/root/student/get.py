from uuid import UUID
from fastapi import APIRouter, Depends

from src.api import providers
from src.application.student.interfaces.uow import IStudentUoW
from src.application.student.usecases.student import (
    GetGroupStudents,
    GetStudent,
    GetAllStudents,
)
from src.api.responses.root.student.get import (
    Student,
    StudentResponse,
    StudentsReponse,
)

router = APIRouter()


@router.get("/student/{id}")
async def get_student(id: UUID, uow: IStudentUoW = Depends(providers.uow_provider)):
    student = await GetStudent(uow)(id)

    return StudentResponse(
        surname=student.surname,
        name=student.name,
        patronymic=student.patronymic,
        phone=student.user.phone,
        telegram_id=student.user.telegram_id,
        telegram_username=student.user.telegram_username,
        birthday=student.birthday.strftime(r"%Y-%m-%d"),
        email=student.user.email,
        timezone=student.user.timezone,
        access_start=student.access_start.strftime(r"%Y-%m-%d"),
        access_end=student.access_end.strftime(r"%Y-%m-%d"),
    )


@router.get("/students")
async def get_students(uow: IStudentUoW = Depends(providers.uow_provider)):
    students = await GetAllStudents(uow)()

    return StudentsReponse(
        students=[
            Student(
                id=student.id,
                name=student.name,
                surname=student.surname,
                patronymic=student.patronymic,
            )
            for student in students
        ]
    )