import pytest

from src.application.common.exceptions.common import NotFound
from src.application.teacher.usecases.teacher import GetTeacher
from src.application.undefined.dto.undefined import UndefinedCreateDTO
from src.application.undefined.usecases.undefined import (
    AddUndefined,
    GetUndefined,
    DeleteUndefined,
    DetermineUndefined,
)
from src.application.user.dto.user import UserCreateDTO
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
undefined_create = UndefinedCreateDTO(
    name=NAME,
    surname=SURNAME,
    patronymic=PATRONYMIC,
    birthday=BIRTHDAY,
)


async def test_create_undefined(uow):
    await AddUndefined(uow)(user_create, undefined_create)


async def test_get_undefined(uow):
    undefined = await AddUndefined(uow)(user_create, undefined_create)
    get_undefined = await GetUndefined(uow)(undefined)

    assert undefined == get_undefined.id


async def test_delete_undefined(uow):
    undefined = await AddUndefined(uow)(user_create, undefined_create)
    await DeleteUndefined(uow)(undefined)

    with pytest.raises(NotFound):
        await GetUndefined(uow)(undefined)


async def test_determine_undefined(uow):
    undefined_id = await AddUndefined(uow)(user_create, undefined_create)
    undefined = await GetUndefined(uow)(undefined_id)

    teacher_id = await DetermineUndefined(uow)(undefined_id, UserRole.TEACHER)
    teacher = await GetTeacher(uow)(teacher_id)

    assert teacher.user.id == undefined.user.id
