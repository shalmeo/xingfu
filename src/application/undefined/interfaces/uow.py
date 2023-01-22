from src.application.common.interfaces.uow import IUoW
from src.application.student.interfaces.persistense import IStudentRepo
from src.application.teacher.interfaces.persistense import ITeacherRepo
from src.application.undefined.interfaces.persistense import (
    IUndefinedReader,
    IUndefinedRepo,
)
from src.application.user.interfaces.persistense import IUserRepo


class IUndefinedUoW(IUoW):
    undefined_reader: IUndefinedReader
    undefined_repo: IUndefinedRepo

    user_repo: IUserRepo
    student_repo: IStudentRepo
    teacher_repo: ITeacherRepo
