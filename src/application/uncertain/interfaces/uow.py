from src.application.common.interfaces.uow import IUoW
from src.application.student.interfaces.persistense import IStudentRepo
from src.application.teacher.interfaces.persistense import ITeacherRepo
from src.application.uncertain.interfaces.persistense import (
    IUncertainReader,
    IUncertainRepo,
)
from src.application.user.interfaces.persistense import IUserRepo


class IUncertainUoW(IUoW):
    uncertain_reader: IUncertainReader
    uncertain_repo: IUncertainRepo

    user_repo: IUserRepo
    student_repo: IStudentRepo
    teacher_repo: ITeacherRepo
