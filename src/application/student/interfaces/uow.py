from src.application.student.interfaces.persistense import IStudentReader, IStudentRepo
from src.application.common.interfaces.uow import IUoW
from src.application.undefined.interfaces.persistense import IUndefinedRepo
from src.application.user.interfaces.persistense import IUserRepo


class IStudentUoW(IUoW):
    student_reader: IStudentReader
    student_repo: IStudentRepo

    user_repo: IUserRepo
    undefined_repo: IUndefinedRepo
