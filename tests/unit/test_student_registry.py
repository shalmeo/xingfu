import datetime

import pytest

from src.application.common.exceptions.common import NotFound
from src.application.student.dto.student import StudentCreateDTO, StudentUpdateDTO
from src.application.student.usecases.student import (
    AddStudent,
    GetStudent,
    DeleteStudent,
    UpdateStudent,
)
from src.application.user.dto.user import UserCreateDTO, UserUpdateDTO
from src.domain.user.models.user import UserRole
from tests.fixtures.constants import (
    NAME,
    SURNAME,
    PATRONYMIC,
    BIRTHDAY,
    EMAIL,
    TIMEZONE,
    PHONE,
)

UPDATE = "UPDATE"

user_create = UserCreateDTO(
    email=EMAIL,
    timezone=TIMEZONE,
    phone=PHONE,
    role=UserRole.TEACHER,
    telegram_id=None,
    telegram_username=None,
)
student_create = StudentCreateDTO(
    name=NAME,
    surname=SURNAME,
    patronymic=PATRONYMIC,
    birthday=BIRTHDAY,
)


async def test_create_student(uow):
    await AddStudent(uow)(user_create, student_create)


async def test_get_student(uow):
    student = await AddStudent(uow)(user_create, student_create)
    get_student = await GetStudent(uow)(student)

    assert student == get_student.id


async def test_delete_student(uow):
    student = await AddStudent(uow)(user_create, student_create)
    await DeleteStudent(uow)(student)

    with pytest.raises(NotFound):
        await GetStudent(uow)(student)


async def test_update_student(uow):
    addstudent = await AddStudent(uow)(user_create, student_create)
    student_update = StudentUpdateDTO(
        id=addstudent,
        name=NAME + UPDATE,
        surname=SURNAME + UPDATE,
        patronymic=PATRONYMIC + UPDATE,
        birthday=BIRTHDAY,
        access_start=datetime.datetime.now(),
        access_end=datetime.datetime.now(),
    )
    user_update = UserUpdateDTO(
        email=EMAIL + UPDATE,
        timezone=TIMEZONE + UPDATE,
        phone=PHONE,
        role=UserRole.TEACHER,
        telegram_id=999,
        telegram_username="username",
    )
    await UpdateStudent(uow)(user_update, student_update)
    student = await GetStudent(uow)(addstudent)

    assert student.name == student_update.name
    assert student.surname == student_update.surname
    assert student.patronymic == student_update.patronymic
    assert student.birthday == student_update.birthday
    assert student.access_end == student_update.access_end
    assert student.access_start == student_update.access_start

    assert student.user.email == user_update.email
    assert student.user.phone == user_update.phone
    assert student.user.telegram_id == user_update.telegram_id
    assert student.user.telegram_username == user_update.telegram_username
    assert student.user.timezone == user_update.timezone


# async def test_load_students(
#     root_service: RootService,
#     students_excel_path: str,
# ):
#     importer = StudentExcelImporter(students_excel_path)
#     students = importer.import_()
#     assert students == [
#         {
#             "timezone": TIMEZONE,
#             "name": NAME,
#             "surname": SURNAME,
#             "patronymic": PATRONYMIC,
#             "email": EMAIL,
#             "username": None,
#             "telegram_id": TELEGRAM_ID,
#             "phone": PHONE,
#             "level": None,
#             "description": None,
#             "birthday": "2000-10-13 00:00:00",
#         }
#     ]
#
#
# async def test_import_student(
#     uow: SQLAlchemyUoW,
#     root_service: RootService,
#     students_excel_path: str,
# ):
#     importer = StudentExcelImporter(students_excel_path)
#     students = importer.import_()
#     for student in students:
#         import_student = dto.ImportStudent(
#             name=student["name"],
#             surname=student["surname"],
#             patronymic=student["patronymic"],
#             telegram_id=student["telegram_id"],
#             telegram_username=student["username"],
#             birthday=student["birthday"],
#             email=student["email"],
#             phone=student["phone"],
#             timezone=student["timezone"],
#             level=student["level"],
#             description=student["description"],
#         )
#         await uow.root.import_student(import_student)
