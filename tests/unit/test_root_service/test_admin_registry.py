import datetime

import pytest

from src.application.common.exceptions.common import NotFound
from src.application.admin.dto.admin import AdminCreateDTO, AdminUpdateDTO
from src.application.admin.usecases.admin import (
    AddAdmin,
    GetAdmin,
    DeleteAdmin,
    UpdateAdmin,
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
admin_create = AdminCreateDTO(
    name=NAME,
    surname=SURNAME,
    patronymic=PATRONYMIC,
    birthday=BIRTHDAY,
    level=None,
    description=None,
)


async def test_create_admin(uow):
    await AddAdmin(uow)(user_create, admin_create)


async def test_get_admin(uow):
    admin = await AddAdmin(uow)(user_create, admin_create)
    get_admin = await GetAdmin(uow)(admin)

    assert admin == get_admin.id


async def test_delete_admin(uow):
    admin = await AddAdmin(uow)(user_create, admin_create)
    await DeleteAdmin(uow)(admin)

    with pytest.raises(NotFound):
        await GetAdmin(uow)(admin)


async def test_update_admin(uow):
    addadmin = await AddAdmin(uow)(user_create, admin_create)
    admin_update = AdminUpdateDTO(
        id=addadmin,
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
    await UpdateAdmin(uow)(user_update, admin_update)
    admin = await GetAdmin(uow)(addadmin)

    assert admin.name == admin_update.name
    assert admin.surname == admin_update.surname
    assert admin.patronymic == admin_update.patronymic
    assert admin.birthday == admin_update.birthday
    assert admin.level == admin_update.level
    assert admin.description == admin_update.description
    assert admin.access_end == admin_update.access_end
    assert admin.access_start == admin_update.access_start

    assert admin.user.email == user_update.email
    assert admin.user.phone == user_update.phone
    assert admin.user.telegram_id == user_update.telegram_id
    assert admin.user.telegram_username == user_update.telegram_username
    assert admin.user.timezone == user_update.timezone


# async def test_load_admins(
#     root_service: RootService,
#     admins_excel_path: str,
# ):
#     importer = AdminExcelImporter(admins_excel_path)
#     admins = importer.import_()
#     assert admins == [
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
# async def test_import_admin(
#     uow: SQLAlchemyUoW,
#     root_service: RootService,
#     admins_excel_path: str,
# ):
#     importer = AdminExcelImporter(admins_excel_path)
#     admins = importer.import_()
#     for admin in admins:
#         import_admin = dto.ImportAdmin(
#             name=admin["name"],
#             surname=admin["surname"],
#             patronymic=admin["patronymic"],
#             telegram_id=admin["telegram_id"],
#             telegram_username=admin["username"],
#             birthday=admin["birthday"],
#             email=admin["email"],
#             phone=admin["phone"],
#             timezone=admin["timezone"],
#             level=admin["level"],
#             description=admin["description"],
#         )
#         await uow.root.import_admin(import_admin)
