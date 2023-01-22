from datetime import date

from src.domain.undefined.models.undefined import Undefined


def create_undefined(
    user_id: int,
    name: str,
    surname: str,
    patronymic: str,
    birthday: date,
) -> Undefined:
    return Undefined(
        user_id=user_id,
        name=name,
        surname=surname,
        patronymic=patronymic,
        birthday=birthday,
    )
