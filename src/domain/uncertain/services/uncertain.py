from datetime import date

from src.domain.uncertain.models.uncertain import Uncertain


def create_uncertain(
    user_id: int,
    name: str,
    surname: str,
    patronymic: str,
    birthday: date,
) -> Uncertain:
    return Uncertain(
        user_id=user_id,
        name=name,
        surname=surname,
        patronymic=patronymic,
        birthday=birthday,
    )
