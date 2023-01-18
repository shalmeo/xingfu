import pytest

from src.application.common.exceptions.common import NotFound
from src.application.group.dto.group import GroupCreateDTO, GroupUpdateDTO
from src.application.group.usecases.group import (
    AddGroup,
    GetGroup,
    DeleteGroup,
    UpdateGroup,
)
from src.application.student.usecases.student import AddStudent
from src.application.teacher.usecases.teacher import AddTeacher
from src.application.user.dto.user import UserCreateDTO
from src.domain.user.models.user import UserRole
from tests.fixtures.constants import EMAIL, TIMEZONE

UPDATE = "UPDATE"


async def test_create_group(uow, user_create, teacher_create):
    teacher_id = await AddTeacher(uow)(user_create, teacher_create)
    group_create = GroupCreateDTO(name="TestGroup", description=None, teacher_id=teacher_id, students=[])
    await AddGroup(uow)(group_create)


async def test_get_group(uow, user_create, teacher_create):
    teacher_id = await AddTeacher(uow)(user_create, teacher_create)
    group_create = GroupCreateDTO(name="TestGroup", description=None, teacher_id=teacher_id, students=[])
    group = await AddGroup(uow)(group_create)
    get_group = await GetGroup(uow)(group)

    assert group == get_group.id


async def test_delete_group(uow):
    group_create = GroupCreateDTO(name="TestGroup", description=None, teacher_id=None, students=[])
    group = await AddGroup(uow)(group_create)
    await DeleteGroup(uow)(group)

    with pytest.raises(NotFound):
        await GetGroup(uow)(group)


async def test_update_group(uow, user_create, teacher_create, student_create):
    teacher_user_create = UserCreateDTO(
        email=EMAIL + "TEACHER",
        timezone=TIMEZONE,
        role=UserRole.TEACHER,
    )
    student_user_create = UserCreateDTO(
        email=EMAIL + "STUDENT",
        timezone=TIMEZONE,
        role=UserRole.TEACHER,
    )

    teacher_id = await AddTeacher(uow)(teacher_user_create, teacher_create)
    student_id = await AddStudent(uow)(student_user_create, student_create)
    group_create = GroupCreateDTO(name="TestGroup", description=None, teacher_id=teacher_id, students=[])
    addgroup = await AddGroup(uow)(group_create)
    group_update = GroupUpdateDTO(
        id=addgroup, name="TestGroup" + UPDATE, description="DESCRIPTION", teacher_id=None, students=[student_id]
    )
    await UpdateGroup(uow)(group_update)
    group = await GetGroup(uow)(addgroup)

    assert group.name == group_update.name
    assert group.description == group_update.description
    assert group.teacher is None
    assert group.students[0].id == student_id


# async def test_load_groups(
#     root_service: RootService,
#     groups_excel_path: str,
# ):
#     importer = GroupExcelImporter(groups_excel_path)
#     groups = importer.import_()
#     assert groups == [
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
# async def test_import_group(
#     uow: SQLAlchemyUoW,
#     root_service: RootService,
#     groups_excel_path: str,
# ):
#     importer = GroupExcelImporter(groups_excel_path)
#     groups = importer.import_()
#     for group in groups:
#         import_group = dto.ImportGroup(
#             name=group["name"],
#             surname=group["surname"],
#             patronymic=group["patronymic"],
#             telegram_id=group["telegram_id"],
#             telegram_username=group["username"],
#             birthday=group["birthday"],
#             email=group["email"],
#             phone=group["phone"],
#             timezone=group["timezone"],
#             level=group["level"],
#             description=group["description"],
#         )
#         await uow.root.import_group(import_group)
