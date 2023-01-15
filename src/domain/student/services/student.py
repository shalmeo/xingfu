from datetime import date

from src.domain.student.models.student import Student


def create_student(
    user_id: int,
    name: str,
    surname: str,
    patronymic: str,
    birthday: date,
) -> Student:
    return Student(
        user_id=user_id,
        name=name,
        surname=surname,
        patronymic=patronymic,
        birthday=birthday,
    )


def update_student(
    teacher: Student,
    name: str,
    surname: str,
    patronymic: str,
    birthday: date,
    access_start: date,
    access_end: date,
) -> Student:
    teacher.name = name
    teacher.surname = surname
    teacher.patronymic = patronymic
    teacher.birthday = birthday
    teacher.access_start = access_start
    teacher.access_end = access_end

    return teacher
