from datetime import date
from typing import Optional

from src.domain.teacher.models.teacher import Teacher


def create_teacher(
    user_id: int,
    name: str,
    surname: str,
    patronymic: str,
    birthday: date,
    level: Optional[str] = None,
    description: Optional[str] = None,
) -> Teacher:
    return Teacher(
        user_id=user_id,
        name=name,
        surname=surname,
        patronymic=patronymic,
        birthday=birthday,
        level=level,
        description=description,
    )


def update_teacher(
    teacher: Teacher,
    name: str,
    surname: str,
    patronymic: str,
    birthday: date,
    level: str,
    description: str,
    access_start: date,
    access_end: date,
) -> Teacher:
    teacher.name = name
    teacher.surname = surname
    teacher.patronymic = patronymic
    teacher.birthday = birthday
    teacher.level = level
    teacher.description = description
    teacher.access_start = access_start
    teacher.access_end = access_end

    return teacher
