from datetime import datetime
from typing import Protocol

from src.application.common.dto.common import Paginate
from src.application.common.interfaces.school_nickname import (
    IStudentWithSchoolNickname,
    ITeacherWithSchoolNickname,
)


class IUser:
    id: int
    telegram_id: int
    phone: int
    created_at: datetime


def get_student_school_nickname(student: IStudentWithSchoolNickname) -> str:
    return f"{student.user.name}{student.animal}"


def get_teacher_school_nickname(teacher: ITeacherWithSchoolNickname) -> str:
    return f"{teacher.user.name} {teacher.user.patronymic}{teacher.animal}"


def get_user_id_by_unique_code(unique_code: str) -> int:
    parts = unique_code.split("-")

    return int(parts[-1])


def get_paginate(count: int, offset: int, limit: int) -> Paginate:
    pages = count // limit + bool(count % limit)
    current_page = offset // limit + 1

    return Paginate(limit=limit, offset=offset, current_page=current_page, pages=pages)
