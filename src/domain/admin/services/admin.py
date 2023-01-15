from datetime import date

from src.domain.admin.models.admin import Admin


def create_admin(
    user_id: int,
    name: str,
    surname: str,
    patronymic: str,
    birthday: date,
    level: str,
    description: str,
) -> Admin:
    return Admin(
        user_id=user_id,
        name=name,
        surname=surname,
        patronymic=patronymic,
        birthday=birthday,
        level=level,
        description=description,
    )


def update_admin(
    admin: Admin,
    name: str,
    surname: str,
    patronymic: str,
    birthday: date,
    level: str,
    description: str,
    access_start: date,
    access_end: date,
) -> Admin:
    admin.name = name
    admin.surname = surname
    admin.patronymic = patronymic
    admin.birthday = birthday
    admin.level = level
    admin.description = description
    admin.access_start = access_start
    admin.access_end = access_end

    return admin
