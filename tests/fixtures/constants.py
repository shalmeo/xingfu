import datetime

import pytest

from src.application.student.dto.student import StudentCreateDTO
from src.application.teacher.dto.teacher import TeacherCreateDTO
from src.application.user.dto.user import UserCreateDTO
from src.domain.user.models.user import UserRole

NAME = "Марк"
SURNAME = "Тестов"
PATRONYMIC = "Тестович"
BIRTHDAY = datetime.date.today()
EMAIL = "testovmark@mail.ru"
TIMEZONE = "UTC+3"
TELEGRAM_ID = 99999999
PHONE = 79993334455

LEVEL = "LEVEL"
DESCRIPTION = "DESCRIPTION"


@pytest.fixture
def user_create():
    return UserCreateDTO(
        email=EMAIL,
        timezone=TIMEZONE,
        phone=PHONE,
        role=UserRole.TEACHER,
        telegram_id=None,
        telegram_username=None,
    )


@pytest.fixture
def teacher_create():
    return TeacherCreateDTO(
        name=NAME,
        surname=SURNAME,
        patronymic=PATRONYMIC,
        birthday=BIRTHDAY,
        level=None,
        description=None,
    )


@pytest.fixture
def student_create():
    return StudentCreateDTO(
        name=NAME,
        surname=SURNAME,
        patronymic=PATRONYMIC,
        birthday=BIRTHDAY,
    )
