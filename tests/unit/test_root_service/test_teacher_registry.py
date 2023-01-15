import datetime

import pytest

from src.application.common.exceptions.common import NotFound
from src.application.teacher.dto.teacher import TeacherCreateDTO, TeacherUpdateDTO
from src.application.teacher.usecases.teacher import (
    AddTeacher,
    GetTeacher,
    DeleteTeacher,
    UpdateTeacher,
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
    LEVEL,
    DESCRIPTION,
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
teacher_create = TeacherCreateDTO(
    name=NAME,
    surname=SURNAME,
    patronymic=PATRONYMIC,
    birthday=BIRTHDAY,
    level=None,
    description=None,
)


async def test_create_teacher(uow):
    await AddTeacher(uow)(user_create, teacher_create)


async def test_get_teacher(uow):
    teacher = await AddTeacher(uow)(user_create, teacher_create)
    get_teacher = await GetTeacher(uow)(teacher)

    assert teacher == get_teacher.id


async def test_delete_teacher(uow):
    teacher = await AddTeacher(uow)(user_create, teacher_create)
    await DeleteTeacher(uow)(teacher)

    with pytest.raises(NotFound):
        await GetTeacher(uow)(teacher)


async def test_update_teacher(uow):
    addteacher = await AddTeacher(uow)(user_create, teacher_create)
    teacher_update = TeacherUpdateDTO(
        id=addteacher,
        name=NAME + UPDATE,
        surname=SURNAME + UPDATE,
        patronymic=PATRONYMIC + UPDATE,
        birthday=BIRTHDAY,
        level=LEVEL,
        description=DESCRIPTION,
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
    await UpdateTeacher(uow)(user_update, teacher_update)
    teacher = await GetTeacher(uow)(addteacher)

    assert teacher.name == teacher_update.name
    assert teacher.surname == teacher_update.surname
    assert teacher.patronymic == teacher_update.patronymic
    assert teacher.birthday == teacher_update.birthday
    assert teacher.level == teacher_update.level
    assert teacher.description == teacher_update.description
    assert teacher.access_end == teacher_update.access_end
    assert teacher.access_start == teacher_update.access_start

    assert teacher.user.email == user_update.email
    assert teacher.user.phone == user_update.phone
    assert teacher.user.telegram_id == user_update.telegram_id
    assert teacher.user.telegram_username == user_update.telegram_username
    assert teacher.user.timezone == user_update.timezone


# async def test_load_teachers(
#     root_service: RootService,
#     teachers_excel_path: str,
# ):
#     importer = TeacherExcelImporter(teachers_excel_path)
#     teachers = importer.import_()
#     assert teachers == [
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
# async def test_import_teacher(
#     uow: SQLAlchemyUoW,
#     root_service: RootService,
#     teachers_excel_path: str,
# ):
#     importer = TeacherExcelImporter(teachers_excel_path)
#     teachers = importer.import_()
#     for teacher in teachers:
#         import_teacher = dto.ImportTeacher(
#             name=teacher["name"],
#             surname=teacher["surname"],
#             patronymic=teacher["patronymic"],
#             telegram_id=teacher["telegram_id"],
#             telegram_username=teacher["username"],
#             birthday=teacher["birthday"],
#             email=teacher["email"],
#             phone=teacher["phone"],
#             timezone=teacher["timezone"],
#             level=teacher["level"],
#             description=teacher["description"],
#         )
#         await uow.root.import_teacher(import_teacher)
