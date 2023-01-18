import pytest

from src.application.common.exceptions.common import NotFound
from src.application.teacher.usecases.teacher import GetTeacher
from src.application.uncertain.dto.uncertain import UncertainCreateDTO
from src.application.uncertain.usecases.uncertain import (
    AddUncertain,
    GetUncertain,
    DeleteUncertain,
    DetermineUncertain,
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
uncertain_create = UncertainCreateDTO(
    name=NAME,
    surname=SURNAME,
    patronymic=PATRONYMIC,
    birthday=BIRTHDAY,
)


async def test_create_uncertain(uow):
    await AddUncertain(uow)(user_create, uncertain_create)


async def test_get_uncertain(uow):
    uncertain = await AddUncertain(uow)(user_create, uncertain_create)
    get_uncertain = await GetUncertain(uow)(uncertain)

    assert uncertain == get_uncertain.id


async def test_delete_uncertain(uow):
    uncertain = await AddUncertain(uow)(user_create, uncertain_create)
    await DeleteUncertain(uow)(uncertain)

    with pytest.raises(NotFound):
        await GetUncertain(uow)(uncertain)


async def test_determine_uncertain(uow):
    uncertain_id = await AddUncertain(uow)(user_create, uncertain_create)
    uncertain = await GetUncertain(uow)(uncertain_id)

    teacher_id = await DetermineUncertain(uow)(uncertain_id, UserRole.TEACHER)
    teacher = await GetTeacher(uow)(teacher_id)

    assert teacher.user.id == uncertain.user.id
